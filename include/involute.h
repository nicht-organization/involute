#ifndef INVOLUTE_H
#define INVOLUTE_H

#include <stdint.h>

#define INVOLUTE_MASK_64 0xFFFFFFFFFFFFFFFFULL

typedef struct {
    uint64_t ground_truth;
    uint8_t  is_valid;
} InvoluteResult;

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

#endif // INVOLUTE_H