import re

# 1
print("1:", bool(re.fullmatch(r'ab*', "abbb")))

# 2
print("2:", bool(re.fullmatch(r'ab{2,3}', "abb")))

# 3
print("3:", re.findall(r'[a-z]+_[a-z]+', "hello_world test_var ABC_def"))

# 4
print("4:", re.findall(r'[A-Z][a-z]+', "Hello World TEST Apple"))

# 5
print("5:", bool(re.fullmatch(r'^a.*b$', "axyzb")))

# 6
print("6:", re.sub(r'[ ,.]', ':', "Hello, world. Python is great"))

# 7
def snake_to_camel(text):
    return re.sub(r'_([a-z])', lambda m: m.group(1).upper(), text)

print("7:", snake_to_camel("my_variable_name"))

# 8
print("8:", re.split(r'(?=[A-Z])', "HelloWorldTest"))

# 9
print("9:", re.sub(r'(?<!^)(?=[A-Z])', ' ', "HelloWorldTest"))

# 10
def camel_to_snake(text):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()

print("10:", camel_to_snake("helloWorldTest"))