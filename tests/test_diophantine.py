import os
import pytest
from involute.diophantine import (
    CrossEquationUnifier, 
    batch_evaluate_gates, 
    stream_file
)
from involute.ffi import GATE_MOD4, GATE_MOD8, GATE_ALL

def test_cross_equation_unification_family():
    unifier = CrossEquationUnifier(epsilon=0.1, flags=GATE_ALL)
    base_pairs = [(2, 3), (4, 5)]
    results = unifier.prove_family(base_pairs, exp_tuple=(3, 3, 3))
    
    assert len(results) == 2
    for eq, status in results.items():
        assert "passed_gates" in status
        assert "certified_termination" in status
        assert "proven_no_solution" in status

def test_simd_batch_evaluate_gates_execution():
    a_vals = [2, 4, 7, 13]
    b_vals = [3, 5, 11, 17]
    c_vals = [35, 189, 1672, 7124]
    
    # Empty input boundary check (hits line 19)
    assert batch_evaluate_gates([], [], []) == []

    # Custom bitwise gate flags execution
    results = batch_evaluate_gates(a_vals, b_vals, c_vals, flags=(GATE_MOD4 | GATE_MOD8))
    assert isinstance(results, list)
    assert len(results) == 4
    assert all(isinstance(r, bool) for r in results)

def test_stream_file_zero_copy_mmap(tmp_path):
    # Setup temporary binary dataset
    bin_file = tmp_path / "triples.bin"
    
    # Write 2 triples of uint64_t values (6 * 8 = 48 bytes)
    raw_bytes = (
        (2).to_bytes(8, 'little') + (3).to_bytes(8, 'little') + (5).to_bytes(8, 'little') +
        (4).to_bytes(8, 'little') + (5).to_bytes(8, 'little') + (9).to_bytes(8, 'little')
    )
    bin_file.write_bytes(raw_bytes)

    # 1. Test streaming valid binary dataset (hits lines 32-45)
    results = stream_file(str(bin_file), flags=GATE_ALL)
    assert len(results) == 2
    assert isinstance(results[0], bool)

    # 2. Empty file boundary check
    empty_file = tmp_path / "empty.bin"
    empty_file.write_bytes(b"")
    assert stream_file(str(empty_file)) == []

    # 3. Missing file exception boundary
    with pytest.raises(FileNotFoundError):
        stream_file(tmp_path / "non_existent.bin")
