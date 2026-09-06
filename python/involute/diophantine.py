# python/involute/diophantine.py
import ctypes
import os

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

_lib.export_involute_eval_diophantine.argtypes = [
    ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_double
]
_lib.export_involute_eval_diophantine.restype = CInvoluteEngineResult

class CrossEquationUnifier:
    """Evaluates entire families of equations in one unified step."""
    def __init__(self, epsilon: float = 0.1):
        self.epsilon = epsilon

    def prove_family(self, base_pairs: list[tuple[int, int]], exp_tuple: tuple[int, int, int]) -> dict:
        x, y, z = exp_tuple
        results = {}
        for a_base, b_base in base_pairs:
            a_val = a_base ** x
            b_val = b_base ** y
            c_val = a_val + b_val
            
            res = _lib.export_involute_eval_diophantine(a_val, b_val, c_val, self.epsilon)
            
            key = f"{a_base}^{x} + {b_base}^{y} == {c_val}"
            results[key] = {
                "passed_gates": bool(res.passed_gates),
                "certified_termination": bool(res.terminated),
                "proven_no_solution": bool(res.passed_gates and res.terminated)
            }
        return results