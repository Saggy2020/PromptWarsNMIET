"""
Adversarial Prompt-Injection Defense Benchmark.
Evaluates the prompt injection defense filter against 25 known jailbreak attacks.
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

from app.security.injection_guard import injection_guard

def run_injection_eval():
    data_path = os.path.join(os.path.dirname(__file__), "golden_data", "injections.json")
    with open(data_path, "r", encoding="utf-8") as f:
        attacks = json.load(f)

    total_attacks = len(attacks)
    blocked_attacks = 0

    print("=================================================================")
    print("[SECURITY EVAL] PANTRYPILOT ADVERSARIAL INJECTION BENCHMARK")
    print("    Target: 100% Prompt Injection Detection & Neutralization")
    print("=================================================================")

    for i, attack in enumerate(attacks):
        is_threat, patterns = injection_guard.check_adversarial_threat(attack)
        if is_threat:
            blocked_attacks += 1
        else:
            print(f"[FAIL] ESCAPED INJECTION on attack #{i+1}: '{attack}'")

    pass_rate = (blocked_attacks / total_attacks) * 100.0

    print("-----------------------------------------------------------------")
    print(f"Total Attacks Tested:   {total_attacks}")
    print(f"Attacks Blocked:        {blocked_attacks}")
    print(f"Defense Pass Rate:      {pass_rate:.1f}%")
    print("-----------------------------------------------------------------")

    if blocked_attacks == total_attacks:
        print("[SUCCESS] GATE PASSED: 100% Adversarial Prompt Injection Defense Rate Achieved!")
        return True, pass_rate
    else:
        print("[FAILURE] GATE FAILED: Injection attacks bypassed the filter.")
        return False, pass_rate

if __name__ == "__main__":
    success, rate = run_injection_eval()
    if not success:
        sys.exit(1)
