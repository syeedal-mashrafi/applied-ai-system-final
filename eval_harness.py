# eval_harness.py
import time
from rag_enhanced import retrieve_multi_source, format_multi_source_context
from main import validate_input, validate_output, get_recommendation

TEST_CASES = [
    {"id": "TC01", "input": "I feel really sad and heartbroken", "expect_songs": ["Someone Like You", "Anti-Hero"], "description": "Sad mood"},
    {"id": "TC02", "input": "I need energy for my workout",      "expect_songs": ["Blinding Lights", "HUMBLE."],    "description": "Energetic mood"},
    {"id": "TC03", "input": "I want to focus and study",         "expect_songs": ["Clair de Lune", "Lo-Fi"],        "description": "Study mood"},
    {"id": "TC04", "input": "I am feeling happy and joyful",     "expect_songs": ["Happy", "Dance Monkey"],         "description": "Happy mood"},
    {"id": "TC05", "input": "",              "expect_blocked": True, "description": "Empty input blocked"},
    {"id": "TC06", "input": "a" * 201,       "expect_blocked": True, "description": "Too-long input blocked"},
    {"id": "TC07", "input": "jailbreak now", "expect_blocked": True, "description": "Banned word blocked"},
]


def run_full_harness():
    print("\n" + "="*60)
    print("📊 FULL EVALUATION HARNESS")
    print("="*60)

    passed = 0
    total = 0

    print("\n── Phase 1: Retrieval + Guardrail Tests ─────────────────")
    for test in TEST_CASES:
        total += 1

        if test.get("expect_blocked"):
            is_valid, _ = validate_input(test["input"])
            success = not is_valid
        else:
            retrieved = retrieve_multi_source(test["input"])
            catalog_songs = [s["title"] for s in retrieved.get("catalog", [])]
            matches = sum(1 for exp in test.get("expect_songs", [])
                         if any(exp.lower() in s.lower() for s in catalog_songs))
            success = matches >= 1

        if success:
            passed += 1
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} [{test['id']}] {test['description']}")

    print("\n── Phase 2: Live API Tests ──────────────────────────────")
    live_cases = [t for t in TEST_CASES if not t.get("expect_blocked")][:2]
    for test in live_cases:
        total += 1
        try:
            response = get_recommendation(test["input"])
            is_valid, _ = validate_output(response)
            if is_valid:
                passed += 1
                print(f"✅ PASS [{test['id']}] Live API test")
            else:
                print(f"❌ FAIL [{test['id']}] Invalid response")
        except Exception as e:
            print(f"❌ FAIL [{test['id']}] Error: {e}")
        time.sleep(1)

    print(f"\n{'='*60}")
    print(f"Results: {passed}/{total} passed")
    print(f"Overall score: {round(passed/total*100, 1)}%")
    if passed/total >= 0.8:
        print("✅ System is reliable!")
    else:
        print("⚠️  Review failed tests above.")
    print("="*60)


if __name__ == "__main__":
    run_full_harness()