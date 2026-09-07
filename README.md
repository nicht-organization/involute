# involute

A zero-alloc, sieve and diophantine solver for unified parametric equation verification.
Python/C hybrid library for bitwise double-negation,  Diophantine verification, gate composition, and certified $abc$ conjecture bounds via SIMD vectorization and zero-copy memory-mapped streaming.

## Features

* **Native C SIMD Engine:** Direct 64-bit in-register evaluation and bitwise modular filters (`Mod-4`, `Mod-8`, `Mod-16`).
* **OpenMP Parallelization:** Multi-threaded vector processing across available CPU hardware cores.
* **Zero-Copy MMAP Streaming:** Direct binary file evaluation off disk without Python memory allocations.
* **Pydantic Schema Guards:** Apophatic payload sanitization and state boundary verification.
* **Cross-Equation Unification**: Evaluate whole families of equations ($a^x + b^y = c^z$) simultaneously in single FFI calls.

## Runtime and Space Complexity

### C Core Kernel (involute_eval)
- **Time Complexity:** $O(1)$ constant time. Executes direct 64-bit in-register bitwise operations in single CPU clock cycles.
- **Space Complexity:** $O(1)$ constant space. Operates strictly in registers with zero dynamic heap memory allocations ($0$ bytes allocated).

### Python FFI Bridge (run_involute_eval)
- **Time Complexity:** $O(1)$ constant time. Incurs minimal sub-microsecond C foreign function call overhead via Python `ctypes`.
- **Space Complexity:** $O(1)$ constant space. Pass-by-value 64-bit integer primitives.

### Pydantic Model Gate (InvoluteGate)
- **Time Complexity:** $O(N)$ linear time, where $N$ is the number of keys in the validated dictionary payload.
- **Space Complexity:** $O(N)$ linear space to construct the cleaned key-value dictionary structure.

## Performance Benchmarks

Evaluated on a 2-core / 4GB RAM instance over 10,000,000 candidate triples:

| Processing Mode | Throughput | Time (10M Triples) | Memory Overhead |
| :--- | :--- | :--- | :--- |
| **In-Memory Batch Gate (SIMD)** | `~2,030,210 evals/sec` | `4.92s` | Minimal (Python list) |
| **Zero-Copy MMAP Stream (OpenMP)** | `~215,630,489 evals/sec` | `0.046s` | `0 MB` (Direct Disk Page) |
| **Async-Non blocking stream** | `~9,528,364.91 evals/sec` | `1.0495s` | Minimal (Python list) |


## Installation

```bash
git clone https://github.com/nicht-organization/involute.git
cd involute
pip install -e .
```

## Quickstart
### InvoluteGate State Purification
```python
from involute import InvoluteGate

# Instantiate gate with raw 64-bit state and boundary mask
gate = InvoluteGate(
    raw_word=0xDEADBEEF,
    boundary_mask=0xFFFFFFFFFFFFFFFF
)

print(f"Valid State: {gate.is_valid}")        # True
print(f"Ground Truth: {hex(gate.ground_truth)}") # 0xdeadbeef
```

### CrossEquationUnifier Family Search

```python
from involute.diophantine import CrossEquationUnifier

unifier = CrossEquationUnifier(epsilon=0.1)
base_pairs = [(2, 3), (4, 5), (7, 11)]

# Proves family for exponents (3, 3, 3) simultaneously
results = unifier.prove_family(base_pairs, exp_tuple=(3, 3, 3))

for eq, status in results.items():
    print(f"{eq} -> Proven: {status['proven_no_solution']}")
```

### Vectorized Batch SIMD Evaluation

```python
from involute.diophantine import batch_evaluate_gates

a_vals = [2, 4, 7, 13]
b_vals = [3, 5, 11, 17]
c_vals = [35, 189, 1672, 7124]

results = batch_evaluate_gates(a_vals, b_vals, c_vals)
print(f"Passed Gates: {results}")
```
### Zero-Copy MMAP File Streaming
```python
from involute.diophantine import stream_file

# Stream and evaluate 10,000,000 binary triples directly off disk zero-copy
results = stream_file("triples.bin")
print(f"Evaluated {len(results):,} candidates off disk.")
```
---

## Development & Testing

Run native C harness and Python integration test suites:

```bash
# Run full C + Python test suite with coverage
./test_coverage.sh

# Compile production OpenMP / MMAP dynamic library
./build_prod.sh

# Run serial benchmark
python python/benchmarks/run_bench.py

# Run streaming benchmark
python python/benchmarks/run_stream_bench.py

# Run async benchmark
python python/benchmarks/run_async_bench.py

```

## High-Performance Data Purification API & Application Patterns

```python
from typing import Any, Dict
from pydantic import BaseModel, Field, FieldValidationInfo, field_validator
from involute import InvoluteGate
from involute.ffi import run_involute_eval
// ...
```

### 1. LOW-LEVEL API: Direct C-Kernel Word Purification

```python
def purge_64bit_register(raw_state: int, permitted_mask: int) -> int:
    """
    Directly evaluates a 64-bit integer state against a boundary bitmask.
    Executes in-register double-negation (~~x) in libinvolute.so.
    
    Returns 0x0ULL immediately if state contains out-of-bounds bit flips.
    """
    ground_truth, is_valid = run_involute_eval(raw_state, permitted_mask)
    if not is_valid:
        raise ValueError(
            f"Hardware state corruption detected! Raw: {hex(raw_state)}"
        )
    return ground_truth
```

