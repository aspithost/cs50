-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Thief
-- City thief escaped to
-- Accomplice

-- July 28, 2021 and that it took place on Humphrey Street.

-- Ran .schema to inspect all the tables in DB

-- I want to obtain the description from the crime scene report from the crimes on Humphrey Street on July 28th, 2021.
-- In this case, there were two separate crimes (also "littering"), so I just read the description of the stolen CS50 duck.
SELECT description FROM crime_scene_reports
WHERE year = 2021
AND month = 7
AND day = 28
AND street = 'Humphrey Street';
-- Theft of the duck at 10:15am at Humphrey Street bakery. Interviews conducted, all mention bakery.

-- Get all transcripts of police interviews on the day of the crime
SELECT name, transcript
FROM interviews
WHERE year = 2021
AND month = 7
AND day = 28
-- Ruth, Eugene and Raymond's interviews related to the CS50 duck theft based on the transcripts


-- Ruth: Sometime within ten minutes of the theft, I saw the thief get into
-- a car in the bakery parking lot and drive away. If you have security footage
-- from the bakery parking lot, you might want to look for cars that left
-- the parking lot in that time frame.


-- Determine names of people that left the bakery within 10 minutes of 10:15AM on July 28th.
SELECT name
FROM people
    JOIN bakery_security_logs
    ON people.license_plate = bakery_security_logs.license_plate
        WHERE bakery_security_logs.year = 2021
        AND bakery_security_logs.month = 7
        AND bakery_security_logs.day = 28
        AND bakery_security_logs.hour = 10
        AND bakery_security_logs.minute >= 15
        AND bakery_security_logs.minute <= 25
        AND bakery_security_logs.activity = 'exit'
ORDER BY name;
-- Barry, Bruce, Diana, Iman, Kelsey, Luca, Sofia, Vanessa


-- Eugene: I don't know the thief's name, but it was someone I recognized.
-- Earlier this morning, before I arrived at Emma's bakery, I was walking by
-- the ATM on Leggett Street and saw the thief there withdrawing some money.


-- Get names of people who withdrew money from the ATM on Leggett Street on July 28th, 2021
SELECT name
FROM people
    JOIN bank_accounts ON people.id = bank_accounts.person_id
    JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
    WHERE year = 2021
    AND month = 7
    AND DAY = 28
    AND atm_location = 'Leggett Street'
    AND transaction_type = 'withdraw'
ORDER BY name;
-- Benista, Brooke, Bruce, Diana, Iman, Kenny, Luca, Taylor


-- Get names of people who both withdrew money from ATM on Leggett Street on July 28th, 2021
-- AND were seen leaving Emma's bakery between 10:15AM and 10:25AM
SELECT name
FROM people
    JOIN bakery_security_logs
    ON people.license_plate = bakery_security_logs.license_plate

    JOIN bank_accounts
    ON people.id = bank_accounts.person_id

    JOIN atm_transactions
    ON bank_accounts.account_number = atm_transactions.account_number

        WHERE bakery_security_logs.year = 2021
        AND bakery_security_logs.month = 7
        AND bakery_security_logs.day = 28
        AND bakery_security_logs.hour = 10
        AND bakery_security_logs.minute >= 15
        AND bakery_security_logs.minute <= 25
        AND bakery_security_logs.activity = 'exit'

        AND atm_transactions.year = 2021
        AND atm_transactions.month = 7
        AND atm_transactions.day = 28
        AND atm_transactions.atm_location = 'Leggett Street'
        AND atm_transactions.transaction_type = 'withdraw'

ORDER BY name;
-- Bruce, Diana, Iman, Luca


-- Raymond: As the thief was leaving the bakery, they called someone who talked
-- to them for less than a minute. In the call, I heard the thief say that they
-- were planning to take the earliest flight out of Fiftyville tomorrow.
-- The thief then asked the person on the other end of the phone to purchase the flight ticket.


-- See who made a phone call of under a minute on July 28th, 2021
SELECT DISTINCT(name)
FROM people
    JOIN phone_calls ON people.phone_number = phone_calls.caller
    WHERE year = 2021
    AND month = 7
    AND day = 28
    AND duration < 60
