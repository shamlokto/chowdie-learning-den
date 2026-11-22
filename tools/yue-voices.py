#!/usr/bin/env python3
"""Cantonese voices for a deck, made with Gemini text-to-speech (the owner found it far better than device voices).

Every string literal in the deck that is a Cantonese phrase (Chinese characters and punctuation, optionally a name in
Latin letters, at most 40 characters) gets one clip: audio/yue/<key>.mp3, where key = FNV-1a (32-bit, over code points)
in base 36. audio/yue.js maps key -> file for all clips. The deck calls yue('早晨') with the WHOLE phrase as one literal;
the injected player (<script id="yue-player"> in <head>) plays the clip, or falls back to the device zh-HK voice.

    GEMINI_API_KEY must be set (never printed).   python3 tools/yue-voices.py chinese/cantonese.html [DRY=1]
"""
import base64, json, os, re, subprocess, sys, pathlib, urllib.request, concurrent.futures as cf

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'audio' / 'yue'
MODEL = os.environ.get('GM', 'gemini-3.8-flash-tts')
VOICE = os.environ.get('YUE_VOICE', 'Kore')
CJK = r'㐀-鿿豈-﫿'
PHRASE = re.compile(rf'^(?=.*[{CJK}])[{CJK}　-〿＀-￯\s，。！？、…A-Za-z~]+$')
LIT = re.compile(r"'((?:[^'\\\n]|\\.)*)'|\"((?:[^\"\\\n]|\\.)*)\"|`((?:[^`\\]|\\.)*)`")  # templates with ${} are skipped below

PLAYER = r"""<script src="../audio/yue.js"></script>
<script id="yue-player">
/* Cantonese clips made by tools/yue-voices.py (Gemini TTS); falls back to the device zh-HK voice */
window.yueKey=function(s){var h=0x811c9dc5;for(var c of String(s)){h^=c.codePointAt(0);h=Math.imul(h,16777619)>>>0}return h.toString(36)};
window.yueDev=function(s){try{var v=speechSynthesis.getVoices().find(function(v){return /zh[-_]HK|yue/i.test(v.lang)});var u=new SpeechSynthesisUtterance(s);u.lang='zh-HK';if(v)u.voice=v;u.rate=.85;speechSynthesis.speak(u)}catch(e){}};
window.yue=function(s){s=String(s).trim();try{speechSynthesis.cancel();if(window.denStop)denStop()}catch(e){}
 var f=window.YUE_AUDIO&&window.YUE_AUDIO[yueKey(s)];if(!f){yueDev(s);return}
 var a=window.__yueA||(window.__yueA=new Audio());a.pause();a.src='../audio/yue/'+f;var p=a.play();if(p&&p.catch)p.catch(function(){yueDev(s)})};
</script>
"""


def key(s):
    h = 0x811c9dc5
    for ch in s:
        h ^= ord(ch); h = (h * 16777619) & 0xffffffff
    d = '0123456789abcdefghijklmnopqrstuvwxyz'; o = ''
    while True:
        h, r = divmod(h, 36); o = d[r] + o
        if not h: return o


def phrases(text):
    """Prefer the deck's explicit list (const YUE_PHRASES=[...]); otherwise scan quoted literals line by line."""
    out = set()
    k = max(text.find('YUE_PHRASES=['), text.find('YUE_LIST=['))
    if k != -1:
        text = text[k:text.index('];', k)]
    for m in LIT.finditer(text):
        s = next(g for g in m.groups() if g is not None).replace("\\'", "'").strip()
        if s and '${' not in s and len(s) <= 40 and PHRASE.match(s):
            out.add(s)
    return sorted(out)


