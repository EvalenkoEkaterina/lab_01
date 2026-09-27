class ExpressionError(ValueError):
    pass
class EmptyExpressionError(ExpressionError):
    pass


class InvalidCharacterError(ExpressionError):
    pass


class InvalidNumberError(ExpressionError):
    pass
class UnknownUnitError(ExpressionError):
    pass


class DividedNumberError(ExpressionError):
    pass


class IncompatibleUnitsError(ExpressionError):
    pass


class UnderZeroError(ExpressionError):
    pass