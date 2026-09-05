#include <assert.h>
#include <stdio.h>
#include <stdint.h>
#include "../include/involut.h"

void test_c_double_negation(void) {
    uint64_t raw_word = 0xAAAAAAAAAAAAAAAA;
    uint64_t purified = involut_purify_word(raw_word);

    /* Verify bitwise double negation invariant: ~~x == x */
    assert(purified == raw_word);

    /* Verify zero payload pass-through */
    uint64_t noisy_word = 0x0;
    assert(involut_purify_word(noisy_word) == 0x0);
}

int main(void) {
    test_c_double_negation();
    printf("C register-level tests passed successfully.\n");
    return 0;
}