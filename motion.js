/* Den Motion: short painted clips for "Things that move" on the Den wish list.
   A clip is img/motion/<id>.mp4 with its first frame as img/motion/<id>-poster.webp (made by the art team).
   The player tries the clip and only fades it in once it is really playing, so a clip that isn't there yet is
   simply skipped: pages behave exactly as before until the art lands. Clips play after a tap, are muted,
   can be tapped to skip, and never play for people who turn motion off.
   Clip ids:
     door-<panel>    hub: a subject's painting wakes up when its Den spot is tapped (maths, english, chinese, science,
                     spelling, music, stories, bible, grownups)
     hello-<crew>    hub: tap a crew portrait and they wave (chowdie, wala, flamecharge, flame, mommy, baddie)
     lair-intro      boss levels: Baddie pops out with a cheeky laugh on the first slide
     lair-escape     boss levels: Baddie runs off in a puff of smoke before the "Baddie is beaten" fireworks
     daddy-bow       boss levels: the crew cheers and Baddie Daddy takes a funny bow when he is beaten */
(function(){
const here=(document.currentScript&&document.currentScript.src)||location.href;
const BASE=here.replace(/motion\.js(\?.*)?$/,'')+'img/motion/';
const calm=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
const LABELS={
 'door-maths':'The maths classroom painting comes alive','door-english':'Pages flutter in the library painting','door-chinese':'Lanterns sway in the 华文 garden',
 'door-science':'Bubbles rise in the science painting','door-spelling':'Flamecharge\'s nest glows','door-music':'Lights sweep across the music stage',
 'door-stories':'The reading nook comes alive','door-bible':'The desert scene comes alive','door-grownups':'The grown-ups\' desk comes alive',
 'hello-chowdie':'Chowdie waves hello','hello-wala':'Wala waves hello','hello-flamecharge':'Flamecharge flaps hello','hello-flame':'Flame the Eagle swoops hello',
 'hello-mommy':'Mommy Elephant toots hello','hello-baddie':'Baddie Vampire gives a sneaky wave',
 'lair-intro':'Baddie Vampire pops out laughing','lair-escape':'Baddie runs off in a puff of smoke','daddy-bow':'The crew cheers while Baddie Daddy takes a bow'};

let css=false;
function style(){if(css)return;css=true;const st=document.createElement('style');st.textContent=`
.den-motion{position:absolute;z-index:0;overflow:hidden;border-radius:inherit;opacity:0;transition:opacity .25s;cursor:pointer;background:transparent}
.den-motion.on{opacity:1}
.den-motion video{width:100%;height:100%;object-fit:cover;display:block}
.den-motion.pop{position:fixed;inset:0;z-index:3000;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(31,58,74,.55);border-radius:0}
.den-motion.pop .frame{position:relative;width:min(100%,640px);aspect-ratio:16/9;border:3px solid #1F3A4A;border-radius:22px;overflow:hidden;box-shadow:0 7px 0 #1F3A4A;background:#FFFDF6}
.den-motion.pop .x{position:absolute;top:8px;right:8px;width:40px;height:40px;border-radius:50%;border:2.5px solid #1F3A4A;background:#fff;font:800 18px sans-serif;color:#1F3A4A;cursor:pointer}
@keyframes den-wiggle{0%,100%{transform:rotate(0)}25%{transform:rotate(-8deg) scale(1.06)}75%{transform:rotate(8deg) scale(1.06)}}
.den-wiggle{animation:den-wiggle .5s ease 2}
@media (prefers-reduced-motion: reduce){.den-motion{transition:none}.den-wiggle{animation:none}}`;document.head.appendChild(st)}

let current=null;
function stop(){if(current)current()}
/* Play clip `id` over `host` (an element), or as a pop-up when opts.pop. Resolves true if it played. */
function play(id,host,opts={}){
 return new Promise(done=>{
  if(calm()||document.hidden||!host)return done(false);
  style();stop();
  const box=document.createElement('div');box.className='den-motion'+(opts.pop?' pop':'');
  const v=document.createElement('video');
  v.muted=true;v.defaultMuted=true;v.playsInline=true;v.setAttribute('playsinline','');v.setAttribute('muted','');v.preload='auto';
  v.setAttribute('aria-label',LABELS[id]||'');if(opts.pos)v.style.objectPosition=opts.pos;
  let frame=box;
  if(opts.pop){frame=document.createElement('div');frame.className='frame';const x=document.createElement('button');x.type='button';x.className='x';x.textContent='✕';x.setAttribute('aria-label','Close');
   frame.append(v,x);box.appendChild(frame);box.setAttribute('role','dialog');box.setAttribute('aria-label',LABELS[id]||'Clip');document.body.appendChild(box)}
  else{box.appendChild(v);if(getComputedStyle(host).position==='static')host.style.position='relative';
   const r=opts.over?opts.over.getBoundingClientRect():null,h=host.getBoundingClientRect();
   if(r){Object.assign(box.style,{left:(r.left-h.left-host.clientLeft)+'px',top:(r.top-h.top-host.clientTop)+'px',width:r.width+'px',height:r.height+'px'})}else box.style.inset='0';
   if(opts.wash)box.style.setProperty('--wash-layer',opts.wash);
   host.insertBefore(box,host.firstChild)}
  let finished=false,started=false;
  const end=played=>{if(finished)return;finished=true;clearTimeout(wait);clearTimeout(cap);current=null;box.classList.remove('on');
   document.removeEventListener('keydown',key);setTimeout(()=>box.remove(),played?260:0);done(played)};
  const key=e=>{if(e.key==='Escape')end(started)};
  current=()=>end(started);
  // give the clip a moment to start; if it is missing or slow, carry on without it
  const wait=setTimeout(()=>{if(!started)end(false)},opts.wait||2500);
  const cap=setTimeout(()=>end(started),12000);
  v.addEventListener('playing',()=>{started=true;box.classList.add('on');if(opts.pop){const x=box.querySelector('.x');x&&x.focus({preventScroll:true})}},{once:true});
  v.addEventListener('ended',()=>end(true));
  v.addEventListener('error',()=>end(false));
  box.addEventListener('click',()=>end(started));
  document.addEventListener('keydown',key);
  v.poster=BASE+id+'-poster.webp';v.src=BASE+id+'.mp4';
  const p=v.play();if(p&&p.catch)p.catch(()=>end(false));
 })}
window.DenMotion={play,stop,BASE};

/* ---- Hub: magic doors and crew hellos ---- */
if(document.querySelector('.subject-panel .panel-header-banner')){
 style();
 const st=document.createElement('style');st.textContent=`.panel-header-banner>h2{position:relative;z-index:1}
.panel-header-banner .den-motion::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(var(--wash),.88),rgba(var(--wash),.2) 55%,rgba(var(--wash),0) 80%);pointer-events:none}
.char-card .char-avatar{cursor:pointer}`;document.head.appendChild(st);
 const door=k=>{if(!k||k==='all')return;const b=document.querySelector('[data-panel="'+k+'"] .panel-header-banner');if(!b||b.offsetParent===null)return;
  const pos=(getComputedStyle(b).backgroundPosition||'').split(',').pop().trim();play('door-'+k,b,{pos})};
 // a Den spot (abacus, lantern, piano…) opens its subject through the hash; play once the panel is showing
 document.querySelectorAll('[data-jump-subject]').forEach(a=>a.addEventListener('click',()=>setTimeout(()=>door(a.dataset.jumpSubject),120)));
 document.querySelectorAll('.char-card').forEach(c=>{const who=[...c.classList].find(x=>x.startsWith('char-')&&x!=='char-card');const av=c.querySelector('.char-avatar');if(!who||!av)return;
  const name=(c.querySelector('.char-title')||{}).textContent||who.slice(5);
  av.setAttribute('role','button');av.tabIndex=0;av.setAttribute('aria-label','Say hello to '+name);
  const go=()=>play('hello-'+who.slice(5),c,{pop:true,wait:2000}).then(ok=>{if(!ok&&!calm()){av.classList.remove('den-wiggle');void av.offsetWidth;av.classList.add('den-wiggle')}});
  av.addEventListener('click',go);av.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();go()}})});
}

