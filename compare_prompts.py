import json
from pathlib import Path

def load(path):
    return {x["id"]: x for x in json.loads(Path(path).read_text(encoding="utf-8"))}

v1 = load("results/prompt_v1_scored.json")
v2 = load("results/prompt_v2_scored.json")
ids = sorted(set(v1) & set(v2))

passed1 = lambda i: v1[i].get("keyword_check") == "PASS"
passed2 = lambda i: v2[i].get("keyword_check") == "PASS"

p1 = sum(passed1(i) for i in ids)
p2 = sum(passed2(i) for i in ids)
improved = [i for i in ids if not passed1(i) and passed2(i)]
regressed = [i for i in ids if passed1(i) and not passed2(i)]

report = f"""PROMPT V1 vs V2 — AUTOMATED COMPARISON
Cases compared: {len(ids)}
V1 keyword checks passed: {p1}/{len(ids)} ({p1/len(ids)*100:.1f}%)
V2 keyword checks passed: {p2}/{len(ids)} ({p2/len(ids)*100:.1f}%)
Change: {p2-p1:+d} cases
Review → PASS: {len(improved)} — {', '.join(improved) or 'None'}
PASS → Review: {len(regressed)} — {', '.join(regressed) or 'None'}

Important: keyword checks are a rough screening metric, not true factual accuracy.
"""
Path("results/prompt_comparison.txt").write_text(report, encoding="utf-8")
print(report)
print("Saved to results/prompt_comparison.txt")
