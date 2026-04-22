def calculate(expression):
    """
    Evaluates a math expression and returns the result as a string.

    >>> calculate('2 + 2')
    '4'
    >>> calculate('25 * 4 + 10')
    '110'
    >>> calculate('1 / 0')
    'Error: division by zero'
    >>> calculate('not valid !!!')
    'Error: invalid syntax (<string>, line 1)'
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f'Error: {e}'


SCHEMA = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Evaluate a mathematical expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression to evaluate."}
            },
            "required": ["expression"],
        },
    },
}
