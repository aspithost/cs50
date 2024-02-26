SELECT "teams"."name", SUM("H") AS "total hits"
FROM "performances"
JOIN "teams" ON "teams"."id" = "team_id"
WHERE "performances"."year" = 2001
GROUP BY "performances"."team_id"
ORDER BY SUM("H") DESC
LIMIT 5