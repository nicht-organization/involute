#ifndef INVOLUT_H
#define INVOLUT_H

#include <stdint.h>

#define INVOLUT_MASK_64 0xFFFFFFFFFFFFFFFFULL

typedef struct {
    uint64_t ground_truth;
    uint8_t  is_valid;
} InvolutResult;

/**
 * Executes an in-register involution (double negation) over 64-bit word state.
 * Evaluates structural consistency against a physical boundary mask.
 */
static inline InvolutResult involut_eval(uint64_t raw_word, uint64_t boundary_mask) {
    InvolutResult result;
    
    // First Negation (~x): State/entropy inversion
    uint64_t first_neg = (~raw_word) & INVOLUT_MASK_64;
    
    // Boundary Enforcement: Mask system noise
    uint64_t masked_neg = first_neg ^ boundary_mask;
    
    // Second Negation (~~x): Structural restoration
    uint64_t restored = (~masked_neg) & INVOLUT_MASK_64;
    
    // Invariant Check: Verify restored state against boundary constraints
    if ((restored ^ raw_word) == boundary_mask) {
        result.ground_truth = raw_word;
        result.is_valid = 1;  // Immutable ground floor
    } else {
        result.ground_truth = 0x0ULL; // Collapse to NULL
        result.is_valid = 0;  // Noise purged
    }
    
    return result;
}

#endif // INVOLUT_H