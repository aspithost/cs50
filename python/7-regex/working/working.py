import re


def main():
    print(convert(input("Hours: ").strip()))


def convert(s):
    if matches := re.fullmatch(r"(1[0-2]|[1-9])(:[0-5][0-9])?\s(A|P)M\sto\s(1[0-2]|[1-9])(:[0-5][0-9])?\s(A|P)M", s):
        first_num, first_char, second_num, second_char = matches.group(1, 3, 4, 6)
        first = format(int(first_num), first_char)
        second = format(int(second_num), second_char)
        return f"{first} to {second}"
    else:
        raise ValueError


def format(num, char):
    if num == 12:
        num = 0
    if char == 'P':
        num += 12
    return f"{num:02}:00"


if __name__ == "__main__":
    main()