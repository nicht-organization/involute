#include <assert.h>
#include <stdio.h>
#include <stdint.h>
#include "../include/involute.h"

void test_c_success_path(void) {
    uint64_t raw_word = 0x00000000FFFFFFFFULL;
    uint64_t allow_mask = 0x00000000FFFFFFFFULL; 

    InvoluteResult res = involute_eval(raw_word, allow_mask);

    assert(res.is_valid == 1);
    assert(res.ground_truth == raw_word);
}

void test_c_failure_branch_and_collapse(void) {
    uint64_t raw_word = 0xDEADBEEF12345678ULL;
    uint64_t restrict_mask = 0x00000000FFFFFFFFULL; // raw_word breaches allowed mask

    InvoluteResult res = involute_eval(raw_word, restrict_mask);

    assert(res.is_valid == 0);
    assert(res.ground_truth == 0x0ULL);
}

int main(void) {
    test_c_success_path();
    test_c_failure_branch_and_collapse();
    printf("All C register-level tests passed successfully.\n");
    return 0;
}