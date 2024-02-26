def main():
    userinput = input("Expression: ")

    x, operator, y = userinput.split(" ")

    x = int(x)
    y = int(y)

    match operator:
        case "+":
            print(float(x + y))
        case "-":
            print(float(x - y))
        case "*":
            print(float(x * y))
        case "/":
            print(float(x / y))


main()