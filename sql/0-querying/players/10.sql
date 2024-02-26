SELECT "first_name", "last_name", ("final_game" - "debut") AS "Seasons Played", "debut"
FROM "players"
ORDER BY ("final_game" - "debut") DESC
LIMIT 10;