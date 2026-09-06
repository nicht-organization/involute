# involute

A hybrid C/Python high-performance data purification filter using bitwise double-negation logic ($\sim\sim x$) and boundary-mask invariants.

## Features

* **Native C Engine:** Direct 64-bit in-register evaluation compiled via GCC (`libinvolute.so`).
* **Zero-Copy FFI:** `ctypes`-backed execution layer between Python schemas and compiled C binaries.
* **Apophatic Data Sieving:** Pydantic `InvoluteGate` integration for automatic payload sanitization and hardware-level boundary verification.
## Runtime and Space Complexity

### C Core Kernel (involute_eval):
- Time Complexity: $O(1)$ constant time. 
  Executes direct 64-bit in-register bitwise operations (~, ^, &) in single CPU clock cycles.
- Space Complexity: $O(1)$ constant space.
  Operates strictly in registers with zero dynamic heap memory allocations ($0$ bytes allocated).
### Python FFI Bridge (run_involute_eval):
 - Time Complexity: $O(1)$ constant time. Incurs minimal sub-microsecond C foreign function call overhead via Python ctypes.
 - Space Complexity: $O(1)$ constant space. Pass-by-value 64-bit integer primitives.
### Pydantic Model Gate (InvoluteGate):
 - Time Complexity: $O(N)$ linear time, where $N$ is the number of keys in the validated dictionary payload.
 - Space Complexity: $O(N)$ linear space to construct the cleaned key-value dictionary structure.

## API Documentation

### C Engine Header (involute.h)

#### involute_eval(raw_word, boundary_mask)
Executes in-register double-negation logic over a raw 64-bit word and evaluates parity against a boundary bitmask.

##### Parameters:

- raw_word (uint64_t): Raw 64-bit state word evaluated for noise or corrupted bit flips.

- boundary_mask (uint64_t): Permitted 64-bit active bitmask boundary.

##### Returns:

 - InvoluteResult (struct): 
   Contains:
   - ground_truth (uint64_t, restored payload or 0x0ULL) and
   - is_valid (uint8_t, 1 if valid, 0 if corrupt).

### Low-Level Python FFI (involute.ffi)

#### run_involute_eval(raw_word, boundary_mask)
Python binding layer executing export_involute_eval in libinvolute.so via ctypes.

##### Parameters:

- raw_word (int): Unsigned 64-bit integer representing the raw payload word.

- boundary_mask (int): Unsigned 64-bit integer defining active bit boundary limits.

#### Returns:

- tuple[int, bool]:
  Pair (ground_truth, is_valid) indicating
  - evaluated output and 
  - valid bit status.

### High-Level Schema Gate (involute.schema)

InvoluteGate(BaseModel)
Pydantic model guard delegating binary purification to the native C kernel.

#### Fields:

- raw_word (int, required): 64-bit payload integer to sanitize.

- boundary_mask (int, optional): Permitted bitmask (defaults to 0xFFFFFFFFFFFFFFFF).

- ground_truth (int, read-only): Sanitized output integer derived from C kernel.

- is_valid (bool, read-only): Validation result flag from C kernel.

## Installation

```bash
git clone [https://github.com/nicht-organization/involute.git](https://github.com/nicht-organization/involute.git)
cd involute
pip install -e .
```

## Quickstart

```python
from involute import InvoluteGate

# Instantiate gate with raw 64-bit state and boundary mask
gate = InvoluteGate(
    raw_word=0xDEADBEEF,
    boundary_mask=0xFFFFFFFFFFFFFFFF
)

# C kernel evaluation results
print(f"Valid State: {gate.is_valid}")        # True
print(f"Ground Truth: {hex(gate.ground_truth)}") # 0xdeadbeef
```

## Development & Testing

Run native C harness and Python integration test suites:

```bash
# Run Python FFI and schema integration tests
pytest -v

# Run direct C harness
gcc -Iinclude tests/test_involute.c -o tests/test_involute
./tests/test_involute
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

## License

[The Unlicense](LICENSE)

