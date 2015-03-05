
DROP DATABASE IF EXISTS faxes;
CREATE DATABASE IF NOT EXISTS faxes;
USE faxes;

CREATE TABLE IF NOT EXISTS `fax_users` (
    `fax_user_id` int unsigned NOT NULL auto_increment,
    `fax_user_name` varchar(128) NOT NULL,
    `fax_user_first_name` varchar(64) NULL,
    `fax_user_last_name` varchar(64) NULL,
    `fax_user_middle_initial` char NULL,
    PRIMARY KEY  (`user_id`)
);

CREATE TABLE IF NOT EXISTS `fax_file_types` (
    `fax_file_type_id` int unsigned NOT NULL auto_increment,
    `fax_file_ext` varchar(4)
    PRIMARY KEY  (`fax_file_type_id`)
);

CREATE TABLE IF NOT EXISTS `fax_header_templates` (
    `fax_header_template_id` int unsigned NOT NULL auto_increment,
    `fax_header_template_file_name` varchar(1024) NOT NULL,
    PRIMARY KEY  (`fax_header_template_id`)
);

CREATE TABLE IF NOT EXISTS `fax_conversion_status` (
    `fax_conversion_status_id` int unsigned NOT NULL auto_increment,
    `fax_conversion_status_description` varchar(64),
    PRIMARY KEY  (`fax_conversion_status_id`)
);

INSERT INTO fax_conversion_status VALUES
(0, 'New'),
(1, 'Success'),
(2, 'Error');

CREATE TABLE IF NOT EXISTS `fax_file_repository` (
    `fax_file_repository_id` int unsigned NOT NULL auto_increment,
    `fax_file_name` varchar(1024) NOT NULL,
    `destination_number` varchar(50) NOT NULL,
    `source_number` varchar(50) NOT NULL,
    `fax_header_template_id` int unsigned NOT NULL REFERENCES fax_header_templates(fax_header_template_id),
    `fax_conversion_status_id` int unsigned NOT NULL REFERENCES fax_conversion_status(fax_conversion_status_id),
    `user_id` int unsigned NOT NULL REFERENCES users(user_id),
    `fax_file_type_id` int unsigned NOT NULL REFERENCES fax_file_types(fax_file_type_id),
    PRIMARY KEY  (`fax_file_repository_id`)
)

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
    `fax_file` varchar(1024) NOT NULL,
    `fax_timestamp` timestamp DEFAULT CURRENT_TIMESTAMP,
    `user_id` int unsigned NOT NULL REFERENCES users(user_id),
    `outbound_fax_status_id` int unsigned NOT NULL REFERENCES outbound_fax_status(outbound_fax_status_id),
    PRIMARY KEY  (`outbound_fax_id`)
);

CREATE TABLE IF NOT EXISTS `outbound_fax_attempts` (
    `outbound_fax_attempt_id` int unsigned NOT NULL auto_increment,
    `attempt_timestamp` timestamp DEFAULT CURRENT_TIMESTAMP,
    `attempt_result_code` int NOT NULL DEFAULT 0,
    `attempt_result_message` varchar(256) NOT NULL DEFAULT '',
    `outbound_fax_id` int unsigned NOT NULL REFERENCES outbound_faxes(outbound_fax_id),
    PRIMARY KEY (`outbound_fax_attempt_id`) 
);
