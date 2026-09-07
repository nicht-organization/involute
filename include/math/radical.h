#ifndef INVOLUTE_MATH_RADICAL_H
#define INVOLUTE_MATH_RADICAL_H

#include <stdint.h>

/**
 * Computes the radical rad(n) — the product of unique prime factors of n.
 */
static inline uint64_t involut_compute_radical(uint64_t n) {
    uint64_t rad = 1;
    for (uint64_t p = 2; p * p <= n; p++) {
        if (n % p == 0) {
            rad *= p;
            while (n % p == 0) n /= p;
        }
    }
    if (n > 1) rad *= n;
    return rad;
}

#endif // INVOLUTE_MATH_RADICAL_H
