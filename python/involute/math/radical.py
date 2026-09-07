import ctypes
from ..core.ffi import _lib

_lib.export_involute_compute_radical.argtypes = [ctypes.c_uint64]
_lib.export_involute_compute_radical.restype = ctypes.c_uint64


def compute_radical(n: int) -> int:
    """Computes the radical rad(n) — the product of unique prime factors of n."""
    if n <= 0:
        raise ValueError("Radical can only be computed for positive integers.")
    return _lib.export_involute_compute_radical(n)
