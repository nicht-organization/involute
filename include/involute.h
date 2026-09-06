#ifndef INVOLUTE_H
#define INVOLUTE_H

#include <stdint.h>
#include <stddef.h>
#include <math.h>

#define INVOLUTE_MASK_64 0xFFFFFFFFFFFFFFFFULL

typedef struct {
    uint64_t ground_truth;
    uint8_t  is_valid;
} InvoluteResult;

typedef struct {
    uint64_t a;
    uint64_t b;
    uint64_t c;
    uint8_t terminated;
    uint8_t passed_gates;
} InvoluteEngineResult;

/**
 * Executes an in-register involution (double negation) over 64-bit word state.
 */
static inline InvoluteResult involute_eval(uint64_t raw_word, uint64_t boundary_mask) {
    InvoluteResult result;
    
    uint64_t first_neg = (~raw_word) & INVOLUTE_MASK_64;
    uint64_t restored = (~first_neg) & INVOLUTE_MASK_64;
    
    if (restored == raw_word && (raw_word & ~boundary_mask) == 0x0ULL) {
        result.ground_truth = raw_word;
        result.is_valid = 1;
    } else {
        result.ground_truth = 0x0ULL;
        result.is_valid = 0;
    }
    return result;
}

// 1. Certified Termination (abc Bound)
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

static inline uint8_t involut_verify_abc(uint64_t a, uint64_t b, uint64_t c, double eps) {
    uint64_t rad_abc = involut_compute_radical(a) * 
                       involut_compute_radical(b) * 
                       involut_compute_radical(c);
    double bound = pow((double)rad_abc, 1.0 + eps);
    return ((double)c < bound) ? 1 : 0;
}

// Mod-4 Parity Gate
static inline uint8_t involut_gate_mod4(uint64_t z) {
    return (z % 4 != 0);
}

// Mod-8 Quadratic Gate
static inline uint8_t involut_gate_mod8(uint64_t a, uint64_t b, uint64_t c) {
    uint64_t res_a = (a * a) % 8;
    uint64_t res_b = (b * b) % 8;
    uint64_t res_c = (c * c) % 8;
    return ((res_a + res_b) % 8 == res_c);
}

// Mod-16 Residue Gate
static inline uint8_t involut_gate_mod16(uint64_t a, uint64_t b, uint64_t c) {
    uint64_t rem = (a + b) % 16;
    return (rem != (c % 16)); 
}

static inline uint8_t involut_gate_composition(uint64_t z) {
    if (!involut_gate_mod4(z)) return 0;
    return 1;
}

static inline uint8_t involut_gate_composition8(uint64_t a, uint64_t b, uint64_t c) {
    if (!involut_gate_mod4(c)) return 0;
    if (!involut_gate_mod8(a, b, c)) return 0;
    return 1;
}

#endif // INVOLUTE_H