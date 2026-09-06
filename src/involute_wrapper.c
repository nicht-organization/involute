#include "involute.h"

// Exported symbol for ctypes/FFI
InvoluteResult export_involute_eval(uint64_t raw_word, uint64_t boundary_mask) {
    return involute_eval(raw_word, boundary_mask);
}

InvoluteEngineResult export_involute_eval_diophantine(uint64_t a, uint64_t b, uint64_t c, double eps) {
    InvoluteEngineResult res;
    res.a = a;
    res.b = b;
    res.c = c;
    
    // Gate execution short-circuit
    res.passed_gates = involut_gate_composition(c);
    if (!res.passed_gates) {
        res.terminated = 0;
        return res;
    }

    // Certified termination bound check
    res.terminated = involut_verify_abc(a, b, c, eps);
    return res;
}