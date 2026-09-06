#include "involute.h"

// Exported symbol for ctypes/FFI
InvoluteResult export_involute_eval(uint64_t raw_word, uint64_t boundary_mask) {
    return involute_eval(raw_word, boundary_mask);
}