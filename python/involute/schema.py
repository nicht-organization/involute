from typing import Any, Dict
from pydantic import BaseModel, ConfigDict, model_validator


class InvoluteGate(BaseModel):
    """Pydantic model guard stripping unmapped fields and synthetic artifacts."""

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="before")
    @classmethod
    def double_negation_sieve(cls, values: Any) -> Any:
        if not isinstance(values, dict):
            return values

        cleaned: Dict[str, Any] = {}
        for k, v in values.items():
            # Reject artificial attributes and memory artifacts
            if str(k).startswith("_synthetic_") or str(k).startswith("__"):
                continue

            # Double negation filter logic: ~~x == x
            not_v = None if v is None else not v
            not_not_v = None if not_v is None else not not_v

            if not_not_v == (bool(v) if v is not None else None):
                cleaned[k] = v

        return cleaned