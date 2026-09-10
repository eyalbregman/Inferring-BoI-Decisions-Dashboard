"""Phase 4: build the dashboard -> index.html at the repo root (the one canonical file:
in the folder, in git, and served by GitHub Pages from main/). Two sheets: reasoning-only
vs prior-rate-known. Chart.js from cdnjs."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S_BLIND = json.load(open(os.path.join(ROOT, 'results', 'scores.json')))
S_RATE = json.load(open(os.path.join(ROOT, 'results', 'scores_rate.json')))
FEDS_PATH = os.path.join(ROOT, 'results', 'fed_sentence_scores.json')
S_FEDSENT = json.load(open(FEDS_PATH)) if os.path.exists(FEDS_PATH) else []
PAYLOAD = json.dumps({"blind": S_BLIND, "rate": S_RATE, "fedSent": S_FEDSENT}, indent=1)

FONTS = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&'
         'family=IBM+Plex+Serif:wght@600&display=swap">')
CHARTJS = '<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>'

STYLE = r"""
:root{
  --bg:#f2f5f8; --card:#ffffff; --ink:#182130; --muted:#586576;
  --line:#e0e5ec; --line-soft:#eef1f5;
  --accent:#1f4e79;
  --good:#347b53; --good-fill:#e7f3ec; --good-edge:#8bc4a3;
  --bad:#bd4032;  --bad-fill:#fbe9e6;  --bad-edge:#e0a49b;
  --warn:#b9772a;
  --shadow:0 1px 2px rgba(24,33,48,.04), 0 1px 10px rgba(24,33,48,.03);
}
:root:not([data-theme="light"]){ }
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#10141a; --card:#181d25; --ink:#e7ecf2; --muted:#98a3b2;
    --line:#2a313c; --line-soft:#21272f;
    --accent:#7db0dd;
    --good:#63b98a; --good-fill:#16241d; --good-edge:#2f5a44;
    --bad:#e08074;  --bad-fill:#2a1a18;  --bad-edge:#5c3a34;
    --warn:#d69a52;
    --shadow:0 1px 2px rgba(0,0,0,.3), 0 1px 12px rgba(0,0,0,.2);
  }
}
:root[data-theme="dark"]{
  --bg:#10141a; --card:#181d25; --ink:#e7ecf2; --muted:#98a3b2;
  --line:#2a313c; --line-soft:#21272f;
  --accent:#7db0dd;
  --good:#63b98a; --good-fill:#16241d; --good-edge:#2f5a44;
  --bad:#e08074;  --bad-fill:#2a1a18;  --bad-edge:#5c3a34;
  --warn:#d69a52;
  --shadow:0 1px 2px rgba(0,0,0,.3), 0 1px 12px rgba(0,0,0,.2);
}

*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"IBM Plex Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased;}
.wrap{max-width:1000px;margin:0 auto;padding:44px 22px 72px;}

.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:11.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--accent);margin:0 0 10px;font-weight:500}
h1{font-family:"IBM Plex Serif",Georgia,serif;font-weight:600;font-size:27px;line-height:1.25;
  text-wrap:balance;margin:0 0 10px;letter-spacing:-.005em}
.sub{color:var(--muted);margin:0 0 22px;max-width:64ch}
.sub b{color:inherit}

.tabs{display:flex;flex-wrap:wrap;gap:2px 0;margin:0 0 22px;border-bottom:1px solid var(--line)}
.tab{appearance:none;border:0;background:none;font:inherit;font-size:14px;font-weight:500;cursor:pointer;
  color:var(--muted);padding:11px 4px;margin-right:22px;border-bottom:2px solid transparent;
  transition:color .12s,border-color .12s}
.tab:hover{color:var(--ink)}
.tab[aria-selected="true"]{color:var(--ink);border-color:var(--accent)}
.tab:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:3px}


