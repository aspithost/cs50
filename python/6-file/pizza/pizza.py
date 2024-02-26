from csv import reader
from sys import argv, exit
from tabulate import tabulate


def main():
    path = check_path()
    table = format_table(path)
    print(tabulate(table, headers="firstrow", tablefmt="grid"))

def check_path():
    if len(argv) < 2:
        exit("Too few command-line arguments")
    elif len(argv) > 2:
        exit("Too many command-line arguments")
    elif not argv[1].endswith(".csv"):
        exit("Not a CSV file")
    else:
        return argv[1]


def format_table(path):
    table = []
    try:
        with open(path) as file:
            for row in reader(file):
                table.append(row)
    except FileNotFoundError:
        exit("File does not exist")
    return table


main()