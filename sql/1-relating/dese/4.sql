SELECT "city", COUNT(*)
FROM "schools"
WHERE "type" LIKE 'public school'
GROUP BY "city"
ORDER BY COUNT(*) DESC, "city"
LIMIT 10;