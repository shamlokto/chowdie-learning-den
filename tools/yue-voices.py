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
LIT = re.compile(r"'((?:[^'\\\n]|\\.)*)'|\"((?:[^\"\\\n]|\\.)*)\"|`([^`$\\]*)`")

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
    out = set()
    for m in LIT.finditer(text):
        s = next(g for g in m.groups() if g is not None).replace("\\'", "'").strip()
        if s and len(s) <= 40 and PHRASE.match(s):
            out.add(s)
    return sorted(out)


def tts(s, dst):
    body = {"contents": [{"parts": [{"text": "用廣東話讀出嚟（Read aloud in Cantonese, warm and gentle, for a young child）： " + s}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}}}}}
    u = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    for attempt in range(3):
        try:
            r = urllib.request.Request(u, data=json.dumps(body).encode(),
                                       headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
            d = json.load(urllib.request.urlopen(r, timeout=120))
            p = d["candidates"][0]["content"]["parts"][0]["inlineData"]
            raw = base64.b64decode(p["data"]); mt = p.get("mimeType", "")
            src = str(dst) + '.src'; open(src, 'wb').write(raw)
            if raw[:4] == b'RIFF': inp = ['-i', src]
            else:
                rate = (re.search(r'rate=(\d+)', mt) or [0, '24000'])[1]; inp = ['-f', 's16le', '-ar', rate, '-ac', '1', '-i', src]
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y'] + inp +
                           ['-af', 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse',
                            '-ac', '1', '-b:a', '40k', str(dst)], check=True)
            os.remove(src); return True
        except Exception as e:
            err = e
    print('FAILED', s, type(err).__name__); return False


def main(decks):
    OUT.mkdir(parents=True, exist_ok=True)
    want = {}
    for rel in decks:
        p = ROOT / rel; t = p.read_text(encoding='utf-8')
        ph = phrases(t); print(rel, len(ph), 'phrases')
        for s in ph: want[key(s)] = s
        if 'id="yue-player"' not in t:
            t = t.replace('</head>', PLAYER + '</head>', 1); p.write_text(t, encoding='utf-8')
    todo = {k: s for k, s in want.items() if not (OUT / f'{k}.mp3').exists()}
    print(len(todo), 'new clips', sum(len(s) for s in todo.values()), 'chars')
    if os.environ.get('DRY'):
        return
    with cf.ThreadPoolExecutor(int(os.environ.get('JOBS', '4'))) as ex:
        list(ex.map(lambda kv: tts(kv[1], OUT / f'{kv[0]}.mp3'), todo.items()))
    have = {f.stem: f.name for f in OUT.glob('*.mp3')}
    (ROOT / 'audio' / 'yue.js').write_text('window.YUE_AUDIO=' + json.dumps(dict(sorted(have.items()))) + ';\n', encoding='utf-8')
    print('yue.js:', len(have), 'clips')


if __name__ == '__main__':
    main(sys.argv[1:])
