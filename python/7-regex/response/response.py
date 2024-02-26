from validators import email


def main():
    print(check_email(input("What's your email address? ")))


def check_email(s):
    if email(s):
        return "Valid"
    else:
        return "Invalid"


if __name__ == "__main__":
    main()