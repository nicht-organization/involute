import os
import time
import ctypes
import numpy as np

_lib_path = os.path.abspath("python/involute/libinvolute.so")
_lib = ctypes.CDLL(_lib_path)

_lib.export_involute_mmap_stream_eval.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint8)]
_lib.export_involute_mmap_stream_eval.restype = ctypes.c_size_t

def run_mmap_benchmark(filename="triples.bin", num_triples=10_000_000):
    print(f"Generating binary dataset on disk ({num_triples:,} triples)...")
    raw_data = np.random.randint(1, 10000, size=(num_triples, 3), dtype=np.uint64)
    raw_data.tofile(filename)
    
    file_size_mb = os.path.getsize(filename) / (1024 * 1024)
    print(f"File created: {file_size_mb:.2f} MB on disk.")

    out_buffer = (ctypes.c_uint8 * num_triples)()
    
    print("\nExecuting Zero-Copy MMAP + OpenMP Parallel Sweep...")
    start = time.perf_counter()
    processed = _lib.export_involute_mmap_stream_eval(filename.encode('utf-8'), out_buffer)
    elapsed = time.perf_counter() - start

    throughput = processed / elapsed
    print(f"Streamed & Evaluated: {processed:,} triples")
    print(f"Time Taken:            {elapsed:.4f} seconds")
    print(f"Stream Throughput:     {throughput:,.2f} evals/sec")

    os.remove(filename)

if __name__ == "__main__":
    run_mmap_benchmark()
