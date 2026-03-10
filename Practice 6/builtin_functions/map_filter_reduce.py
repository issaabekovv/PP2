from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

squared = list(map(lambda x: x ** 2, numbers))
print("Squared numbers using map():", squared)

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers using filter():", even_numbers)

sum_all = reduce(lambda a, b: a + b, numbers)
print("Sum using reduce():", sum_all)

print("Length:", len(numbers))
print("Minimum:", min(numbers))
print("Maximum:", max(numbers))
print("Sum:", sum(numbers))
print("Sorted descending:", sorted(numbers, reverse=True))