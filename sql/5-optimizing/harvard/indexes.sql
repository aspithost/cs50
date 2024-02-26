CREATE INDEX "student_enrollments_index" ON "enrollments" ("student_id", "course_id");


CREATE INDEX "course_enrollments_index" ON "enrollments" ("course_id", "student_id");


CREATE INDEX "course_satisfies_index" ON "satisfies" ("course_id", "requirement_id");


CREATE INDEX "department_index" ON "courses" ("department");


CREATE INDEX "academic_year_index" ON "courses" ("semester")
WHERE "semester" = 'Fall 2023'
OR "semester" = 'Spring 2024';