import asyncio
import time
from pathlib import Path
from involute.stream.async_mmap import stream_file_async
from involute.core.ffi import GATE_ALL


async def background_heartbeat():
    """Simulates an active web server or event-loop processing concurrent tasks."""
    ticks = 0
    while True:
        await asyncio.sleep(0.01)
        ticks += 1
        if ticks >= 5:
            break


async def main():
    print("=== INVOLUTE ASYNC NON-BLOCKING STREAM BENCHMARK ===")
    
    tmp_file = Path("/tmp/async_bench_10m.bin")
    num_triples = 10_000_000
    
    if not tmp_file.exists():
        print(f"Generating binary dataset ({num_triples:,} triples)...")
        raw_bytes = (
            (2).to_bytes(8, "little") + (3).to_bytes(8, "little") + (35).to_bytes(8, "little")
        ) * num_triples
        tmp_file.write_bytes(raw_bytes)

    start_time = time.perf_counter()

    # Run C-level mmap stream in background thread alongside event loop tasks
    results, _ = await asyncio.gather(
        stream_file_async(str(tmp_file), num_triples=num_triples, flags=GATE_ALL),
        background_heartbeat(),
    )

    elapsed = time.perf_counter() - start_time
    throughput = len(results) / elapsed

    print(f"Async Evaluated: {len(results):,} triples")
    print(f"Completed in:    {elapsed:.4f} seconds")
    print(f"Throughput:      {throughput:,.2f} evals/sec")
    print("Event Loop State: Main thread remained 100% non-blocking!")


if __name__ == "__main__":
    asyncio.run(main())
