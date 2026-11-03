#!/usr/bin/env python3
"""Build (or rebuild) the painted Den map on the hub (index.html).

A painted treehouse room (wide screens) or a cut-open treehouse (phones) with painted objects placed on top.
Each object is a link: subjects open their tab on the hub, the treasure chest opens the Star Bank, the sticker
album opens the sticker book, and Baddie's hole searches for the Baddie levels. Small movements (lantern swing,
kopi steam, twinkling fairy lights, music notes, Baddie's blinking eyes) are CSS, so they stay sharp, cost nothing
to download and switch off for children who turn off motion.

The block sits between <!-- den-map:start --> and <!-- den-map:end --> just before the crew section.
Positions are in the painting's own pixels (x = centre, y = bottom of the object). Edit LAYOUT and run:
    python3 tools/den-map.py
"""
import pathlib, re, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
HUB = ROOT / "index.html"

# id: (label, href, subject tab or None, image)
SPOTS = {
    "abacus":     ("Maths",           "#maths",       "maths",    "den/abacus"),
    "desk":       ("English",         "#english",     "english",  "den/desk"),
    "lantern":    ("华文 Chinese",     "#chinese",     "chinese",  "cn/lantern"),
    "microscope": ("Science",         "#science",     "science",  "den/microscope"),
    "nest":       ("Spelling · 听写",  "#spelling",    "spelling", "den/nest"),
    "piano":      ("Music",           "#music",       "music",    "cn/piano"),
    "armchair":   ("Stories",         "#stories",     "stories",  "den/armchair"),
    "kopi":       ("Grown-ups",       "#grownups",    "grownups", "cn/kopi"),
    "chest":      ("Star Bank",       "bank.html",    None,       "den/chest"),
    "album":      ("Sticker book",    "stickers.html", None,      "den/album"),
    "hole":       ("Baddie's lair",   "#all",         None,       None),
}

# Image sizes of the objects (width, height) so each art box keeps its shape before the picture loads
SIZES = {"den/abacus": (440, 422), "den/desk": (340, 302), "den/microscope": (316, 363), "den/nest": (440, 355),
         "cn/piano": (259, 275), "den/armchair": (440, 301), "cn/kopi": (224, 153), "den/chest": (278, 277),
         "den/album": (440, 357), "cn/lantern": (173, 247)}

LAYOUT = {
    "wide": {"bg": "den/room", "W": 1280, "H": 720,
             "alt": "A cosy treehouse room with a round window, shelves and fairy lights",
             "spots": [("lantern", 448, 205, 88, {"hang": 26}), ("abacus", 322, 272, 118, {}), ("kopi", 105, 200, 92, {"lab": "above"}),
                       ("album", 110, 284, 105, {}), ("nest", 965, 218, 130, {}), ("microscope", 1170, 195, 100, {}),
                       ("armchair", 255, 470, 215, {}), ("desk", 470, 610, 165, {}), ("chest", 640, 640, 150, {}),
                       ("piano", 1085, 470, 170, {}), ("hole", 880, 690, 170, {"lab": "above"})],
             "motes": (500, 120, 280, 300),  # x, y, w, h of the sunbeam the dust floats in
             "lights": [[31,2],[1254,25],[48,26],[1234,47],[84,68],[1212,69],[712,69],[924,70],[554,71],[931,80],[726,83],[1184,88],[537,87],[119,93],[308,94],[738,93],[1155,101],[947,100],[289,103],[755,104],[1091,108],[1124,108],[149,110],[324,112],[964,113],[249,118],[181,119],[1021,119],[981,121],[215,123],[1001,124],[348,126],[827,128],[370,136],[440,144],[402,145]]},
    "tall": {"bg": "den/tree", "W": 720, "H": 1280,
             "alt": "A treehouse with three floors in a big rain tree",
             "spots": [("lantern", 270, 440, 62, {"hang": 40}), ("nest", 460, 497, 110, {}),
                       ("abacus", 195, 755, 120, {}), ("kopi", 440, 752, 70, {"lab": "above"}), ("microscope", 535, 752, 80, {}),
                       ("armchair", 215, 997, 160, {}), ("piano", 500, 995, 125, {}),
                       ("desk", 120, 1215, 130, {}), ("chest", 275, 1240, 120, {"lab": "above"}),
                       ("album", 480, 1240, 95, {"lab": "above"}), ("hole", 615, 1125, 130, {"lab": "above"})],
             "motes": (40, 380, 640, 300),
             "lights": [[369,272],[357,275],[379,286],[336,294],[390,298],[314,308],[404,311],[290,320],[385,321],[425,324],[344,326],[264,328],[489,328],[445,330],[469,330],[240,331],[226,332],[330,332],[318,337],[410,340],[457,343],[240,343],[252,345],[436,345],[275,348],[206,539],[238,540],[355,542],[120,542],[137,541],[588,542],[334,552],[573,551],[228,555],[494,556],[418,558],[508,560],[554,559],[472,562],[530,563],[446,563],[306,564],[279,568],[353,570],[125,784],[337,787],[151,791],[245,792],[416,792],[492,793],[224,794],[318,794],[580,795],[510,796],[296,798],[271,799],[434,800],[477,800],[457,803],[524,804],[563,803],[543,807],[178,808]]},
}

