def main():
    word = input("Input: ")
    for c in word:
        copy = c.lower()
        if copy != "a" and copy != "e" and copy != "i" and copy != "o" and copy != "u":
            print(c, end="")
    print()

main()