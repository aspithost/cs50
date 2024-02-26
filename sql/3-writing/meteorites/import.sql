-- cat import.sql | sqlite3 meteorites.db

CREATE TABLE IF NOT EXISTS "temp" (
    "name" TEXT,
    "id" INTEGER,
    "nametype" TEXT,
    "class" TEXT,
    "mass" REAL,
    "discovery" INTEGER,
    "year" INTEGER,
    "lat" REAL,
    "long" REAL
);

.import --csv --skip 1 meteorites.csv temp

-- All meteorites with the nametype “Relict” are not included in the meteorites table.
DELETE FROM "temp"
WHERE "nametype" LIKE 'relict';

-- Any empty values in meteorites.csv are represented by NULL in the meteorites table.
-- Keep in mind that the mass, year, lat, and long columns have empty values in the CSV.
UPDATE "temp"
SET "mass" = NULL
WHERE "mass" = '';

UPDATE "temp"
SET "year" = NULL
WHERE "year" = '';

UPDATE "temp"
SET "lat" = NULL
WHERE "lat" = '';

UPDATE "temp"
SET "long" = NULL
WHERE "long" = '';

CREATE TABLE IF NOT EXISTS "meteorites" (
    "id" INTEGER,
    "name" TEXT,
    "class" TEXT,
    "mass" REAL,
    "discovery" INTEGER,
    "year" INTEGER,
    "lat" REAL,
    "long" REAL,
    PRIMARY KEY("id")
);

-- All columns with decimal values (e.g., 70.4777) should be rounded to the nearest hundredths place (e.g., 70.4777 becomes 70.48).
-- Keep in mind that the mass, lat, and long columns have decimal values.
INSERT INTO "meteorites" ("name", "class", "mass", "discovery", "year", "lat", "long")
SELECT "name", "class", ROUND("mass", 2), "discovery", "year", ROUND("lat", 2), ROUND("long", 2) FROM "temp"
-- The meteorites are sorted by year, oldest to newest, and then—if any two meteorites landed in the same year—by name, in alphabetical order.
-- You’ve updated the IDs of the meteorites from meteorites.csv, according to the order specified in #4
ORDER BY "year" ASC, "name" ASC;;

DROP TABLE "temp";