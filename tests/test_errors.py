import pytest

from toolkit import calculator, converter, validator
from toolkit.errors import ExpressionError, EmptyExpressionError, IncompatibleUnitsError, InvalidNumberError, InvalidCharacterError, UnknownUnitError, UnderZeroError, DividedNumberError


#is allowed
def test_is_allowed_digit():
    """Проверяет, что цифра распознается как допустимый символ."""
    assert validator.is_allowed("5") is True
def test_is_allowed_operator():
    """Проверяет, что оператор сложения распознается как допустимый символ."""
    assert validator.is_allowed("+") is True
def test_is_allowed_invalid_symbol():
    """Проверяет, что недопустимый символ ('$') возвращает False."""
    assert validator.is_allowed("$") is False
#invalid character 
def test_invalid_character():
    """Проверяет, что валидная строка корректно проходит проверку на отсутствие недопустимых символов."""
    assert validator.invalid_character("2 + 5") is None

#validate number
def test_validate_number_valid():
    """Проверяет успешное преобразование валидной числовой строки в число с плавающей точкой."""
    assert validator.validate_number("1.5") == 1.5

#find unit group
def test_find_unit_group():
    """Проверяет корректность определения группы для известной единицы измерения."""
    assert validator.find_unit_group("km") == ("length", "km")
def test_find_unit_group_unknown_raises():
    """Проверяет выброс ExpressionError при попытке найти группу для неизвестной единицы измерения."""
    with pytest.raises(UnknownUnitError):
        validator.find_unit_group("ab")


#validate units 
def test_validate_units_same_group():
    """Проверяет валидацию пары единиц измерения из одной и той же группы."""
    result = validator.validate_units("km", "m")
    assert result == ("length", "km", "m")
def test_validate_units_incompatible_raises():
    """Проверяет выброс ExpressionError при валидации единиц измерения из несовместимых групп."""
    with pytest.raises(IncompatibleUnitsError):
        validator.validate_units("g", "f")



#Позитивные тесты калькулятора
def test_calculator_precedence():
    """Проверяет правильность учета приоритета математических операций."""
    assert calculator.calculate("5+7*3") == 26
def test_calc_division_float():
    """Проверяет выполнение операции деления с получением результата с плавающей точкой."""
    assert calculator.calculate("15/4") == 3.75
def test_calc_negative():
    """Проверяет корректность вычислений с отрицательным числом."""
    assert calculator.calculate("4*-5") == -20
def test_calc_double_negative():
    """Проверяет правильность умножения двух отрицательных чисел."""
    assert calculator.calculate("-3*-4") == 12
def test_calc_unary_minus():
    """Проверяет обработку унарного минуса в выражении."""
    assert calculator.calculate("8+-2") == 6


#Негативные тесты калькулятора
def test_empty_expression():
    """Проверяет выброс ExpressionError при передаче пустой строки с выражением."""
    with pytest.raises(EmptyExpressionError):
        calculator.calculate("")
def test_division_by_zero():
    """Проверяет выброс ExpressionError при делении на ноль."""
    with pytest.raises(DividedNumberError):
        calculator.calculate("2/0")
def test_missing_operand():
    """Проверяет выброс ExpressionError при отсутствии второго операнда в выражении."""
    with pytest.raises(ExpressionError):
        calculator.calculate("7+")
def test_two_operators():
    """Проверяет выброс ExpressionError при наличии двух операторов подряд."""
    with pytest.raises(ExpressionError):
        calculator.calculate("8/*3")
def test_invalid_character_error():
    """Проверяет выброс ExpressionError при наличии нечислового спецсимвола в выражении."""
    with pytest.raises(InvalidCharacterError):
        calculator.calculate("2@3-4")
def test_invalid_character_error_letter():
    """Проверяет выброс ExpressionError при наличии буквы в выражении."""
    with pytest.raises(ExpressionError):
        calculator.calculate("1 + a")


#Позитивные тесты конвертера
def test_convert_length():
    """Проверяет корректность конвертации единиц длины (миллиметры в метры)."""
    assert converter.convert(1000,"mm", "m") == 1
def test_convert_mass():
    """Проверяет корректность конвертации единиц массы (килограммы в граммы)."""
    assert converter.convert(4, "kg", "g") == 4000
def test_convert_temp():
    """Проверяет корректность конвертации температуры из градусов Цельсия в Фаренгейты."""
    assert converter.convert(3, "c", "f") == 37.4
def test_convert_temp_absolute_zero():
    """Проверяет конвертацию температуры из Цельсия в Кельвины в точке абсолютного нуля."""
    assert converter.convert(-273.15, "c", "k") == pytest.approx(0, abs=1e-6)
def test_convert_units_case_insensitive():
    """Проверяет нечувствительность конвертера к регистру символов единиц измерения."""
    assert converter.convert(3000, "MM", "M") == 3


#Негвтивные тесты конвертера
def test_convert_below_absolute_zero_raises():
    """Проверяет выброс ExpressionError при попытке конвертации температуры ниже абсолютного нуля."""
    with pytest.raises(UnderZeroError):
        converter.convert(-400, "c", "k")
def test_convert_incompatible_units_raises():
    """Проверяет выброс ExpressionError при попытке конвертации несовместимых единиц измерения."""
    with pytest.raises(IncompatibleUnitsError):
            converter.convert(1, "mm", "kg")