ORDER BY name;
-- Benista, Bruce, Carina, Diana, Kelsey, Kenny, Sofia, Taylor


-- Get names of people who both withdrew money from ATM on Leggett Street on July 28th, 2021
-- AND were seen leaving Emma's bakery between 10:15AM and 10:25AM
-- AND made a phone call of < 1 minute on that day
SELECT name
FROM people
    JOIN bank_accounts
    ON people.id = bank_accounts.person_id

    JOIN atm_transactions
    ON bank_accounts.account_number = atm_transactions.account_number

    JOIN bakery_security_logs
    ON people.license_plate = bakery_security_logs.license_plate

    JOIN phone_calls
    ON people.phone_number = phone_calls.caller

        WHERE bakery_security_logs.year = 2021
        AND bakery_security_logs.month = 7
        AND bakery_security_logs.day = 28
        AND bakery_security_logs.hour = 10
        AND bakery_security_logs.minute >= 15
        AND bakery_security_logs.minute <= 25
        AND bakery_security_logs.activity = 'exit'

        AND atm_transactions.year = 2021
        AND atm_transactions.month = 7
        AND atm_transactions.day = 28
        AND atm_transactions.atm_location = 'Leggett Street'
        AND atm_transactions.transaction_type = 'withdraw'

        AND phone_calls.year = 2021
        AND phone_calls.month = 7
        AND phone_calls.day = 28
        AND phone_calls.duration < 60

ORDER BY name;
-- Bruce, Diana


-- Get names of people on first outbound flight from Fiftyville on July 29th, 2021
SELECT name
FROM people
    JOIN passengers
    ON people.passport_number = passengers.passport_number

    JOIN flights
    ON passengers.flight_id = flights.id
        WHERE flights.id IN (
            SELECT flights.id
            FROM flights
                JOIN airports ON airports.id = flights.origin_airport_id
                WHERE airports.city = 'Fiftyville'
                AND year = 2021
                AND month = 7
                AND day = 29
            ORDER BY hour, minute
            LIMIT 1
        )
ORDER BY name;
-- Bruce, Doris, Edward, Kelsey, Kenny, Luca, Sofia, Taylor


-- Get names of people who both withdrew money from ATM on Leggett Street on July 28th, 2021
-- AND were seen leaving Emma's bakery between 10:15AM and 10:25AM
-- AND made a phone call of < 1 minute on that day
-- AND were on the first outbound flight from Fiftyville on July 29th, 2021
SELECT name
FROM people
    JOIN bakery_security_logs
    ON people.license_plate = bakery_security_logs.license_plate

    JOIN bank_accounts
    ON people.id = bank_accounts.person_id

    JOIN atm_transactions
    ON bank_accounts.account_number = atm_transactions.account_number

    JOIN phone_calls
    ON people.phone_number = phone_calls.caller

    JOIN passengers
    ON people.passport_number = passengers.passport_number

    JOIN flights
    ON passengers.flight_id = flights.id

        WHERE bakery_security_logs.year = 2021
        AND bakery_security_logs.month = 7
        AND bakery_security_logs.day = 28
        AND bakery_security_logs.hour = 10
        AND bakery_security_logs.minute >= 15
        AND bakery_security_logs.minute <= 25
        AND bakery_security_logs.activity = 'exit'

        AND atm_transactions.year = 2021
        AND atm_transactions.month = 7
        AND atm_transactions.day = 28
        AND atm_transactions.atm_location = 'Leggett Street'
        AND atm_transactions.transaction_type = 'withdraw'

        AND phone_calls.year = 2021
        AND phone_calls.month = 7
        AND phone_calls.day = 28
        AND phone_calls.duration < 60

        AND flights.id IN (
            SELECT flights.id
            FROM flights
                JOIN airports ON airports.id = flights.origin_airport_id
                WHERE airports.city = 'Fiftyville'
                AND year = 2021
                AND month = 7
                AND day = 29
            ORDER BY hour, minute
            LIMIT 1
        )
-- The thief: Bruce


