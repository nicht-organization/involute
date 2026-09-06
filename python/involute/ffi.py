import ctypes
import os

# Define C struct matching InvoluteResult
class CInvoluteResult(ctypes.Structure):
    _fields_ = [
        ("ground_truth", ctypes.c_uint64),
        ("is_valid", ctypes.c_uint8),
    ]

# Load shared library
_lib_path = os.path.join(os.path.dirname(__file__), "libinvolute.so")
_lib = ctypes.CDLL(_lib_path)

# Bind to exported wrapper symbol
_lib.export_involute_eval.argtypes = [ctypes.c_uint64, ctypes.c_uint64]
_lib.export_involute_eval.restype = CInvoluteResult


def run_involute_eval(raw_word: int, boundary_mask: int) -> tuple[int, bool]:
    res = _lib.export_involute_eval(raw_word, boundary_mask)
    return res.ground_truth, bool(res.is_valid)