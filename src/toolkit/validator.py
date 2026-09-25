import math


class ExpressionError(ValueError):
    pass


OPS = ("+", "-", "*", "/")


def check_input(expr):
    if expr is None or not isinstance(expr, str) or not expr.strip():
        raise ExpressionError("Empty expression")
'''
Проверка условия на пустое выражение
(если не подалось значение; проверка является ли строкой; пуста ли строка после удаления пробелов в концах)
'''

def is_allowed(ch):
    if ch.isspace():
        return True
    if ch.isdigit() or ch.isalpha():
        return True
    if ch in ",.+-*/()":
        return True
    return False
'''
Проверка на недопустимый символ 
(если пробел; цифра или буква; или +-.,/()/, то возвращаем True, иначе False
'''

def invalid_character(expr):
    for i, ch in enumerate(expr):
        if not is_allowed(ch):
            return f"Invalid character: {ch!r} at position {i}"
    return None
'''
Проверка на недопустимый символ 
проходимся по строке с помощью функции enumerate , которая выводит и символ и его позицию в случае, если символ не проходит проверку на условие
'''

def validate_string(expr):
    check_input(expr)
    error = invalid_character(expr)
    if error:
        raise ExpressionError(error)
'''
Совмещение двух проверок в одну проверку
'''

def validate_tokens(tokens):
    prev = None
    for tok in tokens:
        if tok in OPS:
            if prev is None:
                raise ExpressionError("Operator at the beginning")
            if prev in '*/':
                raise ExpressionError("Two operators in a row")
        prev = tok
    if prev in OPS:
        raise ExpressionError("Operator at the end")

# def missing_operand(tokens):
#     if not tokens:
#         return None
#     if tokens[0] in OPS:
#         return f"Missing operand before '{tokens[0]}' at position 0"
#     if tokens[-1] in OPS:
#             return f"Missing operand after '{tokens[-1]}' at position '{len(tokens) - 1}"
    
'''
Функция поиска пропущенных операндов
если значение осталось None и символ в операторах, то он стоит в начале
если предыдущее значение было оператором и нынешнее тоже, ошибка
если последний токен равен оператору, то после него ничего больше нет, значит операнд в конце пропущен
'''


def validate_number(text):
    try:
        return float(text)
    except ValueError:
        raise ExpressionError("Invalid number")
'''
функция проверяет подается ли на ввод число(можно ли сделать float)
запятая заменяется на точку для возможности ввода дробного числа через запятую
'''
def find_unit_group(name):
    name = name.lower()
    if name in ("m", "km", "cm", "mm"):
        return "length", name
    if name in ("kg", "g", "mg"):
        return "weight", name
    if name in ("c", "f", "k"):
        return "temperature", name

    raise ExpressionError(f"Unknown unit: {name}")
'''
функция проверяет на введенную неизвестную единицу
сначала приводим единицы к одному единому регистру(нам не важен регистр)
если не попадает ни под одну из проверяемых условий, ошибка
'''

def validate_units(from_name, to_name):
    a = find_unit_group(from_name)
    b = find_unit_group(to_name)

    if a[0] != b[0]:
        raise ExpressionError("Incompatible units")

    return a[0], a[1], b[1]
'''
Проверка на сопоставимость групп вводимых единиц
если группа не совпадает, ошибка 
иначе возвращаем группу и единицы, из которой и в какую переводить
'''
def validate_temperature(value, unit):
    if unit == "c" and value < -273.15:
        raise ExpressionError("Invalid temperature")
    if unit == "f" and value < -459.67:
        raise ExpressionError("Invalid temperature")
    if unit == "k" and value < 0:
        raise ExpressionError("Invalid temperature")
'Проверка на неверное числовое значение, ниже нуля в разных группах'


# class ExpressionError(ValueError):
#     pass


# def check_input(expr):
#     if expr is None:
#         raise ExpressionError("Empty expression")

#     if not isinstance(expr, str):
#         raise TypeError("Expression must be str")

#     if not expr.strip():
#         raise ExpressionError("Empty expression")


# OPS = ("+", "-", "*", "/")


# def is_allowed(ch):
#     if ch.isspace():
#         return True

#     if ch.isdigit():
#         return True

#     if ch.isalpha():
#         return True

#     if ch in ",.+-*/()":
#         return True

#     return False


# def invalid_character(expr):
#     for i, ch in enumerate(expr):
#         if not is_allowed(ch):
#             return f"Invalid character: {ch!r} at position {i}"

#     return None


# def validate_string(expr):
#     check_input(expr)

#     error = invalid_character(expr)

#     if error:
#         raise ExpressionError(error)


# def validate_tokens(tokens):
#     prev = None

#     for tok in tokens:
#         if tok in OPS:
#             if prev is None:
#                 raise ExpressionError("Operator at the beginning")

#             if prev in OPS:
#                 raise ExpressionError("Two operators in a row")

#         prev = tok

#     if prev in OPS:
#         raise ExpressionError("Operator at the end")


# def validate_number(text):
#     if "e" in text.lower():
#         raise ExpressionError(f"Invalid numeric value: {text!r}")

#     try:
#         value = float(text.replace(",", "."))
#     except ValueError:
#         raise ExpressionError(f"Invalid numeric value: {text!r}")

#     return value


# def find_unit_group(name, units_table):
#     name = name.lower()

#     for group in units_table:
#         if name in units_table[group]:
#             return group, name

#     raise ExpressionError(f"Unknown unit: {name}")


# def validate_units(from_name, to_name, units_table):
#     from_group, from_unit = find_unit_group(from_name, units_table)
#     to_group, to_unit = find_unit_group(to_name, units_table)

#     if from_group != to_group:
#         raise ExpressionError("Incompatible units")

#     return from_group, from_unit, to_unit