def runtime_phrases(rel):
    """Ask the deck itself (window.YUE_PHRASES) for every phrase yue() can be called with, in every configuration."""
    js = r"""const {chromium}=require('/opt/node-tools/node_modules/playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
     await p.route('https://script.google.com/**',r=>r.abort());await p.goto('file://'+process.argv[1]);await p.waitForTimeout(600);
     const out=await p.evaluate(()=>window.YUE_PHRASES?window.YUE_PHRASES():null);console.log(JSON.stringify(out));await b.close()})();"""
    r = subprocess.run(['node', '-e', js, str(ROOT / rel)], capture_output=True, text=True, timeout=120)
    try:
        data = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        return []
    return [(d[0] if isinstance(d, list) else d).strip() for d in (data or []) if d]


CARRIERS = ['我哋一齊用廣東話讀。 ', '跟住我用廣東話讀： ', '我哋一齊用廣東話慢慢讀……  ']  # a full stop gives the cleanest pause to cut at
SAME = str.maketrans('餵啊吖啦妳祢着裏囉嘛', '喂呀呀喇你你著裡囉嘛')  # the listening model's spelling variants of the same sounds
MODELS = os.environ.get('GM', 'gemini-3.8-flash-lite-tts,gemini-3.1-flash-tts-preview').split(',')
JUDGE = os.environ.get('GJ', 'gemini-3.5-flash')
REVIEW = []
# characters the voice model misreads, replaced by same-sound characters in the text sent to it (the deck still shows
# the proper ones): 嫲 maa4 was read as 媽 maa1; 唞 tau2 was read as 晨
SAY = str.maketrans({'嫲': '麻', '唞': '抖'})


def _api(model, body, timeout=180):
    import time
    u = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    for attempt in range(4):
        try:
            r = urllib.request.Request(u, data=json.dumps(body).encode(),
                                       headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
            return json.load(urllib.request.urlopen(r, timeout=timeout))
        except urllib.error.HTTPError as e:
            msg = e.read().decode('utf-8', 'replace')
            if e.code == 429 and 'per_day' in msg:
                raise RuntimeError('daily quota used up for ' + model)
            if e.code in (429, 500, 503):
                time.sleep(20); continue
            raise RuntimeError(f'{model} HTTP {e.code}')
    raise RuntimeError(model + ' kept failing')


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout or 0)


def _norm(t):
    return re.sub(rf'[^{CJK}A-Za-z]', '', t or '').lower().translate(SAME)


def heard(mp3):
    """What a listening model hears in the clip (content check; it cannot reliably tell Cantonese from Mandarin on short words)."""
    b = base64.b64encode(open(mp3, 'rb').read()).decode()
    q = 'Transcribe exactly what is spoken in this Cantonese clip, in Traditional Chinese characters (keep English names as spoken). Reply JSON only: {"heard": "..."}'
    d = _api(JUDGE, {"contents": [{"parts": [{"inlineData": {"mimeType": "audio/mp3", "data": b}}, {"text": q}]}],
                     "generationConfig": {"responseMimeType": "application/json", "temperature": 0}})
    try:
        return json.loads(d["candidates"][0]["content"]["parts"][0]["text"]).get("heard", "")
    except Exception:
        return ''


