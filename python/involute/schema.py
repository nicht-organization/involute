from typing import Any, Dict
from pydantic import BaseModel, ConfigDict, model_validator
from .core.ffi import run_register_eval


class InvoluteGate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    raw_word: int = 0
    boundary_mask: int = 0xFFFFFFFFFFFFFFFF
    ground_truth: int = 0
    is_valid: bool = False

    @model_validator(mode="before")
    @classmethod
    def preprocess_payload(cls, data: Any) -> Any:
        if isinstance(data, dict):
            return cls.double_negation_sieve(data)
        return data

    @model_validator(mode="after")
    def validate_via_c_kernel(self) -> "InvoluteGate":
        if self.raw_word != 0 or self.boundary_mask != 0xFFFFFFFFFFFFFFFF:
            truth, valid = run_register_eval(self.raw_word, self.boundary_mask)
            self.ground_truth = truth
            self.is_valid = bool(valid)
            if not valid:
                raise ValueError("State corrupted or breached boundary mask.")
        return self

    @classmethod
    def double_negation_sieve(cls, values: Any) -> Any:
        if not isinstance(values, dict):
            return values

        cleaned: Dict[str, Any] = {}
        for key, val in values.items():
            if key.startswith("_synthetic_") or key.startswith("__"):
                continue
            cleaned[key] = val
        return cleaned
