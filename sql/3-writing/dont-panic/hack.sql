-- Create fake user_log entry
INSERT INTO "user_logs" ("type", "old_username", "new_username", "old_password", "new_password")
SELECT 'update', 'admin', 'admin', (
    SELECT "password"
    FROM "users"
    WHERE "username" LIKE 'admin'
),
(
    SELECT "password"
    FROM "users"
    WHERE "username" LIKE 'emily33'
);

-- set password of admin to hash of 'oops!'
UPDATE "users"
SET "password" = '982c0381c279d139fd221fce974916e7'
WHERE "username" LIKE 'admin';

-- erase logs
DELETE FROM "user_logs"
WHERE "type" LIKE 'update'
AND "old_username" LIKE 'admin'
AND "new_password" = '982c0381c279d139fd221fce974916e7';