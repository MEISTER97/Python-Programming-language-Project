import Lexen

try:
    while True:
        text = input('Main > ')
        if text.strip() == "":
            continue
        if text.lower() in ('exit', 'quit'):
            print("Exiting the program...")
            break
        result, error = Lexen.run('<stdin>', text)

        if error:
            print(error.as_string())
        elif result:
            if len(result.elements)==1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))
except KeyboardInterrupt:
    print("\nProgram interrupted. Exiting...")



'''
def run_repl():
    print("Welcome to the REPL. Type 'exit' or 'quit' to exit.")

    try:
        while True:
            text = input('Main > ')
            if text.lower() in ('exit', 'quit'):
                print("Exiting the program...")
                break

            # Assuming Lexen.run() takes input text and returns (result, error)
            result, error = Lexen.run('<stdin>', text)

            if error:
                print(error.as_string())
            else:
                print(result)
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    run_repl()
'''
