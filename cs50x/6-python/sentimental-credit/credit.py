from cs50 import get_string
from re import fullmatch


def main():
    number = get_string("Number: ")

    # Check for valid length
    if not fullmatch(r"(\d{13}|\d{15,16})", number):
        return print_invalid()

    # Get checksum
    length = len(number)
    checksum = 0
    for i in range(length):
        num = int(number[i])

        if (length - i) % 2 == 0:
            double = num * 2
            if double >= 10:
                checksum += 1
            checksum += double % 10
        else:
            checksum += num

    # If checksum ends with 0
    if checksum % 10:
        return print_invalid()

    number_one = int(number[0])
    number_two = int(number[1])
    # Check VISA
    if length == 13 or length == 16 and number_one == 4:
        print("VISA")

    # Check AMEX
    elif length == 15 and number_one == 3 and (number_two == 4 or number_two == 7):
        print("AMEX")

    # Check Mastercard
    elif length == 16 and number_one == 5 and number_two >= 1 and number_two <= 5:
        print("MASTERCARD")

    else:
        print_invalid()


def print_invalid():
    print("INVALID")


main()