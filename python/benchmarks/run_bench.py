import time
import random
from involute.diophantine import batch_evaluate_gates

def benchmark_simd_gates(iterations: int = 10_000_000):
    print(f"Generating {iterations:,} test triples...")
    a_list = [random.randint(1, 10_000) for _ in range(iterations)]
    b_list = [random.randint(1, 10_000) for _ in range(iterations)]
    c_list = [random.randint(1, 10_000) for _ in range(iterations)]

    print("Running SIMD C-Kernel Gate Evaluation...")
    start_time = time.perf_counter()
    results = batch_evaluate_gates(a_list, b_list, c_list)
    elapsed = time.perf_counter() - start_time

    throughput = iterations / elapsed
    print(f"Completed in: {elapsed:.4f} seconds")
    print(f"Throughput:   {throughput:,.2f} evaluations/sec")
    print(f"Passed Gates: {sum(results):,} / {iterations:,}")

if __name__ == "__main__":
    benchmark_simd_gates()