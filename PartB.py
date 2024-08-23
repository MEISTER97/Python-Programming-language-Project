from functools import reduce

# Part B-Q1
fib = lambda n: reduce(lambda x, _: x + [x[-1] + x[-2]], range(n - 2), [0, 1])[:n]

# Example usage:
print(fib(10))  # Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Part B-Q2

concat_with_space = lambda lst: reduce(lambda x, y: x + ' ' + y, lst)

# Example usage
lst = ["Hello", "world", "from", "lambda"]
result = concat_with_space(lst)
print(result + "\n")  # Output: "Hello world from lambda"


# Part B-Q3


def cumulative_sum_of_squares(lists):
    return list(map(
        lambda sublist: reduce(
            lambda acc, x: (lambda even_check: even_check(x))(lambda z: z % 2 == 0) and acc + (lambda y: y * y)(
                x) or acc,
            sublist, 0),
        lists))


# Example usage
lists = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]
result = cumulative_sum_of_squares(lists)
print(result)  # Output: [20, 100, 100]


# Part B-Q4


def cumulative_operation(op):
    def apply_operation(sequence):
        result = sequence[0]
        for element in sequence[1:]:
            result = op(result, element)
        return result

    return apply_operation


factorial = lambda n: cumulative_operation(lambda x, y: x * y)(range(1, n + 1))

exponentiation = lambda base, exp: cumulative_operation(lambda x, y: x * y)([base] * exp)

# Factorial of 5
print(factorial(5))  # Output: 120

# Exponentiation of 2^3
print(exponentiation(2, 3))  # Output: 8

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
