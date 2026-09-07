import pytest
from involute.math.radical import compute_radical


def test_compute_radical_valid():
    # rad(12) = 2 * 3 = 6
    assert compute_radical(12) == 6
    # rad(7) = 7
    assert compute_radical(7) == 7


def test_compute_radical_invalid_value():
    with pytest.raises(ValueError, match="positive integers"):
        compute_radical(0)

    with pytest.raises(ValueError, match="positive integers"):
        compute_radical(-5)
