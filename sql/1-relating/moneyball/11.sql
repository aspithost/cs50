SELECT "first_name", "last_name", ("salaries"."salary" / "performances"."h") AS "dollars per hit"
FROM "players"
JOIN "salaries" ON "salaries"."player_id" = "players"."id"
JOIN "performances" ON "performances"."player_id" = "players"."id"
WHERE "performances"."h" > 0
AND "salaries"."year" = 2001
AND "performances"."year" = 2001
GROUP BY "players"."id"
ORDER BY ("salaries"."salary" / "performances"."h") ASC, "first_name" ASC, "last_name" ASC
LIMIT 10