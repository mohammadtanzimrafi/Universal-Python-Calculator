Project Title: Universal Python Calculator

This project is a growing Python calculator.

Version 2.0
The current version keeps the codebase cleaner with supporting real calculator-style input.

Current Features:
1. Real calculator style input:
   * `2 + 3 * 4`
   * `sqrt(81)`
   * `sin(pi / 2)`
   * `15 % 4`
   * `ans * 2`
2. Supported operators:
   * Addition `+`
   * Subtraction `-`
   * Multiplication `*`
   * Division `/`
   * Modulus `%`
   * Power `^`
3. Supported functions:
   * `sqrt`
   * `sin`, `cos`, `tan`
   * `asin`, `acos`, `atan`
   * `log`, `log10`
   * `abs`
   * `round`
   * `fact` and `factorial`
4. Supported constants:
   * `pi`
   * `e`
   * `ans` for the last result
5. Friendly commands:
   * `help`
   * `history`
   * `clear`
   * `clear history`
   * `exit`
6. Clean terminal output with a simple calculator prompt.
7. Safe expression evaluation with validation.
8. Calculation history tracking.

Code Quality Improvements:
1. Reduced the architecture to a simple app layer and engine layer.
2. Kept the entry point very small.
3. Used plain functions instead of heavier class-based structure.
4. Kept math support centralized in one engine file.
5. Made it easy to add future functions and constants in one place.

Suggested Project Structure:
1. `basic_operation.py` - entry point
2. `calculator/app.py` - user interaction and commands
3. `calculator/engine.py` - math functions, constants, and safe evaluation

Planned Next Steps:
1. Add degree and radian mode switching.
2. Add memory features like `M+`, `M-`, and memory recall.
3. Add unit conversion mode.
4. Add financial mode.
5. Add automated tests.
6. Build a GUI version later.