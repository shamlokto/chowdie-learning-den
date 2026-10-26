/* Den Stars: a star bank for first-try answers, shared by the hub, the Star Bank and every deck.
   Rules (the Google Sheet backend in stars-backend/Code.gs enforces the same ones):
   - Only question slides earn (Star check quizzes, Baddie lies, Baddie Daddy challenges, story and music exam questions).
   - Right on the FIRST tap = a star. Any wrong tap first = no star, and the question rests for 7 days.
   - A question answered in the last 7 days earns nothing. After 7 days it can earn a review star.
   - Baddie Daddy challenges are worth 2. Finishing every question in a deck, boss round or story in one go earns a one-time bonus.
   Who is learning comes from localStorage 'denUser'. Daddy and Mommy collect as beta testers. */
(function(){
// Paste the Apps Script web app URL here. Empty = stars are saved on this device only.
const SYNC_URL='https://script.google.com/macros/s/AKfycby0Y3I4e4kAtF6zex4kcs6ZPw6D2FVPucMe-0MdgnlAbiR08vWuSJKyy9If9X6Zj_5eew/exec';
const USERS={willis:'Willis',megan:'Megan',daddy:'Daddy',mommy:'Mommy'};
const BETA={daddy:1,mommy:1};
const WEEK=7*864e5, BONUS={deck:3,boss:5,daddy:10,story:2};
const ls={get(k){try{return localStorage.getItem(k)}catch(e){return null}},set(k,v){try{localStorage.setItem(k,v)}catch(e){}}};
const who=()=>ls.get('denUser');
const load=u=>{try{return JSON.parse(ls.get('denStars:'+u))||{}}catch(e){return {}}};
const book=u=>{const b=load(u);b.log=b.log||[];b.srv=b.srv||null;return b};
const save=(u,b)=>ls.set('denStars:'+u,JSON.stringify(b));
const uid=()=>Date.now().toString(36)+Math.random().toString(36).slice(2,8);
const subs=[];const changed=u=>subs.forEach(f=>{try{f(u)}catch(e){}});

/* Local view of the rules: used on its own without a backend, and to guess the result while the Sheet answers */
function lastTouch(b,key){let t=0;b.log.forEach(e=>{if(e.type==='attempt'&&e.key===key&&e.ts>t)t=e.ts});
 const s=b.srv&&b.srv.recent&&b.srv.recent[key];return Math.max(t,s||0)}
function everEarned(b,key){return b.log.some(e=>e.key===key&&e.stars>0)||!!(b.srv&&b.srv.earned&&b.srv.earned.includes(key))}
function totals(u){const b=book(u);
 if(SYNC_URL&&b.srv){const pend=b.log.filter(e=>!e.synced).reduce((n,e)=>n+(e.stars||0),0);return {balance:b.srv.balance+pend,lifetime:b.srv.lifetime+Math.max(0,pend),spent:b.srv.spent}}
 let earned=0,spent=0;b.log.forEach(e=>{if(e.stars>0)earned+=e.stars;else spent-=e.stars||0});return {balance:earned-spent,lifetime:earned,spent}}

/* Talk to the Google Sheet. Plain-text POST keeps it a "simple" request, so Apps Script needs no CORS preflight. */
async function call(payload){const r=await fetch(SYNC_URL,{method:'POST',body:JSON.stringify(payload),redirect:'follow'});if(!r.ok)throw new Error('HTTP '+r.status);return r.json()}
let busy=false;const again=new Set();
async function sync(u=who()){if(!SYNC_URL||!USERS[u])return;if(busy){again.add(u);return}busy=true;
 try{const b=book(u),pend=b.log.filter(e=>!e.synced);
  const res=await call({op:'sync',user:u,events:pend.map(e=>({id:e.id,type:e.type,key:e.key,ok:e.ok,value:e.value,kind:e.kind,deck:e.deck,note:e.note}))});
  if(res&&res.ok){const nb=book(u);(res.results||[]).forEach(r=>{const e=nb.log.find(x=>x.id===r.id);if(e){e.synced=true;e.stars=r.stars;e.result=r.kind}});
   nb.srv=res.state;nb.log=nb.log.filter(e=>!e.synced||Date.now()-e.ts<WEEK);save(u,nb);changed(u);
   (res.results||[]).forEach(r=>{const e=pend.find(x=>x.id===r.id);if(e&&e.guess!==r.stars&&r.kind!=='dup')toast(r.stars>0?`⭐ ${r.stars} banked for ${USERS[u]}.`:`The Star Bank says this one isn't ready yet.`)})}}
 catch(e){/* offline: try again later */}
 finally{busy=false;const next=[...again][0];if(next){again.delete(next);sync(next)}}}

/* Record an attempt or bonus. Returns {stars, kind} using the local view of the rules. */
function record(u,ev){const b=book(u);let stars=0,kind,last=0;
 if(ev.type==='attempt'){last=lastTouch(b,ev.key);
  if(last&&Date.now()-last<WEEK)kind='resting';else if(!ev.ok)kind='miss';else{stars=ev.value;kind=everEarned(b,ev.key)?'review':'new'}}
 else if(ev.type==='bonus'){if(b.log.some(e=>e.key===ev.key)||(b.srv&&b.srv.bonuses&&b.srv.bonuses.includes(ev.key)))return {stars:0,kind:'had'};stars=BONUS[ev.kind]||0;kind='bonus'}
 if(kind==='resting')return {stars,kind,when:last};
 const e=Object.assign({id:uid(),ts:Date.now(),stars,guess:stars,synced:false},ev);b.log.push(e);
 if(b.log.length>5000&&!SYNC_URL)b.log=b.log.slice(-5000);
 save(u,b);changed(u);if(SYNC_URL)setTimeout(()=>sync(u),200);return {stars,kind,when:last}}

/* Small pop-up message at the bottom of a deck */
let tEl,tTimer;
function toast(html,ms=4200){if(!document.body)return;if(!tEl){tEl=document.createElement('div');tEl.className='den-toast';tEl.setAttribute('role','status');document.body.appendChild(tEl);
  const st=document.createElement('style');st.textContent=`.den-toast{position:fixed;left:50%;top:12px;transform:translate(-50%,-160%);z-index:2000;max-width:min(92vw,520px);padding:10px 18px;border-radius:20px;border:3px solid #1F3A4A;background:#FFF7D6;color:#1F3A4A;font:800 16px/1.3 'Nunito',sans-serif;box-shadow:0 5px 0 #1F3A4A;text-align:center;transition:transform .35s cubic-bezier(.2,1.4,.4,1);pointer-events:none}
.den-toast.on{transform:translate(-50%,0)}@media (max-width:480px){.den-toast{font-size:14px;padding:8px 14px}}@media (prefers-reduced-motion:reduce){.den-toast{transition:none}}`;document.head.appendChild(st)}
 tEl.innerHTML=html;tEl.classList.add('on');clearTimeout(tTimer);tTimer=setTimeout(()=>tEl.classList.remove('on'),ms)}

const fnv=s=>{let h=2166136261;for(let k=0;k<s.length;k++){h^=s.charCodeAt(k);h=Math.imul(h,16777619)}return (h>>>0).toString(36)};
const day=t=>new Date(t+WEEK).toLocaleDateString(undefined,{weekday:'short',day:'numeric',month:'short'});

/* Device-only rewards for the Star Bank when there is no backend yet (with a backend, the Sheet checks the PIN) */
function reward(u,n,note){const b=book(u);b.log.push({id:uid(),ts:Date.now(),type:n<0?'redeem':'gift',stars:n,note,synced:true});save(u,b);changed(u)}
window.DenStars={SYNC_URL,USERS,BETA,BONUS,who,totals,sync,record,reward,toast,book,onChange:f=>subs.push(f),call:SYNC_URL?call:null};

/* ---- Deck hook: wraps the deck engine's win() and watches for wrong taps (the engine marks them with class "no") ---- */
if(typeof S==='undefined'||typeof win!=='function'||typeof api==='undefined')return;
const path=location.pathname.split('/').slice(-2).join('/'),isStory=path.startsWith('stories/');
const isQ=sc=>sc&&(sc.quiz||sc._ans!==undefined);
const group=sc=>sc.part==='boss'?'boss':sc.part==='daddy'?'daddy':isStory?'story':'deck';
// A question's id comes from its content, so editing other slides doesn't change it. Identical twins get ~1, ~2…
const KEYS=(()=>{const seen={};return S.map(sc=>{if(!isQ(sc))return null;const h=fnv(sc.title+'|'+JSON.stringify(sc.quiz?[sc.quiz.answer,sc.quiz.options]:[sc._ans,sc.options||null]));
 const n=seen[h]=(seen[h]||0)+1;return path+'#'+h+(n>1?'~'+(n-1):'')})})();
const key=k=>KEYS[k];
const missed=new Set(),done=new Set();let told=false;
const plain=s=>String(s||'').replace(/<[^>]+>/g,'');
function ready(){const u=who();if(USERS[u])return u;if(!u&&!told){told=true;toast('Pick who is learning on the <a href="../index.html" style="color:inherit">home page</a> to collect stars!',5200)}return null}
function attempt(k,ok){const u=ready();if(!u||done.has(k))return null;done.add(k);const sc=S[k];
 return record(u,{type:'attempt',key:key(k),ok,value:sc.part==='daddy'?2:1,deck:path,note:plain(document.title)+' · '+plain(sc.title)})}
new MutationObserver(ms=>{for(const m of ms){const b=m.target;if(b.tagName==='BUTTON'&&b.classList.contains('no')&&isQ(S[i])&&b.closest('#ui')){missed.add(i);attempt(i,false)}}})
 .observe(document.body,{subtree:true,attributes:true,attributeFilter:['class']});
const win0=win;
win=function(){const k=i,first=!done.has(k);const r=win0.apply(this,arguments);const u=ready();if(!u)return r;
 if(isQ(S[k])){if(first){const res=attempt(k,true);
   if(res.stars)toast(`⭐ +${res.stars} ${res.kind==='review'?'review star! You still remember it':'banked for '+USERS[u]}! <span style="opacity:.75">(${totals(u).balance} in the bank)</span>`);
   else toast(`You already did this one this week. It can earn a star again from ${day(res.when)}.`)}
  else if(missed.has(k))toast(`You got there! Stars are for first tries, so this one can earn a star from ${day(Date.now())}.`)
  const g=group(S[k]),all=S.map((s,n)=>isQ(s)&&group(s)===g?n:-1).filter(n=>n>=0);
  if(all.every(n=>earned.has(n))){const b=record(u,{type:'bonus',kind:g,key:'bonus:'+path+':'+g,deck:path,note:plain(document.title)+' · '+{deck:'whole deck',boss:'beat Baddie',daddy:'beat Baddie Daddy',story:'finished the story'}[g]});
   if(b.stars)setTimeout(()=>toast(`🎉 ${{deck:'Deck finished',boss:'Baddie beaten',daddy:'Baddie Daddy beaten',story:'Story finished'}[g]}! +${b.stars} bonus stars`),3200)}}
 return r};
api.win=win;
if(SYNC_URL&&USERS[who()])sync();
addEventListener('online',()=>sync());
})();
