# AI Study Tutor — Hallucination Evaluation System

## Overview
An AI product evaluation project that tests whether a study tutor answers from a supplied study guide, handles ambiguity, acknowledges missing information, and resists misleading questions.

## Problem
AI tutors can give unsupported or misleading answers. A product team needs a repeatable way to evaluate answer quality before deploying the tutor to students.

## Evaluation Dataset
- 30 test cases
- 12 answerable questions
- 8 unanswerable questions
- 5 ambiguous questions
- 5 adversarial questions

The test cases cover cellular respiration concepts and include expected actions, reference facts, required keywords, and scoring notes.

## Experiment
Two prompt versions were evaluated against the same test cases using Gemini 3.5 Flash Lite.

- Prompt V1: baseline tutor instructions
- Prompt V2: clearer rules for unsupported premises, ambiguity, scientific distinctions, and concise answers

## Preliminary Results
| Metric | Prompt V1 | Prompt V2 |
|---|---:|---:|
| Cases evaluated | 30 | 30 |
| Keyword checks passed | 18/30 (60%) | 18/30 (60%) |

V2 changed the outcome for two cases: TC-25 changed from review to pass, while TC-21 changed from pass to review. The net change was zero cases.

**Important:** These are keyword-check results, not verified factual-accuracy scores. Exact keyword matching can flag correct answers that use different wording. Semantic correctness requires a stronger evaluation method.

## Product Learnings
1. Prompt changes should be evaluated against a fixed test set.
2. Keyword matching is useful for simple checks but is insufficient as a standalone quality metric.
3. Ambiguous questions, unsupported premises, and refusal behavior need explicit evaluation.
4. Evaluation should include both answer quality and the risk of unsupported claims.

## Limitations
- The test set contains only 30 questions from one science topic.
- Keyword matching does not reliably measure semantic correctness.
- Results may vary between model versions and runs.
- Broader testing and human-reviewed or calibrated semantic evaluation are needed before drawing deployment conclusions.

## Tech Stack
- Python
- Google Gemini API
- JSON test cases
- Automated evaluation scripts

## How to Run
1. Install dependencies: `py -m pip install google-genai python-dotenv`
2. Add your Gemini API key to a local `.env` file.
3. Keep `.env` private; never commit API keys.
4. Run the evaluation and scoring scripts from the project directory.

## Future Improvements
- Add semantic evaluation and human-reviewed reference labels.
- Track refusal quality, factual support, and hallucination risk separately.
- Build a dashboard for results by question category.
- Expand the dataset to more subjects and difficulty levels.
