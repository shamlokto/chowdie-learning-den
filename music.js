/* den-music: gentle background music and answer sounds for a deck, made live with Web Audio (no audio files).
   A soft guzheng-like pluck plays a slow pentatonic tune (宮商角徵羽: C D E G A) over a quiet drone; a 🎵 button
   (top-right of the header) turns it on/off and remembers the choice (localStorage denMusic). Right answers
   (den:answer from stars.js) ring a little rising arpeggio; a wrong tap (a .no class on a #ui button) plays a soft low "boop".
   Music starts on the first tap anywhere (browsers need a gesture), ducks while a voice clip plays, and pauses when hidden.
   Include with: <script id="den-music" src="../music.js" defer></script> before stars.js. */
(function(){
  let ac=null,master=null,on=true,timer=null,step=0,duck=1;
  try{on=localStorage.getItem('denMusic')!=='off'}catch(e){}
  const N={C4:261.63,D4:293.66,E4:329.63,G4:392,A4:440,C5:523.25,D5:587.33,E5:659.25,G5:783.99,A5:880,C3:130.81,G3:196,A3:220};
  // two gentle phrases (pentatonic), each beat ~0.62 s; null = rest
  const TUNE=['E5','G5','A5','G5','E5','D5','C5',null,'D5','E5','G5','E5','D5','C5','A4',null,
              'C5','D5','E5','G5','A5','G5','E5',null,'D5','C5','A4','C5','D5','C5',null,null];
  const BASS=['C3',null,null,null,'A3',null,null,null,'G3',null,null,null,'C3',null,null,null];
  const ctx=()=>{if(!ac){try{ac=new (window.AudioContext||window.webkitAudioContext)();master=ac.createGain();master.gain.value=.0;master.connect(ac.destination)}catch(e){return null}}if(ac.state!=='running')ac.resume();return ac};
  function pluck(f,t,vol,dur){const o=ac.createOscillator(),o2=ac.createOscillator(),g=ac.createGain(),lp=ac.createBiquadFilter();
    o.type='triangle';o.frequency.value=f;o2.type='sine';o2.frequency.value=f*2.003;lp.type='lowpass';lp.frequency.setValueAtTime(3200,t);lp.frequency.exponentialRampToValueAtTime(900,t+dur);
    g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vol,t+.008);g.gain.exponentialRampToValueAtTime(.0001,t+dur);
    const g2=ac.createGain();g2.gain.value=.25;o.connect(lp);o2.connect(g2);g2.connect(lp);lp.connect(g);g.connect(master);o.start(t);o2.start(t);o.stop(t+dur+.05);o2.stop(t+dur+.05)}
  function tick(){if(!ac)return;const t=ac.currentTime+.05,b=.62;
    for(let k=0;k<4;k++){const n=TUNE[(step+k)%TUNE.length],bs=BASS[(step+k)%BASS.length],tt=t+k*b;if(n)pluck(N[n],tt,.5,1.6);if(bs)pluck(N[bs],tt,.35,2.4)}
    step=(step+4)%TUNE.length}
  function setVol(){if(master)master.gain.setTargetAtTime(on&&!document.hidden?.06*duck:0,ac.currentTime,.4)}
  function start(){if(!on||timer)return;if(!ctx())return;setVol();tick();timer=setInterval(tick,2480)}
  function stop(){clearInterval(timer);timer=null;setVol()}
  // answer sounds (play even when music is off: they are short and quiet)
  function chime(){if(!ctx())return;const t=ac.currentTime+.02,g=master.gain.value;['C5','E5','G5','C5'].forEach((n,k)=>{const f=k===3?N.C5*2:N[n];sfx(f,t+k*.09,.12,.5)})}
  function boop(){if(!ctx())return;const t=ac.currentTime+.02;sfx(N.G3,t,.1,.35);sfx(N.E5/4,t+.12,.08,.4)}
  function sfx(f,t,vol,dur){const o=ac.createOscillator(),g=ac.createGain();o.type='sine';o.frequency.value=f;g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vol,t+.01);g.gain.exponentialRampToValueAtTime(.0001,t+dur);o.connect(g);g.connect(ac.destination);o.start(t);o.stop(t+dur+.05)}
  addEventListener('den:answer',chime);
  new MutationObserver(ms=>{for(const m of ms){const b=m.target;if(b.tagName==='BUTTON'&&b.classList.contains('no')&&b.closest&&b.closest('#ui')&&!b.dataset.booped){b.dataset.booped=1;boop()}}})
    .observe(document.documentElement,{subtree:true,attributes:true,attributeFilter:['class']});
  // duck under voices: any <audio> playing (den-audio, yue clips) or speech
  setInterval(()=>{let busy=false;try{busy=speechSynthesis.speaking}catch(e){}if(window.__yueA&&!window.__yueA.paused)busy=true;
    document.querySelectorAll('audio').forEach(a=>{if(!a.paused)busy=true});if(window.DEN_A&&!window.DEN_A.paused)busy=true;
    const d=busy?.35:1;if(d!==duck){duck=d;setVol()}},300);
  document.addEventListener('visibilitychange',setVol);
  addEventListener('pointerdown',()=>{start()},{once:true,capture:true});
  // the toggle
  function button(){const host=document.querySelector('header')||document.body,b=document.createElement('button');b.type='button';b.id='musicBtn';
    b.setAttribute('aria-label','Music on or off');b.setAttribute('aria-pressed',on);b.textContent=on?'🎵':'🔇';
    b.style.cssText='font-size:22px;line-height:1;padding:6px 10px;border-radius:999px;border:3px solid var(--ink,#1F3A4A);background:var(--paper,#fff);box-shadow:0 3px 0 var(--ink,#1F3A4A);cursor:pointer';
    b.onclick=e=>{e.stopPropagation();on=!on;try{localStorage.setItem('denMusic',on?'on':'off')}catch(x){}b.textContent=on?'🎵':'🔇';b.setAttribute('aria-pressed',on);on?start():stop()};
    const pill=document.getElementById('starpill');if(pill&&pill.parentNode)pill.parentNode.insertBefore(b,pill);else host.appendChild(b)}
  document.readyState==='loading'?document.addEventListener('DOMContentLoaded',button):button();
})();
