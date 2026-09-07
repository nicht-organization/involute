#include "math/radical.h"

// Exported wrapper for direct FFI single-value radical computation
uint64_t export_involute_compute_radical(uint64_t n) {
    return involut_compute_radical(n);
}
