from validator import ExpressionError

def tokenize_char(expr):
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
                raise ExpressionError(f"Invalid number: {str!r}")
            tokens.append(str)
            # Собираем число, увеличивая i, пока число не кончилось
            pass
        elif expr[i] in '+-*/':
            tokens.append(expr[i])
            i += 1
        else:
            raise ValueError(f"Неизвестный символ: {expr[i]}")
    return tokens



# def validate(tokens):#ошибки в отдельном файле 
#     prev_tok = None

#     for tok in tokens:
#         if tok in ('+', '-'):
#             if prev_tok in ('*', '/', '+', '-') or prev_tok is None:
#                 #унарный + / -
#                 pass
#         elif tok in ('*', '/'):
#             if prev_tok is None or prev_tok in ('+', '-', '*', '/'):
#                 return False
#         else:
#             if prev_tok not in (None, '+','-', '*','/'):
#                 return False
#         prev_tok = tok
#     return prev_tok not in ('+', '-', '*', '/')



OPERATOR = {'+': 1, '-': 1, '*': 2, '/': 2, 'u-':3, 'u+':3}
def shunting(tokens):
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
                    raise ExpressionError("Division by zero")
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


