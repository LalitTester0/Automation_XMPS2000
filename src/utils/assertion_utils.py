import pytest_check as check

# Storage for verification results of the current test
_verification_results = []

def verify_equal(actual, expected, message):
    status = "PASS" if actual == expected else "FAIL"
    result = {
        "status": status,
        "message": message,
        "expected": expected,
        "actual": actual
    }
    _verification_results.append(result)
    
    if actual == expected:
        print(f"[PASS] {message} | Expected={expected} Actual={actual}")
    else:
        print(f"[FAIL] {message} | Expected={expected} Actual={actual}")

    check.equal(actual, expected, message)

def get_verification_results():
    """Returns the list of verification results."""
    return _verification_results

def clear_verification_results():
    """Clears the verification results storage."""
    global _verification_results
    _verification_results = []

def verify_not_equal(actual, expected, message):
    
    status = "PASS" if actual != expected else "FAIL"

    result = {
        "status": status,
        "message": message,
        "expected": f"Not {expected}",
        "actual": actual
    }
    _verification_results.append(result)

    if actual != expected:
        print(f"[PASS] {message} | Expected!= {expected} Actual={actual}")
    else:
        print(f"[FAIL] {message} | Expected!= {expected} Actual={actual}")

    # pytest-check equivalent for not equal
    check.not_equal(actual, expected, message)