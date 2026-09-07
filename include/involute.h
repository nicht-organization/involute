#ifndef INVOLUTE_H
#define INVOLUTE_H

#include <stdint.h>
#include <stddef.h>

#include "core/register.h"
#include "core/gates.h"
#include "math/radical.h"
#include "math/abc_bound.h"
#include "stream/mmap_engine.h"

typedef struct {
    uint64_t a;
    uint64_t b;
    uint64_t c;
    int terminated;
    int passed_gates;
} InvoluteEngineResult;

void export_involute_eval_diophantine(
    uint64_t a, uint64_t b, uint64_t c, 
    double eps, uint32_t flags, 
    InvoluteEngineResult* out
);

void export_involute_batch_gate_eval_omp(
    const uint64_t* a_arr,
    const uint64_t* b_arr,
    const uint64_t* c_arr,
    uint8_t* results_out,
    size_t length,
    uint32_t flags
);

size_t export_involute_mmap_stream_eval(const char* filepath, uint8_t* out_buffer, uint32_t flags);

#endif // INVOLUTE_H
