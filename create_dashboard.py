import json
from pathlib import Path
from collections import Counter
from html import escape

root = Path(".")
out = root / "results"
out.mkdir(exist_ok=True)

def load(name):
    return json.loads((out / name).read_text(encoding="utf-8"))

v1 = load("prompt_v1_scored.json")
v2 = load("prompt_v2_scored.json")

def summary(rows):
    total = len(rows)
    passed = sum(r.get("keyword_check") == "PASS" for r in rows)
    categories = Counter(r.get("category", "Unknown") for r in rows)
    return total, passed, categories

n1, p1, _ = summary(v1)
n2, p2, categories = summary(v2)

comparison = (out / "prompt_comparison.txt").read_text(encoding="utf-8")
cards = "".join(
    f'<div class="card"><div class="muted">{escape(cat.title())}</div>'
    f'<div class="number">{count}</div><div class="muted">test cases</div></div>'
    for cat, count in sorted(categories.items())
)

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Study Tutor Evaluation</title>
<style>
body{{font-family:Arial,sans-serif;max-width:1000px;margin:40px auto;padding:0 20px;background:#f5f7fb;color:#172033}}
h1{{margin-bottom:8px}} .muted{{color:#657089;font-size:14px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin:22px 0}}
.card{{background:white;padding:22px;border-radius:12px;box-shadow:0 2px 10px #1827440c}}
.number{{font-size:30px;font-weight:700;margin:10px 0}}
.panel{{background:white;padding:22px;border-radius:12px;margin:16px 0;overflow-wrap:anywhere}}
table{{width:100%;border-collapse:collapse}}th,td{{padding:12px;text-align:left;border-bottom:1px solid #e6eaf1}}
.note{{background:#fff8e7;padding:14px;border-radius:8px;line-height:1.5}}
</style></head><body>
<h1>AI Study Tutor</h1>
<p class="muted">Prompt evaluation dashboard · Gemini 3.5 Flash Lite · 30 test cases</p>
<div class="grid">
<div class="card"><div class="muted">Test cases</div><div class="number">{len(v2)}</div></div>
<div class="card"><div class="muted">V1 keyword passes</div><div class="number">{p1}/{n1}</div><div class="muted">{p1/n1*100:.1f}%</div></div>
<div class="card"><div class="muted">V2 keyword passes</div><div class="number">{p2}/{n2}</div><div class="muted">{p2/n2*100:.1f}%</div></div>
</div>
<h2>Test-set composition</h2><div class="grid">{cards}</div>
<div class="panel"><h2>Prompt comparison</h2>
<table><tr><th>Metric</th><th>Prompt V1</th><th>Prompt V2</th></tr>
<tr><td>Cases evaluated</td><td>{n1}</td><td>{n2}</td></tr>
<tr><td>Keyword checks passed</td><td>{p1}/{n1}</td><td>{p2}/{n2}</td></tr>
<tr><td>Keyword pass rate</td><td>{p1/n1*100:.1f}%</td><td>{p2/n2*100:.1f}%</td></tr>
</table></div>
<div class="panel"><h2>Interpretation</h2>
<p class="note">Keyword matching is a preliminary screening signal, not verified factual accuracy. Correct answers can be flagged when they use different wording. The current results do not establish that either prompt is more accurate.</p>
<h3>Product takeaway</h3>
<p>Use a fixed evaluation set to compare prompts, then improve the evaluator before making claims about factual accuracy or hallucination reduction.</p></div>
<div class="panel"><h2>Experiment notes</h2><pre>{escape(comparison)}</pre></div>
<p class="muted">Generated locally from existing JSON results. No additional model calls were made.</p>
</body></html>"""

(out / "dashboard.html").write_text(html, encoding="utf-8")
print("Dashboard created:", out / "dashboard.html")
print(f"V1: {p1}/{n1} keyword passes | V2: {p2}/{n2} keyword passes")
