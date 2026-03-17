import pytest
from src.utils.assertion_utils import verify_equal

def test_dummy_verification_1():
    """Dummy test for Excel report verification."""
    verify_equal(1, 1, "Verify 1 equals 1")
    verify_equal(2, 2, "Verify 2 equals 2")

def test_dummy_verification_2():
    """Another dummy test for Excel report verification."""
    verify_equal("apple", "apple", "Verify apple is apple")
    verify_equal("orange", "banana", "Verify orange is banana (Expected Fail)")
