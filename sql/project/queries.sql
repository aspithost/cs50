-- Show a list of players and starting position per game
SELECT
    `lineups`.`match_id`,
    `lineups`.`position`,
    `player_names`.`first_name`,
    `player_names`.`last_name`
FROM `lineups`
JOIN `player_names` ON `player_names`.`team_member_id` = `lineups`.`team_member_id`
ORDER BY `lineups`.`match_id`, `last_name`;


-- What teams has Abel been part of the last two seasons?
SELECT
    `team_members`.`season`,
    `club_and_team`.`club_name`,
    `club_and_team`.`team_number`
FROM `team_members`
JOIN `club_and_team` ON `team_members`.`team_id` = `club_and_team`.`team_id`
WHERE `team_members`.`player_id` = (
    SELECT `id`
    FROM `players`
    WHERE `first_name` LIKE 'Abel'
    AND `last_name` LIKE 'Spithost'
)
AND `team_members`.`season` IN ('22-23', '23-24')
ORDER BY `season` DESC;


-- Check if a club like "Potetos" has a 7th team
SELECT `club_name`, `team_number`
FROM `club_and_team`
WHERE `team_id` = `get_team_id`('potetos', 7);


-- Check if the G.S.F.V. Drs. Vijfjehas a 10th team
SELECT `club_name`, `team_number`
FROM `club_and_team`
WHERE `team_id` = `get_team_id`('vijfje', 10);


-- Find the latest matches played by v.v. Potetos 7
SELECT *
FROM `matches`
WHERE `home_team_id` = `get_team_id`('potetos', 7)
OR `away_team_id` = `get_team_id`('potetos', 7)
AND `status` = 'PLAYED'
ORDER BY `date` DESC;


-- What players scored a goal in the last two seasons?
SELECT
    `match_id`,
    `player_names`.`first_name`,
    `player_names`.`last_name`,
    `type`,
    `half`,
    `minute`
FROM `match_events`
JOIN `player_names` ON `player_names`.`team_member_id` = `match_events`.`primary_team_member_id`
WHERE `type` IN ('goal', 'penalty_goal')
ORDER BY `match_id` DESC;


-- Find the duration of the halves of Potetos games of 22-23 season
SELECT
    `match_id`,
    `half`,
    `end_date`,
    ROUND(
        TIMESTAMPDIFF(
            SECOND,
            `start_date`,
            `end_date`
        ) / 60
    ) AS `half_minutes`
FROM `match_halves`
WHERE `match_id` IN (
    SELECT `id`
    FROM `matches`
    WHERE (
        `matches`.`home_team_id` = `get_team_id`('potetos', 7)
        OR `matches`.`away_team_id` = `get_team_id`('potetos', 7)
    )
    AND `league_id` = `get_season_id`('22-23')
    ORDER BY `date` DESC
);


-- Show the starting lineup for Potetos 7's last game of the 22-23 season
SELECT
    `matches`.`id`,
    `lineups`.`position`,
    `player_names`.`first_name`,
    `player_names`.`last_name`
FROM `matches`
JOIN `lineups` ON `lineups`.`match_id` = `matches`.`id`
JOIN `player_names` ON `player_names`.`team_member_id` = `lineups`.`team_member_id`
WHERE (
    `matches`.`home_team_id` = `get_team_id`('potetos', 7)
    OR `matches`.`away_team_id` = `get_team_id`('potetos', 7)
)
AND `matches`.`id` = (
    SELECT `matches`.`id`
    FROM `matches`
    JOIN `leagues` ON `leagues`.`id` = `matches`.`league_id`
    WHERE `leagues`.`season` = '22-23'
    ORDER BY `matches`.`date` DESC
    LIMIT 1
);


-- What leagues has Potetos 7 played in and is Potetos 7 currently playing in?
SELECT `season`, `name`
FROM `leagues`
WHERE `id` IN (
    SELECT `league_id`
    FROM `matches`
    WHERE `home_team_id` = `get_team_id`('potetos', 7)
    OR `away_team_id` = `get_team_id`('potetos', 7)
);


