#ifndef INVOLUTE_STREAM_MMAP_ENGINE_H
#define INVOLUTE_STREAM_MMAP_ENGINE_H

#include <stdint.h>
#include <stddef.h>

size_t export_involute_mmap_stream_eval(const char* filepath, uint8_t* results_out, uint32_t flags);

#endif // INVOLUTE_STREAM_MMAP_ENGINE_H
