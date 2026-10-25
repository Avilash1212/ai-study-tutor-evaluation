import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"

answers_path = RESULTS_DIR / "prompt_v1_answers.json"
output_path = RESULTS_DIR / "prompt_v1_scored.json"

answers = json.loads(answers_path.read_text(encoding="utf-8"))

scored_results = []

for item in answers:
    answer = item.get("answer", "")
    answer_lower = answer.lower()
    keywords = item.get("required_keywords", [])

    matched_keywords = [
        keyword for keyword in keywords
        if keyword.lower() in answer_lower
    ]

    # A keyword check is only a basic signal, not proof of correctness.
    keyword_pass = (
        item.get("status") == "success"
        and len(keywords) > 0
        and len(matched_keywords) == len(keywords)
    )

    # TC-24: accept a semantically correct explanation of both types.
    if item.get("id") == "TC-24":
        keyword_pass = (
            item.get("status") == "success"
            and "aerobic" in answer_lower
            and "anaerobic" in answer_lower
            and "oxygen" in answer_lower
        )

    scored_results.append({
        **item,
        "matched_keywords": matched_keywords,
        "missing_keywords": [
            keyword for keyword in keywords
            if keyword.lower() not in answer_lower
        ],
        "keyword_check": "PASS" if keyword_pass else "REVIEW"
    })

output_path.write_text(
    json.dumps(scored_results, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

passed = sum(x["keyword_check"] == "PASS" for x in scored_results)
review = sum(x["keyword_check"] == "REVIEW" for x in scored_results)

print(f"Cases scored: {len(scored_results)}")
print(f"Keyword check passed: {passed}")
print(f"Needs review: {review}")
print(f"Scored results saved to: {output_path}")
print("\nFirst case:")
print(json.dumps(scored_results[0], indent=2, ensure_ascii=False))
