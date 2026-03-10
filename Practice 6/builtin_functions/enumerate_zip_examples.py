names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]


print("Using enumerate():")
for index, name in enumerate(names, start=1):
    print(index, name)


print("\nUsing zip():")
for name, score in zip(names, scores):
    print(f"{name}: {score}")


value = "123"
print("\nType checking:")
print("Original value:", value, type(value))

converted_value = int(value)
print("Converted to int:", converted_value, type(converted_value))

float_value = float(converted_value)
print("Converted to float:", float_value, type(float_value))

str_value = str(float_value)
print("Converted back to string:", str_value, type(str_value))