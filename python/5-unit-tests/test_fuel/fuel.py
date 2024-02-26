def main():
    while True:
        try:
            percentage = gauge(convert(input("Fraction: ")))
        except (ValueError, ZeroDivisionError):
            continue
        return print(percentage)


def convert(fraction):
    try:
        x, y = fraction.split('/')
    except ValueError:
        raise
    try:
        x = int(x)
        y = int(y)
    except ValueError:
        raise
    if y == 0:
        raise ZeroDivisionError
    elif x < 0 or x > y:
        raise ValueError
    else:
        try:
            return round((x / y) * 100)
        except ValueError:
            raise


def gauge(percentage):
    if percentage < 2:
        return "E"
    elif percentage < 99:
        return str(percentage) + "%"
    elif percentage <= 100:
        return "F"


if __name__ == "__main__":
    main()