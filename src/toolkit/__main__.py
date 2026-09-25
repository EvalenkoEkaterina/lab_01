# import sys
# from calculator import shunting, evaluate, tokenize_char
# import converter



# def main():
#     if len(sys.argv) != 2:
#             print("Ожидается ровно один аргумент", file=sys.stderr)
#             sys.exit(1)
#     expr = sys.argv[1]
#     try:
#         tokens = tokenize_char(expr)
#         rpn_tokens = shunting(tokens)
#         result = evaluate(rpn_tokens)
#         print(result)
#     except Exception as e:
#         print(f"Ошибка: {e}", file=sys.stderr)
#         sys.exit(1)
#     t

# if __name__ == "__main__":
#     main()
import sys

from calculator import tokenize_char,shunting, evaluate
from converter import convert
from validator import ExpressionError, validate_string, validate_tokens


def run_converter():
    try:
        line = input("Введите значение и единицу: ")
        parts = line.split()
        if len(parts) != 2:
            raise ExpressionError("Введите: <значение> <единица>")
        to_name = input("Во что перевести: ")
        result = convert(parts[0], parts[1], to_name)
        print("Результат:", result, to_name.lower())
    except ExpressionError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) > 1:
        expr = sys.argv[1]
        try:
            validate_string(expr)
            tokens = tokenize_char(expr)
            validate_tokens(tokens)
            result = evaluate(shunting(tokens))
            print(result)
        except ExpressionError as e:
            print(e, file=sys.stderr)
            sys.exit(1)

    else:
        run_converter()
    


if __name__ == "__main__":
    main()