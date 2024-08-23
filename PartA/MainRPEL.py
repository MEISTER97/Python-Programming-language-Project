from PartA import basic


def main():
    print("Welcome to the RPEL Lambda Tester!")

    # Define test cases
    test_cases = [
        "(3+4)*(2-1)",  # Test arithmetic operations: addition, subtraction, and multiplication
        "10 == 10 && 2 == 3",  # Test boolean expression with logical AND
        "10 != 10 || 10 != 2",  # Test boolean expression with logical OR
        "FUNC add(a, b) -> a + b",  # Test function definition with two parameters
        "add(5, 10)",  # Test function call with two arguments
        "FUNC factorial(n) -> IF n == 0 THEN 1 ELSE n * factorial(n - 1)",
        # Test recursive function definition (factorial)
        "factorial(5)",  # Test recursive function call (factorial of 5)
        "((LAMBDA x . x + 1)(10))",  # Test lambda expression with a single variable
        "((LAMBDA x, y . x + y)(5, 10))",  # Test lambda expression with two variables
        "((LAMBDA x, y, z . x + y * z)(1, 2, 3))",  # Test lambda expression with three variables
        "(LAMBDA x . x * x )(4)",  # Test lambda expression that squares a number
    ]

    for text in test_cases:
        print(f"Testing: {text}")

        try:
            # Run the RPEL expression
            result, error = basic.run('<stdin>', text)

            if error:
                print(f"Error: {error}")
            else:
                print(f"Result: {result}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")


def tryRPEL():
    try:
        while True:
            text = input('Main > ')
            if text.strip() == "":
                continue
            if text.lower() in ('exit', 'quit'):
                print("Exiting the program...")
                break
            result, error = basic.run('<stdin>', text)
            if error:
                print(error.as_string())
            else:
                print(repr(result))
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")


if __name__ == "__main__":
    main()
    tryRPEL()
