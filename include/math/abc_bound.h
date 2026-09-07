#ifndef INVOLUTE_MATH_ABC_BOUND_H
#define INVOLUTE_MATH_ABC_BOUND_H

#include <stdint.h>
#include <math.h>
#include "math/radical.h"

static inline uint8_t involut_verify_abc(uint64_t a, uint64_t b, uint64_t c, double eps) {
    uint64_t rad_abc = involut_compute_radical(a) * 
                       involut_compute_radical(b) * 
                       involut_compute_radical(c);
    double bound = pow((double)rad_abc, 1.0 + eps);
    return ((double)c < bound) ? 1 : 0;
}

#endif // INVOLUTE_MATH_ABC_BOUND_H
