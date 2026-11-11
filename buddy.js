/* Den Buddy ("Pick your buddy" on the Den wish list): each child's chosen crew friend sits beside the lesson
   and cheers when they get a question right on the first try, with a bigger cheer for finishing a deck,
   a Baddie round or a story. Tap the buddy to pick another one (or none). The choice is kept per child
   (localStorage denBuddy:<user>). Listens for den:answer / den:finish from stars.js. Added to every deck by
   tools/den-polish.py, before stars.js. The kids like the original SVG crew, so the drawings below are the
   decks' own otter / wala / flame / mommy, kept private to this script. */
(()=>{ if(typeof S==='undefined'||!document.getElementById('stage')) return;
const C={ink:'#1F3A4A',paper:'#FFFDF6',accent:'#FF7A45',sun:'#FFC83D',sky:'#5BB8E8',leaf:'#4FAE63',berry:'#E5577A',grape:'#8E6BD8',muted:'#58707D',line:'#B7D8CF',good:'#3EA45A',bad:'#E0574F'};
/* ---- crew drawings (copied from the decks; origin = feet centre, about 110-130 tall at s=1) ---- */
function otter(x,y,s=1,o={}){ // origin = feet centre; about 110 tall at s=1
  const wave=o.wave?`<path d="M30 -58 q16 -14 12 -32" stroke="${C.ink}" stroke-width="3" fill="#9A6A45" stroke-linecap="round"/><ellipse cx="42" cy="-92" rx="8" ry="9" fill="#9A6A45" stroke="${C.ink}" stroke-width="3"/>`:`<ellipse cx="26" cy="-48" rx="8" ry="12" fill="#9A6A45" stroke="${C.ink}" stroke-width="3" transform="rotate(-25 26 -48)"/>`;
  return `<g transform="translate(${x} ${y}) scale(${s})"><g class="${o.still?'':'a-bob'}">
  <path d="M-30 -10 q-40 6 -44 -24 q14 14 40 4z" fill="#82552F" stroke="${C.ink}" stroke-width="3" stroke-linejoin="round"/>
  <ellipse cx="0" cy="-36" rx="34" ry="38" fill="#9A6A45" stroke="${C.ink}" stroke-width="3"/>
  <ellipse cx="0" cy="-30" rx="21" ry="27" fill="#F2DDBE"/>
  <ellipse cx="-16" cy="-2" rx="12" ry="7" fill="#82552F" stroke="${C.ink}" stroke-width="3"/><ellipse cx="16" cy="-2" rx="12" ry="7" fill="#82552F" stroke="${C.ink}" stroke-width="3"/>
  <ellipse cx="-26" cy="-48" rx="8" ry="12" fill="#9A6A45" stroke="${C.ink}" stroke-width="3" transform="rotate(25 -26 -48)"/>${wave}
  <circle cx="-27" cy="-100" r="9" fill="#9A6A45" stroke="${C.ink}" stroke-width="3"/><circle cx="27" cy="-100" r="9" fill="#9A6A45" stroke="${C.ink}" stroke-width="3"/>
  <circle cx="0" cy="-86" r="32" fill="#9A6A45" stroke="${C.ink}" stroke-width="3"/>
  <ellipse cx="0" cy="-74" rx="22" ry="15" fill="#F2DDBE"/>
  <circle cx="-13" cy="-92" r="5.5" fill="${C.ink}"/><circle cx="13" cy="-92" r="5.5" fill="${C.ink}"/>
  <circle cx="-11" cy="-94" r="2" fill="#fff"/><circle cx="15" cy="-94" r="2" fill="#fff"/>
  <ellipse cx="-22" cy="-78" rx="6" ry="3.5" fill="#F4A3A8"/><ellipse cx="22" cy="-78" rx="6" ry="3.5" fill="#F4A3A8"/>
  <path d="M-6 -81 q6 -5 12 0 q-6 7 -12 0z" fill="${C.ink}"/>
  <path d="M-6 -71 q6 6 12 0" stroke="${C.ink}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M-12 -78 l-18 -3 M-12 -75 l-18 2 M12 -78 l18 -3 M12 -75 l18 2" stroke="${C.ink}" stroke-width="1.5" stroke-linecap="round"/>
  </g></g>`;
}
function wala(x,y,s=1,o={}){
  const fur='#9FA9B3',fur2='#C9D0D6',ink=C.ink;
  const arm=o.wave?`<path d="M28 -52 q18 -16 14 -36" stroke="${ink}" stroke-width="3" fill="none" stroke-linecap="round"/><ellipse cx="42" cy="-90" rx="9" ry="10" fill="${fur}" stroke="${ink}" stroke-width="3"/>`
    :`<ellipse cx="26" cy="-44" rx="9" ry="14" fill="${fur}" stroke="${ink}" stroke-width="3" transform="rotate(-20 26 -44)"/>`;
  const leaf=o.leaf===false?'':`<g transform="translate(-30 -40) rotate(-30)"><path d="M0 0 q10 -26 0 -44 q-10 18 0 44z" fill="${C.leaf}" stroke="${ink}" stroke-width="2.5"/><line x1="0" y1="2" x2="0" y2="-40" stroke="${ink}" stroke-width="1.5"/></g>`;
  return `<g transform="translate(${x} ${y}) scale(${s})"><g class="${o.still?'':'a-bob'}">
  <ellipse cx="0" cy="-34" rx="33" ry="36" fill="${fur}" stroke="${ink}" stroke-width="3"/>
  <ellipse cx="0" cy="-28" rx="20" ry="25" fill="${fur2}"/>
  <ellipse cx="-16" cy="-2" rx="13" ry="7" fill="${fur}" stroke="${ink}" stroke-width="3"/><ellipse cx="16" cy="-2" rx="13" ry="7" fill="${fur}" stroke="${ink}" stroke-width="3"/>
  ${leaf}<ellipse cx="-26" cy="-44" rx="9" ry="14" fill="${fur}" stroke="${ink}" stroke-width="3" transform="rotate(20 -26 -44)"/>${arm}
  <circle cx="-36" cy="-104" r="20" fill="${fur}" stroke="${ink}" stroke-width="3"/><circle cx="36" cy="-104" r="20" fill="${fur}" stroke="${ink}" stroke-width="3"/>
  <circle cx="-36" cy="-104" r="11" fill="#F4C6CC"/><circle cx="36" cy="-104" r="11" fill="#F4C6CC"/>
  <path d="M-44 -112 q-6 -6 -2 -12 M-30 -118 q0 -8 6 -10 M44 -112 q6 -6 2 -12 M30 -118 q0 -8 -6 -10" stroke="${ink}" stroke-width="2" fill="none" stroke-linecap="round"/>
  <circle cx="0" cy="-84" r="33" fill="${fur}" stroke="${ink}" stroke-width="3"/>
  <ellipse cx="0" cy="-72" rx="20" ry="12" fill="${fur2}"/>
  <circle cx="-15" cy="-92" r="5" fill="${ink}"/><circle cx="15" cy="-92" r="5" fill="${ink}"/>
  <circle cx="-13" cy="-94" r="1.8" fill="#fff"/><circle cx="17" cy="-94" r="1.8" fill="#fff"/>
  <ellipse cx="-23" cy="-76" rx="6" ry="3.5" fill="#F4A3A8"/><ellipse cx="23" cy="-76" rx="6" ry="3.5" fill="#F4A3A8"/>
  <ellipse cx="0" cy="-80" rx="10" ry="12" fill="#3B3F4A" stroke="${ink}" stroke-width="2"/><ellipse cx="-3" cy="-85" rx="3" ry="2" fill="#fff" opacity=".5"/>
  <path d="M-6 -64 q6 5 12 0" stroke="${ink}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <g transform="translate(26 -118) rotate(20)"><path d="M0 0 l-12 -8 v16z M0 0 l12 -8 v16z" fill="${C.bad}" stroke="${ink}" stroke-width="2" stroke-linejoin="round"/><circle r="4" fill="${C.bad}" stroke="${ink}" stroke-width="2"/></g>
  </g></g>`;
}
function flame(x,y,s=1,o={}){
  const ink=C.ink,red='#E8552B',org='#FF8A3D',yel='#FFC83D',belly='#FFE7A8',dk='#C2410C',bk='#FFB020';
  const wingR=o.wave?`<path d="M24 -60 q20 -34 50 -58 l-4 12 l12 -6 l-6 12 l13 -3 l-8 11 l12 1 l-11 9 l9 5 q-22 10 -42 34z" fill="${org}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/><path d="M34 -66 q12 -18 28 -30" stroke="${dk}" stroke-width="2.5" fill="none" stroke-linecap="round"/>`
   :o.pencil?`<path d="M24 -62 q30 0 36 28 l-9 -3 l2 10 l-9 -5 l-1 9 l-8 -7 q-4 4 -12 -2z" fill="${org}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/><g transform="translate(58 -34) rotate(-35)"><rect x="-6" y="-34" width="12" height="40" fill="${C.sky}" stroke="${ink}" stroke-width="2.5"/><path d="M-6 6 l6 12 l6 -12z" fill="#F2D2B0" stroke="${ink}" stroke-width="2"/><rect x="-6" y="-40" width="12" height="7" fill="${C.berry}" stroke="${ink}" stroke-width="2"/></g>`
   :`<path d="M24 -62 q28 6 34 40 l-9 -5 l0 11 l-8 -7 l-3 10 l-6 -9 q-4 2 -8 -4z" fill="${org}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>`;
  const wingL=`<path d="M-24 -62 q-28 6 -34 40 l9 -5 l0 11 l8 -7 l3 10 l6 -9 q4 2 8 -4z" fill="${org}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>`;
  return `<g transform="translate(${x} ${y}) scale(${s})"><g class="${o.still?'':'a-bob'}">
  <g class="${o.still?'':'flick'}"><path d="M-14 -12 q-46 12 -64 -10 q22 4 30 -10 q-26 -6 -32 -30 q22 18 36 10 q-12 -14 -8 -34 q14 28 34 38z" fill="${red}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>
  <path d="M-20 -16 q-30 6 -44 -8 q18 2 26 -10 q-14 -8 -16 -22 q14 14 30 14z" fill="${yel}"/></g>
  <path d="M0 -76 q34 2 32 38 q-2 36 -32 38 q-30 -2 -32 -38 q-2 -36 32 -38z" fill="${org}" stroke="${ink}" stroke-width="3"/>
  <path d="M0 -66 q20 2 20 30 q-2 26 -20 28 q-18 -2 -20 -28 q0 -28 20 -30z" fill="${belly}"/>
  <path d="M-10 -46 l5 5 l5 -5 l5 5 l5 -5 M-10 -30 l5 5 l5 -5 l5 5 l5 -5" stroke="${yel}" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M-14 -2 v7 M14 -2 v7" stroke="#D9A21B" stroke-width="5" stroke-linecap="round"/>
  <path d="M-25 12 q2 -8 11 -7 q9 -1 11 7 M-14 5 v7 M3 12 q2 -8 11 -7 q9 -1 11 7 M14 5 v7" stroke="#D9A21B" stroke-width="4.5" fill="none" stroke-linecap="round"/>
  <path d="M-25 12 l-2 4 M-3 12 l2 4 M-14 12 v4 M3 12 l-2 4 M25 12 l2 4 M14 12 v4" stroke="${ink}" stroke-width="3" stroke-linecap="round"/>
  ${wingL}${wingR}
  <g class="${o.still?'':'flick'}" style="transform-origin:0px -118px"><path d="M-22 -108 q-14 -14 -30 -14 q12 -6 22 -4 q-16 -14 -20 -30 q16 10 26 18 q-4 -18 4 -34 q6 20 16 26 q4 -14 16 -20 q-4 18 0 30 q10 -8 22 -6 q-12 8 -16 22z" fill="${red}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>
  <path d="M-12 -112 q-6 -14 -2 -26 q6 12 12 14 q2 -10 10 -16 q-2 14 2 24z" fill="${yel}"/></g>
  <path d="M0 -122 q32 0 32 30 q0 16 -10 26 q-10 8 -22 8 q-12 0 -22 -8 q-10 -10 -10 -26 q0 -30 32 -30z" fill="${org}" stroke="${ink}" stroke-width="3"/>
  <path d="M-30 -96 q-12 4 -16 12 q10 -2 16 0 M30 -96 q12 4 16 12 q-10 -2 -16 0" fill="${org}" stroke="${ink}" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M-22 -88 q4 16 22 22 q18 -6 22 -22 q-10 6 -22 6 q-12 0 -22 -6z" fill="${belly}"/>
  <circle cx="-12" cy="-94" r="7" fill="${yel}" stroke="${ink}" stroke-width="2"/><circle cx="12" cy="-94" r="7" fill="${yel}" stroke="${ink}" stroke-width="2"/>
  <circle cx="-11" cy="-93" r="4.6" fill="${ink}"/><circle cx="11" cy="-93" r="4.6" fill="${ink}"/>
  <circle cx="-9.5" cy="-95" r="1.8" fill="#fff"/><circle cx="12.5" cy="-95" r="1.8" fill="#fff"/>
  <path d="M-24 -106 q10 -2 18 6 M24 -106 q-10 -2 -18 6" stroke="${dk}" stroke-width="5" fill="none" stroke-linecap="round"/>
  <ellipse cx="-22" cy="-80" rx="5" ry="3" fill="#F4A3A8" opacity=".85"/><ellipse cx="22" cy="-80" rx="5" ry="3" fill="#F4A3A8" opacity=".85"/>
  <path d="M-9 -88 q9 -6 18 0 q2 10 -4 18 q-3 4 -5 9 q-2 -5 -5 -9 q-6 -8 -4 -18z" fill="${bk}" stroke="${ink}" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M-4 -70 q4 3 8 0 q-2 5 -4 9 q-2 -4 -4 -9z" fill="#B45309"/>
  <path d="M-5 -84 h1 M4 -84 h1" stroke="${ink}" stroke-width="2.4" stroke-linecap="round"/>
  </g></g>`;
}
function mommy(x,y,s=1,o={}){
  const ink=C.ink,sk='#B9B3D9',sk2='#9F98C6',ear='#F6B9CB',bow='#E5577A',nail='#FFF6EA';
  const armR=o.wave?`<path d="M24 -52 q24 -18 36 -58" stroke="${ink}" stroke-width="21" fill="none" stroke-linecap="round"/><path d="M24 -52 q24 -18 36 -58" stroke="${sk}" stroke-width="15" fill="none" stroke-linecap="round"/><path d="M54 -114 q6 -4 12 0" stroke="${ink}" stroke-width="2" fill="none"/>`
    :`<ellipse cx="29" cy="-42" rx="10" ry="16" fill="${sk}" stroke="${ink}" stroke-width="3" transform="rotate(-18 29 -42)"/>`;
  /* trunk shapes, starting between the eyes */
  const trunk=o.toot?`<path d="M-9 -84 q-4 -26 14 -46 q12 -12 26 -16 l6 12 q-14 6 -22 16 q-12 16 -4 38z" fill="${sk}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/><ellipse cx="41" cy="-140" rx="7" ry="9" fill="${sk2}" stroke="${ink}" stroke-width="2.5" transform="rotate(-60 41 -140)"/>
      <g class="${o.still?'':'a-wig'}"><path d="M62 -168 v-22 q8 2 10 8 M58 -158 a5 4 -20 1 0 4 -10" stroke="${ink}" stroke-width="2.5" fill="${ink}"/><path d="M78 -140 v-20 l12 -3 v20" stroke="${ink}" stroke-width="2.5" fill="none"/><ellipse cx="74" cy="-140" rx="5" ry="4" fill="${ink}" transform="rotate(-20 74 -140)"/><ellipse cx="86" cy="-143" rx="5" ry="4" fill="${ink}" transform="rotate(-20 86 -143)"/></g>`
   :o.trombone?`<path d="M-9 -84 q-6 22 2 36 q4 4 14 2 l-2 -10 q-6 0 -6 -6 q-2 -10 2 -22z" fill="${sk}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>`
   :o.baton?`<path d="M-9 -84 q-2 26 14 34 q16 6 26 -6 l-9 -9 q-6 6 -12 2 q-8 -6 -6 -22z" fill="${sk}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/><path d="M28 -56 l40 -40" stroke="#fff" stroke-width="5" stroke-linecap="round"/><path d="M28 -56 l40 -40" stroke="${ink}" stroke-width="1.5" stroke-linecap="round" opacity=".5"/><circle cx="30" cy="-54" r="5" fill="#8A5A2B" stroke="${ink}" stroke-width="2"/>`
   :`<path d="M-9 -84 q-4 30 4 44 q6 12 18 6 q8 -6 2 -14 q-4 -4 -8 0 q-6 -6 -4 -36z" fill="${sk}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>`;
  const mouth=o.sing?`<path d="M9 -76 q9 14 18 0z" fill="#7A2E44" stroke="${ink}" stroke-width="2.5" stroke-linejoin="round"/>`:`<path d="M9 -76 q9 9 18 0" stroke="${ink}" stroke-width="2.5" fill="none" stroke-linecap="round"/>`;
  return `<g transform="translate(${x} ${y}) scale(${s})"><g class="${o.still?'':'a-bob'}">
  <path d="M30 -24 q16 2 18 16" stroke="${ink}" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M46 -10 l4 6 l-7 -1z" fill="${ink}"/>
  <ellipse cx="0" cy="-36" rx="37" ry="37" fill="${sk}" stroke="${ink}" stroke-width="3"/>
  <ellipse cx="0" cy="-30" rx="22" ry="24" fill="#CFCAE6"/>
  <rect x="-33" y="-16" width="24" height="18" rx="9" fill="${sk}" stroke="${ink}" stroke-width="3"/><rect x="9" y="-16" width="24" height="18" rx="9" fill="${sk}" stroke="${ink}" stroke-width="3"/>
  <path d="M-29 1 q3 -5 6 0 M-22 1 q3 -5 6 0 M13 1 q3 -5 6 0 M20 1 q3 -5 6 0" fill="${nail}" stroke="${ink}" stroke-width="1.5"/>
  <ellipse cx="-29" cy="-42" rx="10" ry="16" fill="${sk}" stroke="${ink}" stroke-width="3" transform="rotate(18 -29 -42)"/>${o.wave||o.trombone?'':armR}
  <!-- piano-key collar -->
  <path d="M-30 -64 q30 14 60 0 l2 10 q-32 16 -64 0z" fill="#fff" stroke="${ink}" stroke-width="2.5" stroke-linejoin="round"/>
  ${[-22,-12,0,12,22].map(k=>`<rect x="${k-2.5}" y="${-62+Math.abs(k)*-.12+ (Math.abs(k)<14?4:1)}" width="5" height="7" fill="${ink}"/>`).join('')}
  <!-- big ears -->
  <path d="M-26 -112 q-40 -16 -52 12 q-8 30 20 42 q14 6 26 -6z" fill="${sk}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>
  <path d="M-30 -104 q-30 -10 -38 10 q-4 20 16 28 q8 2 16 -4z" fill="${ear}"/>
  <path d="M26 -112 q40 -16 52 12 q8 30 -20 42 q-14 6 -26 -6z" fill="${sk}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>
  <path d="M30 -104 q30 -10 38 10 q4 20 -16 28 q-8 2 -16 -4z" fill="${ear}"/>
  ${o.wave?armR:''}
  <!-- head -->
  <ellipse cx="0" cy="-96" rx="34" ry="31" fill="${sk}" stroke="${ink}" stroke-width="3"/>
  <path d="M-8 -126 q-2 -8 6 -10 M2 -126 q2 -9 10 -8" stroke="${ink}" stroke-width="2" fill="none" stroke-linecap="round"/>
  <circle cx="-14" cy="-102" r="5.5" fill="${ink}"/><circle cx="14" cy="-102" r="5.5" fill="${ink}"/>
  <circle cx="-12" cy="-104" r="2" fill="#fff"/><circle cx="16" cy="-104" r="2" fill="#fff"/>
  <path d="M-20 -106 l-5 -4 M-19 -101 l-6 -1 M20 -106 l5 -4 M19 -101 l6 -1" stroke="${ink}" stroke-width="2" stroke-linecap="round"/>
  <ellipse cx="-24" cy="-88" rx="6" ry="3.5" fill="#F4A3A8"/><ellipse cx="24" cy="-88" rx="6" ry="3.5" fill="#F4A3A8"/>
  ${mouth}
    ${trunk}
  ${o.trombone?`<g transform="translate(6 30) rotate(-6 14 -72)"><path d="M10 -76 h96 a6 6 0 0 1 0 12 h-90" fill="none" stroke="${ink}" stroke-width="7" stroke-linecap="round"/><path d="M10 -76 h96 a6 6 0 0 1 0 12 h-90" fill="none" stroke="#F2C14E" stroke-width="3.5" stroke-linecap="round"/>
   <path d="M28 -76 v-14 h40" fill="none" stroke="${ink}" stroke-width="7" stroke-linejoin="round"/><path d="M28 -76 v-14 h40" fill="none" stroke="#F2C14E" stroke-width="3.5" stroke-linejoin="round"/>
   <path d="M66 -93 l22 -10 v26 l-22 -10z" fill="#F2C14E" stroke="${ink}" stroke-width="2.5" stroke-linejoin="round"/><ellipse cx="88" cy="-90" rx="4" ry="13" fill="#E0A21B" stroke="${ink}" stroke-width="2.5"/>
   <rect x="2" y="-80" width="9" height="8" rx="2" fill="#E0A21B" stroke="${ink}" stroke-width="2"/></g>
   <path d="M22 -30 q24 -2 46 -16" stroke="${ink}" stroke-width="19" fill="none" stroke-linecap="round"/><path d="M22 -30 q24 -2 46 -16" stroke="${sk}" stroke-width="13" fill="none" stroke-linecap="round"/>`:''}
  <!-- pink bow with a little gold treble-clef charm -->
  <g transform="translate(20 -124) rotate(18)"><path d="M0 0 q-16 -14 -20 0 q4 14 20 0z M0 0 q16 -14 20 0 q-4 14 -20 0z" fill="${bow}" stroke="${ink}" stroke-width="2.5" stroke-linejoin="round"/><circle r="5" fill="#FFD43B" stroke="${ink}" stroke-width="2"/><path d="M0 -3 q3 0 2 3 q-2 3 -3 0 v6" stroke="${ink}" stroke-width="1.2" fill="none"/></g>
  </g></g>`;
}
const CREW={otter:{name:'Chowdie',draw:otter,ring:'#F59E0B'},wala:{name:'Wala',draw:wala,ring:'#38BDF8'},
 flame:{name:'Flamecharge',draw:flame,ring:'#F97316'},mommy:{name:'Mommy',draw:mommy,ring:'#8B5CF6'}};
const DEFAULT={willis:'wala',megan:'flame',daddy:'otter',mommy:'mommy'};
const NAMES={willis:'Willis',megan:'Megan',daddy:'Daddy',mommy:'Mommy'};
const ls={get(k){try{return localStorage.getItem(k)}catch(e){return null}},set(k,v){try{localStorage.setItem(k,v)}catch(e){}}};
const user=()=>ls.get('denUser');
const key=()=>'denBuddy:'+(user()||'guest');
const pick=()=>{const b=ls.get(key());return b==='none'||CREW[b]?b:(DEFAULT[user()]||'otter')};
const calm=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
const zh=/\/chinese\/[^/]*$/.test(location.pathname);
const LINES=zh?['好棒！','答对了！','太厉害了！','一次就对！','真聪明！']:['First try!','You got it!','Brilliant!','Super star!','Woohoo!','Nailed it!'];
const BIG=zh?'全部完成！你真棒！':'You did it all!';
const svgOf=(id,o,vb='-70 -150 140 160')=>`<svg viewBox="${vb}" aria-hidden="true">${CREW[id].draw(0,0,1,Object.assign({still:true},o))}</svg>`;

const st=document.createElement('style');st.textContent=`
.den-brow{display:flex;align-items:center;gap:10px}
.den-buddy{width:50px;height:50px;border-radius:50%;border:3px solid var(--ring,#1F3A4A);background:#FFFDF6;padding:0;cursor:pointer;box-shadow:0 3px 0 #1F3A4A;overflow:hidden;flex:none}
.den-buddy svg{width:100%;height:100%;display:block;transform:translateY(8%) scale(1.25)}
.den-buddy.none{border-style:dashed;--ring:#94A3B8;font:800 22px/1 sans-serif;color:#94A3B8}
.den-buddy:focus-visible,.den-bpick button:focus-visible{outline:3px solid #FFC83D;outline-offset:2px}
.den-bpick{position:fixed;z-index:60;left:50%;transform:translateX(-50%);background:#FFFDF6;border:3px solid #1F3A4A;border-radius:20px;box-shadow:0 6px 0 #1F3A4A;padding:12px;width:min(320px,calc(100vw - 32px))}
.den-bpick p{margin:0 0 8px;font:800 16px/1.2 'Baloo 2','Nunito',sans-serif;color:#1F3A4A}
.den-bpick .g{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.den-bpick button{display:flex;flex-direction:column;align-items:center;gap:2px;padding:6px 2px 4px;border-radius:14px;border:2.5px solid var(--ring,#CBD5E1);background:#fff;cursor:pointer;font:800 12px/1.1 'Nunito',sans-serif;color:#1F3A4A}
.den-bpick button svg{width:52px;height:52px}
.den-bpick button[aria-pressed="true"]{background:#FFF7D6}
.den-bpick .off{grid-column:1/-1;flex-direction:row;justify-content:center;border-style:dashed;padding:6px}
.den-cheer{position:absolute;z-index:45;pointer-events:none;display:flex;align-items:flex-end;gap:2px}
.den-cheer svg{width:118px;height:135px;filter:drop-shadow(0 4px 3px rgba(31,58,74,.25))}
.den-cheer .say{order:-1;margin-bottom:84px;background:#fff;border:3px solid #1F3A4A;border-radius:16px;padding:5px 12px 3px;font:800 18px/1.15 'Baloo 2','Nunito','Noto Sans SC',sans-serif;color:#1F3A4A;white-space:nowrap;box-shadow:0 3px 0 rgba(31,58,74,.2)}
.den-cheer.big svg{width:150px;height:172px}.den-cheer.big .say{font-size:21px;margin-bottom:110px}
@media (max-width:520px){.den-buddy{width:44px;height:44px}.den-cheer svg{width:88px;height:100px}.den-cheer .say{font-size:15px;margin-bottom:62px}.den-cheer.big svg{width:112px;height:128px}.den-cheer.big .say{font-size:17px;margin-bottom:84px}}
@media (prefers-reduced-motion: no-preference){
 .den-cheer{animation:denBUp .35s cubic-bezier(.3,1.5,.5,1) both}.den-cheer.bye{animation:denBDown .3s ease-in both}
 .den-cheer svg{animation:denBHop .38s ease-in-out .35s 2 alternate}.den-cheer.big svg{animation:denBHop .34s ease-in-out .3s 6 alternate}
 .den-cheer .say{animation:denBPop .3s .2s cubic-bezier(.3,1.6,.5,1) both}
 .den-buddy.bump{animation:denBBump .5s ease}}
@keyframes denBUp{from{transform:translateY(60%);opacity:0}}@keyframes denBDown{to{transform:translateY(60%);opacity:0}}
@keyframes denBHop{to{transform:translateY(-14px)}}@keyframes denBPop{from{transform:scale(.3);opacity:0}}
@keyframes denBBump{40%{transform:scale(1.18) rotate(-6deg)}}`;document.head.appendChild(st);

/* the buddy chip beside the star counter, and its picker */
const pill=document.getElementById('starpill');
const row=document.createElement('div');row.className='den-brow';row.style.position='relative';
const chip=document.createElement('button');chip.type='button';chip.className='den-buddy';chip.setAttribute('aria-haspopup','dialog');
if(pill){pill.parentNode.insertBefore(row,pill);row.append(chip,pill)}else{const h=document.querySelector('header');if(!h)return;h.appendChild(row);row.appendChild(chip)}
function paint(){const b=pick();chip.classList.toggle('none',b==='none');
 if(b==='none'){chip.innerHTML='+';chip.style.removeProperty('--ring');chip.setAttribute('aria-label','Pick a buddy');chip.title='Pick a buddy'}
 else{chip.innerHTML=svgOf(b,{});chip.style.setProperty('--ring',CREW[b].ring);chip.setAttribute('aria-label','Your buddy is '+CREW[b].name+'. Tap to change');chip.title='Your buddy: '+CREW[b].name}}
let pop=null;
function closePicker(back){if(!pop)return;pop.remove();pop=null;document.removeEventListener('pointerdown',outside,true);if(back)chip.focus()}
const outside=e=>{if(pop&&!pop.contains(e.target)&&e.target!==chip&&!chip.contains(e.target))closePicker(false)};
function openPicker(){if(pop)return closePicker(true);const cur=pick();pop=document.createElement('div');pop.className='den-bpick';pop.setAttribute('role','dialog');pop.setAttribute('aria-label','Pick your buddy');
 pop.innerHTML='<p>Pick your buddy</p><div class="g">'+Object.keys(CREW).map(id=>`<button type="button" data-b="${id}" style="--ring:${CREW[id].ring}" aria-pressed="${cur===id}">${svgOf(id,{wave:true})}${CREW[id].name}</button>`).join('')
  +`<button type="button" class="off" data-b="none" aria-pressed="${cur==='none'}">No buddy</button></div>`;
 pop.style.top=Math.round(chip.getBoundingClientRect().bottom+8)+'px';row.appendChild(pop);pop.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{ls.set(key(),b.dataset.b);paint();closePicker(true);if(b.dataset.b!=='none')cheer('Hi! Let\'s learn!',false)}));
 pop.addEventListener('keydown',e=>{if(e.key==='Escape')closePicker(true)});
 setTimeout(()=>document.addEventListener('pointerdown',outside,true),0);(pop.querySelector('[aria-pressed="true"]')||pop.querySelector('button')).focus()}
