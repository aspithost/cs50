CREATE DATABASE IF NOT EXISTS `footballdb`;
USE `footballdb`;

-- Tables
CREATE TABLE IF NOT EXISTS `players` (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `first_name` VARCHAR(32) NOT NULL,
    `last_name` VARCHAR(32) NOT NULL,
    `middle_name` VARCHAR(32),
    `date_of_birth` DATE NOT NULL,
    `position` ENUM('GK', 'D', 'M', 'F', 'S'),
    `shoots` ENUM('L', 'R', 'E') NOT NULL,
    `profile_picture` BLOB,
    PRIMARY KEY(`id`)
);

CREATE TABLE IF NOT EXISTS `locations` (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `city` VARCHAR(32) NOT NULL,
    `country_code` CHAR(32) NOT NULL,
    `street_address` VARCHAR(32),
    `postal_code` VARCHAR(32),
    PRIMARY KEY(`id`)
);

CREATE TABLE IF NOT EXISTS `clubs` (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `location_id` INT UNSIGNED,
    `name` VARCHAR(32) NOT NULL,
    `founding_year` SMALLINT UNSIGNED,
    `logo` BLOB,
    PRIMARY KEY(`id`),
    FOREIGN KEY(`location_id`) REFERENCES `locations`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `club_colors` (
    `club_id` INT UNSIGNED,
    `shirt_primary` ENUM('black', 'brown', 'gray', 'silver', 'white', 'green', 'yellow', 'gold', 'orange', 'red', 'maroon', 'pink', 'purple', 'navy', 'blue', 'turquoise') NOT NULL,
    `shirt_secondary` ENUM('black', 'brown', 'gray', 'silver', 'white', 'green', 'yellow', 'gold', 'orange', 'red', 'maroon', 'pink', 'purple', 'navy', 'blue', 'turquoise'),
    `shirt_pattern` ENUM( 'plain', 'blocks', 'horizontal', 'vertical', 'bars_horizontal_single', 'bars_horizontal_multiple', 'bars_vertical_single', 'bars_vertical_multiple') NOT NULL,
    `shorts` ENUM('black', 'brown', 'gray', 'silver', 'white', 'green', 'yellow', 'gold', 'orange', 'red', 'maroon', 'pink', 'purple', 'navy', 'blue', 'turquoise') NOT NULL,
    `socks` ENUM('black', 'brown', 'gray', 'silver', 'white', 'green', 'yellow', 'gold', 'orange', 'red', 'maroon', 'pink', 'purple', 'navy', 'blue', 'turquoise') NOT NULL,
    FOREIGN KEY(`club_id`) REFERENCES `clubs`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `teams` (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `club_id` INT UNSIGNED,
    `number` TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY(`id`),
    FOREIGN KEY(`club_id`) REFERENCES `clubs`(`id`) ON DELETE CASCADE,
    CONSTRAINT `unique_team_number` UNIQUE(`number`, `club_id`)
);

CREATE TABLE IF NOT EXISTS `team_members` (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `team_id` INT UNSIGNED,
    `player_id` INT UNSIGNED,
    `season` ENUM('22-23', '23-24', '24-25') NOT NULL,
    `jersey_number` TINYINT UNSIGNED CHECK(`jersey_number` >= 0 AND `jersey_number` < 100),
    `nickname` VARCHAR(32),
    CONSTRAINT `unique_team_member` UNIQUE (`team_id`, `player_id`, `season`),
    PRIMARY KEY(`id`),
    FOREIGN KEY(`team_id`) REFERENCES `teams`(`id`) ON DELETE CASCADE,
    FOREIGN KEY(`player_id`) REFERENCES `players`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `leagues`(
    `id` INT UNSIGNED AUTO_INCREMENT,
    `name` VARCHAR(64) NOT NULL,
    `season` ENUM('22-23', '23-24', '24-25') NOT NULL,
    `type` ENUM('LEAGUE', 'CUP', 'FRIENDLY') NOT NULL,
    PRIMARY KEY(`id`)
);

CREATE TABLE IF NOT EXISTS `matches` (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `home_team_id` INT UNSIGNED,
    `away_team_id` INT UNSIGNED,
    `league_id` INT UNSIGNED,
    `location_id` INT UNSIGNED,
    `status` ENUM(
        'TO_BE_PLAYED',
        'IN_PROGRESS',
        'PLAYED',
        'CANCELLED',
        'POSTPONED',
        'STOPPED'
    ) DEFAULT 'TO_BE_PLAYED',
    `date` TIMESTAMP NOT NULL,
    PRIMARY KEY(`id`),
    FOREIGN KEY(`home_team_id`) REFERENCES `teams`(`id`) ON DELETE CASCADE,
    FOREIGN KEY(`away_team_id`) REFERENCES `teams`(`id`) ON DELETE CASCADE,
    FOREIGN KEY(`league_id`) REFERENCES `leagues`(`id`) ON DELETE CASCADE,
    FOREIGN KEY(`location_id`) REFERENCES `locations`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `match_halves` (
    `match_id` INT UNSIGNED,
    `half` ENUM(
        '1',
        '2',
        '3',
        '4',
        '5'
    ) NOT NULL,
    `start_date` TIMESTAMP NOT NULL,
    `end_date` TIMESTAMP,
    FOREIGN KEY(`match_id`) REFERENCES `matches`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `match_events` (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `match_id` INT UNSIGNED,
    `team_id` INT UNSIGNED,
    `primary_team_member_id` INT UNSIGNED,
    `secondary_team_member_id` INT UNSIGNED NULL,
    `type` ENUM(
        'GOAL',
        'PENALTY_GOAL',
        'PENALTY_SAVE',
        'PENALTY_MISS',
        'OWN_GOAL',
        'YELLOW_CARD',
        'RED_CARD',
        'SUBSTITUTION',
        'SUBSTITUTION INJURY'
    ) NOT NULL,
    `half` ENUM('1', '2', '3', '4', '5'),
    `minute` TINYINT UNSIGNED,
    PRIMARY KEY(`id`),
    FOREIGN KEY(`match_id`) REFERENCES `matches`(`id`) ON DELETE CASCADE,
    FOREIGN KEY(`primary_team_member_id`) REFERENCES `team_members`(`id`) ON DELETE CASCADE,
    FOREIGN KEY(`secondary_team_member_id`) REFERENCES `team_members`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `lineups` (
    `match_id` INT UNSIGNED,
    `team_id` INT UNSIGNED,
    `team_member_id` INT UNSIGNED,
    `position` ENUM(
        'STAFF',
        'BENCH',
        'SUSPENDED',
        'INJURED',
        'GK',
        'DL', 'DCL', 'DC', 'DCR', 'DR',
        'WBL','DML', 'DM', 'DMR', 'WBR',
        'ML', 'MCL', 'MC', 'MCR', 'MR',
        'AML', 'AMCL', 'AMC', 'AMCR', 'AMR',
        'STL', 'ST', 'STR'
    ) NOT NULL,
    CONSTRAINT `lineups_player` UNIQUE (`match_id`, `team_member_id`),
    FOREIGN KEY(`match_id`) REFERENCES `matches`(`id`) ON DELETE CASCADE,
    FOREIGN KEY(`team_id`) REFERENCES `teams`(`id`) ON DELETE CASCADE,
    FOREIGN KEY(`team_member_id`) REFERENCES `team_members`(`id`) ON DELETE CASCADE
);


-- Indexes
CREATE INDEX `leagues_season` ON `leagues` (`season`);

CREATE INDEX `matches_status` ON `matches` (`status`);

CREATE INDEX `match_events_type` ON `match_events`(`type`);


-- Views
CREATE VIEW `club_and_team` AS
SELECT
    `teams`.`id` AS `team_id`,
    `clubs`.`name` AS `club_name`,
    `teams`.`number` AS `team_number`
FROM `teams`
JOIN `clubs` ON `clubs`.`id` = `teams`.`club_id`;

CREATE VIEW `player_names` AS
SELECT
    `team_members`.`id` AS `team_member_id`,
    `first_name`,
    `last_name`
FROM `players`
JOIN `team_members` ON `team_members`.`player_id` = `players`.`id`;


-- Functions
DELIMITER //
CREATE FUNCTION `get_team_id`(
    `club_name` VARCHAR(32),
    `team_number` TINYINT UNSIGNED
)
RETURNS INT UNSIGNED
READS SQL DATA
BEGIN
    DECLARE `team_id` INT UNSIGNED;

    SELECT `id` INTO `team_id`
    FROM `teams`
    WHERE `number` = `team_number`
    AND (
        SELECT `id`
        FROM `clubs`
        WHERE `name` LIKE CONCAT('%', `club_name`, '%')
    );

    RETURN `team_id`;
END //
DELIMITER ;