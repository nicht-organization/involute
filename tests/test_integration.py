import pytest
from involute.core.ffi import run_register_eval, run_involute_eval
from involute.schema import InvoluteGate


def test_ffi_c_kernel_direct_execution():
    """Verify raw FFI call into libinvolute.so for register evaluation."""
    raw_word = 0xAAAAAAAAAAAAAAAA
    boundary_mask = 0xFFFFFFFFFFFFFFFF

    ground_truth, is_valid = run_register_eval(raw_word, boundary_mask)

    assert is_valid == 1
    assert ground_truth == raw_word


def test_schema_delegation_to_c_kernel():
    """Verify high-level Pydantic InvoluteGate model delegates to C engine."""
    gate = InvoluteGate(
        raw_word=0xDEADBEEF,
        boundary_mask=0xFFFFFFFFFFFFFFFF
    )

    assert gate.is_valid is True
    assert gate.ground_truth == 0xDEADBEEF


def test_c_kernel_boundary_breach():
    """Verify corrupted state or boundary breach fails validation in C."""
    raw_word = 0x1
    boundary_mask = 0x0

    ground_truth, is_valid = run_register_eval(raw_word, boundary_mask)

    assert is_valid == 0
    assert ground_truth == 0x0


def test_diophantine_ffi_direct_execution():
    """Verify Diophantine engine evaluation via ctypes FFI."""
    res = run_involute_eval(2, 3, 35)
    assert res.a == 2
    assert res.b == 3
    assert res.c == 35
