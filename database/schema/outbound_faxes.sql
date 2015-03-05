
CREATE DATABASE IF NOT EXISTS faxes;
USE faxes;

CREATE TABLE IF NOT EXISTS `users` (
    `user_id` int unsigned NOT NULL auto_increment,
    `user_name` varchar(128) NOT NULL,
    `first_name` varchar(64) NULL,
    `last_name` varchar(64) NULL,
    `first_initial` char NULL,
    PRIMARY KEY  (`user_id`)
);

CREATE TABLE IF NOT EXISTS `outbound_fax_status` (
    `outbound_fax_status_id` int unsigned NOT NULL,
    `outbound_fax_status_description` varchar(64)
);

INSERT INTO outbound_fax_status VALUES
(0, 'Pending'),
(1, 'In progress'),
(2, 'Finished');

CREATE TABLE IF NOT EXISTS `outbound_faxes` (
    `outbound_fax_id` int unsigned NOT NULL auto_increment,
    `destination_number` varchar(50) NOT NULL,
    `source_number` varchar(50) NOT NULL,
    `max_attempts` int NOT NULL DEFAULT 5,
    `num_attempts` int NOT NULL DEFAULT 0,
    `sleep_time` int NOT NULL DEFAULT 60,
    `user_id` int unsigned NOT NULL REFERENCES users(user_id),
    `outbound_fax_status_id` int unsigned NOT NULL REFERENCES outbound_fax_status(outbound_fax_status_id),
    PRIMARY KEY  (`outbound_fax_id`)
);

CREATE TABLE IF NOT EXISTS `outbound_fax_attempts` (
    `outbound_fax_attempt_id` int unsigned NOT NULL auto_increment,
    `outbound_fax_id` int unsigned NOT NULL REFERENCES outbound_faxes(outbound_fax_id),
    PRIMARY KEY (`outbound_fax_attempt_id`) 
);
