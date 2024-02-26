SELECT "first_name", "last_name"
FROM "players"
WHERE "id" IN (
    SELECT "salaries"."player_id"
    FROM "salaries"
    JOIN "performances" ON "performances"."player_id" = "salaries"."player_id"
    WHERE "performances"."h" > 0
    AND "performances"."year" = 2001
    AND "salaries"."year" = 2001
    GROUP BY "salaries"."player_id"
    ORDER BY ("salaries"."salary" / "performances"."h") ASC
    LIMIT 10
)
AND "id" IN (
    SELECT "salaries"."player_id"
    FROM "salaries"
    JOIN "performances" ON "performances"."player_id" = "salaries"."player_id"
    WHERE "performances"."RBI" > 0
    AND "performances"."year" = 2001
    AND "salaries"."year" = 2001
    GROUP BY "salaries"."player_id"
    ORDER BY ("salaries"."salary" / "performances"."RBI") ASC
    LIMIT 10
)
ORDER BY "id" ASC