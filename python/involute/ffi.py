# python/involute/ffi.py
import ctypes
import os

class CInvoluteResult(ctypes.Structure):
    _fields_ = [
        ("ground_truth", ctypes.c_uint64),
        ("is_valid", ctypes.c_uint8),
    ]

class CInvoluteEngineResult(ctypes.Structure):
    _fields_ = [
        ("a", ctypes.c_uint64),
        ("b", ctypes.c_uint64),
        ("c", ctypes.c_uint64),
        ("terminated", ctypes.c_uint8),
        ("passed_gates", ctypes.c_uint8),
    ]

_lib_path = os.path.join(os.path.dirname(__file__), "libinvolute.so")
_lib = ctypes.CDLL(_lib_path)

# Gate Configuration Bitflags
GATE_MOD4  = 1 << 0
GATE_MOD8  = 1 << 1
GATE_MOD16 = 1 << 2
GATE_MOD3  = 1 << 3
GATE_MOD5  = 1 << 4
GATE_MOD7  = 1 << 5
GATE_ALL   = GATE_MOD4 | GATE_MOD8 | GATE_MOD16 | GATE_MOD3 | GATE_MOD5 | GATE_MOD7

# Bind function signatures
_lib.export_involute_eval.argtypes = [ctypes.c_uint64, ctypes.c_uint64]
_lib.export_involute_eval.restype = CInvoluteResult

_lib.export_involute_eval_diophantine.argtypes = [
    ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_double, ctypes.c_uint32
]
_lib.export_involute_eval_diophantine.restype = CInvoluteEngineResult

_lib.export_involute_batch_gate_eval_omp.argtypes = [
    ctypes.POINTER(ctypes.c_uint64),
    ctypes.POINTER(ctypes.c_uint64),
    ctypes.POINTER(ctypes.c_uint64),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_size_t,
    ctypes.c_uint32
]
_lib.export_involute_batch_gate_eval_omp.restype = None

_lib.export_involute_mmap_stream_eval.argtypes = [
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32
]
_lib.export_involute_mmap_stream_eval.restype = ctypes.c_size_t

def run_involute_eval(raw_word: int, boundary_mask: int) -> tuple[int, bool]:
    res = _lib.export_involute_eval(raw_word, boundary_mask)
    return res.ground_truth, bool(res.is_valid)
