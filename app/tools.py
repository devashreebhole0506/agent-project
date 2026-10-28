from datetime import datetime
from zoneinfo import ZoneInfo

from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Calculate a basic arithmetic expression."""

    import ast
    import operator

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }

    unary_operators = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool):
                raise ValueError("Boolean values are not allowed.")

            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Only numeric constants are allowed.")

        if isinstance(node, ast.BinOp):
            operator_type = type(node.op)

            if operator_type not in operators:
                raise ValueError("Unsupported operator.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent is too large.")

            return operators[operator_type](left, right)

        if isinstance(node, ast.UnaryOp):
            operator_type = type(node.op)

            if operator_type not in unary_operators:
                raise ValueError("Unsupported unary operator.")

            return unary_operators[operator_type](
                evaluate(node.operand)
            )

        raise ValueError("Unsupported expression.")

    try:
        if len(expression) > 256:
            raise ValueError("Expression is too long.")
        tree = ast.parse(expression, mode="eval")
        result = evaluate(tree.body)
        if isinstance(result, (int, float)) and abs(result) > 1e100:
            raise ValueError("Result is too large.")
        return str(result)
    except Exception as exc:
        return f"Calculator error: {exc}"


@tool
def project_lookup(topic: str) -> str:
    """Look up information about the demo AI agent project."""

    knowledge = {
        "framework": "The project uses LangChain and FastAPI.",
        "calculator": "The calculator evaluates basic arithmetic expressions.",
        "api": "The API exposes a POST /agent endpoint.",
        "tools": "The demo agent includes a calculator, project lookup, and time utility.",
    }

    normalized_topic = topic.lower()

    for key, value in knowledge.items():
        if key in normalized_topic:
            return value

    return "No matching information was found in the project knowledge base."


@tool
def current_time(timezone_name: str = "Asia/Kolkata") -> str:
    """Return the current date and time for a valid IANA timezone."""

    try:
        now = datetime.now(ZoneInfo(timezone_name))
        return now.isoformat()
    except Exception:
        return "Time lookup error: invalid or unavailable timezone."
