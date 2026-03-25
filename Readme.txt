Project Title: Universal Python Calculator

This project now uses a cleaner real-world GUI layout with separated standard and advanced controls, stronger number visibility, and a more professional scientific-calculator style.

Version 3.0
The current version improves the UI into a more production-style desktop calculator with split panels, mode buttons, and scrollable advanced tools.

Current Features:
1. Professional desktop GUI using Tkinter.
2. Large, high-contrast display for expressions and results.
3. Bigger number buttons for easier everyday use.
4. Split layout:
   * Standard panel for normal calculations
   * Advanced panel for scientific and memory tools
   * Separate history panel
5. DEG and RAD mode as real clickable buttons.
6. Scrollable advanced tools area.
7. Scrollable history list.
8. Memory controls:
   * `MC`
   * `MR`
   * `M+`
   * `M-`
9. Real calculator-style direct expressions such as:
   * `2 + 3 * 4`
   * `sqrt(81)`
   * `sin(90)` in DEG mode
   * `sin(pi / 2)` in RAD mode
   * `mem + 5`
10. Scientific functions available from the side panel.
11. Reusable history selection.
12. Cleaner status feedback and easier interaction.

Code Structure:
1. `basic_operation.py` - entry point
2. `calculator/app.py` - GUI application
3. `calculator/engine.py` - safe math engine

Why this version is better:
1. Easier to use like a standard and scientific calculator together.
2. Cleaner visual separation between normal and advanced actions.
3. Better suited for future upgrades like tabs, themes, and converter mode.

Suggested Next Steps:
1. Add keyboard shortcuts for memory actions.
2. Add copy result and save history options.
3. Add tabs for Standard, Scientific, and Converter modes.
4. Add theme switching with light and dark professional skins.
