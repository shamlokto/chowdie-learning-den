#!/usr/bin/env python3
"""Keep the paintings clear: storybook captions (and Bible verse cards) move out of the picture into a parchment strip
just above it.

Story and Bible decks draw their storybook text with story(...) as a parchment box on top of the painting, and Bible
decks draw verses with vcard(...) over the bottom of it. This tool rewrites both helpers so they queue their text
instead (capAdd), and render() shows the queue in <div id="capstrip"> above the <svg id="stage">; slides with no
caption hide the strip. Idempotent. Run:
    python3 tools/den-captions.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARK = "/* den-captions */"

OLD_STORY = ("draw:()=>scene()+G(`<rect x=\"16\" y=\"12\" width=\"${extra.capw||608}\" height=\"${L.length*24+20}\" rx=\"12\" "
             "fill=\"#FFF8EC\" stroke=\"#1F3A4A\" stroke-width=\"2.5\" opacity=\".96\"/>`+L.map((l,k)=>T(30,38+k*24,l,'sm',"
             "'style=\"font-size:16px;font-style:italic\"')).join(''),'a-fade',.1)+(hb?bag(extra.bag):'')},extra)}")
NEW_STORY = "draw:()=>scene()+capAdd('<p class=\"cap\">'+capEsc(cap)+'</p>')+(hb?bag(extra.bag):'')},extra)}"

HELPERS = (MARK + "\n/* captions live in #capstrip above the picture (tools/den-captions.py) so the painting stays clear */\n"
           "const CAPQ=[],capEsc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'),capAdd=h=>{CAPQ.push(h);return ''};\n"
           "function capFlush(){const el=document.getElementById('capstrip');if(!el)return;el.innerHTML=CAPQ.filter(h=>h.startsWith('<p class=\"cap\"')).concat(CAPQ.filter(h=>!h.startsWith('<p class=\"cap\"'))).join('');el.hidden=!CAPQ.length;CAPQ.length=0}\n")

OLD_VCARD_RE = re.compile(r"const vcard=\(t,ref,y=300\)=>\{const L=wrapT\('“'\+t\+'”',52\);.*?'a-pop',\.5\)\};")
NEW_VCARD = "const vcard=(t,ref)=>capAdd('<p class=\"vc\">“'+capEsc(t)+'”<cite>'+capEsc(ref)+'</cite></p>');"

OLD_RENDER = "svg.innerHTML=sc.draw?sc.draw(api):'';"
NEW_RENDER = "CAPQ.length=0;svg.innerHTML=sc.draw?sc.draw(api):'';capFlush();"

STRIP = '<div id="capstrip" class="capstrip" hidden></div>\n    '
CSS = ("<style id=\"den-captions-css\">\n"
       ".capstrip{background:#FFF8EC;border:2.5px solid #1F3A4A;border-radius:14px;padding:8px 14px;display:flex;flex-direction:column;gap:6px}\n"
       ".capstrip[hidden]{display:none}\n"
       ".capstrip p{margin:0;font-style:italic;font-size:17px;line-height:1.45;color:#1F3A4A}\n"
       ".capstrip p.vc{font-size:18px;text-align:center;background:#FFFDF6;border-radius:10px;padding:4px 8px}\n"
       ".capstrip p.vc cite{display:block;font-style:normal;font-size:13px;color:#58707D;text-align:right}\n"
       "@media (max-width:480px){.capstrip p{font-size:16px}.capstrip p.vc{font-size:16px}}\n"
       "</style>\n")


def apply(p):
    s = p.read_text(encoding="utf-8")
    if MARK in s:
        return "already"
    if OLD_STORY not in s:
        return "skip (no story caption)"
    s = s.replace(OLD_STORY, NEW_STORY)
    k = s.index("/* story page: scene + a parchment caption at the top")
    s = s[:k] + HELPERS + s[k:]
    s, nv = OLD_VCARD_RE.subn(NEW_VCARD, s)
    assert s.count(OLD_RENDER) == 1, p
    s = s.replace(OLD_RENDER, NEW_RENDER)
    assert s.count('<svg id="stage"') == 1, p
    s = s.replace('<svg id="stage"', STRIP + '<svg id="stage"')
    s = s.replace("</head>", CSS + "</head>", 1)
    p.write_text(s, encoding="utf-8")
    return "ok" + (" +verses" if nv else "")


if __name__ == "__main__":
    for p in sorted(ROOT.glob("*/*.html")):
        if "parchment caption at the top" in p.read_text(encoding="utf-8"):
            print(p.relative_to(ROOT), apply(p))
