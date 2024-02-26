-- Murder on Jan 15th, 2018 in SQL city

-- Get crime scene report
SELECT description
FROM crime_scene_report
WHERE date = 20180115
AND type = 'murder'
AND city = 'SQL City';


-- Security footage shows that there were 2 witnesses.
-- The first witness lives at the last house on "Northwestern Dr".
-- The second witness, named Annabel, lives somewhere on "Franklin Ave".


-- Get interview of first witness
SELECT transcript
FROM interview
WHERE person_id IN (
    SELECT id
    FROM person
    WHERE address_street_name = 'Northwestern Dr'
    ORDER BY address_number DESC
    LIMIT 1
);


-- I heard a gunshot and then saw a man run out. He had a "Get Fit Now Gym" bag.
-- The membership number on the bag started with "48Z".Only gold members have those bags.
-- The man got into a car with a plate that included "H42W".


-- Get interview of second witness
SELECT transcript
FROM interview
WHERE person_id IN (
    SELECT id
    FROM person
    WHERE address_street_name = 'Franklin Ave'
    AND name LIKE 'Annabel%'
);


-- I saw the murder happen, and I recognized the killer from my gym
-- when I was working out last week on January the 9th.


-- Get list of gym "gold members" whose membership starts with "48Z"
SELECT id, person_id
FROM get_fit_now_member
WHERE membership_status = 'gold'
AND id LIKE '48Z%';


-- Get list of cars whose plates include H42W
SELECT id
FROM drivers_license
WHERE plate_number LIKE '%H42W%';


-- Get list of people who worked out on January 9th
SELECT membership_id
FROM get_fit_now_check_in
WHERE check_in_date = 20180109;


-- Combine queries
SELECT person.name
FROM person
    JOIN get_fit_now_member
    ON person.id = get_fit_now_member.person_id
        WHERE get_fit_now_member.membership_status = 'gold'
        AND get_fit_now_member.id LIKE '48Z%'

        AND license_id IN (
            SELECT id
            FROM drivers_license
            WHERE plate_number LIKE '%H42W%'
        )

        AND get_fit_now_member.id IN (
            SELECT membership_id
            FROM get_fit_now_check_in
            WHERE check_in_date = 20180109
        );
-- Jeremy Bowers is the murderer


-- Congrats, you found the murderer! But wait, there's more...
-- If you think you're up for a challenge, try querying the
-- interview transcript of the murderer to find the real villain
-- behind this crime. If you feel especially confident in your
-- SQL skills, try to complete this final step with no more
-- than 2 queries. Use this same INSERT statement with
-- your new suspect to check your answer.


SELECT transcript
FROM interview
WHERE person_id IN (
    SELECT id
    FROM person
    WHERE name = 'Jeremy Bowers'
);
a

-- I was hired by a woman with a lot of money. I don't know her name
-- but I know she's around 5'5" (65") or 5'7" (67"). She has red hair
-- and she drives a Tesla Model S. I know that she attended the
-- SQL Symphony Concert 3 times in December 2017.


-- Get people with red hair and length of 5'5" - 5'7" who drive a Tesla Model S.
SELECT name
FROM person
WHERE license_id IN (
    SELECT id
    FROM drivers_license
    WHERE height >= 65
    AND height <= 67
    AND hair_color = 'red'
    AND car_make = 'Tesla'
    AND car_model = 'Model S'
)
AND id IN (
    SELECT person_id
    FROM facebook_event_checkin
    WHERE event_name = 'SQL Symphony Concert'
    AND date >= 20171201
    AND date <= 20171231
    GROUP BY person_id
    HAVING COUNT(person_id) = 3
)
-- Woman who hired killer: Mirana Priestly


-- Income of woman who hired killer
SELECT annual_income
FROM income
WHERE ssn IN (
    SELECT ssn
    FROM person
    WHERE license_id IN (
        SELECT id
        FROM drivers_license
        WHERE height >= 65
        AND height <= 67
        AND hair_color = 'red'
        AND car_make = 'Tesla'
        AND car_model = 'Model S'
    )
    AND id IN (
        SELECT person_id
        FROM facebook_event_checkin
        WHERE event_name = 'SQL Symphony Concert'
        AND date >= 20171201
        AND date <= 20171231
        GROUP BY person_id
        HAVING COUNT(person_id) = 3
    )
)
-- 310.000