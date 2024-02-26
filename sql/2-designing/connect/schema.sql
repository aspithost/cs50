-- Users
CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "username" TEXT NOT NULL,
    "password_hash" TEXT NOT NULL,
    PRIMARY KEY ("id")
);

-- Schools
CREATE TABLE IF NOT EXISTS "schools" (
    "id" INTEGER,
    "name" TEXT NOT NULL,
    "type" TEXT NOT NULL,
    "location" TEXT NOT NULL,
    "founding_year" INTEGER NOT NULL,
    PRIMARY KEY ("id")
);

-- Companies
CREATE TABLE IF NOT EXISTS "companies" (
    "id" INTEGER,
    "name" TEXT NOT NULL,
    "industry" TEXT NOT NULL,
    "location" TEXT NOT NULL,
    PRIMARY KEY ("id")
);

-- User Connections
CREATE TABLE IF NOT EXISTS "user_connections" (
    "user_id_one" INTEGER,
    "user_id_two" INTEGER,
    FOREIGN KEY("user_id_one") REFERENCES "users"("id"),
    FOREIGN KEY("user_id_two") REFERENCES "users"("id")
);

-- School connections
CREATE TABLE IF NOT EXISTS "school_connections" (
    "affiliation_start_date" NUMERIC NOT NULL,
    "affiliation_end_date" NUMERIC,
    "degree_type" TEXT NOT NULL,
    "user_id" INTEGER,
    "school_id" INTEGER,
    FOREIGN KEY("user_id") REFERENCES "users"("id"),
    FOREIGN KEY("school_id") REFERENCES "schools"("id")
);

-- Company connections
CREATE TABLE IF NOT EXISTS "company_connections" (
    "affiliation_start_date" NUMERIC NOT NULL,
    "affiliation_end_date" NUMERIC,
    "title" TEXT NOT NULL,
    "user_id" INTEGER,
    "company_id" INTEGER,
    FOREIGN KEY("user_id") REFERENCES "users"("id"),
    FOREIGN KEY("company_id") REFERENCES "companies"("id")
)