.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));gap:12px;margin-bottom:6px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:15px 16px;box-shadow:var(--shadow)}
.stat.lead{grid-column:span 2}
.stat .k{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--muted)}
.stat .v{font-size:26px;font-weight:600;margin-top:5px;font-variant-numeric:tabular-nums;letter-spacing:-.01em}
.stat.lead .v{font-size:34px}
.stat .n{font-size:12px;color:var(--muted);margin-top:3px}
.stat .bar{height:4px;border-radius:2px;background:var(--line-soft);margin-top:10px;overflow:hidden}
.stat .bar>i{display:block;height:100%;background:var(--accent)}

.note{border-radius:12px;padding:13px 16px;font-size:13px;margin:16px 0 0;border:1px solid var(--line)}
.note.base{background:var(--card);color:var(--muted);box-shadow:var(--shadow)}
.note.good{background:var(--good-fill);border-color:var(--good-edge);color:var(--good)}
.note b{color:var(--ink);font-weight:600}

.charts{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:30px 0 34px}
@media(max-width:680px){.charts{grid-template-columns:1fr}.stat.lead{grid-column:span 1}}
.panel{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px;box-shadow:var(--shadow)}
.panel h2{font-size:12px;font-family:"IBM Plex Mono",monospace;letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted);margin:0 0 14px;font-weight:500}
.cwrap{position:relative;height:270px;max-width:300px;margin:0 auto}
.cwrap.wide{max-width:none;height:340px}
.panel.full{grid-column:1/-1}
.tone-legend{display:flex;gap:18px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin:2px 0 18px}
.tone-legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:middle}
td.sc{font-family:"IBM Plex Mono",monospace;font-variant-numeric:tabular-nums;text-align:right}
td.sc.h{color:var(--bad)} td.sc.d{color:var(--accent)}
.bydec{display:grid;grid-template-columns:repeat(3,1fr);gap:0}
.bydec .cell{padding:14px 16px;border-right:1px solid var(--line)}
.bydec .cell:last-child{border-right:0}
.bydec .lbl{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.bydec .val{font-size:30px;font-weight:600;font-variant-numeric:tabular-nums;letter-spacing:-.01em;margin-top:4px}
.bydec .val.h{color:var(--bad)} .bydec .val.d{color:var(--accent)}
.bydec .sub2{font-size:12px;color:var(--muted);margin-top:2px}
.bydec .track{height:6px;border-radius:3px;background:var(--line-soft);margin-top:10px;position:relative;overflow:hidden}
.bydec .track>i{position:absolute;top:0;bottom:0;background:currentColor;opacity:.55}

.tablewrap{background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;box-shadow:var(--shadow)}
table{width:100%;border-collapse:collapse}
th,td{padding:9px 14px;text-align:left;font-size:13.5px;border-bottom:1px solid var(--line-soft)}
th{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted);font-weight:500;background:var(--line-soft)}
tbody tr:last-child td{border-bottom:0}
.mono{font-family:"IBM Plex Mono",monospace;font-variant-numeric:tabular-nums}
tr.ok{background:var(--good-fill)}
tr.ok td:first-child{box-shadow:inset 3px 0 0 var(--good-edge)}
tr.bad{background:var(--bad-fill)}
tr.bad td:first-child{box-shadow:inset 3px 0 0 var(--bad-edge)}
.pill{display:inline-block;padding:1px 9px;border-radius:999px;font-size:12px;
  border:1px solid var(--line);background:var(--card);font-family:"IBM Plex Mono",monospace}
td.res .pill{border-color:currentColor}
tr.ok td.guess .pill{color:var(--good)}
tr.bad td.guess .pill{color:var(--bad)}

@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

