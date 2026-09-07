import ctypes
from typing import List, Dict, Tuple
from ..core.ffi import _lib, InvoluteDiophantineResult, GATE_ALL


def batch_evaluate_gates(
    a_list: List[int], b_list: List[int], c_list: List[int], flags: int = GATE_ALL
) -> List[bool]:
    """Parallel batch processing of gate conditions using OpenMP in C."""
    length = len(a_list)
    if not (len(b_list) == length and len(c_list) == length):
        raise ValueError("Input arrays a, b, and c must have equal length.")

    c_uint64_array = ctypes.c_uint64 * length
    c_uint8_array = ctypes.c_uint8 * length

    a_arr = c_uint64_array(*a_list)
    b_arr = c_uint64_array(*b_list)
    c_arr = c_uint64_array(*c_list)
    out_arr = c_uint8_array()

    _lib.export_involute_batch_gate_eval_omp(a_arr, b_arr, c_arr, out_arr, length, flags)
    return [bool(x) for x in out_arr]


class CrossEquationUnifier:
    def __init__(self, epsilon: float = 0.1, flags: int = GATE_ALL):
        self.epsilon = epsilon
        self.flags = flags

    def prove_family(
        self, 
        base_pairs: List[Tuple[int, int]], 
        exp_tuple: Tuple[int, int, int]
    ) -> Dict[str, Dict[str, bool]]:
        x, y, z = exp_tuple
        results = {}
        for a_base, b_base in base_pairs:
            a_val = a_base ** x
            b_val = b_base ** y
            c_val = a_val + b_val
            
            res = InvoluteDiophantineResult()
            _lib.export_involute_eval_diophantine(
                a_val, b_val, c_val, self.epsilon, self.flags, ctypes.byref(res)
            )
            
            key = f"{a_base}^{x} + {b_base}^{y} == {c_val}"
            results[key] = {
                "passed_gates": bool(res.passed_gates),
                "certified_termination": bool(res.terminated),
                "proven_no_solution": bool(res.passed_gates and res.terminated)
            }
        return results
    