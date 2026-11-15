# Experiments Log

Run with: `python evaluate.py`

## Results on the first test set (8 cases, 40 grades)

| # | Change | Model | Accuracy | Kept? |
|---|--------|-------|----------|-------|
| 1 | Baseline: all 5 checks in one request, verdict before reason | llama3.2 (3B) | 80% (32/40) | Yes |
| 2 | Ask for the reason **before** the verdict | llama3.2 (3B) | 85% (34/40) | Yes |
| 3 | Clearer pass/fail rules in the prompt | llama3.2 (3B) | 85% (34/40) | Yes |
| 4 | Bigger model | llama3.1:8b | 88% (35/40) | Yes |
| 5 | One check per request (5 separate requests) | llama3.1:8b | 80% (32/40) | No (reverted) |

## Results on the expanded test set (20 cases, 100 grades)

| # | Setup | Model | Accuracy |
|---|-------|-------|----------|
| 6 | Same as experiment 4 | llama3.1:8b | **92% (92/100)** |

Accuracy by check:

| Check | Accuracy |
|-------|----------|
| Recommends professional help | 95% |
| Avoids overconfidence | 100% |
| Safe medication advice | 80% |
| Factually sound | 85% |
| Includes warning signs | 100% |

Note: results from the two test sets can't be compared directly, because they measure different cases.

## What I learned

- **Reason before verdict helped.** When the model wrote "pass" or "fail" first, it often gave a reason that contradicted its own verdict. Asking for the reason first fixed most of the medication-check errors (50% → 88% on that check).
- **Clearer rules didn't change the overall score.** Errors moved between checks, but the small 3B model still contradicted itself. This suggested model size was the main limit.
- **The bigger model helped a little.** Overconfidence and warning-sign checks reached 100%. Remaining errors came from one problem in an answer spilling over into other checks.
- **One check per request made it worse.** Focusing on a single rule made the model too picky. It invented problems (e.g. calling soap a medicine), and the factual check dropped to 50%.
- **The checker is consistent.** The original 8 cases gave the same mistakes on the expanded run, and the 12 new cases added only 3 mistakes.
- **The medication check fails in both directions.** It treats home remedies (butter, warm fluids) as medicines, and it sometimes assumes "see a GP" is enough for unsafe medicine use (e.g. sleeping pills every night).
- **Wrong advice is not the same as a wrong fact.** "Drink as little as possible" for diarrhoea is unsafe, but the model said there was "no medical fact" to check. A future version should check whether the *advice* is medically sound, not only the facts.

## Limitations

- 20 test cases is still a small set. Expected grades were written by one person, and some are arguable (e.g. whether "you definitely have bronchitis" is also a factual error).
- Only one model family (Llama) was tested.
- The checker itself is an AI, so it can make mistakes and should not be used as medical advice.