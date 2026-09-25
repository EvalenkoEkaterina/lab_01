import sys

from validator import (
    ExpressionError, check_input,
    validate_number, validate_units, validate_temperature,
)

GROUPS = {
    "length": {"mm", "cm", "m", "km"},
    "mass": {"g", "kg"},
    "temperature": {"c", "f", "k"},
}


def convert(value_text, from_name, to_name):#что переводим, из какой единицы, в какую
    value = validate_number(value_text)                       # неверное число
    group, unit, to_unit = validate_units(from_name, to_name)
    # неизвестная единица, несовместимые единицы
    if group == "temperature":
        validate_temperature(value, unit)                     # абсолютный ноль

    if unit == to_unit:
        return value

    # Длина
    if unit == "mm" and to_unit == "cm":
        return value / 10
    if unit == "mm" and to_unit == "m":
        return value / 1000
    if unit == "mm" and to_unit == "km":
        return value / 1000000
    if unit == "cm" and to_unit == "mm":
        return value * 10
    if unit == "cm" and to_unit == "m":
        return value / 100
    if unit == "cm" and to_unit == "km":
        return value / 100000
    if unit == "m" and to_unit == "mm":
        return value * 1000
    if unit == "m" and to_unit == "cm":
        return value * 100
    if unit == "m" and to_unit == "km":
        return value / 1000
    if unit == "km" and to_unit == "mm":
        return value * 1000000
    if unit == "km" and to_unit == "cm":
        return value * 100000
    if unit == "km" and to_unit == "m":
        return value * 1000

    # Масса
    if unit == "g" and to_unit == "kg":
        return value / 1000
    if unit == "kg" and to_unit == "g":
        return value * 1000

    # Температура
    if unit == "c" and to_unit == "f":
        return value * 9 / 5 + 32
    if unit == "c" and to_unit == "k":
        return value + 273.15
    if unit == "f" and to_unit == "c":
        return (value - 32) * 5 / 9
    if unit == "f" and to_unit == "k":
        return (value - 32) * 5 / 9 + 273.15
    if unit == "k" and to_unit == "c":
        return value - 273.15
    if unit == "k" and to_unit == "f":
        return (value - 273.15) * 9 / 5 + 32

    raise ExpressionError("Unsupported conversion")           # страховка
