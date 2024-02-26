def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    # Check if alphanumeric
    if not s.isalnum():
        return False

    length = len(s)
    if length < 2 or length > 6:
        return False

    # If all characters, return true
    if s.isalpha():
        return True

    # Check first two letters
    first_two = s[0:2]
    if not first_two.isalpha():
        return False

    contains_numbers = False
    for c in s[2:]:
        if not contains_numbers and c.isnumeric():
            if c == "0":
                return False
            contains_numbers = True
        if contains_numbers and c.isalpha():
            return False
    return True


if __name__ == "__main__":
    main()