from functools import reduce

# Part B-Q1
fib = lambda n: reduce(lambda x, _: x + [x[-1] + x[-2]], range(n - 2), [0, 1])[:n]

# Example usage:
print(fib(10))  # Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


# Part B-Q2