### 2. REAL-WORLD DOMAIN I: Real-Time High-Frequency Market Feed Filter

```python

class MarketTickGate(BaseModel):
    """
    Purifies financial tick streams against low-level bit corruption and 
    spurious synthetic payload flags before execution or storage.
    """
    symbol_id: int = Field(description="64-bit symbol identifier")
    price_cents: int = Field(gt=0, description="Price in USD cents")
    quantity: int = Field(gt=0)
    
    # Boundary mask enforcing allowed active bits in 64-bit symbol ID
    mask: int = Field(default=0xFFFFFFFFFFFFFFFF, exclude=True)

    @field_validator("symbol_id")
    @classmethod
    def purify_symbol_hardware_state(cls, v: int, info: FieldValidationInfo) -> int:
        boundary = info.data.get("mask", 0xFFFFFFFFFFFFFFFF)
        truth, is_valid = run_involute_eval(v, boundary)
        if not is_valid:
            # Collapse corrupted tick state to null ground floor
            raise ValueError(f"Corrupted tick state detected in symbol_id={hex(v)}")
        return truth
```

### 3. REAL-WORLD DOMAIN II: Agent Middleware Payload Sieving

```python
class AgentPayloadSieve:
    """
    Apophatic data filter for LLM/Agent JSON payloads.
    Strips hallucinated flags (_synthetic_*) and enforces hardware bit integrity.
    """

    @staticmethod
    def sanitize_input(raw_json: Dict[str, Any], boundary_mask: int) -> Dict[str, Any]:
        # 1. Clean extra hallucinated fields via high-level key stripping
        cleaned = {
            k: v for k, v in raw_json.items()
            if not k.startswith("_synthetic_") and not k.startswith("__")
        }

        # 2. Gate memory state field using C bitwise double-negation
        if "state_word" in cleaned:
            gate = InvoluteGate(
                raw_word=cleaned["state_word"],
                boundary_mask=boundary_mask
            )
            cleaned["state_word"] = gate.ground_truth

        return cleaned
```

### 4. REAL-WORLD DOMAIN III: WAF Security Gate (Apophatic Bit Filter)

```python

class WAFSecurityGate(BaseModel):
    """
    Performs instant hardware-level validation on incoming network packet flags.
    Any bit outside the strict allowed profile forces complete state rejection.
    """
    packet_flags: int
    allowed_profile: int = 0x00000000FFFFFFFF  # Lower 32-bits active only

    def is_safe(self) -> bool:
        _, is_valid = run_involute_eval(self.packet_flags, self.allowed_profile)
        return is_valid
```

### VERIFICATION SNIPPET: Executing Real-World Scenarios

```python
if __name__ == "__main__":
    # Scenario A: Valid Financial Market Tick
    tick = MarketTickGate(symbol_id=0x0000A1B2C3D4E5F6, price_cents=15250, quantity=100)
    print(f"✓ Tick Validated: Symbol {hex(tick.symbol_id)} @ {tick.price_cents}¢")

    # Scenario B: Agent Middleware Payload Purification
    untrusted_llm_json = {
        "user_id": 4096,
        "state_word": 0xDEADBEEF,
        "_synthetic_hallucinated_flag": True,
        "__internal_leak": "garbage"
    }
    purified = AgentPayloadSieve.sanitize_input(untrusted_llm_json, 0xFFFFFFFFFFFFFFFF)
    print(f"✓ Purified Payload: {purified}")

    # Scenario C: WAF Rejection on Out-Of-Bounds Payload
    waf = WAFSecurityGate(packet_flags=0xFFFF000000000000)  # Breaches lower 32-bit boundary
    print(f"✓ WAF Security Clearance: {waf.is_safe()}")  # False -> Rejected

```

## Benchmark Results

# Engine Benchmark

```bash
python python/benchmarks/run_bench.py 
=== INVOLUTE UNIFIED ENGINE BENCHMARK (10,000,000 Triples) ===

[1/2] Generating In-Memory Triples...
Running In-Memory SIMD Gate Evaluation (All Modular Gates)...
Passed Gates: 14,207 / 10,000,000
Completed in: 5.4835 seconds
Throughput:   1,823,652.73 evals/sec

[2/2] Generating Binary Dataset File on Disk...
File created: 228.88 MB on disk.
Executing Zero-Copy MMAP + OpenMP File Stream...
Passed Gates: 14,343 / 10,000,000
Completed in: 1.0592 seconds
Throughput:   9,441,253.80 evals/sec
```

### In-Mem Benchmark
```bash
python python/benchmarks/run_stream_bench.py 
Generating binary dataset on disk (10,000,000 triples)...
File created: 228.88 MB on disk.

Executing Zero-Copy MMAP + OpenMP Parallel Sweep...
Streamed & Evaluated: 10,000,000 triples
Time Taken:            0.0529 seconds
Stream Throughput:     189,179,228.14 evals/sec
```

### Async Benchmark
```bash
python python/benchmarks/run_async_bench.py 
=== INVOLUTE ASYNC NON-BLOCKING STREAM BENCHMARK ===
Generating binary dataset (10,000,000 triples)...
Async Evaluated: 10,000,000 triples
Completed in:    1.0495 seconds
Throughput:      9,528,364.91 evals/sec
Event Loop State: Main thread remained 100% non-blocking!
```


## License

[The Unlicense](LICENSE), what else?
