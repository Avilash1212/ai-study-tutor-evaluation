
import json
from pathlib import Path

# Find the project folder and data files
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

study_guide_path = DATA_DIR / "cellular_respiration.txt"
test_cases_path = DATA_DIR / "test_cases.json"

# Read the study guide
study_guide = study_guide_path.read_text(encoding="utf-8")

# Read the 30 test cases
test_cases = json.loads(
    test_cases_path.read_text(encoding="utf-8")
)

print("Study guide loaded:", len(study_guide), "characters")
print("Test cases loaded:", len(test_cases))
print("Evaluation setup is ready!")

