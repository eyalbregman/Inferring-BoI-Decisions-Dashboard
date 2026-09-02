"""Phase 4: build the dashboard -> index.html at the repo root (the one canonical file:
in the folder, in git, and served by GitHub Pages from main/). Two sheets: reasoning-only
vs prior-rate-known. Chart.js from cdnjs."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S_BLIND = json.load(open(os.path.join(ROOT, 'results', 'scores.json')))
S_RATE = json.load(open(os.path.join(ROOT, 'results', 'scores_rate.json')))
PAYLOAD = json.dumps({"blind": S_BLIND, "rate": S_RATE}, indent=1)

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
.sub{color:var(--muted);margin:0 0 26px;max-width:64ch}

.tabs{display:flex;gap:4px;margin:0 0 22px;border-bottom:1px solid var(--line)}
.tab{appearance:none;border:0;background:none;font:inherit;font-weight:500;cursor:pointer;
  color:var(--muted);padding:11px 4px;margin-right:22px;border-bottom:2px solid transparent;
  transition:color .12s,border-color .12s}
.tab:hover{color:var(--ink)}
.tab[aria-selected="true"]{color:var(--ink);border-color:var(--accent)}
.tab:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:3px}

.sheetsub{color:var(--muted);font-size:13.5px;margin:0 0 22px;max-width:66ch}

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

footer{margin-top:26px;color:var(--muted);font-size:12px;line-height:1.6;max-width:70ch}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

BODY = r"""
<div class="wrap">
  <p class="eyebrow">Bank of Israel &nbsp;/&nbsp; Nov 2018 &ndash; today</p>
  <h1>Inferring Bank of Israel rate decisions</h1>
  <p class="sub">Every Bank of Israel interest-rate announcement is stripped of its headline, the
     decision sentence, the policy-rate figure and the dates. A model then reads only what's left
     &mdash; the economic reasoning &mdash; and predicts <b>lower</b>, <b>maintain</b> or <b>raise</b>.
     Each announcement is judged in a fresh, isolated context.</p>

  <p class="sheetsub" id="sheetsub"></p>

  <div class="tabs" role="tablist" aria-label="Model condition">
    <button class="tab" role="tab" data-v="blind" aria-selected="true">Reasoning only</button>
    <button class="tab" role="tab" data-v="rate" aria-selected="false">&plus; prior rate level</button>
  </div>

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

  <footer id="foot"></footer>
</div>
"""

SCRIPT = r"""
<script id="data" type="application/json">__DATA__</script>
<script>
const ALL = JSON.parse(document.getElementById('data').textContent);
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const fmtPct = x => x==null ? 'n/a' : Math.round(x*100)+'%';
const SHEETSUB = {
  blind: "The model sees only the blinded rationale — nothing about the rate, the date, or the previous decision.",
  rate: "The model sees only the blinded rationale, and here the previous rate level also — but still nothing "
      + "about the date or the previous decision."
};
let charts = [];

function render(v){
  const S = ALL[v], pc = S.per_class_accuracy;
  document.querySelectorAll('.tab').forEach(t=>t.setAttribute('aria-selected', t.dataset.v===v));
  document.getElementById('sheetsub').textContent = SHEETSUB[v];

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

  document.getElementById('foot').textContent =
    `Ground truth is parsed from each press-release title. The interpreter runs as a subagent in a fresh `
    + `context per announcement and never sees another announcement, the dates, or the real decisions. `
    + `${S.n_decisions} decisions. Source pages retrieved via the Wayback Machine.`;
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
