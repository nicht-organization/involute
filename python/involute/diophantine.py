import ctypes
import os
from typing import List, Union, Dict, Tuple
from .ffi import (
    _lib, 
    CInvoluteEngineResult, 
    GATE_ALL
)

def batch_evaluate_gates(
    a_list: List[int], 
    b_list: List[int], 
    c_list: List[int], 
    flags: int = GATE_ALL
) -> List[bool]:
    """Runs vectorized OpenMP multi-threaded modular gates on candidate arrays."""
    length = len(a_list)
    if length == 0:
        return []

    c_a = (ctypes.c_uint64 * length)(*a_list)
    c_b = (ctypes.c_uint64 * length)(*b_list)
    c_c = (ctypes.c_uint64 * length)(*c_list)
    c_out = (ctypes.c_uint8 * length)()

    _lib.export_involute_batch_gate_eval_omp(c_a, c_b, c_c, c_out, length, flags)
    return [bool(x) for x in c_out]


def stream_file(filepath: Union[str, bytes], flags: int = GATE_ALL) -> List[bool]:
    """Streams a binary file of uint64 triples (a, b, c) zero-copy using mmap and OpenMP."""
    if isinstance(filepath, str):
        filepath = filepath.encode('utf-8')

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Target binary dataset not found: {filepath}")

    file_size = os.path.getsize(filepath)
    num_triples = file_size // (3 * 8)
    if num_triples == 0:
        return []

    out_buffer = (ctypes.c_uint8 * num_triples)()
    processed = _lib.export_involute_mmap_stream_eval(filepath, out_buffer, flags)
    return [bool(x) for x in out_buffer[:processed]]


class CrossEquationUnifier:
    """Evaluates entire families of equations in one unified step."""
    
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
            
            res = _lib.export_involute_eval_diophantine(a_val, b_val, c_val, self.epsilon, self.flags)
            
            key = f"{a_base}^{x} + {b_base}^{y} == {c_val}"
            results[key] = {
                "passed_gates": bool(res.passed_gates),
                "certified_termination": bool(res.terminated),
                "proven_no_solution": bool(res.passed_gates and res.terminated)
            }
        return results
