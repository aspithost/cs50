import inflect

def main():
    p = inflect.engine()
    names = []
    while True:
        try:
            name = input("Name: ")
            names.append(name)
        except EOFError:
            return print(f"Adieu, adieu, to {p.join(names)}")


main()

# prompt user for names, line by line
# when user uses ctrl-d, print out names
