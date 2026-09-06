#include <assert.h>
#include <stdio.h>
#include <stdint.h>
#include "../include/involute.h"

// Forward declaration of C wrapper exports
InvoluteResult export_involute_eval(uint64_t raw_word, uint64_t boundary_mask);
InvoluteEngineResult export_involute_eval_diophantine(uint64_t a, uint64_t b, uint64_t c, double eps, uint32_t flags);

void test_c_success_path(void) {
    uint64_t raw_word = 0x00000000FFFFFFFFULL;
    uint64_t allow_mask = 0x00000000FFFFFFFFULL; 

    InvoluteResult res = involute_eval(raw_word, allow_mask);
    assert(res.is_valid == 1);
    assert(res.ground_truth == raw_word);
}

void test_c_failure_branch_and_collapse(void) {
    uint64_t raw_word = 0xDEADBEEF12345678ULL;
    uint64_t restrict_mask = 0x00000000FFFFFFFFULL;

    InvoluteResult res = involute_eval(raw_word, restrict_mask);
    assert(res.is_valid == 0);
    assert(res.ground_truth == 0x0ULL);
}

void test_diophantine_wrapper_path(void) {
    InvoluteEngineResult res = export_involute_eval_diophantine(2, 3, 5, 0., GATE_ALL);
    assert(res.a == 2);
    assert(res.b == 3);
}

int main(void) {
    test_c_success_path();
    test_c_failure_branch_and_collapse();
    test_diophantine_wrapper_path();
    printf("All C register-level & wrapper tests passed successfully.\n");
    return 0;
}