SELECT COUNT(*)
FROM "players"
WHERE ("bats" LIKE "r" AND "throws" LIKE "l") OR ("bats" LIKE "l" AND "throws" LIKE "r")