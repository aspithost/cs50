from csv import DictReader, DictWriter
from sys import argv, exit


def main():
    infile, outfile = get_path()
    student_list = get_list(infile)
    write_list(outfile, student_list)


def get_path():
    length = len(argv)
    if length < 3:
        exit("Too few command-line arguments")
    elif length > 3:
        exit("Too many command-line arguments")
    elif not argv[1].endswith(".csv"):
        exit("Not a CSV file")
    else:
        return argv[1], argv[2]


def get_list(path):
    students = []
    try:
        with open(path) as file:
            for row in DictReader(file):
                lastname, firstname = row["name"].split(',')
                students.append({ "first": firstname.strip(), "last": lastname, "house": row["house"]})
    except FileNotFoundError:
        exit("File does not exist")
    return students


def write_list(path, list):
    try:
        with open(path, "w") as file:
            writer = DictWriter(file, fieldnames=["first", "last", "house"])
            writer.writeheader()
            for row in list:
                writer.writerow(row)
    except FileNotFoundError:
        exit("File does not exist")


main()