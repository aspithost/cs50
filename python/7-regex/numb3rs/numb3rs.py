import re
import sys


def main():
    print(validate(input("IPv4 Address: ")))


def validate(ip):
    numbers = ip.split('.')
    if len(numbers) != 4:
        return False
    for number in numbers:
        if not re.search(r"^(25[0-5]|(2[0-4]|1\d|[1-9]|)\d)$", number):
            return False

    return True


if __name__ == "__main__":
    main()