chip.addEventListener('click',openPicker);addEventListener('scroll',()=>closePicker(false),{passive:true});
paint();addEventListener('storage',e=>{if(e.key==='denUser'||e.key===key())paint()});

/* the cheer: the buddy pops up at the bottom-right corner of the picture */
let live=null,n=0;
function cheer(text,big){const b=pick();if(b==='none')return;const stage=document.getElementById('stage'),card=stage.closest('.stage')||stage.parentElement;if(!card)return;
 if(stage.querySelector('video'))return; // never sit on top of a video slide
 if(live){live.remove();live=null}
 if(getComputedStyle(card).position==='static')card.style.position='relative';
 const r=stage.getBoundingClientRect(),c=card.getBoundingClientRect();
 const el=document.createElement('div');el.className='den-cheer'+(big?' big':'');el.setAttribute('aria-hidden','true');
 el.innerHTML=svgOf(b,{wave:true})+`<span class="say">${text}</span>`;
 el.style.right=Math.max(4,c.right-r.right-card.clientLeft+6)+'px';el.style.bottom=Math.max(4,c.bottom-r.bottom-card.clientTop+2)+'px';
 card.appendChild(el);live=el;chip.classList.remove('bump');void chip.offsetWidth;chip.classList.add('bump');
 const t=big?3200:1900;setTimeout(()=>{if(live!==el)return;if(calm()){el.remove();live=null;return}el.classList.add('bye');setTimeout(()=>{el.remove();if(live===el)live=null},300)},t)}
const who=()=>NAMES[user()];
addEventListener('den:answer',e=>{if(!e.detail||!e.detail.first)return;const w=who(),k=n++;
 cheer(!zh&&w&&k%3===0?'Yes, '+w+'!':LINES[k%LINES.length],false)});
addEventListener('den:finish',()=>setTimeout(()=>cheer(BIG,true),900));
if(typeof render==='function'){const r0=render;render=function(){if(live){live.remove();live=null}closePicker(false);return r0.apply(this,arguments)}}
window.DenBuddy={pick,cheer};
})();
