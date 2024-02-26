
-- *** The Lost Letter ***

-- Check if the destination address exists in database
SELECT "id"
FROM "addresses"
WHERE "address" LIKE '2 Finnegan Street';

-- Since destination does not exist, get information on packages sent from 900 Sommerville Avenue
SELECT *
FROM "packages"
WHERE "from_address_id" IN (
    SELECT "id"
    FROM "addresses"
    WHERE "address" LIKE '900 Somerville Avenue'
);

-- Anneke sent a package with contents 'congratulatory' letter. Determine whether package was scanned.
SELECT *
FROM "scans"
WHERE "package_id" = (
    SELECT "id"
    FROM "packages"
    WHERE "contents" LIKE 'congratulatory letter'
    AND "from_address_id" = (
        SELECT "id"
        FROM "addresses"
        WHERE "address" LIKE '900 Somerville Avenue'
    )
);

-- Package was sent from Anneke's house and dropped off later that evening. Determine where package was dropped off.
SELECT "address", "type"
FROM "addresses"
WHERE "id" = (
    SELECT "address_id"
    FROM "scans"
    WHERE "action" LIKE "drop"
    AND "package_id" = (
        SELECT "id"
        FROM "packages"
        WHERE "contents" LIKE 'congratulatory letter'
        AND "from_address_id" = (
            SELECT "id"
            FROM "addresses"
            WHERE "address" LIKE '900 Somerville Avenue'
        )
    )
);


-- *** The Devious Delivery ***

-- Check for packages with no from_address_id
SELECT *
FROM "packages"
WHERE "from_address_id" IS NULL;

-- Previous query returned one result with contents 'Duck Debugger' with a to_address_id. Check scans of Duck debugger package
SELECT *
FROM "scans"
WHERE "package_id" = (
    SELECT "id"
    FROM "packages"
    WHERE "from_address_id" IS NULL
)

-- Package was picked up at original destination and later dropped off at another address. Check address type of where package was dropped off
SELECT "type"
FROM "addresses"
WHERE "id" = (
    SELECT "address_id"
    FROM "scans"
    WHERE "action" LIKE 'drop'
    AND "package_id" = (
        SELECT "id"
        FROM "packages"
        WHERE "from_address_id" IS NULL
    )
)
-- Package sent to police station


-- *** The Forgotten Gift ***

-- Determine sent packages from grandfather's address
SELECT *
FROM "packages"
WHERE "from_address_id" = (
    SELECT "id"
    FROM "addresses"
    WHERE "address" LIKE '109 Tileston Street'
);

-- Grandfather sent flowers. Check if package had correct destination
SELECT "address"
FROM "addresses"
WHERE "id" = (
    SELECT "to_address_id"
    FROM "packages"
    WHERE "from_address_id" = (
        SELECT "id"
        FROM "addresses"
        WHERE "address" LIKE '109 Tileston Street'
    )
)
-- Package was addressed to 728 Maple Street

-- Determine what happened to package
SELECT *
FROM "scans"
WHERE "package_id" = (
    SELECT "id"
    FROM "packages"
    WHERE "contents" LIKE 'flowers'
    AND "from_address_id" = (
        SELECT "id"
        FROM "addresses"
        WHERE "address" LIKE '109 Tileston Street'
    )
)

-- Package was dropped off at wrong address and picked up 6 days later by a driver. Determine driver that last picked up package
SELECT "name"
FROM "drivers"
WHERE "id" = (
    SELECT "driver_id"
    FROM "scans"
    WHERE "package_id" = (
        SELECT "id"
        FROM "packages"
        WHERE "contents" LIKE 'flowers'
        AND "from_address_id" = (
            SELECT "id"
            FROM "addresses"
            WHERE "address" LIKE '109 Tileston Street'
        )
    )
    AND "action" LIKE 'pick'
    ORDER BY timestamp DESC
    LIMIT 1
);
