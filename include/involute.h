#ifndef INVOLUTE_H
#define INVOLUTE_H

#include <stdint.h>
#include <stddef.h>
#include <math.h>

#define INVOLUTE_MASK_64 0xFFFFFFFFFFFFFFFFULL
#define GATE_MOD4  (1 << 0)
#define GATE_MOD8  (1 << 1)
#define GATE_MOD16 (1 << 2)
#define GATE_MOD3  (1 << 3)
#define GATE_MOD5  (1 << 4)
#define GATE_MOD7  (1 << 5)
#define GATE_ALL   (GATE_MOD4 | GATE_MOD8 | GATE_MOD16 | GATE_MOD3 | GATE_MOD5 | GATE_MOD7)

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
static inline uint8_t involut_gate_mod4(uint64_t z) { return (z % 4 != 0); }

// Mod-8 Quadratic Gate
static inline uint8_t involut_gate_mod8(uint64_t a, uint64_t b, uint64_t c) {
    return (((a * a) % 8 + (b * b) % 8) % 8 == (c * c) % 8);
}

// Mod-16 Residue Gate
static inline uint8_t involut_gate_mod16(uint64_t a, uint64_t b, uint64_t c) {
    return (((a + b) % 16) != (c % 16));
}

// New Modular Gates: Mod-3, Mod-5, Mod-7
static inline uint8_t involut_gate_mod3(uint64_t a, uint64_t b, uint64_t c) {
    return (((a % 3) + (b % 3)) % 3 == (c % 3));
}
static inline uint8_t involut_gate_mod5(uint64_t a, uint64_t b, uint64_t c) {
    // Quadratic residues mod 5 are {0, 1, 4}
    uint64_t ra = (a * a) % 5;
    uint64_t rb = (b * b) % 5;
    uint64_t rc = (c * c) % 5;
    return ((ra + rb) % 5 == rc);
}
static inline uint8_t involut_gate_mod7(uint64_t a, uint64_t b, uint64_t c) {
    // Cubic residues mod 7 are {0, 1, 6}
    uint64_t ra = (a * a * a) % 7;
    uint64_t rb = (b * b * b) % 7;
    uint64_t rc = (c * c * c) % 7;
    return ((ra + rb) % 7 == rc);
}

// Configurable Gate Evaluator
static inline uint8_t involut_gate_composition_configurable(uint64_t a, uint64_t b, uint64_t c, uint32_t flags) {
    if ((flags & GATE_MOD4)  && !involut_gate_mod4(c)) return 0;
    if ((flags & GATE_MOD8)  && !involut_gate_mod8(a, b, c)) return 0;
    if ((flags & GATE_MOD16) && !involut_gate_mod16(a, b, c)) return 0;
    if ((flags & GATE_MOD3)  && !involut_gate_mod3(a, b, c)) return 0;
    if ((flags & GATE_MOD5)  && !involut_gate_mod5(a, b, c)) return 0;
    if ((flags & GATE_MOD7)  && !involut_gate_mod7(a, b, c)) return 0;
    return 1;
}

#endif // INVOLUTE_H
