#include <assert.h>
#include <stdio.h>
#include <stdint.h>
#include "involute.h"

int main(void) {
    printf("[C-TEST] Running tests...\n");

    InvoluteEngineResult res = {0};
    export_involute_eval_diophantine(2, 3, 35, 0.1, 0x3F, &res);

    assert(res.a == 2);
    assert(res.b == 3);
    assert(res.c == 35);

    printf("[C-TEST] All tests passed.\n");
    return 0;
}