def speak(model, s, dst, carrier=None):
    """Say s after a Cantonese carrier sentence (short words alone often come out in Mandarin), then cut the carrier off.
    Short words are said twice as a list ("十， 十。") and the last one is kept: pauses in a list are reliable.
    Returns what a listening model hears in the WHOLE recording (tiny clips are too short to transcribe), or None."""
    short = len(_norm(s)) <= 4 and not re.search(r'[，、\s]', s.strip())
    t = s.translate(SAY)
    text = (carrier or CARRIERS[0]) + (t.rstrip('。！？!?') + '， ' + t if short else t)
    d = _api(model, {"contents": [{"parts": [{"text": text}]}],
                     "generationConfig": {"responseModalities": ["AUDIO"],
                                          "speechConfig": {"languageCode": "yue-HK", "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}}}}})
    p = d["candidates"][0]["content"]["parts"][0]["inlineData"]
    raw = base64.b64decode(p["data"]); mt = p.get("mimeType", "")
    src, wav, full = str(dst) + '.src', str(dst) + '.wav', str(dst) + '.full.mp3'
    open(src, 'wb').write(raw)
    inp = ['-i', src] if raw[:4] == b'RIFF' else ['-f', 's16le', '-ar', (re.search(r'rate=(\d+)', mt) or [0, '24000'])[1], '-ac', '1', '-i', src]
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y'] + inp + ['-ac', '1', '-ar', '24000', wav], check=True); os.remove(src)
    e = subprocess.run(['ffmpeg', '-i', wav, '-af', 'silencedetect=n=-38dB:d=0.12', '-f', 'null', '-'], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', e)]; en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', e)]
    total = _dur(wav)
    inner = [(a, b) for a, b in zip(st, en) if a > 0.7 and b < total - 0.12]
    if not inner:
        os.remove(wav); return None
    start = max((inner[-1] if short else inner[0])[1] - 0.05, 0)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{start:.3f}', '-i', wav,
                    '-af', 'areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,afade=t=in:d=0.015',
                    '-ac', '1', '-b:a', '48k', str(dst)], check=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', wav, '-b:a', '48k', full], check=True)
    h = heard(full); os.remove(wav); os.remove(full)
    return h


def tts(s, dst):
    import time
    note = 'no clip'; n = len(_norm(s))
    for k, model in enumerate(MODELS):
        time.sleep(float(os.environ.get('GAP', '6.5')))  # Gemini TTS allows 10 requests a minute
        try:
            h = speak(model, s, dst, CARRIERS[k % len(CARRIERS)])
        except Exception as e:
            note = str(e)[:60]; continue
        if h is None:
            note = 'no pause after the carrier'; continue
        d = _dur(dst)
        if _norm(h).translate(SAY).endswith(_norm(s).translate(SAY)) and max(0.15, 0.17 * n) <= d <= 0.6 * n + 1.2:  # too short = cut inside the phrase
            print('ok  ', s, f'{d:.2f}s', model.split('-')[2]); return True
        note = f'{d:.2f}s, whole recording heard as "{h}"'
    REVIEW.append((s, note)); print('REVIEW', s, note); return dst.exists()


def main(decks):
    OUT.mkdir(parents=True, exist_ok=True)
    want = {}
    for rel in decks:
        p = ROOT / rel; t = p.read_text(encoding='utf-8')
        ph = sorted(set(phrases(t)) | set(runtime_phrases(rel))); print(rel, len(ph), 'phrases')
        for s in ph: want[key(s)] = s
        if 'window.yueKey=' not in t:
            k = t.index('>', t.index('<head')) + 1  # top of <head>: den-polish needs '</style></head>' untouched
            t = t[:k] + '\n' + PLAYER + t[k:]; p.write_text(t, encoding='utf-8')
    todo = {k: s for k, s in want.items() if os.environ.get('FORCE') or not (OUT / f'{k}.mp3').exists()}
    print(len(todo), 'new clips', sum(len(s) for s in todo.values()), 'chars')
    if os.environ.get('DRY'):
        return
    with cf.ThreadPoolExecutor(int(os.environ.get('JOBS', '1'))) as ex:
        list(ex.map(lambda kv: tts(kv[1], OUT / f'{kv[0]}.mp3'), todo.items()))
    have = {f.stem: f.name for f in OUT.glob('*.mp3')}
    (ROOT / 'audio' / 'yue.js').write_text('window.YUE_AUDIO=' + json.dumps(dict(sorted(have.items()))) + ';\n', encoding='utf-8')
    print('yue.js:', len(have), 'clips')
    if REVIEW:
        print('TO REVIEW BY EAR:'); [print('  ', a, '|', b) for a, b in REVIEW]


if __name__ == '__main__':
    main(sys.argv[1:])
