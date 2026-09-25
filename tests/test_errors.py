import pytest 
from toolkit import validator
from toolkit.validator import ExpressionError


#is allowed
def test_is_allowed_digit():
    assert validator.is_allowed("5") is True
def test_is_allowed_operator():
    assert validator.is_allowed("+") is True
def test_is_allowed_invalid_symbol():
    assert validator.is_allowed("$") is False
def test_valid_expression_no_error():
    assert validator.is_allowed("2 + 5") is True
def test_validate_string_empty():
    result = validator.validate_string("")
    assert result is not None

#invalid character 
def test_invalid_character():
    assert validator.invalid_character("2 + 5") is None
def test_invalid_character():
    result = validator.invalid_character("2 + 5 @ 3") 
    assert result is not None
    assert "@" in result

#validate number
def test_validate_number_valid():
    assert validator.validate_number("1.5") == 1.5

#find unit group
def test_find_unit_group():
    assert validator.find_unit_group("km") == ("length", "km")
def test_find_unit_group_unknown_raises():
    with pytest.raises(ExpressionError):
        validator.find_unit_group("ab")


#validate units 
def test_validate_units_same_group():
    result = validator.validate_units("km", "m")
    assert result == ("length", "km", "m")
def test_validate_units_incompatible_raises():
    with pytest.raises(ExpressionError):
        validator.validate_units("g", "f")
