-- Users
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT,
    `first_name` VARCHAR(32) NOT NULL,
    `last_name` VARCHAR(32) NOT NULL,
    `username` VARCHAR(16) NOT NULL,
    `password_hash` CHAR(128) NOT NULL,
    PRIMARY KEY (`id`)
);

-- Schools
CREATE TABLE IF NOT EXISTS `schools` (
    `id` INT AUTO_INCREMENT,
    `name` VARCHAR(32) NOT NULL,
    `type` ENUM('Primary', 'Secondary', 'Higher Education') NOT NULL,
    `location` VARCHAR(64) NOT NULL,
    `founding_year` SMALLINT UNSIGNED NOT NULL,
    PRIMARY KEY (`id`)
);

-- Companies
CREATE TABLE IF NOT EXISTS `companies` (
    `id` INT AUTO_INCREMENT,
    `name` VARCHAR(32) NOT NULL,
    `industry` ENUM('Technology', 'Education', 'Business') NOT NULL,
    `location` VARCHAR(64) NOT NULL,
    PRIMARY KEY (`id`)
);

-- User Connections
CREATE TABLE IF NOT EXISTS `user_connections` (
    `user_id_one` INT,
    `user_id_two` INT,
    CONSTRAINT `unique_connection` UNIQUE (`user_id_one`, `user_id_two`),
    FOREIGN KEY(`user_id_one`) REFERENCES `users`(`id`),
    FOREIGN KEY(`user_id_two`) REFERENCES `users`(`id`)
);

-- School connections
CREATE TABLE IF NOT EXISTS `school_connections` (
    `affiliation_start_date` DATE NOT NULL,
    `affiliation_end_date` DATE,
    `degree_type` VARCHAR(32) NOT NULL,
    `user_id` INT,
    `school_id` INT,
    FOREIGN KEY(`user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY(`school_id`) REFERENCES `schools`(`id`)
);

-- Company connections
CREATE TABLE IF NOT EXISTS `company_connections` (
    `affiliation_start_date` DATE NOT NULL,
    `affiliation_end_date` DATE,
    `user_id` INT,
    `company_id` INT,
    FOREIGN KEY(`user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY(`company_id`) REFERENCES `companies`(`id`)
);
