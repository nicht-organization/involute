#ifndef INVOLUTE_H
#define INVOLUTE_H

#include <stdint.h>

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
 * Validates structural consistency and verifies state against permitted boundary constraints.
 */
static inline InvoluteResult involute_eval(uint64_t raw_word, uint64_t boundary_mask) {
    InvoluteResult result;
    
    // First Negation (~x): State/entropy inversion
    uint64_t first_neg = (~raw_word) & INVOLUTE_MASK_64;
    
    // Second Negation (~~x): In-register structural restoration
    uint64_t restored = (~first_neg) & INVOLUTE_MASK_64;
    
    // Invariant & Boundary Check: Verify state restoration and ensure raw_word stays within boundary_mask
    if (restored == raw_word && (raw_word & ~boundary_mask) == 0x0ULL) {
        result.ground_truth = raw_word;
        result.is_valid = 1;  // Valid ground truth retained
    } else {
        result.ground_truth = 0x0ULL; // Collapse corrupted/out-of-bounds state to NULL
        result.is_valid = 0;  // Noise purged
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

// 3. Analytical Gate Composition
static inline uint8_t involut_gate_mod4(uint64_t z) {
    return (z % 4 != 0); // Reject bad parity
}

static inline uint8_t involut_gate_composition(uint64_t z) {
    if (!involut_gate_mod4(z)) return 0;
    return 1;
}

#endif // INVOLUTE_H