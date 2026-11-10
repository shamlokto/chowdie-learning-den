#!/usr/bin/env python3
"""Build (or rebuild) the painted Den map on the hub (index.html).

A painted treehouse room (wide screens) or a cut-open treehouse (phones) with painted objects placed on top.
Each object is a link: subjects open their tab on the hub, the treasure chest opens the Star Bank, the sticker
album opens the sticker book, and Baddie's hole searches for the Baddie levels. Small movements (lantern swing,
kopi steam, twinkling fairy lights, music notes, Baddie's blinking eyes) are CSS, so they stay sharp, cost nothing
to download and switch off for children who turn off motion.

The Den is the hub's cover page: it fills the screen (scaled to cover without cutting off a spot), and the subject
panels only show after a spot is tapped (see the hub navigation script). The block sits between <!-- den-map:start -->
and <!-- den-map:end -->; re-running replaces it in place.
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
    "hole":       ("Baddie's lair",   "#search",      None,       None),
    "willis":     ("Willis's special task", "misc/willis-thanks.html", None, "den/willis-card"),
    "frame":      ("Meet the crew",   "#crew",        None,       "den/frame"),
    "magnifier":  ("Search",          "#search",      None,       "den/magnifier"),
}

# Spots whose decks were refreshed recently: their labels carry a small "UPDATED" badge. Empty the set to remove them.
UPDATED = {"abacus", "desk", "lantern", "microscope", "hole"}

# Image sizes of the objects (width, height) so each art box keeps its shape before the picture loads
SIZES = {"den/abacus": (440, 422), "den/desk": (340, 302), "den/microscope": (316, 363), "den/nest": (440, 355),
         "cn/piano": (259, 275), "den/armchair": (440, 301), "cn/kopi": (224, 153), "den/chest": (278, 277),
         "den/album": (440, 357), "cn/lantern": (173, 247), "den/willis-card": (360, 343), "den/frame": (328, 393), "den/magnifier": (200, 347)}

LAYOUT = {
    "wide": {"bg": "den/room", "W": 1280, "H": 720,
             "alt": "A cosy treehouse room with a round window, shelves and fairy lights",
             "spots": [("lantern", 462, 205, 88, {"hang": 26}), ("abacus", 322, 272, 118, {}), ("kopi", 105, 200, 92, {"lab": "above", "edge": "start"}),
                       ("album", 110, 284, 105, {"edge": "start"}), ("nest", 965, 218, 130, {}), ("microscope", 1170, 195, 100, {"lab": "above", "edge": "end"}),
                       ("armchair", 255, 470, 215, {}), ("desk", 470, 610, 165, {}), ("chest", 640, 640, 150, {}),
                       ("piano", 1085, 470, 132, {}), ("hole", 940, 690, 170, {"lab": "above"}),
                       ("willis", 280, 708, 104, {"lab": "above"}), ("frame", 1175, 288, 82, {"edge": "end"}), ("magnifier", 776, 700, 64, {"lab": "above"})],
             "box": (50, 20, 1232, 718),  # the part that must stay on screen when the painting is scaled to cover it
             "motes": (500, 120, 280, 300),  # x, y, w, h of the sunbeam the dust floats in
             "lights": [[31,2],[1254,25],[48,26],[1234,47],[84,68],[1212,69],[712,69],[924,70],[554,71],[931,80],[726,83],[1184,88],[537,87],[119,93],[308,94],[738,93],[1155,101],[947,100],[289,103],[755,104],[1091,108],[1124,108],[149,110],[324,112],[964,113],[249,118],[181,119],[1021,119],[981,121],[215,123],[1001,124],[348,126],[827,128],[370,136],[440,144],[402,145]]},
    "tall": {"bg": "den/tree", "W": 720, "H": 1280,
             "alt": "A treehouse with three floors in a big rain tree",
             "spots": [("lantern", 270, 440, 62, {"hang": 40}), ("nest", 460, 497, 110, {}),
                       ("abacus", 195, 755, 120, {}), ("kopi", 405, 752, 70, {"lab": "above"}), ("microscope", 552, 752, 80, {}),
                       ("armchair", 215, 997, 160, {}), ("piano", 500, 995, 125, {}),
                       ("desk", 115, 1200, 130, {}), ("chest", 285, 1235, 120, {"lab": "above"}),
                       ("album", 470, 1215, 95, {}), ("hole", 625, 1168, 120, {"lab": "above", "edge": "end"}),
                       ("willis", 62, 814, 90, {"hang": 24, "edge": "start"}), ("frame", 665, 562, 72, {"hang": 22, "edge": "end"}), ("magnifier", 640, 400, 52, {"hang": 24})],
             "box": (8, 290, 712, 1280),
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
    "frame": '<span class="crew-pics" aria-hidden="true"></span>',
    "abacus": "", "desk": "", "armchair": "", "album": "", "lantern": "", "willis": "", "magnifier": "",
}

HOLE = ('<svg viewBox="0 0 170 64" aria-hidden="true"><ellipse cx="85" cy="40" rx="83" ry="22" fill="#8a5a33"/>'
        '<ellipse cx="85" cy="40" rx="74" ry="17" fill="#1b1424"/>'
        '<g class="eyes"><g class="eye"><ellipse cx="68" cy="40" rx="9" ry="6" fill="#f7d93b"/><ellipse class="pupil" cx="68" cy="40" rx="2" ry="5" fill="#1b1424"/></g>'
        '<g class="eye"><ellipse cx="102" cy="40" rx="9" ry="6" fill="#f7d93b"/><ellipse class="pupil" cx="102" cy="40" rx="2" ry="5" fill="#1b1424"/></g>'
        '<rect class="lid" x="56" y="32" width="58" height="16" fill="#1b1424"/></g></svg>')

CSS = r"""
/* The painted Den map (generated by tools/den-map.py) */
/* the Den is the cover page; the hub's own panels show only in the subject view */
body.den-view .container{display:none}
body.subject-view .den-map{display:none}
.den-map{position:relative;height:100vh;height:100dvh;min-height:400px;overflow:hidden;background:#B89B70;z-index:2}
.den-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.den-blur{position:absolute;inset:-40px;background:center/cover no-repeat;filter:blur(18px) saturate(.85) brightness(.92)}
.den-scene{position:absolute;left:0;top:0;width:100%;container-type:inline-size}
.den-scene picture{display:block}
.den-scene .den-bg{display:block;width:100%;height:auto}
.den-tall{display:none}
@media (orientation:portrait){.den-wide{display:none}.den-tall{display:block}}
.den-top{position:absolute;z-index:6;top:max(10px,env(safe-area-inset-top,0px));left:max(12px,env(safe-area-inset-left,0px));right:max(12px,env(safe-area-inset-right,0px));
  display:grid;grid-template-columns:1fr auto 1fr;align-items:start;gap:8px;pointer-events:none}
.den-top .den-who{justify-self:start;grid-column:1;grid-row:1}.den-top .den-hint{justify-self:end;grid-column:3;grid-row:1}
.den-sign{grid-column:2;grid-row:1;margin:0;justify-self:center;text-align:center;font:700 clamp(20px,2.3vw,32px)/1.15 'Fredoka',sans-serif;color:#FFF6DC;
  background:linear-gradient(180deg,#A86B3C,#7E4B25);border:3px solid #4A2A12;border-radius:16px;padding:.25em .8em .2em;box-shadow:0 4px 0 #4A2A12,0 10px 18px rgba(40,20,5,.35);
  text-shadow:0 2px 0 rgba(60,30,10,.55);text-wrap:balance}
.den-top>*{pointer-events:auto}
.den-top .who-chip{margin:0;box-shadow:0 3px 0 rgba(31,58,74,.35);font-size:clamp(18px,1.55vw,21px);flex-wrap:nowrap}
.den-top .who-chip button,.den-top .who-chip .who-bank{font-size:16px}
.den-top .who-chip>span{white-space:nowrap}
.den-hint{margin:0;font:600 clamp(16px,1.5vw,20px)/1.3 'Fredoka',sans-serif;color:#1F3A4A;background:rgba(255,253,246,.92);border:2px solid #1F3A4A;border-radius:999px;padding:.2rem .8rem;display:flex;align-items:center;gap:.5rem;flex-wrap:wrap}
@media (max-width:900px){.den-top{grid-template-columns:auto 1fr}.den-sign{grid-column:1/-1;grid-row:1}.den-top .den-who{grid-column:1;grid-row:2}.den-top .den-hint{grid-column:2;grid-row:2}}
@media (max-width:560px){.den-hint:has(.den-greet){background:none;border:0;padding:0}.den-greet~.den-tap{display:none}
 .den-top{grid-template-columns:1fr;gap:6px}.den-top .den-who{grid-column:1;grid-row:2}.den-top .den-hint{grid-column:1}.den-top .den-hint{grid-row:3;justify-self:start;font-size:16px}.den-sign{font-size:20px;justify-self:stretch}}
.den-back{font:700 1rem 'Fredoka',sans-serif;color:#1F3A4A;background:#FFE58A;border:2.5px solid #1F3A4A;border-radius:999px;padding:.35rem 1rem .25rem;box-shadow:0 3px 0 #1F3A4A;cursor:pointer;align-self:flex-start;margin:0 0 .6rem}
.den-back:hover{transform:translateY(-1px)}.den-back:focus-visible{outline:3px solid #2563EB;outline-offset:2px}
.crew-overlay{position:fixed;inset:0;z-index:900;background:rgba(31,58,74,.55);overflow-y:auto;padding:max(16px,env(safe-area-inset-top,0px)) max(12px,env(safe-area-inset-right,0px)) 24px max(12px,env(safe-area-inset-left,0px))}
.crew-overlay[hidden]{display:none}
.crew-box{background:#FFFDF6;border:3px solid #1F3A4A;border-radius:24px;box-shadow:0 7px 0 #1F3A4A;max-width:1040px;margin:0 auto;padding:1rem}
.crew-close{position:sticky;top:0;z-index:2;float:right;font:700 1rem 'Fredoka',sans-serif;background:#FFE58A;border:2.5px solid #1F3A4A;border-radius:999px;padding:.3rem .9rem .2rem;box-shadow:0 3px 0 #1F3A4A;cursor:pointer}
.crew-close:focus-visible{outline:3px solid #2563EB;outline-offset:2px}
.crew-box .characters-section{margin:0}
.crew-pics{position:absolute;left:17%;right:17%;top:14%;bottom:14%;display:grid;grid-template-columns:1fr 1fr;gap:3%;align-content:center}
.crew-pics svg{display:block;width:100%;height:auto}
.crew-pics .crew-pic{display:block;width:100%;aspect-ratio:1;object-fit:contain;filter:drop-shadow(0 1px 1px rgba(0,0,0,.25))}
.den-spot{position:absolute;left:calc(var(--x) - var(--w)/2);bottom:var(--b);width:var(--w);display:block;text-decoration:none;-webkit-tap-highlight-color:transparent}
.den-art{position:relative;display:block;transition:transform .18s ease,filter .18s ease}
.den-art img{display:block;width:100%;height:auto;filter:drop-shadow(0 4px 3px rgba(60,35,15,.28))}
.den-spot:hover .den-art,.den-spot:focus-visible .den-art{transform:translateY(-6px) scale(1.07);filter:drop-shadow(0 0 6px #fff) drop-shadow(0 0 12px #FFE58A)}
.den-spot:active .den-art{transform:translateY(-2px) scale(1.02)}
.den-spot:focus-visible{outline:none}
.den-spot:focus-visible .den-label{outline:3px solid #2563EB;outline-offset:2px}
.den-label{position:absolute;z-index:4;left:50%;top:100%;transform:translate(-50%,4px);white-space:nowrap;font:700 clamp(18px,1.62cqi,23px)/1.2 'Fredoka',sans-serif;color:#1F3A4A;
  background:#FFFDF6;border:2.5px solid #1F3A4A;border-radius:999px;padding:2px 11px 1px;box-shadow:0 2px 0 #1F3A4A;pointer-events:none;transition:transform .18s ease,background .18s}
.den-tall .den-label{font-size:clamp(16px,4.3cqi,19px);padding:1px 8px 0;border-width:2px}
.lab-above .den-label{top:auto;bottom:100%;transform:translate(-50%,-4px)}
.den-upd{position:absolute;bottom:calc(100% - .35em);right:-.35em;font:800 .46em/1 'Fredoka',sans-serif;letter-spacing:.06em;color:#0E6B2C;background:#BDF5CB;border:2px solid #0E6B2C;border-radius:999px;padding:.22em .45em .18em;transform:rotate(6deg);box-shadow:0 2px 0 #0E6B2C;pointer-events:none}
.lab-start .den-label{left:0;transform:translate(0,4px)}.lab-end .den-label{left:auto;right:0;transform:translate(0,4px)}
.lab-above.lab-start .den-label,.lab-above.lab-end .den-label{transform:translate(0,-4px)}
.lab-start:hover .den-label,.lab-start:focus-visible .den-label,.lab-end:hover .den-label,.lab-end:focus-visible .den-label{transform:translate(0,4px) scale(1.08)}
.lab-above.lab-start:hover .den-label,.lab-above.lab-end:hover .den-label,.lab-above.lab-start:focus-visible .den-label,.lab-above.lab-end:focus-visible .den-label{transform:translate(0,-4px) scale(1.08)}
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
.s-lantern .den-art,.den-spot.hang .den-art{transform-origin:50% calc(-1 * var(--hang));animation:denSwing 3.6s ease-in-out infinite}
.s-lantern .den-art::before,.den-spot.hang .den-art::before{content:"";position:absolute;left:50%;bottom:100%;height:var(--hang);border-left:2px solid #6B4A2F}
.den-spot.hang .den-art{animation-duration:4.4s}
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

/* festivals (dates in the script below) */
.den-fx{position:absolute;left:calc(var(--x) - var(--w)/2);bottom:var(--b);width:var(--w);display:none;pointer-events:none}
.den-fx img,.den-fx svg{display:block;width:100%;height:auto;filter:drop-shadow(0 3px 3px rgba(60,35,15,.3))}
.den-fx.flat{transform:scaleY(.42);transform-origin:50% 100%}
.den-fx.hang{transform-origin:50% calc(-1 * var(--hang));animation:denSwing 4.2s ease-in-out infinite}
.den-fx.hang::before{content:"";position:absolute;left:50%;bottom:100%;height:var(--hang);border-left:2px solid #6B4A2F}
.den-fx.float{animation:denFloat 3.4s ease-in-out infinite}
@keyframes denFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-6%)}}
.den-map[data-fest="cny"] .fx-cny,.den-map[data-fest="raya"] .fx-raya,.den-map[data-fest="deepavali"] .fx-deepavali,.den-map[data-fest="midautumn"] .fx-midautumn,
.den-map[data-fest="national"] .fx-national,.den-map[data-fest="xmas"] .fx-xmas,.den-map[data-fest="bday"] .fx-bday{display:block}
.den-greet{display:inline-block;font:700 clamp(16px,1.5vw,20px) 'Fredoka',sans-serif;color:#7A1F12;background:#FFE58A;border:2px solid #1F3A4A;border-radius:999px;padding:.05rem .8rem;box-shadow:0 2px 0 #1F3A4A}
/* evening: night paintings in dark mode (or ?night=1), dimmer objects, fireflies instead of dust */
@media (prefers-color-scheme:dark){.den-map:not(.den-day) .den-art img,.den-map:not(.den-day) .den-fx img{filter:brightness(.84) saturate(.92) drop-shadow(0 4px 3px rgba(0,0,0,.35))}
 .den-map:not(.den-day) .den-mote{background:#E9FF8A;box-shadow:0 0 6px 3px rgba(210,255,120,.6);width:.8%}.den-map:not(.den-day) .den-bulb{width:2.8%}}
.den-map.den-night .den-art img,.den-map.den-night .den-fx img{filter:brightness(.84) saturate(.92) drop-shadow(0 4px 3px rgba(0,0,0,.35))}
.den-map.den-night .den-mote{background:#E9FF8A;box-shadow:0 0 6px 3px rgba(210,255,120,.6);width:.8%}.den-map.den-night .den-bulb{width:2.8%}
@media (prefers-reduced-motion:reduce){.den-map *,.den-map *::before{animation:none!important;transition:none!important}.den-bulb{opacity:.7}.den-mote,.wisp,.ember,.spark,.note{display:none}}
"""

JS = r"""

/* Festival Den: decorations and a greeting during each festival (Singapore dates; lunar festivals need new dates each year).
   Birthdays: fill in 'MM-DD' for each child. Preview with ?fest=cny|raya|deepavali|midautumn|national|xmas|bday and ?night=1 */
(()=>{const map=document.querySelector('.den-map');if(!map)return;
 const BIRTHDAYS={willis:'',megan:'',daddy:'',mommy:''},NAMES={willis:'Willis',megan:'Megan',daddy:'Daddy',mommy:'Mommy'};
 const FEST=[{id:'cny',hi:'Happy Chinese New Year! 新年快乐!',days:['2026-02-17','2027-02-06','2028-01-26'],before:10,after:15},
  {id:'raya',hi:'Selamat Hari Raya!',days:['2026-03-21','2027-03-10','2028-02-27'],before:7,after:10},
  {id:'deepavali',hi:'Happy Deepavali!',days:['2026-11-08','2027-10-28'],before:7,after:3},
  {id:'midautumn',hi:'Happy Mid-Autumn Festival! 中秋节快乐!',days:['2026-09-25','2027-09-15','2028-10-03'],before:7,after:2},
  {id:'national',hi:'Happy National Day, Singapore!',md:'08-09',before:8,after:5},
  {id:'xmas',hi:'Merry Christmas!',md:'12-25',before:24,after:1}];
 const q=new URLSearchParams(location.search),now=new Date(),day=864e5,today=Date.UTC(now.getFullYear(),now.getMonth(),now.getDate());
 const at=s=>{const [y,m,d]=s.split('-').map(Number);return Date.UTC(y,m-1,d)};
 let who=null;try{who=localStorage.getItem('denUser')}catch(e){}
 let pick=null;const bd=BIRTHDAYS[who];
 if(bd&&bd===String(now.getMonth()+1).padStart(2,'0')+'-'+String(now.getDate()).padStart(2,'0'))pick={id:'bday',hi:`Happy birthday, ${NAMES[who]}!`};
 if(!pick)pick=FEST.find(f=>(f.days||[now.getFullYear()+'-'+f.md]).some(d=>{const t=at(d);return today>=t-f.before*day&&today<=t+f.after*day}));
 const want=q.get('fest');if(want)pick=FEST.find(f=>f.id===want)||(want==='bday'?{id:'bday',hi:'Happy birthday!'}:null);
 if(pick){map.dataset.fest=pick.id;const p=map.querySelector('.den-hint');if(p)p.innerHTML=`<span class="den-greet">${pick.hi}</span> <span class="den-tap">Tap a place to explore!</span>`}
 const n=q.get('night');if(n==='1'||n==='0'){map.classList.add(n==='1'?'den-night':'den-day');
  map.querySelectorAll('picture source').forEach(s=>s.remove());map.querySelectorAll('img.den-bg').forEach(i=>i.src=n==='1'?i.dataset.night:i.dataset.day)}})();
/* Baddie's hole: open the search view already filled in with "Baddie" */
(()=>{document.querySelectorAll('.den-map [data-den-search]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();
 const q=document.getElementById('deckSearchInput');if(q)q.value=a.dataset.denSearch;
 if(location.hash==='#search')dispatchEvent(new HashChangeEvent('hashchange'));else location.hash='search'}))})();
/* Cover layout: scale the painting to fill the screen, but never so far that a spot (the "box") is cut off;
   any strip left over shows a blurred copy of the painting. Portrait screens get the tall treehouse. */
(()=>{const map=document.querySelector('.den-map');if(!map)return;const blur=map.querySelector('.den-blur'),bar=map.querySelector('.den-top');
 const SC={};map.querySelectorAll('.den-scene').forEach(el=>SC[el.dataset.kind]={el,W:+el.dataset.w,H:+el.dataset.h,box:el.dataset.box.split(',').map(Number)});
 function lay(){const vw=map.clientWidth,vh=map.clientHeight;if(!vw||!vh)return;const kind=vw<vh?'tall':'wide';
  Object.entries(SC).forEach(([k,s])=>s.el.style.display=k===kind?'block':'none');
  const {el,W,H,box:[x0,y0,x1,y1]}=SC[kind],bw=x1-x0,bh=y1-y0;
  const ti=bar?bar.offsetTop+bar.offsetHeight+6:0,av=vh-ti;
  const sc=Math.min(Math.max(vw/W,vh/H),vw/bw,av/bh),w=W*sc,h=H*sc,cl=(v,a,b)=>Math.min(Math.max(v,a),b);
  const left=w>=vw?cl(vw/2-(x0+x1)/2*sc,vw-w,0):(vw-w)/2;
  let top=h>=vh?cl(ti+av/2-(y0+y1)/2*sc,vh-h,0):(vh-h)/2;top=cl(top,ti-y0*sc,vh-y1*sc);
  el.style.width=w+'px';el.style.left=left+'px';el.style.top=top+'px';
  const img=el.querySelector('.den-bg');if(blur&&img)blur.style.backgroundImage=`url("${img.currentSrc||img.src}")`}
 lay();addEventListener('resize',lay);addEventListener('den:show',lay);map.querySelectorAll('.den-bg').forEach(i=>i.addEventListener('load',lay));
 if(window.ResizeObserver)new ResizeObserver(lay).observe(map)})();
/* Meet the crew: the picture frame shows the crew's own drawings and opens the crew panel */
(()=>{const ov=document.getElementById('crewOverlay');if(!ov)return;const close=document.getElementById('crewClose');let back=null,n=0;
 const copy=svg=>{const s=svg.cloneNode(true),sfx='-den'+(n++);s.querySelectorAll('[id]').forEach(el=>{const old=el.id;el.id=old+sfx;
  s.querySelectorAll('*').forEach(x=>[...x.attributes].forEach(a=>{if(a.value.includes('#'+old+')'))a.value=a.value.split('#'+old+')').join('#'+old+sfx+')')}))});
  s.setAttribute('aria-hidden','true');s.removeAttribute('role');s.removeAttribute('aria-label');return s};
 const pics=['chowdie','wala','flamecharge','mommy'].map(c=>ov.querySelector('.char-card.char-'+c+' .char-paint')).filter(Boolean);
 const faces=pics.length?pics:[...ov.querySelectorAll('.char-card .char-avatar svg')].slice(0,4);
 document.querySelectorAll('.crew-pics').forEach(box=>faces.forEach(f=>{if(f.tagName==='IMG'){const i=f.cloneNode();i.removeAttribute('loading');i.className='crew-pic';box.appendChild(i)}else box.appendChild(copy(f))}));
 const open=e=>{e.preventDefault();back=document.activeElement;ov.hidden=false;document.body.style.overflow='hidden';close.focus()};
 const shut=()=>{ov.hidden=true;document.body.style.overflow='';if(back)back.focus()};
 document.querySelectorAll('[data-den-crew]').forEach(a=>a.addEventListener('click',open));
 close.addEventListener('click',shut);ov.addEventListener('click',e=>{if(e.target===ov)shut()});
 ov.addEventListener('keydown',e=>{if(e.key==='Escape')shut()})})();
"""


# Festival decorations: (festival, image or svg id, x, y, width, options). Shown only during that festival (see FEST in JS).
CRESCENT = ('<svg viewBox="0 0 100 100" aria-hidden="true"><path d="M58 12a38 38 0 1 0 30 58A30 30 0 1 1 58 12z" fill="#FFD54A" stroke="#C99A06" stroke-width="3"/>'
            '<path d="M74 30l3 9h9l-7 6 3 9-8-5-8 5 3-9-7-6h9z" fill="#FFF3B0" stroke="#C99A06" stroke-width="2"/></svg>')
def sgflags(n):
    out = []
    for k in range(n):
        x = 20 + k * (680 / max(1, n - 1))
        y = 8 + 34 * (1 - ((x - 360) / 340) ** 2)
        out.append(f'<g transform="translate({x:.0f} {y:.0f})"><rect x="-15" y="0" width="30" height="11" fill="#EF3340"/><rect x="-15" y="11" width="30" height="11" fill="#fff"/>'
                   f'<rect x="-15" y="0" width="30" height="22" fill="none" stroke="#1F3A4A" stroke-width="1.5"/>'
                   '<circle cx="-9" cy="5.5" r="3.6" fill="#fff"/><circle cx="-7.8" cy="5.5" r="3.2" fill="#EF3340"/>'
                   '<g fill="#fff"><circle cx="-4" cy="3" r=".9"/><circle cx="-1.5" cy="4.7" r=".9"/><circle cx="-2.4" cy="7.6" r=".9"/><circle cx="-5.6" cy="7.6" r=".9"/><circle cx="-6.5" cy="4.7" r=".9"/></g></g>')
    return ('<svg viewBox="0 0 720 60" aria-hidden="true"><path d="M5 8 Q360 76 715 8" fill="none" stroke="#6B4A2F" stroke-width="2.5"/>' + "".join(out) + "</svg>")
SVG_DECO = {"crescent": (CRESCENT, 1.0), "sgflags": (sgflags(15), 60 / 720)}
FSIZES = {"cn/lantern": (173, 247), "cn/oranges": (239, 155), "cn/hongbao": (194, 164), "cn/cake": (165, 161), "cn/balloon": (190, 212),
          "den/ketupat": (180, 386), "den/diya": (360, 95), "den/rangoli": (360, 371), "den/mooncake": (360, 240), "den/xmastree": (229, 331)}
DECOR = {
    "wide": [("cny", "cn/lantern", 585, 196, 74, {"hang": 36}), ("cny", "cn/lantern", 705, 196, 74, {"hang": 36}),
             ("cny", "cn/oranges", 130, 708, 150, {}), ("cny", "cn/hongbao", 640, 420, 92, {}),
             ("raya", "den/ketupat", 585, 232, 58, {"hang": 36}), ("raya", "den/ketupat", 705, 232, 58, {"hang": 36}), ("raya", "crescent", 545, 300, 92, {}),
             ("deepavali", "den/diya", 640, 422, 200, {}), ("deepavali", "den/diya", 125, 708, 160, {}), ("deepavali", "den/rangoli", 1085, 714, 240, {"flat": 1}),
             ("midautumn", "cn/lantern", 585, 196, 74, {"hang": 36}), ("midautumn", "cn/lantern", 705, 196, 74, {"hang": 36}), ("midautumn", "den/mooncake", 130, 708, 170, {}),
             ("national", "sgflags", 640, 120, 720, {}),
             ("xmas", "den/xmastree", 130, 712, 140, {}),
             ("bday", "cn/cake", 640, 422, 110, {}), ("bday", "cn/balloon", 130, 660, 110, {"float": 1})],
    "tall": [("cny", "cn/lantern", 255, 630, 54, {"hang": 12}), ("cny", "cn/lantern", 475, 645, 54, {"hang": 22}), ("cny", "cn/oranges", 640, 1274, 130, {}),
             ("raya", "den/ketupat", 255, 650, 42, {"hang": 12}), ("raya", "den/ketupat", 475, 660, 42, {"hang": 22}), ("raya", "crescent", 640, 1268, 100, {}),
             ("deepavali", "den/diya", 635, 1274, 160, {}),
             ("midautumn", "cn/lantern", 255, 630, 54, {"hang": 12}), ("midautumn", "cn/lantern", 475, 645, 54, {"hang": 22}), ("midautumn", "den/mooncake", 635, 1274, 140, {}),
             ("national", "sgflags", 352, 600, 470, {}),
             ("xmas", "den/xmastree", 645, 1276, 105, {}),
             ("bday", "cn/cake", 640, 1274, 95, {}), ("bday", "cn/balloon", 255, 660, 66, {"float": 1})],
}
def decor(kind, W, H):
    out = []
    for fest, art, x, y, w, opt in DECOR[kind]:
        style = f"--x:{pct(x, W)};--b:{pct(H - y, H)};--w:{pct(w, W)}"
        cls = f"den-fx fx-{fest}" + (" flat" if opt.get("flat") else "") + (" float" if opt.get("float") else "") + (" hang" if "hang" in opt else "")
        if art in SVG_DECO:
            inner, ratio = SVG_DECO[art]
            ih_px = w * ratio
        else:
            iw, ih = FSIZES[art]
            ih_px = w * ih / iw
            inner = f'<img src="img/{art}.webp" width="{iw}" height="{ih}" alt="" loading="lazy" decoding="async">'
        if "hang" in opt:
            style += f";--hang:{opt['hang'] / ih_px * 100:.1f}%"
        out.append(f'<span class="{cls}" style="{style}" aria-hidden="true">{inner}</span>')
    return "\n".join(out)

def pct(v, total):
    return f"{v / total * 100:.3f}%"

def scene(kind):
    L = LAYOUT[kind]
    W, H = L["W"], L["H"]
    bx = ",".join(str(v) for v in L["box"])
    out = [f'<div class="den-scene den-{kind}" data-kind="{kind}" data-w="{W}" data-h="{H}" data-box="{bx}">',
           f'<picture><source media="(prefers-color-scheme: dark)" srcset="img/{L["bg"]}-night.webp">'
           f'<img class="den-bg" src="img/{L["bg"]}.webp" data-day="img/{L["bg"]}.webp" data-night="img/{L["bg"]}-night.webp" width="{W}" height="{H}" alt="{html.escape(L["alt"])}" loading="lazy" decoding="async"></picture>']
    for n, (x, y) in enumerate(L["lights"]):
        out.append(f'<i class="den-bulb" style="--x:{pct(x, W)};--y:{pct(y, H)};--d:{-(n * 0.37) % 3.2:.2f}s" aria-hidden="true"></i>')
    out.append(decor(kind, W, H))
    mx, my, mw, mh = L["motes"]
    for n in range(8):
        x = mx + mw * ((n * 0.618) % 1)
        y = my + mh * ((n * 0.383 + 0.2) % 1)
        out.append(f'<i class="den-mote" style="--x:{pct(x, W)};--y:{pct(y, H)};--d:{-n * 1.1:.1f}s" aria-hidden="true"></i>')
    for sid, x, y, w, opt in L["spots"]:
        label, href, subject, img = SPOTS[sid]
        cls = f"den-spot s-{sid}" + (" lab-above" if opt.get("lab") == "above" else "") + (" hang" if "hang" in opt and sid != "lantern" else "") + (f" lab-{opt['edge']}" if "edge" in opt else "")
        attrs = f' data-jump-subject="{subject}"' if subject else ""
        if sid == "hole":
            attrs += ' data-den-search="Baddie"'
        if sid == "frame":
            attrs += ' data-den-crew aria-haspopup="dialog"'
        style = f"--x:{pct(x, W)};--b:{pct(H - y, H)};--w:{pct(w, W)}"
        if sid == "hole":
            art = HOLE
        else:
            iw, ih = SIZES[img]
            art = f'<img src="img/{img}.webp" width="{iw}" height="{ih}" alt="" loading="lazy" decoding="async">' + DECO.get(sid, "")
            if "hang" in opt:
                style += f";--hang:{opt['hang'] / (w * ih / iw) * 100:.1f}%"
        out.append(f'<a class="{cls}" href="{href}"{attrs} style="{style}"><span class="den-art">{art}</span>'
                   f'<span class="den-label">{html.escape(label)}' + ('<span class="den-upd">UPDATED</span>' if sid in UPDATED else '') + '</span></a>')
    out.append("</div>")
    return "\n".join(out)

def block():
    return ("<!-- den-map:start (generated by tools/den-map.py) -->\n"
            f"<style id=\"den-map-css\">{CSS}</style>\n"
            "<script>document.body.classList.add(/^#[^#]/.test(location.hash)?'subject-view':'den-view')</script>\n"
            '<section class="den-map" aria-labelledby="denMapTitle">\n'
            '<div class="den-blur" aria-hidden="true"></div>\n'
            f"{scene('wide')}\n{scene('tall')}\n"
            '<div class="den-top"><h1 class="den-sign" id="denMapTitle">Welcome to Chowdie&#x27;s Learning Den!</h1><div class="den-who" id="denWho"></div><p class="den-hint"><span class="den-tap">Tap a place to explore!</span></p></div>\n'
            "</section>\n"
            f"<script>{JS}</script>\n"
            "<!-- den-map:end -->\n")

if __name__ == "__main__":
    s = HUB.read_text(encoding="utf-8")
    m = re.search(r"<!-- den-map:start.*?<!-- den-map:end -->\n", s, flags=re.S)
    if m:
        s = s[:m.start()] + block() + s[m.end():]
    else:
        k = s.index('<div class="container">')
        s = s[:k] + block() + s[k:]
    HUB.write_text(s, encoding="utf-8")
    print("den map written")
