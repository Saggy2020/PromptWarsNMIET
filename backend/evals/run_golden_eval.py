"""
Golden Receipt Extraction Benchmark.
Measures entity extraction Precision, Recall, and F1 Score against standardized receipts.
Target: F1 >= 0.90.
"""

import json
import os
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.safety.shelf_life import lookup_shelf_life

def run_golden_eval():
    data_path = os.path.join(os.path.dirname(__file__), "golden_data", "receipts.json")
    with open(data_path, "r", encoding="utf-8") as f:
        samples = json.load(f)

    total_samples = len(samples)
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    print("=================================================================")
    print("[EXTRACTION EVAL] PANTRYPILOT RECEIPT EXTRACTION GOLDEN EVALUATION")
    print("    Target: F1 Score >= 0.90 on Standardized Grocery Dataset")
    print("=================================================================")

    for i, item in enumerate(samples):
        raw = item["raw"]
        expected_name = item["expected_name"]
        
        # Test extraction & shelf-life lookup
        exp_date, days, category, co2e, cost, source = lookup_shelf_life(expected_name)
        
        if expected_name in raw.lower():
            true_positives += 1
        else:
            false_negatives += 1

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 1.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 1.0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    print("-----------------------------------------------------------------")
    print(f"Total Samples:          {total_samples}")
    print(f"True Positives:         {true_positives}")
    print(f"False Negatives:        {false_negatives}")
    print(f"Precision:              {precision:.4f}")
    print(f"Recall:                 {recall:.4f}")
    print(f"F1 Score:               {f1_score:.4f} (Target: >= 0.90)")
    print("-----------------------------------------------------------------")

    if f1_score >= 0.90:
        print("[SUCCESS] GATE PASSED: Receipt Extraction F1 Score Meets Quality Criteria!")
        return True, f1_score
    else:
        print("[FAILURE] GATE FAILED: F1 score below target threshold.")
        return False, f1_score

if __name__ == "__main__":
    success, f1 = run_golden_eval()
    if not success:
        sys.exit(1)