-- The thief's (Bruce's) accomplish that he called for less than a minute
-- on the date of the crime
SELECT name
FROM PEOPLE
WHERE phone_number IN (
    SELECT receiver
    FROM people
        JOIN phone_calls ON people.phone_number = phone_calls.caller
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND duration < 60
        AND name = 'Bruce'
);
-- The accomplice: Robin


-- Or, using the full query.
SELECT name
FROM PEOPLE
WHERE phone_number in (
    SELECT phone_calls.receiver
    FROM people
        JOIN bakery_security_logs
        ON people.license_plate = bakery_security_logs.license_plate

        JOIN bank_accounts
        ON people.id = bank_accounts.person_id

        JOIN atm_transactions
        ON bank_accounts.account_number = atm_transactions.account_number

        JOIN phone_calls
        ON people.phone_number = phone_calls.caller

        JOIN passengers
        ON people.passport_number = passengers.passport_number

        JOIN flights
        ON passengers.flight_id = flights.id

            WHERE bakery_security_logs.year = 2021
            AND bakery_security_logs.month = 7
            AND bakery_security_logs.day = 28
            AND bakery_security_logs.hour = 10
            AND bakery_security_logs.minute >= 15
            AND bakery_security_logs.minute <= 25
            AND bakery_security_logs.activity = 'exit'

            AND atm_transactions.year = 2021
            AND atm_transactions.month = 7
            AND atm_transactions.day = 28
            AND atm_transactions.atm_location = 'Leggett Street'
            AND atm_transactions.transaction_type = 'withdraw'

            AND phone_calls.year = 2021
            AND phone_calls.month = 7
            AND phone_calls.day = 28
            AND phone_calls.duration < 60

            AND flights.id IN (
                SELECT flights.id
                FROM flights
                    JOIN airports ON airports.id = flights.origin_airport_id
                    WHERE airports.city = 'Fiftyville'
                    AND year = 2021
                    AND month = 7
                    AND day = 29
                ORDER BY hour, minute
                LIMIT 1
            )
);
-- The accomplice: Robin


-- The city the thief (Bruce) escaped to
SELECT city
FROM airports
WHERE id IN (
    SELECT destination_airport_id
    FROM flights
        JOIN airports ON airports.id = flights.origin_airport_id
        WHERE airports.city = 'Fiftyville'
        AND year = 2021
        AND month = 7
        AND day = 29
    ORDER BY hour, minute
    LIMIT 1
);
-- New York City


-- Or, using full SQL query:
SELECT city
FROM airports
WHERE id IN (
    SELECT flights.destination_airport_id
    FROM people
        JOIN bakery_security_logs
        ON people.license_plate = bakery_security_logs.license_plate

        JOIN bank_accounts
        ON people.id = bank_accounts.person_id

        JOIN atm_transactions
        ON bank_accounts.account_number = atm_transactions.account_number

        JOIN phone_calls
        ON people.phone_number = phone_calls.caller

        JOIN passengers
        ON people.passport_number = passengers.passport_number

        JOIN flights
        ON passengers.flight_id = flights.id

            WHERE bakery_security_logs.year = 2021
            AND bakery_security_logs.month = 7
            AND bakery_security_logs.day = 28
            AND bakery_security_logs.hour = 10
            AND bakery_security_logs.minute >= 15
            AND bakery_security_logs.minute <= 25
            AND bakery_security_logs.activity = 'exit'

            AND atm_transactions.year = 2021
            AND atm_transactions.month = 7
            AND atm_transactions.day = 28
            AND atm_transactions.atm_location = 'Leggett Street'
            AND atm_transactions.transaction_type = 'withdraw'

            AND phone_calls.year = 2021
            AND phone_calls.month = 7
            AND phone_calls.day = 28
            AND phone_calls.duration < 60

            AND flights.id IN (
                SELECT flights.id
                FROM flights
                    JOIN airports ON airports.id = flights.origin_airport_id
                    WHERE airports.city = 'Fiftyville'
                    AND year = 2021
                    AND month = 7
                    AND day = 29
                ORDER BY hour, minute
                LIMIT 1
            )
);
-- The destination: New York City