BODY = r"""
<div class="wrap">
  <p class="eyebrow">Bank of Israel interest-rate announcements &nbsp;/&nbsp; Nov 2018 &ndash; today</p>
  <h1 id="h1">Inferring Bank of Israel interest-rate decisions</h1>
  <p class="sub" id="subp"></p>

  <div class="tabs" role="tablist" aria-label="View">
    <button class="tab" role="tab" data-v="blind" aria-selected="true">Decision from reasoning alone</button>
    <button class="tab" role="tab" data-v="rate" aria-selected="false">Decision &plus; prior rate level</button>
    <button class="tab" role="tab" data-v="fed" aria-selected="false">Fed-anchored hawkish&ndash;dovish tone</button>
  </div>

  <div id="view-infer">
    <div class="cards" id="cards"></div>
    <div class="note base" id="baseline-note"></div>
    <div class="note good" id="compare-note" hidden></div>

    <div class="charts">
      <div class="panel"><h2>Correct vs incorrect</h2><div class="cwrap"><canvas id="pie1"></canvas></div></div>
      <div class="panel"><h2>Where it went wrong</h2><div class="cwrap"><canvas id="pie2"></canvas></div></div>
    </div>

    <div class="tablewrap">
      <table id="tbl">
        <thead><tr><th>Date</th><th>New rate</th><th>Change</th><th>Agent guess</th><th>Reality</th></tr></thead>
        <tbody></tbody>
      </table>
    </div>
  </div>

  <div id="view-fed" hidden>
    <div class="cards" id="fed-cards"></div>

    <div class="panel full" id="fed-bydec" style="margin:4px 0 18px"></div>

    <div class="tone-legend">
      <span><i style="background:var(--bad)"></i>Hawkish (score &gt; 0)</span>
      <span><i style="background:var(--accent)"></i>Dovish (score &lt; 0)</span>
      <span>Marker = actual decision that month (&#9650; raise &nbsp; &#9644; maintain &nbsp; &#9660; lower)</span>
    </div>
    <div class="panel full" style="margin-bottom:22px">
      <h2>Fed-anchored sentence score by announcement &mdash; Nov 2018 to today</h2>
      <div class="cwrap wide"><canvas id="fedTL"></canvas></div>
    </div>
    <div class="tablewrap">
      <table id="fedtbl">
        <thead><tr><th>Date</th><th>Decision</th><th>Hawkish</th><th>Dovish</th><th>Neutral</th><th>Total</th><th>Score</th></tr></thead>
        <tbody></tbody>
      </table>
    </div>
  </div>
</div>
"""

