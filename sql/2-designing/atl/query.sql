-- INSERT INTO "passengers" ("first_name", "last_name", "age")
-- VALUES ('Amelia', 'Earhart', 39)

-- INSERT INTO "airlines" ("name")
-- VALUES ('Delta')

-- INSERT INTO "concourses" ("concourse", "airline_id")
-- SELECT 'T' AS "concourse", "id" AS "airline_id"
-- FROM "airlines"
-- WHERE "name" LIKE 'Delta'

-- CREATE TABLE IF NOT EXISTS "concourses_new" (
--     "airline_id" INTEGER,
--     "concourse" TEXT NOT NULL CHECK("concourse" IN ('A', 'B', 'C', 'D', 'E', 'F', 'T')),
--     PRIMARY KEY ("concourse", "airline_id"),
--     FOREIGN KEY("airline_id") REFERENCES "airlines"("id")
-- );

-- INSERT INTO "concourses_new"("airline_id", "concourse")
-- SELECT "airline_id", "concourse"
-- FROM "concourses"

-- DROP TABLE "concourses"

-- ALTER TABLE "concourses_new" RENAME TO "concourses"

-- INSERT INTO "airports" ("code")
-- VALUES
-- ("ATL"),
-- ("BOS")

-- INSERT INTO "flights" ("number", "departure_time", "arrival_time", "airline_id", "from_airport_id", "to_airport_id")
-- VALUES ('300', '2023-08-03-18:46', '2023-08-03-21:09',
--     (SELECT "id" FROM "airlines" WHERE "name" LIKE 'delta'),
--     (SELECT "id" FROM "airports" WHERE "code" LIKE 'ATL'),
--     (SELECT "id" FROM "airports" WHERE "code" LIKE 'BOS'))

-- INSERT INTO "checkins" ("datetime", "passenger_id", "flight_id")
-- VALUES ('2023-08-03 15:03',
--     (
--         SELECT "id"
--         FROM "passengers"
--         WHERE "first_name" LIKE 'Amelia'
--         AND "last_name" LIKE 'Earhart'
--     ),
--     (
--         SELECT "id"
--         FROM "flights"
--         WHERE "number" LIKE '300'
--         AND "airline_id" = (
--             SELECT "id"
--             FROM "airlines"
--             WHERE "name" LIKE 'delta'
--         )
--         AND "departure_time" LIKE '2023-08-%'
--     )
-- )