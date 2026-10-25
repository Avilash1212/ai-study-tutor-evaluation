import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3.5-flash-lite"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"
OUTPUT_PATH = RESULTS_DIR / "prompt_v2_answers.json"

if not API_KEY:
    raise ValueError("GEMINI_API_KEY was not found in your .env file.")

study_guide = (DATA_DIR / "cellular_respiration.txt").read_text(encoding="utf-8")
test_cases = json.loads(
    (DATA_DIR / "test_cases.json").read_text(encoding="utf-8")
)

client = genai.Client(api_key=API_KEY)

prompt = (BASE_DIR / "prompt_v2.txt").read_text(encoding="utf-8")

RESULTS_DIR.mkdir(exist_ok=True)

if OUTPUT_PATH.exists():
    results = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
else:
    results = []

results_by_id = {item["id"]: item for item in results}

pending_cases = [
    case for case in test_cases
    if case["id"] not in results_by_id
    or results_by_id[case["id"]].get("status") != "success"
]

print(f"Already successful: {sum(item.get('status') == 'success' for item in results_by_id.values())}")
print(f"Cases to retry: {len(pending_cases)}")

for index, case in enumerate(pending_cases, start=1):
    print(f"\n[{index}/{len(pending_cases)}] Running {case['id']}...")

    if index > 1:
        print("Waiting 65 seconds to respect the free-tier rate limit...")
        time.sleep(65)

    full_prompt = prompt.format(
        study_guide=study_guide,
        question=case["question"]
    )

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=full_prompt,
            config={"temperature": 0.0}
        )

        answer = response.text or ""
        status = "success"
        error = None
        print("Answer received.")

    except Exception as exc:
        answer = ""
        status = "error"
        error = str(exc)
        print(f"Request failed: {error[:300]}")

    results_by_id[case["id"]] = {
        "id": case["id"],
        "category": case["category"],
        "question": case["question"],
        "expected_action": case["expected_action"],
        "reference_fact": case["reference_fact"],
        "required_keywords": case.get("required_keywords", []),
        "scoring_notes": case.get("scoring_notes", ""),
        "model": MODEL,
        "answer": answer,
        "status": status,
        "error": error
    }

    ordered_results = [
        results_by_id[case_item["id"]]
        for case_item in test_cases
        if case_item["id"] in results_by_id
    ]

    OUTPUT_PATH.write_text(
        json.dumps(ordered_results, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

success_count = sum(
    item.get("status") == "success"
    for item in results_by_id.values()
)

print(f"\nFinished. Successful answers: {success_count}/{len(test_cases)}")
print(f"Results saved to: {OUTPUT_PATH}")
