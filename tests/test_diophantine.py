import pytest
from involute.diophantine import CrossEquationUnifier, batch_evaluate_gates

def test_cross_equation_unification_family():
    unifier = CrossEquationUnifier(epsilon=0.1)
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
    
    # Executes batch gate C extension loop
    results = batch_evaluate_gates(a_vals, b_vals, c_vals)
    assert isinstance(results, list)
    assert len(results) == 4
    assert all(isinstance(r, bool) for r in results)

def test_diophantine_edge_cases():
    # Force single-item fallback boundary
    results = batch_evaluate_gates([2], [3], [35])
    assert len(results) == 1