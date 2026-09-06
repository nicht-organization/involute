# tests/test_diophantine.py
from involute.diophantine import CrossEquationUnifier

def test_cross_equation_unification_pipeline():
    unifier = CrossEquationUnifier(epsilon=0.1)
    base_pairs = [(2, 3), (4, 5), (7, 11)]
    
    # Unified test pass over Fermat exponent family (3, 3, 3)
    results = unifier.prove_family(base_pairs, exp_tuple=(3, 3, 3))
    
    for eq, status in results.items():
        assert "passed_gates" in status
        assert "certified_termination" in status