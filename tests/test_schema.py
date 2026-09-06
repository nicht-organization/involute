# tests/test_schema.py
import pytest
from pydantic import ValidationError
from involute import InvoluteGate


def test_double_negation_and_stripping():
    payload = {
        "valid_key": "data",
        "_synthetic_flag": True,
        "__internal_mem": 0xDEADBEEF,
        "_valid_private": "kept",
        "null_val": None,
        "truthy_val": 1,
        "falsy_zero": 0,
        "falsy_bool": False,
        "empty_str": "",
    }

    # Calls double_negation_sieve directly
    cleaned = InvoluteGate.double_negation_sieve(payload)

    # Valid items preserved (hits line 30)
    assert cleaned["valid_key"] == "data"
    assert cleaned["_valid_private"] == "kept"
    assert cleaned["null_val"] is None
    assert cleaned["truthy_val"] == 1
    assert cleaned["falsy_zero"] == 0
    assert cleaned["falsy_bool"] is False
    assert cleaned["empty_str"] == ""

    # Synthetic artifacts purged (hits line 20)
    assert "_synthetic_flag" not in cleaned
    assert "__internal_mem" not in cleaned


def test_non_dict_input_pass_through():
    # Hits early return branch for non-dictionary inputs
    assert InvoluteGate.double_negation_sieve("string_payload") == "string_payload"
    assert InvoluteGate.double_negation_sieve([1, 2, 3]) == [1, 2, 3]
    assert InvoluteGate.double_negation_sieve(None) is None


def test_pydantic_extra_forbid():
    class UserGate(InvoluteGate):
        valid_key: str

    user = UserGate(valid_key="ok")
    assert user.valid_key == "ok"

    with pytest.raises(ValidationError):
        UserGate(valid_key="ok", unmapped_field="noise")

def test_schema_synthetic_key_pruning_raises():
    data = {"valid_key": 42, "_synthetic_junk": 999, "__dunder_junk": 123}
    
    # Asserting non-existent filter method raises AttributeError
    with pytest.raises(AttributeError):
        InvoluteGate.filter(data)

    # Asserting direct instantiation with unmapped keys raises ValidationError
    with pytest.raises(ValidationError):
        InvoluteGate(**data)

def test_schema_synthetic_key_pruning_sieve():
    data = {"valid_key": 42, "_synthetic_junk": 999, "__dunder_junk": 123}
    
    # Cleans the dict using the model validator method
    cleaned = InvoluteGate.double_negation_sieve(data)
    
    assert "valid_key" in cleaned
    assert "_synthetic_junk" not in cleaned
    assert "__dunder_junk" not in cleaned
