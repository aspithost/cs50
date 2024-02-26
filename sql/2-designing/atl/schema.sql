-- Passengers
CREATE TABLE IF NOT EXISTS "passengers" (
    "id" INTEGER,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "age" INTEGER NOT NULL,
    PRIMARY KEY("id")
);

-- Airlines
CREATE TABLE IF NOT EXISTS "airlines" (
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id")
);

-- Airports
CREATE TABLE IF NOT EXISTS "airports" (
    "id" INTEGER,
    "code" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id")
);

-- Flights
CREATE TABLE IF NOT EXISTS "flights" (
    "id" INTEGER,
    "number" INTEGER NOT NULL,
    "departure_time" NUMERIC NOT NULL,
    "arrival_time" NUMERIC NOT NULL,
    "airline_id" INTEGER,
    "from_airport_id" INTEGER,
    "to_airport_id" INTEGER,
    PRIMARY KEY("id"),
    FOREIGN KEY("airline_id") REFERENCES "airlines"("id"),
    FOREIGN KEY("from_airport_id") REFERENCES "airports"("id"),
    FOREIGN KEY("to_airport_id") REFERENCES "airports"("id"),
    UNIQUE("number", "departure_time")
);


-- Concourses
CREATE TABLE IF NOT EXISTS "concourses" (
    "airline_id" INTEGER,
    "concourse" TEXT NOT NULL CHECK("concourse" IN ('A', 'B', 'C', 'D', 'E', 'F', 'T')),
    PRIMARY KEY ("concourse", "airline_id"),
    FOREIGN KEY("airline_id") REFERENCES "airlines"("id")
);

-- Check-ins
CREATE TABLE IF NOT EXISTS "checkins" (
    "id" INTEGER,
    "datetime" NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "passenger_id" INTEGER,
    "flight_id" INTEGER,
    PRIMARY KEY("id"),
    FOREIGN KEY("passenger_id") REFERENCES "passengers"("id"),
    FOREIGN KEY("flight_id") REFERENCES "flights"("id")
);