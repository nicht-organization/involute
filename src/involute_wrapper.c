#include <stddef.h>
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
    res.passed_gates = involut_gate_composition8(a, b, c);
    if (!res.passed_gates) {
        res.terminated = 0;
        return res;
    }

    // Certified termination bound check
    res.terminated = involut_verify_abc(a, b, c, eps);
    return res;
}

void export_involute_batch_gate_eval(
    const uint64_t* a_arr, 
    const uint64_t* b_arr, 
    const uint64_t* c_arr, 
    uint8_t* results_out, 
    size_t length
) {
    for (size_t i = 0; i < length; i++) {
        results_out[i] = involut_gate_composition8(a_arr[i], b_arr[i], c_arr[i]);
    }
}