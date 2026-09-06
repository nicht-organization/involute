#include <stddef.h>
#include "involute.h"
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

// Exported symbol for ctypes/FFI
InvoluteResult export_involute_eval(uint64_t raw_word, uint64_t boundary_mask) {
    return involute_eval(raw_word, boundary_mask);
}

InvoluteEngineResult export_involute_eval_diophantine(uint64_t a, uint64_t b, uint64_t c, double eps) {
    InvoluteEngineResult res;
    res.a = a;
    res.b = b;
    res.c = c;
    
    // Gate execution short-circuit
    res.passed_gates = involut_gate_composition8(a, b, c);
    if (!res.passed_gates) {
        res.terminated = 0;
        return res;
    }

    // Certified termination bound check
    res.terminated = involut_verify_abc(a, b, c, eps);
    return res;
}

void export_involute_batch_gate_eval(
    const uint64_t* a_arr, 
    const uint64_t* b_arr, 
    const uint64_t* c_arr, 
    uint8_t* results_out, 
    size_t length
) {
    for (size_t i = 0; i < length; i++) {
        results_out[i] = involut_gate_composition8(a_arr[i], b_arr[i], c_arr[i]);
    }
}

void export_involute_batch_gate_eval_omp(
    const uint64_t* a_arr, 
    const uint64_t* b_arr, 
    const uint64_t* c_arr, 
    uint8_t* results_out, 
    size_t length
) {
    #pragma omp parallel for schedule(static)
    for (size_t i = 0; i < length; i++) {
        results_out[i] = involut_gate_composition8(a_arr[i], b_arr[i], c_arr[i]);
    }
}

size_t export_involute_mmap_stream_eval(const char* filepath, uint8_t* results_out) {
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
        results_out[i] = involut_gate_composition8(a, b, c);
    }

    munmap(mapped_data, total_bytes);
    close(fd);
    return num_triples;
}