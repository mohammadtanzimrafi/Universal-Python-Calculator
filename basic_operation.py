# This project is about a basic calculator.
initialization = input("Enter 'start' to start the calculator, or 'exit' to exit the program: ")
if initialization == "exit":
    print("Exiting the program...")
else:
    print("Welcome to Basic Calculator")
    print("Input an integer number for the calculation you want!")
    print("'1' for Addition")
    print("'2' for Subtraction")
    print("'3' for Multiplication")
    print("'4' for Divition")
    oparator = int(input("Write an integer number for your desired calculation: "))
    if oparator == 1:
        num_1 = float(input())
        num_2 = float(input())
        result = num_1 + num_2
    elif oparator == 2:
        num_1 = float(input())
        num_2 = float(input())
        result = num_1 - num_2
    elif oparator == 3:
        num_1 = float(input())
        num_2 = float(input())
        result = num_1 * num_2
    elif oparator == 4:
        num_1 = float(input())
        num_2 = float(input())
        result = num_1 / num_2
    else:
        result = "Invalid Operation!"
    print(result)