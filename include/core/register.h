#ifndef INVOLUTE_CORE_REGISTER_H
#define INVOLUTE_CORE_REGISTER_H

#include <stdint.h>

#define INVOLUTE_MASK_64 0xFFFFFFFFFFFFFFFFULL

typedef struct {
    uint64_t ground_truth;
    uint8_t  is_valid;
} InvoluteResult;

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

#endif // INVOLUTE_CORE_REGISTER_H
