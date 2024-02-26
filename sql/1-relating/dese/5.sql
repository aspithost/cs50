SELECT "city", COUNT(*)
FROM "schools"
WHERE "type" LIKE 'public school'
GROUP BY "city"
HAVING COUNT(*) <= 3
ORDER BY COUNT(*) DESC, "city"