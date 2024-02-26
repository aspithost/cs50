from sys import exit


def main():
    try:
        word = shorten(input("Input: "))
    except ValueError:
        exit(1)
    print(word)
    exit(0)


def shorten(word):
    copy = ""
    for c in word:
        c_copy = c.lower()
        if c_copy != "a" and c_copy != "e" and c_copy != "i" and c_copy != "o" and c_copy != "u":
            copy += c
    return copy


if __name__ == "__main__":
    main()