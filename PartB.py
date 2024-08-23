from functools import reduce

# Part B-Q1
fibonacci = lambda n, a=0, b=1: [] if n == 0 else [a] if n == 1 else [a] + fibonacci(n - 1, b, a + b)

# Example usage:
print(fibonacci(10))  # Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Part B-Q2

concatenate = lambda strings: reduce(lambda x, y: x + ' ' + y, strings)

# Example usage
lst = ["Hello", "world", "from", "lambda"]
result = concatenate(lst)
print(result + "\n")  # Output: "Hello world from lambda"

# Part B-Q3

cumulative_sum_of_squares = lambda lists: list(map(
    lambda sublist: reduce(
        lambda acc, x: acc + (lambda sq: sq if (lambda even_check: even_check(x))(lambda z: z % 2 == 0) else 0)(x ** 2),
        set(sublist), 0
    ),
    lists
))

# Example usage
input_lists = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [2, 2, 2], [5]]
result = cumulative_sum_of_squares(input_lists)
print(result)  # Output: [20, 100, 244, 4, 0]


# Part B-Q4
def cumulative_operation(op):
    def apply_operation(sequence):
        result = sequence[0]
        for element in sequence[1:]:
            result = op(result, element)
        return result

    return apply_operation


# Factorial function: computes the product of numbers from 1 to n
factorial = lambda n: cumulative_operation(lambda x, y: x * y)(range(1, n + 1))

# Exponentiation function: computes base raised to the power of exp
exponentiation = lambda base, exp: cumulative_operation(lambda x, y: x * base)([base] * (exp - 1) + [base])

# Factorial of 5
print(factorial(5))  # Output: 120

# Exponentiation of 2^3
print(exponentiation(3, 4))  # Output: 81

# Part B-Q5

print(reduce(lambda acc, x: acc + x, map(lambda y: y ** 2, filter(lambda num: num % 2 == 0, [1, 2, 3, 4, 5, 6]))))
# Output:56

# Part B-Q6

count_palindromes = lambda lst: list(map(lambda sublist: len(list(filter(lambda s: s == s[::-1], sublist))), lst))

input_list = [["level", "world", "madam"], ["hello", "noon", "abcba"], ["xyz"]]
print(count_palindromes(input_list))  # Output: [2, 2, 0]


# Part B-Q7
# The term Lazy evaluation is the following program work as:
# Generates and processes values one by one, delaying computation until it is necessary
# generate_values() is called, but instead of converting it to a list, it's directly used in the list comprehension.
# The list comprehension [square(x) for x in generate_values()] iterates over the generator lazily
# while the Eager evaluation is generating all values first, then processes them.

def generate_values():
    print('Generating values...')
    yield 1
    yield 2
    yield 3


def square(x):
    print(f'Squaring {x}')
    return x * x


print('Eager evaluation:')
values = list(generate_values())
squared_values = [square(x) for x in values]
print(squared_values)

print('\nLazy evaluation:')
squared_values = [square(x) for x in generate_values()]
print(squared_values)

# Part B-Q8

get_primes_desc = lambda nums: sorted(
    [x for x in nums if x > 1 and all(x % i != 0 for i in range(2, int(x ** 0.5) + 1))],
    reverse=True)

nums = [29, 15, 3, 11, 7, 19, 4, 23]
print(get_primes_desc(nums))  # Output: [29, 23, 19, 11, 7, 3]
