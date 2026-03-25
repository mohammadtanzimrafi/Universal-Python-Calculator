import math


def get_number(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid number. Please enter a valid numeric value.")


def print_menu():
    print("\nChoose an operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Power")
    print("6. Modulus")
    print("7. Percentage")
    print("8. Square Root")
    print("9. Show History")
    print("0. Exit")


def calculate(choice, history):
    if choice == "1":
        num_1 = get_number("Enter the first number: ")
        num_2 = get_number("Enter the second number: ")
        result = num_1 + num_2
        expression = f"{num_1} + {num_2} = {result}"
    elif choice == "2":
        num_1 = get_number("Enter the first number: ")
        num_2 = get_number("Enter the second number: ")
        result = num_1 - num_2
        expression = f"{num_1} - {num_2} = {result}"
    elif choice == "3":
        num_1 = get_number("Enter the first number: ")
        num_2 = get_number("Enter the second number: ")
        result = num_1 * num_2
        expression = f"{num_1} * {num_2} = {result}"
    elif choice == "4":
        num_1 = get_number("Enter the first number: ")
        num_2 = get_number("Enter the second number: ")
        if num_2 == 0:
            print("Error: Division by zero is not allowed.")
            return
        result = num_1 / num_2
        expression = f"{num_1} / {num_2} = {result}"
    elif choice == "5":
        num_1 = get_number("Enter the base number: ")
        num_2 = get_number("Enter the power: ")
        result = num_1 ** num_2
        expression = f"{num_1} ^ {num_2} = {result}"
    elif choice == "6":
        num_1 = get_number("Enter the first number: ")
        num_2 = get_number("Enter the second number: ")
        if num_2 == 0:
            print("Error: Modulus by zero is not allowed.")
            return
        result = num_1 % num_2
        expression = f"{num_1} % {num_2} = {result}"
    elif choice == "7":
        num_1 = get_number("Enter the number: ")
        num_2 = get_number("Enter the percentage value: ")
        result = (num_1 * num_2) / 100
        expression = f"{num_2}% of {num_1} = {result}"
    elif choice == "8":
        num_1 = get_number("Enter the number: ")
        if num_1 < 0:
            print("Error: Square root of a negative number is not supported here.")
            return
        result = math.sqrt(num_1)
        expression = f"sqrt({num_1}) = {result}"
    elif choice == "9":
        if not history:
            print("No calculations in history yet.")
            return
        print("\nCalculation History:")
        for index, item in enumerate(history, start=1):
            print(f"{index}. {item}")
        return
    else:
        print("Invalid choice. Please select a valid menu option.")
        return

    history.append(expression)
    print(f"Result: {result}")


def main():
    history = []
    print("Welcome to Universal Python Calculator v1.1")

    while True:
        initialization = input(
            "\nType 'start' to use the calculator or 'exit' to close it: "
        ).strip().lower()

        if initialization == "exit":
            print("Exiting the program...")
            break

        if initialization != "start":
            print("Invalid input. Please type 'start' or 'exit'.")
            continue

        while True:
            print_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "0":
                print("Returning to the main menu...")
                break

            calculate(choice, history)


if __name__ == "__main__":
    main()
