import datetime
import inflect
from sys import exit


def main():
    print(calc_minutes(datetime.date.today(), get_date(input("Date of Birth: "))))


def get_date(d):
    try:
        return datetime.date.fromisoformat(d)
    except ValueError:
        exit("Invalid date")


def calc_minutes(current_date, dob):
    p = inflect.engine()
    minutes = (current_date - dob).days * 24 * 60
    words = p.number_to_words(minutes, andword='')
    return f"{words} minutes".capitalize()


if __name__ == "__main__":
    main()