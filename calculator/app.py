from calculator.engine import CONSTANTS, FUNCTIONS, evaluate_expression


WELCOME_TEXT = """
+-------------------------------------------+
|     Universal Python Calculator v2.0      |
+-------------------------------------------+
 Type expressions naturally:
   2 + 3 * 4
   sqrt(81)
   sin(pi / 2)
   ans * 2

 Commands:
   help, history, clear, clear history, exit
""".strip("\n")


def main():
    history = []
    last_answer = 0.0

    print(WELCOME_TEXT)

    while True:
        user_input = input("\ncalc> ").strip()

        if not user_input:
            print("Enter a calculation or type 'help'.")
            continue

        command = user_input.lower()

        if command in {"exit", "quit"}:
            print("Exiting the program...")
            break

        if command == "help":
            show_help()
            continue

        if command == "history":
            show_history(history)
            continue

        if command == "clear":
            last_answer = 0.0
            print("Last answer cleared.")
            continue

        if command == "clear history":
            history.clear()
            print("History cleared.")
            continue

        try:
            result = evaluate_expression(user_input, ans=last_answer)
        except ValueError as error:
            print(f"Error: {error}")
            continue

        last_answer = result
        output = format_number(result)
        history.append(f"{user_input} = {output}")
        print(f"= {output}")


def show_help():
    print("\nQuick Help")
    print("  Use normal math expressions with parentheses when needed.")
    print("  Reuse the last result with 'ans'.")
    print("  Power can be written as '^' or '**'.")
    print("\nOperators")
    print("  +  -  *  /  %  ^")
    print("\nFunctions")
    print(f"  {', '.join(sorted(FUNCTIONS))}")
    print("\nConstants")
    print(f"  {', '.join(sorted(CONSTANTS))}, ans")


def show_history(history):
    if not history:
        print("No calculations in history yet.")
        return

    print("\nHistory")
    for index, item in enumerate(history, start=1):
        print(f"  {index}. {item}")


def format_number(value):
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.10g}"
