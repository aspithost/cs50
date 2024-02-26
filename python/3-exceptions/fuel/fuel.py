def main():
    while True:
        userinput = input("Fraction: ")
        x, _, y = userinput.partition('/')
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            pass
        else:
            if x >= 0 and y >= 0:
                try:
                    number = round((x / y) * 100)
                except (ValueError, ZeroDivisionError):
                    pass
                else:
                    if number < 2:
                        return print("E")
                    elif number < 99:
                        return print(f"{number}%")
                    elif number <= 100:
                        return print("F")


main()