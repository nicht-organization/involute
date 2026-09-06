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

typedef uint64_t v4ui __attribute__ ((vector_size (32))); // 256-bit SIMD vector (4x uint64_t)

// Batch SIMD evaluation for array of candidates
void export_involute_batch_gate_eval(
    const uint64_t* a_arr, 
    const uint64_t* b_arr, 
    const uint64_t* c_arr, 
    uint8_t* results_out, 
    size_t length
) {
    size_t i = 0;

    // Vectorized 4-lane pipeline execution
    for (; i + 4 <= length; i += 4) {
        v4ui vec_a = *(v4ui*)&a_arr[i];
        v4ui vec_b = *(v4ui*)&b_arr[i];
        v4ui vec_c = *(v4ui*)&c_arr[i];

        // Bitwise Mod-4 check: c % 4 == (c & 3)
        v4ui mod4_mask = vec_c & 3;

        for (int lane = 0; lane < 4; lane++) {
            uint64_t a = ((uint64_t*)&vec_a)[lane];
            uint64_t b = ((uint64_t*)&vec_b)[lane];
            uint64_t c = ((uint64_t*)&vec_c)[lane];
            
            uint8_t m4_passed = (((uint64_t*)&mod4_mask)[lane] != 0);
            uint8_t m8_passed = involut_gate_mod8(a, b, c);

            results_out[i + lane] = m4_passed && m8_passed;
        }
    }

    // Scalar fallback loop for remaining items
    for (; i < length; i++) {
        results_out[i] = involut_gate_composition(a_arr[i], b_arr[i], c_arr[i]);
    }
}