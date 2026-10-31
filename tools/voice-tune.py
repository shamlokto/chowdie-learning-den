#!/usr/bin/env python3
"""Tune the read-aloud voices in every deck (they use the device's own text-to-speech).

What it does, idempotently (safe to re-run):
  * pickVoice() / denVoice(): prefer the device's Premium/Enhanced voices (free download on Mac and iPad:
    Settings > Accessibility > Spoken Content > Voices), then the character's gender, then an SG/GB/AU
    (or CN) accent, and never pick a novelty voice (Fred, Zarvox, Junior, the Eloquence voices...).
  * Wala sounds like a young kid: her own voice (Zoe Premium when installed), pitched up and a bit quicker.
  * Softer pitch for the other cute voices (Flamecharge, Mommy, the narrator...) so they stop sounding
    chipmunky. Baddie, Baddie Daddy and the other deep voices keep their funny growl.
  * Android (Chrome / Samsung Internet): wait for the phone's voice list before speaking, leave a short gap
    after cancel() (Android drops a line spoken straight after it), and never ask for a language the phone
    lacks (en-SG): use the chosen voice's own language, else en-US / zh-CN. Mac and iPad keep speaking
    synchronously inside the tap, which Safari needs.
  * Mixed-language lines: a number or acronym sitting inside Chinese (我坐MRT上学, 要20分钟) is read by the
    Chinese voice instead of switching voice mid-sentence.
Run:  python3 tools/voice-tune.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent

VODD = r"""const VODD=/albert|bad news|bahh|bells|boing|bubbles|cellos|good news|jester|organ|superstar|trinoids|whisper|wobble|zarvox|junior|ralph|kathy|fred|deranged|hysterical|princess|eddy|\bflo\b|grandma|grandpa|\breed\b|rocko|sandy|shelley|eloquence/i;"""
QUAL = r"""const VQ=v=>{const s=v.name+' '+v.voiceURI;return /premium/i.test(s)?3:/enhanced|neural|natural/i.test(s)?2:0};"""

VFEM = r"""const VFEM=/female|samantha|karen|tessa|moira|fiona|victoria|serena|kate|zira|aria|jenny|libby|sonia|maisie|natasha|clara|luna|ava|zoe|allison|susan|nicky|matilda|isha|stephanie|google uk english female|google us english|tingting|ting-ting|lili|yu-shu|shasha|meijia|mei-jia|xiaoxiao|xiaoyi|xiaohan|xiaomeng|huihui|yaoyao|google 普通话|google 國語/i;"""
VMALE = r"""const VMALE=/\bmale\b|daniel|alex|david|mark|guy|ryan|george|arthur|evan|nathan|\btom\b|aaron|oliver|gordon|\blee\b|yunxi|yunyang|kangkang|google uk english male/i;"""
VKID = r"""const VKID=/zoe/i; /* Wala's own voice (Zoe Premium on Mac/iPad); other characters avoid it so she stands out */"""
PICK = r"""function pickVoice(vs,zh,pref,kid){const ok=v=>!VODD.test(v.name+' '+v.voiceURI)&&(zh?(/^(zh|cmn)/i.test(v.lang)&&!/HK|TW|yue/i.test(v.lang)):/^en/i.test(v.lang));
  const loc=zh?/(CN|SG|Hans)/i:/(SG|GB|AU)/i, score=v=>(pref&&pref.test(v.name)?4:0)+VQ(v)+(loc.test(v.lang)?1:0)+(VKID.test(v.name)?(kid?8:-1):0);
  let best=null,b=-1; vs.filter(ok).forEach(v=>{const s=score(v); if(s>b){b=s;best=v}}); return best;}"""
DENVOICE = r"""function denVoice(){let best=null,b=-1; speechSynthesis.getVoices().filter(v=>/^en/i.test(v.lang)&&!VODD.test(v.name+' '+v.voiceURI)).forEach(v=>{const s=VQ(v)+(/(SG|GB|AU)/i.test(v.lang)?1:0); if(s>b){b=s;best=v}}); return best;}"""

VSAY = r"""var VTOK=0, VANDROID=/Android/i.test(navigator.userAgent);
function vSay(make){const t=++VTOK; speechSynthesis.cancel(); const go=()=>{if(t===VTOK) make().forEach(u=>speechSynthesis.speak(u))};
  if(!VANDROID) return go(); if(speechSynthesis.getVoices().length) return setTimeout(go,80);
  let d=false; const f=()=>{if(!d){d=true;go()}}; speechSynthesis.addEventListener('voiceschanged',f,{once:true}); setTimeout(f,1000);}"""
SPEAKNOW = r"""function speakNow(t,who=WHO){ try{ vSay(()=>{
  const s=t.replace(/<i class="py">.*?<\/i>/g,' ').replace(/<[^>]+>/g,' ').replace(/ℓ/g,' litres').replace(/\s+/g,' ');
  const vs=speechSynthesis.getVoices(); const P=VOICE[who]||VOICE.otter;
  const en=pickVoice(vs,false,P.pref,P.kid), zh=pickVoice(vs,true,P.pref,P.kid);
  const parts=s.split(CJK).filter(p=>p.replace(/[\s,.!?;:]/g,''));
  for(let k=parts.length-2;k>0;k--) if(/^[\s\dA-Z%.:,-]+$/.test(parts[k])&&CJK.test(parts[k-1])&&CJK.test(parts[k+1])) parts.splice(k-1,3,parts[k-1]+parts[k].trim()+parts[k+1]);
  return parts.map(p=>{const z=CJK.test(p);const u=new SpeechSynthesisUtterance(p);
    const v=z?zh:en; u.lang=v?v.lang.replace('_','-'):(z?'zh-CN':'en-US'); if(v) u.voice=v; const [r,pt]=z?P.zh:P.en; u.rate=r; u.pitch=pt; return u});
 }); }catch(e){} }"""
SPEAKNOW_RE = re.compile(r"function speakNow\(t,who=WHO\)\{ try\{ (?:speechSynthesis\.cancel\(\);|vSay\(\(\)=>\{).*?\n (?:\}\); )?\}catch\(e\)\{\} \}", re.S)
NARR_RE = re.compile(r"try\{ speechSynthesis\.cancel\(\); (const u=new SpeechSynthesisUtterance.*?if\(v\) u\.voice=v;) speechSynthesis\.speak\(u\);\}catch\(e\)\{\} \}")
WL_OLD = ("function speak(t,zh){try{speechSynthesis.cancel();const vs=speechSynthesis.getVoices();const v=pickVoice(vs,zh,VFEM);\n"
          "  t.split(/(?<=[.。!！?？])\\s*/).filter(s=>s.trim()).forEach(p=>{const u=new SpeechSynthesisUtterance(p);u.lang=zh?'zh-CN':'en-SG';if(v)u.voice=v;u.rate=(zh?.8:.92)*(slow?.75:1);u.pitch=1.05;speechSynthesis.speak(u)})}catch(e){}}")
WL_NEW = ("function speak(t,zh){try{vSay(()=>{const vs=speechSynthesis.getVoices();const v=pickVoice(vs,zh,VFEM);\n"
          "  return t.split(/(?<=[.。!！?？])\\s*/).filter(s=>s.trim()).map(p=>{const u=new SpeechSynthesisUtterance(p);u.lang=v?v.lang.replace('_','-'):(zh?'zh-CN':'en-US');if(v)u.voice=v;u.rate=(zh?.8:.92)*(slow?.75:1);u.pitch=1.05;return u})})}catch(e){}}")

OLD_SPLIT = "s.split(CJK).filter(p=>p.replace(/[\\s,.!?;:]/g,'')).forEach(p=>{"
NEW_SPLIT = ("const parts=s.split(CJK).filter(p=>p.replace(/[\\s,.!?;:]/g,''));\n"
             "  for(let k=parts.length-2;k>0;k--) if(/^[\\s\\dA-Z%.:,-]+$/.test(parts[k])&&CJK.test(parts[k-1])&&CJK.test(parts[k+1])) parts.splice(k-1,3,parts[k-1]+parts[k].trim()+parts[k+1]);\n"
             "  parts.forEach(p=>{")

# Wala: a young kid. Her own voice (VKID), pitched up and a little quicker; Chinese stays a bit slower for learners.
WALA = "wala:{en:[1.12,1.5],zh:[.9,1.4],pref:VFEM,kid:true}"
# who: (old literal, new literal). Deep voices (baddie, daddy, eagle, owl, guard, turtle) are left alone.
PITCH = [
    ("wala:{en:[1.08,1.75],zh:[.86,1.6],pref:VFEM}", WALA),
    ("wala:{en:[1.05,1.3],zh:[.86,1.25],pref:VFEM}", WALA),
    ("pickVoice(vs,false,P.pref), zh=pickVoice(vs,true,P.pref);", "pickVoice(vs,false,P.pref,P.kid), zh=pickVoice(vs,true,P.pref,P.kid);"),
    ("otter:{en:[.94,1.1],zh:[.8,1.05],pref:null}", "otter:{en:[.94,1.0],zh:[.82,1.0],pref:null}"),
    ("VOICE.flame={en:[1.0,1.35],zh:[.82,1.3],pref:VFEM}", "VOICE.flame={en:[1.0,1.15],zh:[.84,1.12],pref:VFEM}"),
    ("VOICE.mommy={en:[.96,1.18],zh:[.84,1.15],pref:VFEM}", "VOICE.mommy={en:[.96,1.05],zh:[.86,1.05],pref:VFEM}"),
    ("VOICE.pneumo={en:[1.1,1.7],zh:[.9,1.6],pref:VFEM}", "VOICE.pneumo={en:[1.08,1.3],zh:[.9,1.25],pref:VFEM}"),
    ("VOICE.doc={en:[.95,1.1],zh:[.85,1.1],pref:VFEM}", "VOICE.doc={en:[.95,1.0],zh:[.85,1.0],pref:VFEM}"),
    ("u.pitch=1.25;", "u.pitch=1.05;"),  # spelling word lists
    ("u.rate=.92; u.pitch=1.1;", "u.rate=.92; u.pitch=1.0;"),  # narrator-only decks
]
OLD_FIND = re.compile(r"const v=speechSynthesis\.getVoices\(\)\.find\(v=>/en\[-_\]\((?:SG\|GB\|AU|GB\|SG\|AU)\)/i\.test\(v\.lang\)\)\|\|speechSynthesis\.getVoices\(\)\.find\(v=>/\^en/i\.test\(v\.lang\)\);")


def tune(src):
    s = src
    if "function pickVoice" in s:
        s = re.sub(r"const VFEM=/.*?/i;", lambda m: VFEM, s, count=1)
        s = re.sub(r"const VMALE=/.*?/i;", lambda m: VMALE, s, count=1)
        s = re.sub(r"function pickVoice\(vs,zh,pref(?:,kid)?\)\{.*?(?:\|\|base\[0\];\}|return best;\})", lambda m: PICK, s, count=1, flags=re.S)
        if "const VODD=" not in s:
            s = s.replace(VFEM, VFEM + "\n" + VODD + "\n" + QUAL, 1)
        if "const VKID=" not in s:
            s = s.replace(QUAL, QUAL + "\n" + VKID, 1)
        s = s.replace(OLD_SPLIT, NEW_SPLIT)
        s = OLD_FIND.sub("const v=pickVoice(speechSynthesis.getVoices(),false,null);", s)  # narrator line in story decks
    elif OLD_FIND.search(s):
        s = OLD_FIND.sub("const v=denVoice();", s)
        s = re.sub(r"(\n)(function speak\(t\)\{)", lambda m: m.group(1) + VODD + "\n" + QUAL + "\n" + DENVOICE + "\n" + m.group(2), s, count=1)
    for old, new in PITCH:
        s = s.replace(old, new)
    if "const VODD=" in s:  # every speaking deck: Android-safe speaking
        if "function vSay" not in s:
            s = s.replace(QUAL, QUAL + "\n" + VSAY, 1)
        s = SPEAKNOW_RE.sub(lambda m: SPEAKNOW, s)
        s = NARR_RE.sub(lambda m: "try{ vSay(()=>{ " + m.group(1) + " return [u];}); }catch(e){} }", s)
        s = s.replace(WL_OLD, WL_NEW)
        s = s.replace("try{speechSynthesis.cancel()}catch(e){}", "try{VTOK++;speechSynthesis.cancel()}catch(e){}")
    return s


changed = 0
for f in sorted(ROOT.rglob("*.html")):
    src = f.read_text(encoding="utf-8")
    out = tune(src)
    if out != src:
        f.write_text(out, encoding="utf-8")
        changed += 1
        print("tuned", f.relative_to(ROOT))
print(changed, "files changed")
