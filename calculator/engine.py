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

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


def factorial(value):
    if not float(value).is_integer() or value < 0:
        raise ValueError("factorial() only supports non-negative integers.")
    return math.factorial(int(value))


def build_functions(angle_mode):
    use_degrees = angle_mode.upper() == "DEG"

    def _input_angle(value):
        return math.radians(value) if use_degrees else value

    def _output_angle(value):
        return math.degrees(value) if use_degrees else value

    return {
        "sqrt": math.sqrt,
        "sin": lambda value: math.sin(_input_angle(value)),
        "cos": lambda value: math.cos(_input_angle(value)),
        "tan": lambda value: math.tan(_input_angle(value)),
        "asin": lambda value: _output_angle(math.asin(value)),
        "acos": lambda value: _output_angle(math.acos(value)),
        "atan": lambda value: _output_angle(math.atan(value)),
        "log": math.log,
        "log10": math.log10,
        "abs": abs,
        "round": round,
        "fact": factorial,
        "factorial": factorial,
    }


def evaluate_expression(expression, ans=0.0, memory=0.0, angle_mode="DEG"):
    normalized = expression.replace("^", "**")

    try:
        tree = ast.parse(normalized, mode="eval")
    except SyntaxError as error:
        raise ValueError("Invalid expression. Try something like 2 + 3 * 4.") from error

    context = {
        "variables": {
            "ans": ans,
            "mem": memory,
            **CONSTANTS,
        },
        "functions": build_functions(angle_mode),
    }
    return _evaluate_node(tree.body, context)


def _evaluate_node(node, context):
    if isinstance(node, ast.BinOp):
        left = _evaluate_node(node.left, context)
        right = _evaluate_node(node.right, context)
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
        return operation(_evaluate_node(node.operand, context))

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct function calls are allowed.")

        function_name = node.func.id.lower()
        function = context["functions"].get(function_name)
        if function is None:
            raise ValueError(f"Unknown function '{function_name}'.")

        values = [_evaluate_node(argument, context) for argument in node.args]
        try:
            return function(*values)
        except TypeError as error:
            raise ValueError(f"Invalid arguments for '{function_name}'.") from error
        except ValueError as error:
            raise ValueError(str(error)) from error

    if isinstance(node, ast.Name):
        name = node.id.lower()
        if name in context["variables"]:
            return context["variables"][name]
        raise ValueError(f"Unknown value '{node.id}'.")

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)

    raise ValueError("That expression is not supported.")
