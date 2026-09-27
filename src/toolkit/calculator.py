from .validator import validate_tokens
from .errors import ExpressionError, InvalidCharacterError, InvalidNumberError, DividedNumberError, EmptyExpressionError


def tokenize_char(expr):
    """
    Разбивает строку выражения на список токенов посимвольно.

    Пробелы и табуляции пропускаются.
    Цифры и точки собираются подряд в один токен-число
    (например, "12.5" станет одним токеном, а не пятью символами);
    если собранная строка не парсится как float, поднимается
    ExpressionError с сообщением о некорректном числе.
    Операторы '+', '-', '*', '/' добавляются как отдельные токены.
    Любой другой символ считается недопустимым и вызывает
    ExpressionError.

    Параметры:
        expr (str): исходное выражение.

    Возвращает:
        list[str]: список токенов (чисел в виде строк и операторов).

    Исключения:
        ExpressionError: если встречен недопустимый символ
            или число не может быть преобразовано в float.
    """
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i].isspace() or expr[i] == '\t':
            i += 1 # переходим к следующему символу         
        elif expr[i].isdigit() or expr[i] == '.':
            str = ''
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                str += expr[i]
                i += 1
            try:
                float(str)
            except ValueError:
                raise InvalidNumberError(f"Invalid number: {str!r}")
            tokens.append(str)
            # Собираем число, увеличивая i, пока число не кончилось
        elif expr[i] in '+-*/':
            tokens.append(expr[i])
            i += 1
        else:
            raise InvalidCharacterError(f"Неизвестный символ: {expr[i]}")
    return tokens


OPERATOR = {'+': 1, '-': 1, '*': 2, '/': 2, 'u-':3, 'u+':3}
def shunting(tokens):
    """
    Преобразует список токенов из инфиксной записи в постфиксную (ОПЗ)
    по алгоритму сортировочной станции (shunting-yard).

    Учитывает приоритет операторов: '*' и '/' выше, чем '+' и '-'
    (см. словарь OPERATOR). Унарные '+' и '-' (когда оператор стоит
    в начале выражения или сразу после другого оператора) распознаются
    отдельно как 'u+' и 'u-' и имеют наивысший приоритет, чтобы
    выполняться раньше бинарных операций.

    Параметры:
        tokens (list[str]): список токенов в инфиксном порядке
            (числа как строки и операторы '+', '-', '*', '/').

    Возвращает:
        list[str]: список токенов в постфиксном порядке (ОПЗ),
            готовый для вычисления функцией evaluate.
    """
    output = []
    operator_stack = []
    prev_tok = None

    for tok in tokens:

        if tok in ('-' , '+') and (prev_tok is None or prev_tok in OPERATOR):
            if tok == '-':
                tok = 'u-'
            else:
                tok = 'u+'

        if tok in OPERATOR:
            cur_o = tok
            while (operator_stack and 
                   (OPERATOR[operator_stack[-1]]> OPERATOR[cur_o] or
                   OPERATOR[operator_stack[-1]] == OPERATOR[cur_o] and cur_o not in('u-', 'u+'))):
                output.append(operator_stack.pop())
            operator_stack.append(cur_o)
        else:
            output.append(tok)
        prev_tok = tok
    while operator_stack:
        output.append(operator_stack.pop())
    return output
#if validate(tokens):
   # print(shunting(tokens))
#else:
   # print("Ошибка в выражении")



def evaluate(tokens):
    """
    Вычисляет значение выражения, заданного в постфиксной записи (ОПЗ).

    Использует стек: числа кладутся в стек, при встрече бинарного
    оператора ('+', '-', '*', '/') из стека снимаются два верхних
    значения и результат операции кладётся обратно; при встрече
    унарного оператора ('u-', 'u+') снимается одно значение.
    Деление на ноль поднимает ExpressionError. Если после обработки
    всех токенов в стеке остаётся не ровно одно значение — выражение
    некорректно.

    Параметры:
        tokens (list[str]): список токенов в постфиксном порядке
            (результат работы функции shunting).

    Возвращает:
        float: результат вычисления выражения.

    Исключения:
        ExpressionError: при нехватке операндов (для бинарного
            или унарного оператора), делении на ноль, а также
            если после вычисления в стеке осталось не одно значение.
    """
    stack2 = []
    for tok in tokens:
        if tok in ('+', '-', '*', '/'):
            if len(stack2) < 2:
                raise ExpressionError("Missing operand")
            b = stack2.pop()
            a = stack2.pop()
            if tok == '+':
                stack2.append(a + b)
            elif tok == '-':
                stack2.append(a - b)
            elif tok == '*':
                stack2.append(a * b)
            else:
                if b == 0:
                    raise DividedNumberError("Division by zero")
                stack2.append(a / b)
        elif tok == 'u-':
            if not stack2:
                raise ExpressionError("Missing operand")
            stack2.append(-stack2.pop())
        elif tok == 'u+':
            if not stack2:
                raise ExpressionError("Missing operand")
        else:
            stack2.append(float(tok))
    if len(stack2) != 1:
        raise ExpressionError("Invalid expression")
    return stack2[0]


def calculate(expr):
    """
    Вычисляет значение арифметического выражения, заданного строкой.

    Объединяет весь конвейер обработки: разбивает строку на токены,
    проверяет их на корректность (пропущенные операнды, два оператора
    подряд и т.п.), переводит выражение в постфиксную запись (ОПЗ)
    и вычисляет результат.

    Параметры:
        expr (str): арифметическое выражение, например "2 + 3 * 4".

    Возвращает:
        float: результат вычисления выражения.

    Исключения:
        ExpressionError: если выражение содержит недопустимый символ,
            некорректное число, пропущенный операнд, два оператора
            подряд или деление на ноль.
    """
    if not expr.strip():
        raise EmptyExpressionError("Empty expression")
    tokens = tokenize_char(expr)
    validate_tokens(tokens)
    postfix = shunting(tokens)
    return evaluate(postfix)
