#include "involute.h"

void export_involute_eval_diophantine(
    uint64_t a, uint64_t b, uint64_t c, 
    double eps, uint32_t flags, 
    InvoluteEngineResult* out
) {
    if (!out) return;
    out->a = a;
    out->b = b;
    out->c = c;
    out->passed_gates = involut_gate_composition_configurable(a, b, c, flags);
    out->terminated = out->passed_gates ? involut_verify_abc(a, b, c, eps) : 0;
}

void export_involute_batch_gate_eval_omp(
    const uint64_t* a_arr,
    const uint64_t* b_arr,
    const uint64_t* c_arr,
    uint8_t* results_out,
    size_t length,
    uint32_t flags
) {
    if (!a_arr || !b_arr || !c_arr || !results_out) return;

    #pragma omp parallel for schedule(static)
    for (size_t i = 0; i < length; i++) {
        results_out[i] = involut_gate_composition_configurable(a_arr[i], b_arr[i], c_arr[i], flags);
    }
}
