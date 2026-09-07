#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include "stream/mmap_engine.h"
#include "core/gates.h"

size_t export_involute_mmap_stream_eval(const char* filepath, uint8_t* results_out, uint32_t flags) {
    int fd = open(filepath, O_RDONLY);
    if (fd == -1) return 0;

    struct stat sb;
    if (fstat(fd, &sb) == -1) {
        close(fd);
        return 0;
    }

    size_t file_size = sb.st_size;
    size_t num_triples = file_size / (3 * sizeof(uint64_t));

    if (num_triples == 0) {
        close(fd);
        return 0;
    }

    uint64_t* map = (uint64_t*)mmap(NULL, file_size, PROT_READ, MAP_PRIVATE, fd, 0);
    close(fd);

    if (map == MAP_FAILED) return 0;

    #pragma omp parallel for schedule(static)
    for (size_t i = 0; i < num_triples; i++) {
        uint64_t a = map[i * 3 + 0];
        uint64_t b = map[i * 3 + 1];
        uint64_t c = map[i * 3 + 2];
        results_out[i] = involut_gate_composition_configurable(a, b, c, flags);
    }

    munmap(map, file_size);
    return num_triples;
}
