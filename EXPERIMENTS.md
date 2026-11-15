# Experiments Log

All results use the same 8 test cases in `test_cases.json` (40 grades in total: 8 answers × 5 checks).
Run with: `python evaluate.py`

| # | Change | Model | Accuracy | Kept? |
|---|--------|-------|----------|-------|
| 1 | Baseline: all 5 checks in one request, verdict before reason | llama3.2 (3B) | 80% (32/40) | Yes |
| 2 | Ask for the reason **before** the verdict | llama3.2 (3B) | 85% (34/40) | Yes |
| 3 | Clearer pass/fail rules in the prompt | llama3.2 (3B) | 85% (34/40) | Yes |
| 4 | Bigger model | llama3.1:8b | 88% (35/40) | Yes |
| 5 | One check per request (5 separate requests) | llama3.1:8b | 80% (32/40) | No (reverted) |

## What I learned

- **Reason before verdict helped.** When the model wrote "pass" or "fail" first, it often gave a reason that contradicted its own verdict. Asking for the reason first fixed most of the medication-check errors (50% → 88% on that check).
- **Clearer rules didn't change the overall score.** Errors moved between checks, but the small 3B model still contradicted itself. This suggested model size was the main limit.
- **The bigger model helped a little.** Overconfidence and warning-sign checks reached 100%. Remaining errors came from one problem in an answer spilling over into other checks.
- **One check per request made it worse.** Focusing on a single rule made the model too picky. It invented problems (e.g. calling soap a medicine), and the factual check dropped to 50%.

## Limitations

- Only 8 test cases, so one grade = 2.5%. Small differences (e.g. 85% vs 88%) may be noise.
- Expected grades were written by one person. Some are arguable (e.g. whether "you definitely have bronchitis" is also a factual error).
- Results can vary slightly between runs, even with temperature set to 0.