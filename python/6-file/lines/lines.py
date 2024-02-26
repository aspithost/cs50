from sys import argv, exit

def main():
    path = check_path()
    number_of_lines = count_lines(path)
    print(number_of_lines)


def check_path():
    if len(argv) < 2:
        exit("Too few command-line arguments")
    elif len(argv) > 2:
        exit("Too many command-line arguments")
    elif not argv[1].endswith(".py"):
        exit("Not a Python file")
    else:
        return argv[1]


def count_lines(path):
    try:
        with open(path) as file:
            count = 0
            for line in file:
                if is_line(line):
                    count += 1
            return count
    except FileNotFoundError:
        exit("File does not exist")


def is_line(line):
    stripped = line.lstrip()
    if stripped and not stripped.startswith('#'):
        return True
    else:
        return False


main()