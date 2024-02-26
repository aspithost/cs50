CREATE TABLE students (
    id INTEGER,
    name TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE houses (
    house TEXT,
    head TEXT,
    PRIMARY KEY(house)
);

CREATE TABLE assignment (
    student_id INTEGER,
    house_name TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(house_name) REFERENCES houses(house)
);