CREATE TABLE IF NOT EXISTS "players" (
    "id" INTEGER,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "date_of_birth" TEXT NOT NULL,
    -- 'S' stands for staff.
    "position" TEXT NOT NULL CHECK("position" IN ('GK', 'D', 'M', 'F', 'S')),
    "shoots" TEXT NOT NULL CHECK("shoots" IN ('L', 'R', 'E')),
    "profile_picture" NONE,
    "middle_name" TEXT,
    "nickname" TEXT,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "clubs" (
    "id" INTEGER,
    "name" TEXT NOT NULL,
    "logo" NONE,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "teams" (
    "id" INTEGER,
    "club_id" INTEGER NOT NULL,
    "number" INTEGER NOT NULL,
    PRIMARY KEY("id")
    FOREIGN KEY("club_id") REFERENCES "clubs"("id") ON DELETE CASCADE
    CONSTRAINT "unique_team_number" UNIQUE("number", "club_id")
); 

CREATE TABLE IF NOT EXISTS "club_colors" (
    "club_id" INTEGER UNIQUE,
    "shirt_primary" TEXT NOT NULL,
    "shirt_secondary" TEXT NOT NULL,
    "shirt_pattern" TEXT NOT NULL CHECK("shirt_pattern" IN (
        'plain',
        'blocks',
        'horizontal',
        'vertical',
        'bars_horizontal_single',
        'bars_horizontal_multiple',
        'bars_vertical_single',
        'bars_vertical_multiple'
    )),
    "shorts" TEXT NOT NULL,
    "socks" TEXT NOT NULL,
    FOREIGN KEY("club_id") REFERENCES "clubs"("id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "club_details" (
    "club_id" INTEGER UNIQUE,
    "city" TEXT NOT NULL,
    "country" TEXT NOT NULL,
    "street_address" TEXT,
    "postal_code" TEXT,
    "founded" INTEGER,
    FOREIGN KEY("club_id") REFERENCES "clubs"("id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "team_members" (
    "team_id" INTEGER NOT NULL,
    "player_id" INTEGER NOT NULL,
    "season" TEXT NOT NULL CHECK("season" IN ('22-23', '23-24', '24-25')),
    CONSTRAINT "unique_team_member" UNIQUE ("team_id", "player_id", "season")
    FOREIGN KEY("team_id") REFERENCES "teams"("id") ON DELETE CASCADE
    FOREIGN KEY("player_id") REFERENCES "players"("id") ON DELETE CASCADE
);
