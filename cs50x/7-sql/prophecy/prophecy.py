import csv
from cs50 import SQL


def main():
    db = SQL("sqlite:///roster.db")
    # set_houses(db)
    insert_students(db)


def set_houses(db):
    houses = [
        { "house": "Gryffindor", "head": "Minerva McGonagall" },
        { "house": "Hufflepuff", "head": "Pomona Sprout" },
        { "house": "Ravenclaw", "head": "Filius Flitwick" },
        { "house": "Slytherin", "head": "Severus Snape" },
    ]
    for house in houses:
        db.execute("INSERT INTO houses (house, head) VALUES (?, ?)", house['house'], house['head'])


def insert_students(db):
    with open("students.csv", "r") as file:
        reader = csv.DictReader(file)
        id = 1

        for row in reader:
            # print(row)
            name = row["student_name"]
            house = row["house"]

            db.execute("INSERT INTO students (id, name) VALUES (?, ?)", id, name)
            db.execute("INSERT INTO assignment (student_id, house_name) VALUES(?, ?)", id, house)

            id += 1


if __name__ == "__main__":
    main()