# Little moving extras drawn over an object, in % of its art box
DECO = {
    "kopi": '<i class="wisp" style="left:38%"></i><i class="wisp" style="left:52%;--d:-1.1s"></i><i class="wisp" style="left:64%;--d:-2.2s"></i>',
    "nest": '<i class="ember" style="left:38%"></i><i class="ember" style="left:55%;--d:-.9s"></i><i class="ember" style="left:66%;--d:-1.8s"></i><i class="ember" style="left:47%;--d:-2.6s"></i>',
    "chest": '<i class="spark" style="left:22%;top:18%"></i><i class="spark" style="left:62%;top:8%;--d:-.8s"></i><i class="spark" style="left:44%;top:32%;--d:-1.6s"></i><i class="spark" style="left:80%;top:40%;--d:-2.3s"></i>',
    "piano": '<i class="note" style="left:30%">♪</i><i class="note" style="left:52%;--d:-1.3s">♫</i><i class="note" style="left:70%;--d:-2.6s">♪</i>',
    "microscope": '<i class="spark" style="left:44%;top:30%;--d:-1s"></i>',
    "abacus": "", "desk": "", "armchair": "", "album": "", "lantern": "",
}

HOLE = ('<svg viewBox="0 0 170 64" aria-hidden="true"><ellipse cx="85" cy="40" rx="83" ry="22" fill="#8a5a33"/>'
        '<ellipse cx="85" cy="40" rx="74" ry="17" fill="#1b1424"/>'
        '<g class="eyes"><g class="eye"><ellipse cx="68" cy="40" rx="9" ry="6" fill="#f7d93b"/><ellipse class="pupil" cx="68" cy="40" rx="2" ry="5" fill="#1b1424"/></g>'
        '<g class="eye"><ellipse cx="102" cy="40" rx="9" ry="6" fill="#f7d93b"/><ellipse class="pupil" cx="102" cy="40" rx="2" ry="5" fill="#1b1424"/></g>'
        '<rect class="lid" x="56" y="32" width="58" height="16" fill="#1b1424"/></g></svg>')

