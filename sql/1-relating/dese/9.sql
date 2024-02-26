SELECT "name"
FROM "districts"
WHERE "id" IN (
    SELECT "district_id"
    FROM "expenditures"
    WHERE "pupils" IN (
        SELECT MIN("pupils")
        FROM "expenditures"
    )
)
