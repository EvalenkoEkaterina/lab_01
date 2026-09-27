from .errors import EmptyExpressionError,DividedNumberError,UnderZeroError, IncompatibleUnitsError, InvalidCharacterError, InvalidNumberError, UnknownUnitError

OPS = ("+", "-", "*", "/")


def check_input(expr):
    if expr is None or not isinstance(expr, str) or not expr.strip():
        raise EmptyExpressionError("Empty expression")
'''
Проверка условия на пустое выражение
(если не подалось значение; проверка является ли строкой; пуста ли строка после удаления пробелов в концах)
'''

def is_allowed(ch):
    """Проверяет, что оператор сложения распознается как допустимый символ."""
    return ch.isspace() or ch.isdigit() or ch.isalpha() or ch in ",.+-*/()"

'''
Проверка на недопустимый символ 
(если пробел; цифра или буква; или +-.,/()/, то возвращаем True, иначе False
'''

def invalid_character(expr):
    for i, ch in enumerate(expr):
        if not is_allowed(ch):
            raise InvalidCharacterError(
            f"Invalid character: {ch!r} at position {i}")
    return None
'''
Проверка на недопустимый символ 
проходимся по строке с помощью функции enumerate , которая выводит и символ и его позицию в случае, если символ не проходит проверку на условие
'''

def validate_string(expr):
    check_input(expr)
    invalid_character(expr)
'''
Совмещение двух проверок в одну проверку
'''

def validate_tokens(tokens):
    prev = None
    for tok in tokens:
        if tok in '*/' and prev in '*/':
            raise DividedNumberError("Two operators in a row")
        prev = tok
    if prev in OPS:
        raise DividedNumberError("Operator at the end")

    
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
        raise InvalidNumberError("Invalid numeric value")

    
def find_unit_group(name):
    name = name.lower()
    if name in ("m", "km", "cm", "mm"):
        return "length", name
    if name in ("kg", "g", "mg"):
        return "weight", name
    if name in ("c", "f", "k"):
        return "temperature", name

    raise UnknownUnitError(f"Unknown unit: {name}")
'''
функция проверяет на введенную неизвестную единицу
сначала приводим единицы к одному единому регистру(нам не важен регистр)
если не попадает ни под одну из проверяемых условий, ошибка
'''

def validate_units(from_name, to_name):
    a = find_unit_group(from_name)
    b = find_unit_group(to_name)

    if a[0] != b[0]:
        raise IncompatibleUnitsError("Incompatible units")

    return a[0], a[1], b[1]
'''
Проверка на сопоставимость групп вводимых единиц
если группа не совпадает, ошибка 
иначе возвращаем группу и единицы, из которой и в какую переводить
'''
def validate_temperature(value, unit):
    if unit == "c" and value < -273.15:
        raise UnderZeroError("Invalid temperature")
    if unit == "f" and value < -459.67:
        raise UnderZeroError("Invalid temperature")
    if unit == "k" and value < 0:
        raise UnderZeroError("Invalid temperature")
'Проверка на неверное числовое значение, ниже нуля в разных группах'

def format_number(value):
    if value == int(value):
        return int(value)
    return value