CSS = r"""
/* The painted Den map (generated by tools/den-map.py) */
.den-map{max-width:1040px;margin:0 auto 1.6rem;padding:0 1rem;position:relative;z-index:2}
.den-head{display:flex;align-items:baseline;flex-wrap:wrap;gap:.2rem .8rem;margin:0 0 .6rem}
.den-head h2{font-family:'Fredoka',sans-serif;font-size:clamp(1.4rem,3.4vw,1.9rem);color:#1F3A4A;margin:0}
.den-head p{margin:0;font-weight:700;color:#475569}
.den-scene{position:relative;container-type:inline-size}
.den-scene>.den-bg{display:block;width:100%;height:auto;border:3px solid #1F3A4A;border-radius:24px;box-shadow:0 7px 0 #1F3A4A,0 26px 40px -18px rgba(31,58,74,.45);background:#E9DCC4}
.den-tall{display:none;max-width:460px;margin:0 auto}
@media (max-width:640px){.den-wide{display:none}.den-tall{display:block}}
.den-spot{position:absolute;left:calc(var(--x) - var(--w)/2);bottom:var(--b);width:var(--w);display:block;text-decoration:none;z-index:2;-webkit-tap-highlight-color:transparent}
.den-art{position:relative;display:block;transition:transform .18s ease,filter .18s ease}
.den-art img{display:block;width:100%;height:auto;filter:drop-shadow(0 4px 3px rgba(60,35,15,.28))}
.den-spot:hover .den-art,.den-spot:focus-visible .den-art{transform:translateY(-6px) scale(1.07);filter:drop-shadow(0 0 6px #fff) drop-shadow(0 0 12px #FFE58A)}
.den-spot:active .den-art{transform:translateY(-2px) scale(1.02)}
.den-spot:focus-visible{outline:none}
.den-spot:focus-visible .den-label{outline:3px solid #2563EB;outline-offset:2px}
.den-label{position:absolute;left:50%;top:100%;transform:translate(-50%,4px);white-space:nowrap;font:600 clamp(11px,1.45cqi,15px)/1.25 'Fredoka',sans-serif;color:#1F3A4A;
  background:rgba(255,253,246,.94);border:2px solid #1F3A4A;border-radius:999px;padding:1px 9px 0;box-shadow:0 2px 0 #1F3A4A;pointer-events:none;transition:transform .18s ease,background .18s}
.den-tall .den-label{font-size:clamp(10.5px,3.1cqi,13px);padding:0 6px;border-width:1.5px}
.lab-above .den-label{top:auto;bottom:100%;transform:translate(-50%,-4px)}
.den-spot:hover .den-label,.den-spot:focus-visible .den-label{background:#FFE58A;transform:translate(-50%,4px) scale(1.08)}
.lab-above:hover .den-label,.lab-above:focus-visible .den-label{transform:translate(-50%,-4px) scale(1.08)}
.den-art i{position:absolute;font-style:normal;pointer-events:none}
/* fairy lights and floating dust */
.den-bulb{position:absolute;left:var(--x);top:var(--y);width:2.2%;aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;pointer-events:none;
  background:radial-gradient(circle,rgba(255,245,190,.95) 0 18%,rgba(255,214,102,.55) 35%,rgba(255,214,102,0) 70%);animation:denTwinkle 3.2s ease-in-out var(--d) infinite}
.den-tall .den-bulb{width:3.4%}
@keyframes denTwinkle{0%,100%{opacity:.25}50%{opacity:1}}
.den-mote{position:absolute;left:var(--x);top:var(--y);width:.5%;aspect-ratio:1;border-radius:50%;background:rgba(255,250,225,.9);pointer-events:none;animation:denMote 9s ease-in-out var(--d) infinite}
.den-tall .den-mote{width:.9%}
@keyframes denMote{0%,100%{transform:translate(0,0);opacity:0}20%,80%{opacity:.9}50%{transform:translate(1.4cqi,-3cqi)}}
/* object movements */
.s-lantern .den-art{transform-origin:50% calc(-1 * var(--hang));animation:denSwing 3.6s ease-in-out infinite}
.s-lantern .den-art::before{content:"";position:absolute;left:50%;bottom:100%;height:var(--hang);border-left:2px solid #6B4A2F}
.s-lantern:hover .den-art,.s-lantern:focus-visible .den-art{animation-duration:1.1s}
@keyframes denSwing{0%,100%{rotate:-4deg}50%{rotate:4deg}}
.wisp{bottom:62%;width:12%;height:55%;border-radius:50%;border-left:3px solid rgba(255,255,255,.85);filter:blur(.6px);opacity:0;animation:denSteam 3.3s ease-out var(--d,0s) infinite}
@keyframes denSteam{0%{transform:translateY(20%) scaleY(.6);opacity:0}30%{opacity:.85}100%{transform:translateY(-55%) translateX(18%) scaleY(1.1);opacity:0}}
.ember{bottom:45%;width:5%;aspect-ratio:1;border-radius:50%;background:#FFB23E;box-shadow:0 0 6px 2px #FF7A1A;opacity:0;animation:denEmber 3.2s ease-out var(--d,0s) infinite}
@keyframes denEmber{0%{transform:translate(0,0);opacity:0}15%{opacity:1}100%{transform:translate(30%,-260%);opacity:0}}
.s-nest img{animation:denGlow 2.8s ease-in-out infinite}
@keyframes denGlow{0%,100%{filter:drop-shadow(0 4px 3px rgba(60,35,15,.28))}50%{filter:drop-shadow(0 0 10px rgba(255,140,40,.85))}}
.spark{width:14%;aspect-ratio:1;transform:translate(-50%,-50%) scale(0);
  clip-path:polygon(50% 0,58% 42%,100% 50%,58% 58%,50% 100%,42% 58%,0 50%,42% 42%);background:#FFF8D6;animation:denSpark 2.6s ease-in-out var(--d,0s) infinite}
@keyframes denSpark{0%,60%,100%{transform:translate(-50%,-50%) scale(0) rotate(0)}75%{transform:translate(-50%,-50%) scale(1) rotate(45deg)}}
.note{bottom:80%;font:700 clamp(12px,2.2cqi,22px)/1 serif;color:#7C3AED;text-shadow:0 1px 0 #fff;opacity:0;animation:denNote 3.9s ease-out var(--d,0s) infinite}
.den-tall .note{font-size:clamp(11px,4cqi,18px)}
@keyframes denNote{0%{transform:translate(0,0) rotate(-10deg);opacity:0}20%{opacity:1}100%{transform:translate(40%,-160%) rotate(12deg);opacity:0}}
.s-album img{animation:denWiggle 6s ease-in-out infinite}
@keyframes denWiggle{0%,86%,100%{transform:rotate(0)}89%{transform:rotate(-5deg)}93%{transform:rotate(4deg)}96%{transform:rotate(-2deg)}}
.s-abacus:hover img,.s-armchair:hover img,.s-desk:hover img{animation:denJiggle .5s ease-in-out}
@keyframes denJiggle{25%{transform:rotate(-3deg)}75%{transform:rotate(3deg)}}
.s-hole svg{display:block;width:100%;height:auto;overflow:visible}
.s-hole .eyes{animation:denLook 7s ease-in-out infinite}
.s-hole .lid{transform-origin:85px 40px;transform:scaleY(0);animation:denBlink 4.6s infinite}
.s-hole:hover .eyes,.s-hole:focus-visible .eyes{animation:none;transform:translateY(-6px)}
@keyframes denBlink{0%,92%,100%{transform:scaleY(0)}95%{transform:scaleY(1)}}
@keyframes denLook{0%,40%,100%{transform:translateX(0)}50%,60%{transform:translateX(-9px)}70%,80%{transform:translateX(9px)}}
@media (prefers-reduced-motion:reduce){.den-map *,.den-map *::before{animation:none!important;transition:none!important}.den-bulb{opacity:.7}.den-mote,.wisp,.ember,.spark,.note{display:none}}
"""

