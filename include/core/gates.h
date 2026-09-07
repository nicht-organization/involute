#ifndef INVOLUTE_CORE_GATES_H
#define INVOLUTE_CORE_GATES_H

#include <stdint.h>

#define GATE_MOD4  (1 << 0)
#define GATE_MOD8  (1 << 1)
#define GATE_MOD16 (1 << 2)
#define GATE_MOD3  (1 << 3)
#define GATE_MOD5  (1 << 4)
#define GATE_MOD7  (1 << 5)
#define GATE_ALL   (GATE_MOD4 | GATE_MOD8 | GATE_MOD16 | GATE_MOD3 | GATE_MOD5 | GATE_MOD7)

static inline uint8_t involut_gate_mod4(uint64_t z) { return (z % 4 != 0); }

static inline uint8_t involut_gate_mod8(uint64_t a, uint64_t b, uint64_t c) {
    return (((a * a) % 8 + (b * b) % 8) % 8 == (c * c) % 8);
}

static inline uint8_t involut_gate_mod16(uint64_t a, uint64_t b, uint64_t c) {
    return (((a + b) % 16) != (c % 16));
}

static inline uint8_t involut_gate_mod3(uint64_t a, uint64_t b, uint64_t c) {
    return (((a % 3) + (b % 3)) % 3 == (c % 3));
}

static inline uint8_t involut_gate_mod5(uint64_t a, uint64_t b, uint64_t c) {
    return (((a * a) % 5 + (b * b) % 5) % 5 == (c * c) % 5);
}

static inline uint8_t involut_gate_mod7(uint64_t a, uint64_t b, uint64_t c) {
    uint64_t ra = (a * a * a) % 7;
    uint64_t rb = (b * b * b) % 7;
    uint64_t rc = (c * c * c) % 7;
    return ((ra + rb) % 7 == rc);
}

static inline uint8_t involut_gate_composition_configurable(uint64_t a, uint64_t b, uint64_t c, uint32_t flags) {
    if ((flags & GATE_MOD4)  && !involut_gate_mod4(c)) return 0;
    if ((flags & GATE_MOD8)  && !involut_gate_mod8(a, b, c)) return 0;
    if ((flags & GATE_MOD16) && !involut_gate_mod16(a, b, c)) return 0;
    if ((flags & GATE_MOD3)  && !involut_gate_mod3(a, b, c)) return 0;
    if ((flags & GATE_MOD5)  && !involut_gate_mod5(a, b, c)) return 0;
    if ((flags & GATE_MOD7)  && !involut_gate_mod7(a, b, c)) return 0;
    return 1;
}
#endif // INVOLUTE_CORE_GATES_H
