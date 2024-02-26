from random import randrange


def main():
    level = get_level()
    correct = 0
    for i in range(10):
        first = generate_integer(level)
        second = generate_integer(level)
        answer = first + second
        count = 0
        while True:
            if count < 3:
                try:
                    user_answer = int(input(f"{first} + {second} = "))
                    if user_answer == answer:
                        correct += 1
                        break
                except ValueError:
                    pass
                print("EEE")
                count += 1
            else:
                print(f"{first} + {second} = {answer}")
                break
    print(f"Score: {correct}")


def get_level():
    while True:
        try:
            num = int(input("Level: "))
        except ValueError:
            pass
        else:
            if num >= 1 and num <= 3:
                return num


def generate_integer(level):
    try:
        if level > 1:
            min = pow(10, level - 1)
        else:
            min = 0
        max = pow(10, level)
        return randrange(min, max)
    except ValueError:
        pass


if __name__ == "__main__":
    main()