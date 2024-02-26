camel_case = input("camelCase: ")

new_string = ""
for c in camel_case:
    if c.isupper():
        new_string += "_" + c.lower()
    else:
        new_string += c


print(new_string)