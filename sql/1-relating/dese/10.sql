SELECT "name", "expenditures"."per_pupil_expenditure"
FROM "districts"
JOIN "expenditures" ON "expenditures"."district_id" = "districts"."id"
WHERE "type" LIKE 'public school district'
ORDER BY "expenditures"."per_pupil_expenditure" DESC
LIMIT 10