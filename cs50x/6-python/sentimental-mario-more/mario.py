from cs50 import get_int


def main():
    while True:
        number = get_int("Height: ")
        if number >= 1 and number <= 8:
            for i in range(number):
                i += 1
                print(" " * (number - i), print_hash(i), "  ", print_hash(i), sep="")
            return


def print_hash(i):
    return "#" * i


main()