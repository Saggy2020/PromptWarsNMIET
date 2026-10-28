"""
Deterministic Allergen Safety Eval Harness.
Tests 100% detection of allergen synonyms with ZERO false negatives.
"""

import json
import os
import sys

# Set UTF-8 encoding for standard output if needed
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.safety.ontology import resolve_allergen
from app.models.household import AllergenEnum

def run_safety_eval():
    data_path = os.path.join(os.path.dirname(__file__), "golden_data", "allergen_cases.json")
    with open(data_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    total_cases = len(cases)
    passed_cases = 0
    false_negatives = 0
    false_positives = 0

    print("=================================================================")
    print("[SAFETY EVAL] PANTRYPILOT DETERMINISTIC SAFETY EVALUATION")
    print("    Target: Zero False Negatives on Allergen Synonym Detection")
    print("=================================================================")

    for i, case in enumerate(cases):
        text = case["text"]
        expected_allergen = case["expected_allergen"]
        is_unsafe = case["is_unsafe"]

        matches = resolve_allergen(text)
        detected_allergens = [m[0].value for m in matches]

        if is_unsafe:
            if expected_allergen in detected_allergens:
                passed_cases += 1
            else:
                false_negatives += 1
                print(f"[FAIL] Case #{i+1}: '{text}' expected '{expected_allergen}', got {detected_allergens}")
        else:
            if len(detected_allergens) == 0:
                passed_cases += 1
            else:
                false_positives += 1
                print(f"[WARN] Case #{i+1}: '{text}' triggered {detected_allergens}")

    accuracy = (passed_cases / total_cases) * 100.0
    fn_rate = (false_negatives / total_cases) * 100.0

    print("-----------------------------------------------------------------")
    print(f"Total Test Cases:       {total_cases}")
    print(f"Passed:                 {passed_cases}")
    print(f"False Negatives:        {false_negatives} ({fn_rate:.2f}%)")
    print(f"False Positives:        {false_positives}")
    print(f"Overall Accuracy:       {accuracy:.2f}%")
    print("-----------------------------------------------------------------")

    if false_negatives == 0:
        print("[SUCCESS] GATE PASSED: Zero False Negatives on Deterministic Safety Benchmark!")
        return True, accuracy, false_negatives
    else:
        print("[FAILURE] GATE FAILED: False negatives detected in safety engine.")
        return False, accuracy, false_negatives

if __name__ == "__main__":
    success, acc, fn = run_safety_eval()
    if not success:
        sys.exit(1)