SCRIPT = r"""
<script id="data" type="application/json">__DATA__</script>
<script>
const ALL = JSON.parse(document.getElementById('data').textContent);
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const fmtPct = x => x==null ? 'n/a' : Math.round(x*100)+'%';
const HEAD = {
  blind: "Inferring Bank of Israel interest-rate decisions",
  rate:  "Inferring Bank of Israel interest-rate decisions",
  fed:   "Fed-anchored hawkish&ndash;dovish tone"
};
const INTRO = {
  blind: "Every Bank of Israel interest-rate announcement is stripped of its headline, the decision "
       + "sentence, the policy-rate figure and the dates. A model then reads only what's left &mdash; "
       + "the economic reasoning &mdash; and predicts <b>lower</b>, <b>maintain</b> or <b>raise</b>, each "
       + "announcement judged in a fresh, isolated context. The model sees nothing about the rate, the "
       + "date, or the previous decision.",
  rate:  "Every Bank of Israel interest-rate announcement is stripped of its headline, the decision "
       + "sentence, the policy-rate figure and the dates. A model then reads only what's left &mdash; "
       + "the economic reasoning &mdash; and predicts <b>lower</b>, <b>maintain</b> or <b>raise</b>, each "
       + "announcement judged in a fresh, isolated context. Here it is also told the previous rate "
       + "<i>level</i> &mdash; but still nothing about the date or the previous decision.",
  fed:   "The Fed publishes a fully <b>hawkish</b> and a fully <b>dovish</b> draft of every policy "
       + "statement. Using that contrast as the basis, every sentence of every Bank of Israel "
       + "announcement is judged hawkish, dovish or neutral, and each announcement is scored "
       + "<b>(hawkish &minus; dovish) &divide; total sentences</b> &mdash; from &minus;1 (dovish) to &plus;1 (hawkish)."
};
let charts = [];

function render(v){
  document.querySelectorAll('.tab').forEach(t=>t.setAttribute('aria-selected', t.dataset.v===v));
  const isFed = v === 'fed';
  document.getElementById('view-infer').hidden = isFed;
  document.getElementById('view-fed').hidden = !isFed;
  document.getElementById('h1').innerHTML = HEAD[v];
  document.getElementById('subp').innerHTML = INTRO[v];
  if (isFed){ renderFed(); return; }

  const S = ALL[v], pc = S.per_class_accuracy;

  const acc = fmtPct(S.overall_accuracy);
  const cards = [
    ['Overall accuracy', acc, S.correct+' of '+S.n_decisions+' correct', S.overall_accuracy, true],
    ['Decisions', S.n_decisions, 'Nov 2018 – today', null, false],
    ['Majority baseline', fmtPct(S.majority_class_baseline), "always guess '"+S.majority_class+"'", S.majority_class_baseline, false],
    ['Persistence baseline', fmtPct(S.persistence_baseline), 'guess = last meeting', S.persistence_baseline, false],
    ['Lower', fmtPct(pc.lower.accuracy), pc.lower.correct+' / '+pc.lower.n, pc.lower.accuracy, false],
    ['Maintain', fmtPct(pc.maintain.accuracy), pc.maintain.correct+' / '+pc.maintain.n, pc.maintain.accuracy, false],
    ['Raise', fmtPct(pc.raise.accuracy), pc.raise.correct+' / '+pc.raise.n, pc.raise.accuracy, false],
  ];
  document.getElementById('cards').innerHTML = cards.map(c=>{
    const bar = c[3]==null ? '' : `<div class="bar"><i style="width:${Math.round(c[3]*100)}%"></i></div>`;
    return `<div class="stat${c[4]?' lead':''}"><div class="k">${c[0]}</div>`
         + `<div class="v">${c[1]}</div><div class="n">${c[2]}</div>${bar}</div>`;
  }).join('');

  const liftM = Math.round((S.overall_accuracy - S.majority_class_baseline)*100);
  const liftP = Math.round((S.overall_accuracy - S.persistence_baseline)*100);
  let note = `Rate decisions come in long runs, so the number only means something next to a baseline that `
    + `ignores the text. Always guessing &ldquo;${S.majority_class}&rdquo; scores <b>${fmtPct(S.majority_class_baseline)}</b>; `
    + `guessing &ldquo;same as last meeting&rdquo; scores <b>${fmtPct(S.persistence_baseline)}</b>. `
    + `The model scored <b>${acc}</b> &mdash; ${liftM>=0?'+':''}${liftM} over the first, ${liftP>=0?'+':''}${liftP} over the second.`;
  if (pc.lower.n && pc.lower.correct===0) note += ` It gets raise and maintain almost always right, but caught none of the ${pc.lower.n} lower decisions.`;
  document.getElementById('baseline-note').innerHTML = note;

  const cn = document.getElementById('compare-note');
  if (v==='rate'){
    const B = ALL.blind, bL = B.per_class_accuracy.lower.accuracy;
    const d = Math.round((S.overall_accuracy - B.overall_accuracy)*100);
    const dl = Math.round((pc.lower.accuracy - bL)*100);
    cn.innerHTML = `<b>Versus the reasoning-only sheet:</b> overall ${fmtPct(B.overall_accuracy)} &rarr; ${acc} `
      + `(${d>=0?'+':''}${d} pts), and <b>lower</b> ${fmtPct(bL)} &rarr; ${fmtPct(pc.lower.accuracy)} (${dl>=0?'+':''}${dl} pts). `
      + `Knowing the rate level mostly helps the model see that a high rate leaves room to lower it, and that a rate `
      + `already at the floor cannot be lowered &mdash; not that it reads tone any better.`;
    cn.hidden = false;
  } else cn.hidden = true;

  charts.forEach(c=>c.destroy()); charts = [];
  const gridInk = css('--ink');
  Chart.defaults.font.family = "'IBM Plex Sans', sans-serif";
  Chart.defaults.color = css('--muted');
  charts.push(new Chart(document.getElementById('pie1'), {
    type:'doughnut',
    data:{ labels:['Correct','Incorrect'],
      datasets:[{ data:[S.correct,S.incorrect], borderColor:css('--card'), borderWidth:2,
        backgroundColor:[css('--good'), css('--bad')] }] },
    options:{ responsive:true, maintainAspectRatio:false, animation:false, cutout:'58%',
      plugins:{ legend:{position:'bottom', labels:{boxWidth:10, boxHeight:10, padding:14}},
        tooltip:{callbacks:{label:c=>`${c.label}: ${c.parsed} (${Math.round(100*c.parsed/S.n_decisions)}%)`}} } }
  }));
  const ep = S.error_pairs;
  const palette = [css('--bad'), css('--warn'), css('--accent'), '#7a6ca8', '#5a8fc4'];
  const c2 = document.getElementById('pie2');
  if (ep.length){
    charts.push(new Chart(c2, {
      type:'doughnut',
      data:{ labels: ep.map(e=>e.label),
        datasets:[{ data: ep.map(e=>e.count), borderColor:css('--card'), borderWidth:2,
          backgroundColor: ep.map((_,i)=>palette[i%palette.length]) }] },
      options:{ responsive:true, maintainAspectRatio:false, animation:false, cutout:'58%',
        plugins:{ legend:{position:'bottom', labels:{boxWidth:10, boxHeight:10, padding:10, font:{size:11}}},
          tooltip:{callbacks:{label:c=>`${c.label}: ${c.parsed}`}} } }
    }));
  } else {
    c2.parentElement.innerHTML = '<p style="color:var(--muted);text-align:center;padding-top:90px">No incorrect predictions.</p>';
  }

  const rows = [...S.rows].sort((a,b)=>a.date.localeCompare(b.date));
  const chg = x => x===0 ? 'held' : (x>0?'+':'') + x.toFixed(2) + ' pp';
  document.querySelector('#tbl tbody').innerHTML = rows.map(r=>`
    <tr class="${r.correct?'ok':'bad'}">
      <td class="mono">${r.date}</td>
      <td class="mono">${r.new_rate.toFixed(2)}%</td>
      <td class="mono">${chg(r.change)}</td>
      <td class="guess"><span class="pill">${r.guess ?? '—'}</span></td>
      <td class="res"><span class="pill">${r.actual}</span></td>
    </tr>`).join('');
}
function renderFed(){
  const T = [...ALL.fedSent].sort((a,b)=>a.date.localeCompare(b.date));
  const haw = css('--bad'), dov = css('--accent'), mut = css('--muted');
  const n = T.length;
  const mean = T.reduce((s,r)=>s+r.score,0)/n;
  const sH = T.reduce((s,r)=>s+r.H,0), sD = T.reduce((s,r)=>s+r.D,0), sN = T.reduce((s,r)=>s+r.N,0);
  const tot = sH+sD+sN;
  const grp = d => { const v=T.filter(r=>r.decision===d); return {m:v.reduce((s,r)=>s+r.score,0)/v.length, n:v.length}; };
  const R = grp('raise'), M = grp('maintain'), L = grp('lower');
  const cards = [
    ['Announcements', n, 'raw text, Nov 2018 – today', true],
    ['Sentences classified', tot.toLocaleString(), `${Math.round(100*sH/tot)}% hawkish · ${Math.round(100*sD/tot)}% dovish · ${Math.round(100*sN/tot)}% neutral`, false],
    ['Mean score', (mean>=0?'+':'')+mean.toFixed(2), mean>=0?'net hawkish wording':'net dovish wording', false],
  ];
  document.getElementById('fed-cards').innerHTML = cards.map(c=>
    `<div class="stat${c[3]?' lead':''}"><div class="k">${c[0]}</div><div class="v">${c[1]}</div><div class="n">${c[2]}</div></div>`
  ).join('');

  // score grouped by the decision that was actually taken (the decision is NOT used to compute the score)
  const sgn = (x)=> (x>=0?'+':'')+x.toFixed(2);
  const bar = (x)=>{ const p = Math.min(50, Math.abs(x)/0.4*50);
    return x>=0 ? `left:50%;width:${p}%` : `right:50%;width:${p}%`; };
  const cell = (lbl, g, cls)=>`<div class="cell">
      <div class="lbl">${lbl} &nbsp;<span style="opacity:.6">n=${g.n}</span></div>
      <div class="val ${cls}">${sgn(g.m)}</div>
      <div class="sub2">mean Fed-anchored score</div>
      <div class="track" style="color:${cls==='h'?'var(--bad)':cls==='d'?'var(--accent)':'var(--muted)'}"><i style="${bar(g.m)}"></i></div>
    </div>`;
  document.getElementById('fed-bydec').innerHTML =
    `<div class="bydec">${cell('When the Bank hiked', R, 'h')}${cell('When it held', M, 'd')}${cell('When it cut', L, 'd')}</div>`;

  const shape = {raise:'triangle', maintain:'rect', lower:'triangle'};
  const rot = T.map(r=>r.decision==='lower'?180:0);
  charts.forEach(c=>c.destroy()); charts = [];
  Chart.defaults.font.family = "'IBM Plex Sans', sans-serif";
  Chart.defaults.color = mut;
  charts.push(new Chart(document.getElementById('fedTL'), {
    type:'bar',
    data:{ labels: T.map(r=>r.date),
      datasets:[
        { type:'bar', data: T.map(r=>r.score),
          backgroundColor: T.map(r=>r.score>=0?haw:dov), borderWidth:0,
          categoryPercentage:0.9, barPercentage:0.95, order:2 },
        { type:'line', data: T.map(r=>r.score), showLine:false, order:1,
          pointStyle: T.map(r=>shape[r.decision]||'rect'), rotation: rot,
          pointRadius: T.map(r=>r.decision==='maintain'?4:6),
          pointBackgroundColor:'transparent',
          pointBorderColor: css('--ink'), pointBorderWidth:1.5 }
      ] },
    options:{ responsive:true, maintainAspectRatio:false, animation:false,
      scales:{
        y:{ min:-0.7, max:0.7, title:{display:true,text:'dovish  ←   Fed-anchored score   →  hawkish'},
            grid:{color:c=>Math.abs(c.tick.value)<1e-9?css('--muted'):css('--line-soft')}, ticks:{stepSize:0.1} },
        x:{ ticks:{ maxRotation:90, minRotation:90, autoSkip:true, maxTicksLimit:24, font:{size:9} },
            grid:{display:false} } },
      plugins:{ legend:{display:false},
        tooltip:{ callbacks:{ title:i=>T[i[0].dataIndex].date,
          label:i=>{ const r=T[i.dataIndex];
            return [`score ${r.score>=0?'+':''}${r.score.toFixed(3)}  =  (${r.H} − ${r.D}) / ${r.n}`,
                    `decision that month: ${r.decision}`]; } } } } }
  }));

  const lab = d => d==='raise'?'raise':d==='lower'?'lower':'maintain';
  document.querySelector('#fedtbl tbody').innerHTML = T.map(r=>`
    <tr>
      <td class="mono">${r.date}</td>
      <td><span class="pill">${lab(r.decision)}</span></td>
      <td class="mono" style="text-align:right">${r.H}</td>
      <td class="mono" style="text-align:right">${r.D}</td>
      <td class="mono" style="text-align:right">${r.N}</td>
      <td class="mono" style="text-align:right">${r.n}</td>
      <td class="sc ${r.score>0?'h':r.score<0?'d':''}">${r.score>=0?'+':''}${r.score.toFixed(3)}</td>
    </tr>`).join('');
}

document.querySelectorAll('.tab').forEach(t=>t.addEventListener('click', ()=>render(t.dataset.v)));
render('blind');
</script>
""".replace("__DATA__", PAYLOAD)

PAGE = ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<title>Inferring BoI Rate Decisions</title>" + FONTS + CHARTJS
        + "<style>" + STYLE + "</style></head><body>" + BODY + SCRIPT + "</body></html>")

# One canonical file: index.html at the repo root — it is what sits in the folder, what git
# tracks, and what GitHub Pages serves. Regenerate, then commit + push to update everywhere.
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(PAGE)
print("wrote index.html")
