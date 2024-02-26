def main():
    while True:
        userinput = input("Date: ")
        if '/' in userinput:
            try:
                month, day, year = userinput.split('/')
            except ValueError:
                pass
            else:
                try:
                    month = int(month)
                    day = int(day)
                    year = int(year)
                except ValueError:
                    pass
                else:
                    if month >= 1 and month <= 12 and day >= 1 and day <= 31:
                        print_date(year, month, day)
                        break

        else:
            try:
                month_and_day, year = userinput.split(',')
                month, day = month_and_day.split()
            except ValueError:
                pass
            else:
                try:
                    day = int(day)
                    month = months.index(month) + 1
                    year = int(year)
                except ValueError:
                    pass
                else:
                    if month >= 1 and month <= 12 and day >= 1 and day <= 31:
                        print_date(year, month, day)
                        break


def print_date(year, month, day):
    return print(f"{year}-{month:02}-{day:02}")


months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]


main()