-- Show the date, league and team id's for all games
SELECT
    `date`,
    `leagues`.`name` AS `league_name`,
    `home_team_id`,
    `away_team_id`
FROM `matches`
JOIN `leagues` ON `leagues`.`id` = `matches`.`league_id`;


-- Where does Potetos play its home games?
SELECT `city`, `country_code`, `street_address`, `postal_code`
FROM `locations`
JOIN `clubs` ON `clubs`.`location_id` = `locations`.`id`
WHERE `clubs`.`name` LIKE '%potetos%';


-- What are Potetos' club colors?
SELECT *
FROM `club_colors`
WHERE `club_id` = (
    SELECT `id`
    FROM `clubs`
    WHERE `name` LIKE '%potetos%'
);


-- Show the clubs and teams for all played and scheduled matches
SELECT
    `matches`.`id` AS `match_id`,
    `matches`.`date`,
    `matches`.`status`,
    `home_team`.`club_name` AS `home_club_name`,
    `home_team`.`team_number` AS `home_team_number`,
    `away_team`.`club_name` AS `away_club_name`,
    `away_team`.`team_number` AS `away_team_number`
FROM `matches`
JOIN `club_and_team` AS `home_team`
    ON `home_team`.`team_id` = `matches`.`home_team_id`
JOIN `club_and_team` AS `away_team`
    ON `away_team`.`team_id` = `matches`.`away_team_id`
ORDER BY `matches`.`date` ASC;


-- Get the scores for all games that Potetos 7 played in
SELECT
    `matches`.`id` AS `match_id`,
    `matches`.`date`,
    `matches`.`status`,
    `home_club`.`name` AS `home_club_name`,
    `home_team`.`number` AS `home_team_number`,
    IFNULL(`home_goals`.`goals`, 0) AS `home_goals`,
    IFNULL(`away_goals`.`goals`, 0) AS `away_goals`,
    `away_club`.`name` AS `away_club_name`,
    `away_team`.`number` AS `away_team_number`
FROM `matches`
JOIN `teams` AS `home_team` ON `home_team`.`id` = `matches`.`home_team_id`
JOIN `teams` AS `away_team` ON `away_team`.`id` = `matches`.`away_team_id`
JOIN `clubs` AS `home_club` ON `home_club`.`id` = `home_team`.`club_id`
JOIN `clubs` AS `away_club` ON `away_club`.`id` = `away_team`.`club_id`
LEFT JOIN (
    SELECT `match_id`, COUNT(*) AS `goals`
    FROM `match_events`
    WHERE `type` IN ('goal', 'penalty_goal')
    AND `team_id` = `get_team_id`('potetos', 7)
    GROUP BY `match_id`
) AS `home_goals` ON `home_goals`.`match_id` = `matches`.`id`
LEFT JOIN (
    SELECT `match_id`, COUNT(*) AS `goals`
    FROM `match_events`
    WHERE `type` IN ('goal', 'penalty_goal')
    AND NOT `team_id` = `get_team_id`('potetos', 7)
    GROUP BY `match_id`
) AS `away_goals` ON `away_goals`.`match_id` = `matches`.`id`
WHERE `get_team_id`('potetos', 7) IN (`matches`.`home_team_id`, `matches`.`away_team_id`)
ORDER BY `date` DESC;


-- Insert players into players table
INSERT INTO `players`
(`first_name`, `last_name`, `date_of_birth`, `position`, `shoots`)
VALUES
    ('Abel', 'Spithost', '1992-08-11', 'D', 'L'),
    ('Marten', 'de Roon', '1991-03-29', 'M', 'R');


-- Update a club's name
UPDATE "clubs"
SET "name" = "v.v.v. Potetos"
WHERE "id" = 1;