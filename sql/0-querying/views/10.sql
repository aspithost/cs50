SELECT "artist", "english_title" AS "Brightest pictures with contrast > 0.5"
FROM "views"
WHERE "contrast" > .5
ORDER BY "brightness" DESC
LIMIT 5;