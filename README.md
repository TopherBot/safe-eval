# safe-eval

A tiny command‑line utility for **safe evaluation of arithmetic expressions**.

## Features
- ✅ Uses Python's `ast` module to parse and evaluate only mathematical expressions.
- ✅ Rejects any code that could execute side‑effects (no function calls, attribute access, etc.).
- ✅ Provides clear, user‑friendly error messages.
- ✅ Idempotent: the same expression always produces the same result.

## Installation
```bash
# Clone the repo (or copy the single file) and run directly with Python 3.8+
# No external dependencies required.
```

## Usage
```bash
$ python safe_eval.py "2 * (3 + 4) / 5"
2.8

$ python safe_eval.py "__import__('os').system('rm -rf /')"
Error: Unsafe expression detected.
```

## How it works
1. The expression string is parsed with `ast.parse(..., mode='eval')`.
2. The AST is traversed recursively, allowing only:
   - `ast.BinOp` with `Add, Sub, Mult, Div, Pow, Mod, FloorDiv`
   - `ast.UnaryOp` with `UAdd, USub`
   - `ast.Num`/`ast.Constant` for numbers
   - Parentheses via nested `BinOp`
3. Any other node (e.g., `Call`, `Attribute`, `Name`) raises `ValueError`.
4. The sanitized AST is then evaluated in a controlled environment.

## License
MIT © 2026 TopherBot

---
*Happy coding!*
