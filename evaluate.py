import json

from checker import SafetyReport, check_answer

CHECKS = list(SafetyReport.model_fields)


def main():
    with open("test_cases.json") as f:
        cases = json.load(f)

    total = 0
    correct = 0
    per_check = {check: {"correct": 0, "total": 0} for check in CHECKS}
    mistakes = []

    for case in cases:
        print(f"Checking {case['id']}...")
        _, results = check_answer(case["question"], case["answer"])

        for check in CHECKS:
            expected = case["expected"][check]
            actual = results[check]["result"]
            total += 1
            per_check[check]["total"] += 1

            if expected == actual:
                correct += 1
                per_check[check]["correct"] += 1
            else:
                mistakes.append((case["id"], check, expected, actual, results[check]["reason"]))

    print(f"\n=== Overall accuracy: {correct}/{total} ({correct / total:.0%}) ===\n")

    print("Accuracy by check:")
    for check, counts in per_check.items():
        accuracy = counts["correct"] / counts["total"]
        print(f"  {check}: {counts['correct']}/{counts['total']} ({accuracy:.0%})")

    print(f"\nMistakes ({len(mistakes)}):")
    if not mistakes:
        print("  None")
    for case_id, check, expected, actual, reason in mistakes:
        print(f"  - {case_id} / {check}: expected {expected}, got {actual}")
        print(f"    Reason given: {reason}")


if __name__ == "__main__":
    main()
    