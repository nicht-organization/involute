import pytest
from involute.core.ffi import GATE_ALL, GATE_MOD4, GATE_MOD8
from involute.math.diophantine import CrossEquationUnifier, batch_evaluate_gates
from involute.stream.mmap import stream_file


def test_cross_equation_unification_family():
    unifier = CrossEquationUnifier(epsilon=0.1, flags=GATE_ALL)
    results = unifier.prove_family([(2, 3)], (2, 2, 2))
    assert isinstance(results, dict)


def test_simd_batch_evaluate_gates_execution():
    a_vals = [2, 4, 7, 13]
    b_vals = [3, 5, 11, 17]
    c_vals = [35, 189, 1672, 7124]

    assert batch_evaluate_gates([], [], []) == []

    results = batch_evaluate_gates(a_vals, b_vals, c_vals, flags=(GATE_MOD4 | GATE_MOD8))
    assert isinstance(results, list)
    assert len(results) == 4
    assert all(isinstance(r, bool) for r in results)

def test_stream_file_zero_copy_mmap(tmp_path):
    bin_file = tmp_path / "triples.bin"

    raw_bytes = (
        (2).to_bytes(8, 'little') + (3).to_bytes(8, 'little') + (5).to_bytes(8, 'little') +
        (4).to_bytes(8, 'little') + (5).to_bytes(8, 'little') + (9).to_bytes(8, 'little')
    )
    bin_file.write_bytes(raw_bytes)

    results = stream_file(str(bin_file), flags=GATE_ALL)
    assert len(results) == 2
    assert isinstance(results[0], bool)

def test_batch_evaluate_gates_mismatched_lengths():
    with pytest.raises(ValueError, match="equal length"):
        batch_evaluate_gates([2, 3], [4], [5, 6])
