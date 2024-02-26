SELECT "city", "graduation_rates"."dropped" AS "Dropout percentage"
FROM "schools"
JOIN "graduation_rates" ON "graduation_rates"."school_id" = "schools"."id"
GROUP BY "city"
HAVING "graduation_rates"."dropped" > (
    SELECT AVG("dropped")
    FROM "graduation_rates"
)
ORDER BY "graduation_rates"."dropped" DESC