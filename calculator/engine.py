import ast
import math
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def factorial(value):
    if not float(value).is_integer() or value < 0:
        raise ValueError("factorial() only supports non-negative integers.")
    return math.factorial(int(value))


FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "log": math.log,
    "log10": math.log10,
    "abs": abs,
    "round": round,
    "fact": factorial,
    "factorial": factorial,
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


def evaluate_expression(expression, ans=0.0):
    normalized = expression.replace("^", "**")

    try:
        tree = ast.parse(normalized, mode="eval")
    except SyntaxError as error:
        raise ValueError("Invalid expression. Try something like 2 + 3 * 4.") from error

    return _evaluate_node(tree.body, {"ans": ans})


def _evaluate_node(node, variables):
    if isinstance(node, ast.BinOp):
        left = _evaluate_node(node.left, variables)
        right = _evaluate_node(node.right, variables)
        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("That operator is not supported.")

        if isinstance(node.op, (ast.Div, ast.Mod)) and right == 0:
            raise ValueError("Division by zero is not allowed.")

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        operation = UNARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("That unary operator is not supported.")
        return operation(_evaluate_node(node.operand, variables))

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct function calls are allowed.")

        function_name = node.func.id.lower()
        function = FUNCTIONS.get(function_name)
        if function is None:
            raise ValueError(f"Unknown function '{function_name}'.")

        values = [_evaluate_node(argument, variables) for argument in node.args]
        try:
            return function(*values)
        except TypeError as error:
            raise ValueError(f"Invalid arguments for '{function_name}'.") from error
        except ValueError as error:
            raise ValueError(str(error)) from error

    if isinstance(node, ast.Name):
        name = node.id.lower()
        if name in variables:
            return variables[name]
        if name in CONSTANTS:
            return CONSTANTS[name]
        raise ValueError(f"Unknown value '{node.id}'.")

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)

    raise ValueError("That expression is not supported.")
