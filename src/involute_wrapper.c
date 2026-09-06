#include <stddef.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <omp.h>
#include "involute.h"

InvoluteResult export_involute_eval(uint64_t raw_word, uint64_t boundary_mask) {
    return involute_eval(raw_word, boundary_mask);
}

InvoluteEngineResult export_involute_eval_diophantine(uint64_t a, uint64_t b, uint64_t c, double eps, uint32_t flags) {
    InvoluteEngineResult res = {a, b, c, 0, 0};
    res.passed_gates = involut_gate_composition_configurable(a, b, c, flags);
    if (!res.passed_gates) return res;

    res.terminated = involut_verify_abc(a, b, c, eps);
    return res;
}

void export_involute_batch_gate_eval_omp(
    const uint64_t* a_arr, 
    const uint64_t* b_arr, 
    const uint64_t* c_arr, 
    uint8_t* results_out, 
    size_t length,
    uint32_t flags
) {
    #pragma omp parallel for schedule(static)
    for (size_t i = 0; i < length; i++) {
        results_out[i] = involut_gate_composition_configurable(a_arr[i], b_arr[i], c_arr[i], flags);
    }
}

size_t export_involute_mmap_stream_eval(const char* filepath, uint8_t* results_out, uint32_t flags) {
    int fd = open(filepath, O_RDONLY);
    if (fd == -1) return 0;

    struct stat sb;
    if (fstat(fd, &sb) == -1) { close(fd); return 0; }

    size_t total_bytes = sb.st_size;
    size_t num_triples = total_bytes / (3 * sizeof(uint64_t));

    uint64_t* mapped_data = (uint64_t*)mmap(NULL, total_bytes, PROT_READ, MAP_SHARED, fd, 0);
    if (mapped_data == MAP_FAILED) { close(fd); return 0; }

    #pragma omp parallel for schedule(static)
    for (size_t i = 0; i < num_triples; i++) {
        uint64_t a = mapped_data[i * 3 + 0];
        uint64_t b = mapped_data[i * 3 + 1];
        uint64_t c = mapped_data[i * 3 + 2];
        results_out[i] = involut_gate_composition_configurable(a, b, c, flags);
    }

    munmap(mapped_data, total_bytes);
    close(fd);
    return num_triples;
}
