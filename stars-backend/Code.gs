/* Chowdie's Learning Den: Star Bank backend (Google Apps Script, bound to a Google Sheet).
   Setup steps are in SETUP.md next to this file. Change PARENT_PIN before you deploy. */
const PARENT_PIN = 'CHANGE-ME';            // grown-ups type this in the Star Bank to give out rewards
const USERS = ['willis', 'megan', 'daddy']; // Mommy doesn't collect stars
const WEEK = 7 * 864e5;
const BONUS = { deck: 3, boss: 5, daddy: 10, story: 2 };
const HEAD = ['Time', 'User', 'Type', 'Key', 'OK', 'Stars', 'Note', 'Deck', 'Id'];

function doGet(e) { return reply(handle((e && e.parameter) || {})); }
function doPost(e) {
  let p = {};
  try { p = JSON.parse(e.postData.contents); } catch (err) {}
  return reply(handle(p));
}
function reply(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

function sheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName('Stars');
  if (!sh) { sh = ss.insertSheet('Stars'); sh.appendRow(HEAD); sh.setFrozenRows(1); }
  return sh;
}
function rows(sh) {
  const n = sh.getLastRow();
  if (n < 2) return [];
  return sh.getRange(2, 1, n - 1, HEAD.length).getValues().map(r => ({
    ts: new Date(r[0]).getTime(), user: r[1], type: r[2], key: r[3], ok: r[4] === true || r[4] === 'TRUE', stars: Number(r[5]) || 0, note: r[6], deck: r[7], id: r[8]
  }));
}

function handle(p) {
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const sh = sheet(), all = rows(sh), now = Date.now();
    if (p.op === 'sync') {
      if (USERS.indexOf(p.user) < 0) return { ok: false, error: 'unknown user' };
      const mine = all.filter(r => r.user === p.user), add = [], results = [];
      (p.events || []).slice(0, 500).forEach(ev => {
        const seen = mine.find(r => r.id && r.id === ev.id);
        if (seen) { results.push({ id: ev.id, stars: seen.stars, kind: 'dup' }); return; }
        let stars = 0, kind;
        if (ev.type === 'attempt') {
          const last = mine.filter(r => r.type === 'attempt' && r.key === ev.key).reduce((t, r) => Math.max(t, r.ts), 0);
          if (last && now - last < WEEK) kind = 'resting';
          else if (!ev.ok) kind = 'miss';
          else {
            stars = ev.value === 2 ? 2 : 1;
            kind = mine.some(r => r.key === ev.key && r.stars > 0) ? 'review' : 'new';
          }
        } else if (ev.type === 'bonus') {
          if (mine.some(r => r.type === 'bonus' && r.key === ev.key)) kind = 'had';
          else { stars = BONUS[ev.kind] || 0; kind = 'bonus'; }
        } else return;
        // a question still resting is not logged, so practising it again doesn't restart its 7 days
        if (kind === 'had' || kind === 'resting') { results.push({ id: ev.id, stars: 0, kind }); return; }
        const row = { ts: now, user: p.user, type: ev.type, key: String(ev.key || '').slice(0, 200), ok: !!ev.ok, stars, note: String(ev.note || '').slice(0, 200), deck: String(ev.deck || '').slice(0, 100), id: String(ev.id || '').slice(0, 40) };
        mine.push(row); add.push(row); results.push({ id: ev.id, stars, kind });
      });
      append(sh, add);
      return { ok: true, results, state: state(mine, now) };
    }
    if (p.op === 'bank') {
      const users = {};
      USERS.forEach(u => { const s = state(all.filter(r => r.user === u), now); users[u] = { balance: s.balance, lifetime: s.lifetime, spent: s.spent }; });
      const recent = all.filter(r => r.stars !== 0).slice(-300).reverse().map(r => ({ ts: r.ts, user: r.user, type: r.type, stars: r.stars, note: r.note }));
      return { ok: true, users, recent };
    }
    if (p.op === 'reward') {
      if (String(p.pin) !== PARENT_PIN) return { ok: false, error: 'pin' };
      if (USERS.indexOf(p.user) < 0) return { ok: false, error: 'unknown user' };
      const n = Math.round(Number(p.stars));
      if (!n || Math.abs(n) > 1000) return { ok: false, error: 'amount' };
      const s = state(all.filter(r => r.user === p.user), now);
      if (n < 0 && s.balance + n < 0) return { ok: false, error: 'not enough stars' };
      append(sh, [{ ts: now, user: p.user, type: n < 0 ? 'redeem' : 'gift', key: '', ok: true, stars: n, note: String(p.note || '').slice(0, 200), deck: '', id: String(p.id || '').slice(0, 40) }]);
      return { ok: true };
    }
    return { ok: false, error: 'unknown op' };
  } finally { lock.releaseLock(); }
}

function append(sh, list) {
  if (!list.length) return;
  sh.getRange(sh.getLastRow() + 1, 1, list.length, HEAD.length)
    .setValues(list.map(r => [new Date(r.ts), r.user, r.type, r.key, r.ok, r.stars, r.note, r.deck, r.id]));
}

function state(mine, now) {
  let lifetime = 0, spent = 0;
  const recent = {}, earned = {}, bonuses = [];
  mine.forEach(r => {
    if (r.stars > 0) lifetime += r.stars; else spent -= r.stars;
    if (r.type === 'attempt') {
      if (now - r.ts < WEEK) recent[r.key] = Math.max(recent[r.key] || 0, r.ts);
      if (r.stars > 0) earned[r.key] = 1;
    }
    if (r.type === 'bonus') bonuses.push(r.key);
  });
  return { balance: lifetime - spent, lifetime, spent, recent, earned: Object.keys(earned), bonuses };
}
