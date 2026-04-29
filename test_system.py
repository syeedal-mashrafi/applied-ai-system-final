# test_system.py
from retriever import retrieve_songs
from main import validate_input, validate_output, get_recommendation

def run_tests():
    print("🧪 Running System Tests...\n")
    passed = 0
    total = 0

    test_cases = [
        ("sad",       True,  "Should find songs for sad mood"),
        ("happy",     True,  "Should find songs for happy mood"),
        ("study",     True,  "Should find songs for study mood"),
        ("calm",      True,  "Should find songs for calm mood"),
        ("energetic", True,  "Should find songs for energetic mood"),
        ("xyzabc123", False, "Unknown mood should return no results"),
    ]

    print("── Retrieval Tests ──────────────────────")
    for mood, expect_results, description in test_cases:
        total += 1
        results = retrieve_songs(mood)
        got_results = len(results) > 0
        status = "✅ PASS" if got_results == expect_results else "❌ FAIL"
        if got_results == expect_results:
            passed += 1
        print(f"{status} | {description}")

    print("\n── Input Validation Tests ───────────────")
    validation_cases = [
        ("",              False, "Empty input should fail"),
        ("a" * 201,       False, "Too-long input should fail"),
        ("jailbreak now", False, "Banned word should fail"),
        ("I feel happy",  True,  "Normal input should pass"),
    ]

    for inp, expect_valid, desc in validation_cases:
        total += 1
        is_valid, _ = validate_input(inp)
        status = "✅ PASS" if is_valid == expect_valid else "❌ FAIL"
        if is_valid == expect_valid:
            passed += 1
        print(f"{status} | {desc}")

    print("\n── Live API Test ────────────────────────")
    total += 1
    try:
        response = get_recommendation("relaxing and calm")
        is_valid, _ = validate_output(response)
        if is_valid:
            passed += 1
            print("✅ PASS | Live API returned a valid recommendation")
        else:
            print("❌ FAIL | API response was invalid")
    except Exception as e:
        print(f"❌ FAIL | API call failed: {e}")

    print(f"\n{'='*45}")
    print(f"Results: {passed}/{total} tests passed")
    print(f"Score: {round(passed/total*100, 1)}%")

if __name__ == "__main__":
    run_tests()