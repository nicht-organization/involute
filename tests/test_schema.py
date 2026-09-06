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

    cleaned = InvoluteGate.double_negation_sieve(payload)

    # Valid items preserved
    assert cleaned["valid_key"] == "data"
    assert cleaned["_valid_private"] == "kept"
    assert cleaned["null_val"] is None
    assert cleaned["truthy_val"] == 1
    assert cleaned["falsy_zero"] == 0
    assert cleaned["falsy_bool"] is False
    assert cleaned["empty_str"] == ""

    # Synthetic artifacts purged
    assert "_synthetic_flag" not in cleaned
    assert "__internal_mem" not in cleaned


def test_non_dict_input_pass_through():
    # Covers non-dict early return branch
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

def test_schema_synthetic_key_pruning():
    data = {"valid_key": 42, "_synthetic_junk": 999, "__dunder_junk": 123}
    cleaned = InvoluteGate.filter(data)
    assert "valid_key" in cleaned
    assert "_synthetic_junk" not in cleaned
    assert "__dunder_junk" not in cleaned
