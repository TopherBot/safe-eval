#!/usr/bin/env python3
"""safe_eval.py – Safely evaluate arithmetic expressions.

Author: TopherBot <topherbot@proton.me>
License: MIT
"""

import ast
import operator as op
import sys

# Mapping of AST operators to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}

def _evaluate(node):
    """Recursively evaluate an AST node, allowing only safe operations.

    Raises:
        ValueError: If the expression contains unsafe constructs.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        operator_type = type(node.op)
        if operator_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported operator: {operator_type.__name__}")
        return _ALLOWED_OPERATORS[operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        operator_type = type(node.op)
        if operator_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {operator_type.__name__}")
        return _ALLOWED_OPERATORS[operator_type](operand)

    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric literals are allowed.")

    # Compatibility for older Python versions
    if isinstance(node, ast.Num):
        return node.n

    # Any other node type is disallowed (e.g., Name, Call, Attribute)
    raise ValueError("Unsafe expression detected.")

def safe_eval(expr: str):
    """Parse and safely evaluate a mathematical expression.

    Args:
        expr: The arithmetic expression as a string.
    Returns:
        The numeric result of the expression.
    Raises:
        ValueError: If the expression is unsafe or malformed.
    """
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError("Syntax error in expression.") from e
    return _evaluate(parsed)

def main():
    if len(sys.argv) != 2:
        print("Usage: python safe_eval.py \"<expression>\"")
        sys.exit(1)
    expr = sys.argv[1]
    try:
        result = safe_eval(expr)
        # Idempotent output: plain number without extra formatting
        print(result)
    except ValueError as err:
        print(f"Error: {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