/* ---- Boss levels: Baddie's lair comes alive, and the beat-Daddy celebration ---- */
if(typeof S==='undefined'||typeof win!=='function'||typeof api==='undefined'||typeof render!=='function')return;
if(!S.some(s=>s.part==='boss'||s.part==='daddy'))return;
const stage=document.getElementById('stage'),host=stage&&stage.parentElement;
const isQ=s=>s&&(s.quiz||s._ans!==undefined);
const lastDaddy=S.reduce((n,s,k)=>s.part==='daddy'&&!isQ(s)?k:n,-1);
const clipFor=k=>S[k]&&S[k]._door?'lair-escape':(k===lastDaddy&&k>0&&S.slice(0,k).some(isQ)?'daddy-bow':null);
const render0=render;
render=function(){stop();return render0.apply(this,arguments)};
const win0=win;let held=-1;
win=function(){const k=i,id=clipFor(k),args=arguments,self=this;
 if(!id||held===k||earned.has(k))return win0.apply(self,args);
 held=k;play(id,host,{over:stage,wait:2000}).then(()=>{if(i===k)win0.apply(self,args)});};
api.win=win;
// Baddie pops out when the boss level opens
if(i===0&&host)setTimeout(()=>play('lair-intro',host,{over:stage,wait:2500}),400);
})();
