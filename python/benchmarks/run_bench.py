# python/benchmarks/run_bench.py
import os
import time
import numpy as np
from involute.diophantine import batch_evaluate_gates, stream_file
from involute.ffi import GATE_ALL

def run_unified_benchmarks(num_triples: int = 10_000_000):
    print(f"=== INVOLUTE UNIFIED ENGINE BENCHMARK ({num_triples:,} Triples) ===")
    
    # 1. In-Memory Python Array -> OpenMP C-Kernel SIMD Batch Benchmark
    print("\n[1/2] Generating In-Memory Triples...")
    a_vals = np.random.randint(1, 10000, size=num_triples, dtype=np.uint64).tolist()
    b_vals = np.random.randint(1, 10000, size=num_triples, dtype=np.uint64).tolist()
    c_vals = np.random.randint(1, 10000, size=num_triples, dtype=np.uint64).tolist()

    print("Running In-Memory SIMD Gate Evaluation (All Modular Gates)...")
    start = time.perf_counter()
    batch_results = batch_evaluate_gates(a_vals, b_vals, c_vals, flags=GATE_ALL)
    elapsed = time.perf_counter() - start
    
    print(f"Passed Gates: {sum(batch_results):,} / {num_triples:,}")
    print(f"Completed in: {elapsed:.4f} seconds")
    print(f"Throughput:   {num_triples / elapsed:,.2f} evals/sec")

    # 2. Binary File Disk Stream -> Zero-Copy MMAP + OpenMP Benchmark
    print("\n[2/2] Generating Binary Dataset File on Disk...")
    bin_filepath = "benchmark_triples.bin"
    raw_data = np.random.randint(1, 10000, size=(num_triples, 3), dtype=np.uint64)
    raw_data.tofile(bin_filepath)
    file_size_mb = os.path.getsize(bin_filepath) / (1024 * 1024)
    print(f"File created: {file_size_mb:.2f} MB on disk.")

    print("Executing Zero-Copy MMAP + OpenMP File Stream...")
    start = time.perf_counter()
    stream_results = stream_file(bin_filepath, flags=GATE_ALL)
    elapsed = time.perf_counter() - start

    print(f"Passed Gates: {sum(stream_results):,} / {len(stream_results):,}")
    print(f"Completed in: {elapsed:.4f} seconds")
    print(f"Throughput:   {len(stream_results) / elapsed:,.2f} evals/sec")

    if os.path.exists(bin_filepath):
        os.remove(bin_filepath)

if __name__ == "__main__":
    run_unified_benchmarks()
