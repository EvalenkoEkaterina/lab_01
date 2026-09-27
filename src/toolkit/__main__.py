
import sys

from .calculator import calculate, tokenize_char
from .converter import convert
from .validator import format_number, validate_string, validate_tokens
from .errors import ExpressionError
HELP_TEXT = """\
Использование:
  python -m toolkit calc "EXPRESSION"
  python -m toolkit convert VALUE --from UNIT --to UNIT
  python -m toolkit --help
"""

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print(HELP_TEXT)
        return
    command = sys.argv[1]
    try:
        if command == "calc":
            expr = sys.argv[2]
            validate_string(expr)
            tokens = tokenize_char(expr)
            validate_tokens(tokens)
            result = calculate(expr)
            print(format_number(result))
        elif command == "convert":
            value = sys.argv[2]
            from_unit = sys.argv[4]
            to_unit = sys.argv[6]
            print(convert(value, from_unit, to_unit))
    except ExpressionError as e:
        print(e, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()