JS = r"""
/* Den map: the subject spots use the hub's own data-jump-subject handler; Baddie's hole searches for the Baddie levels */
(()=>{document.querySelectorAll('.den-map [data-den-search]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();
 const all=document.querySelector('.tab-btn[data-subject="all"]'),q=document.getElementById('deckSearchInput');if(all)all.click();
 if(q){q.value=a.dataset.denSearch;q.dispatchEvent(new Event('input'))}const c=document.querySelector('.controls-wrapper');if(c)c.scrollIntoView({behavior:'smooth'})}))})();
"""

def pct(v, total):
    return f"{v / total * 100:.3f}%"

def scene(kind):
    L = LAYOUT[kind]
    W, H = L["W"], L["H"]
    out = [f'<div class="den-scene den-{kind}">',
           f'<img class="den-bg" src="img/{L["bg"]}.webp" width="{W}" height="{H}" alt="{html.escape(L["alt"])}" loading="lazy" decoding="async">']
    for n, (x, y) in enumerate(L["lights"]):
        out.append(f'<i class="den-bulb" style="--x:{pct(x, W)};--y:{pct(y, H)};--d:{-(n * 0.37) % 3.2:.2f}s" aria-hidden="true"></i>')
    mx, my, mw, mh = L["motes"]
    for n in range(8):
        x = mx + mw * ((n * 0.618) % 1)
        y = my + mh * ((n * 0.383 + 0.2) % 1)
        out.append(f'<i class="den-mote" style="--x:{pct(x, W)};--y:{pct(y, H)};--d:{-n * 1.1:.1f}s" aria-hidden="true"></i>')
    for sid, x, y, w, opt in L["spots"]:
        label, href, subject, img = SPOTS[sid]
        cls = f"den-spot s-{sid}" + (" lab-above" if opt.get("lab") == "above" else "")
        attrs = f' data-jump-subject="{subject}"' if subject else ""
        if sid == "hole":
            attrs += ' data-den-search="Baddie"'
        style = f"--x:{pct(x, W)};--b:{pct(H - y, H)};--w:{pct(w, W)}"
        if sid == "hole":
            art = HOLE
        else:
            iw, ih = SIZES[img]
            art = f'<img src="img/{img}.webp" width="{iw}" height="{ih}" alt="" loading="lazy" decoding="async">' + DECO.get(sid, "")
            if "hang" in opt:
                style += f";--hang:{opt['hang'] / (w * ih / iw) * 100:.1f}%"
        out.append(f'<a class="{cls}" href="{href}"{attrs} style="{style}"><span class="den-art">{art}</span>'
                   f'<span class="den-label">{html.escape(label)}</span></a>')
    out.append("</div>")
    return "\n".join(out)

def block():
    return ("<!-- den-map:start (generated by tools/den-map.py) -->\n"
            f"<style id=\"den-map-css\">{CSS}</style>\n"
            '<section class="den-map" aria-labelledby="denMapTitle">\n'
            '<div class="den-head"><h2 id="denMapTitle">Welcome to the Den!</h2><p>Tap a place to explore.</p></div>\n'
            f"{scene('wide')}\n{scene('tall')}\n</section>\n"
            f"<script>{JS}</script>\n"
            "<!-- den-map:end -->\n")

if __name__ == "__main__":
    s = HUB.read_text(encoding="utf-8")
    s = re.sub(r"<!-- den-map:start.*?<!-- den-map:end -->\n", "", s, flags=re.S)
    anchor = '<div class="container">\n<div class="characters-section"'
    k = s.index(anchor)
    HUB.write_text(s[:k] + block() + s[k:], encoding="utf-8")
    print("den map written")
