DROP DATABASE IF EXISTS faxes;
CREATE DATABASE IF NOT EXISTS faxes;
USE faxes;

#####
# Tables
#####

#
# Outbound faxing accounts
#
CREATE TABLE IF NOT EXISTS `fax_users` (
    `fax_user_id` int unsigned NOT NULL auto_increment,
    `fax_user_name` varchar(128) NOT NULL,
    `fax_user_first_name` varchar(64) NULL,
    `fax_user_last_name` varchar(64) NULL,
    `fax_user_middle_initial` char NULL,
    `fax_user_email` varchar(512) NOT NULL,
    PRIMARY KEY  (`fax_user_id`)
);

INSERT INTO fax_users(fax_user_name, fax_user_first_name, fax_user_last_name, fax_user_middle_initial, fax_user_email)
VALUES ('Fax User1', '', '', '', 'fax1@yahoo.com');

#
# Support file types to upload to send
#
CREATE TABLE IF NOT EXISTS `fax_file_types` (
    `fax_file_type_id` int unsigned NOT NULL auto_increment,
    `fax_file_ext` varchar(4),
    `fax_file_description` varchar(256),
    PRIMARY KEY  (`fax_file_type_id`)
);

INSERT INTO fax_file_types(fax_file_ext, fax_file_description) 
VALUES ('bmp', 'bmp format');
INSERT INTO fax_file_types(fax_file_ext, fax_file_description) 
VALUES('gif', 'gif format');
INSERT INTO fax_file_types(fax_file_ext, fax_file_description) 
VALUES('jpg', 'jpeg format');
INSERT INTO fax_file_types(fax_file_ext, fax_file_description) 
VALUES('jpeg', 'jpeg format');
INSERT INTO fax_file_types(fax_file_ext, fax_file_description) 
VALUES('pdf', 'adobe page description format');
INSERT INTO fax_file_types(fax_file_ext, fax_file_description) 
VALUES('png', 'portable network graphics format');
INSERT INTO fax_file_types(fax_file_ext, fax_file_description) 
VALUES('txt', 'text format');
INSERT INTO fax_file_types(fax_file_ext, fax_file_description) 
VALUES('tif', 'tiff format');
INSERT INTO fax_file_types(fax_file_ext, fax_file_description) 
VALUES('tiff', 'tiff format');

#
# What cover page templates available to users when request to send fax
#
CREATE TABLE IF NOT EXISTS `fax_header_templates` (
    `fax_header_template_id` int unsigned NOT NULL auto_increment,
    `fax_header_template_file_name` varchar(1024) NOT NULL,
    PRIMARY KEY  (`fax_header_template_id`)
);

#
# Fax cover page that associates to each outbound fax requests
#
CREATE TABLE IF NOT EXISTS `outbound_fax_covers` (
    `outbound_fax_cover_id` int unsigned NOT NULL auto_increment,
    `fax_header_template_id` int unsigned NOT NULL REFERENCES fax_header_templates(fax_header_template_id),
    `subject` varchar(128) NULL,
    `from_name` varchar(64) NOT NULL,
    `from_contact_number` varchar(50) NULL,
    `to_name` varchar(64) NOT NULL,
    `to_company_name` varchar(256) NULL,
    `to_contact_number` varchar(50) NULL,
    `to_fax_number` varchar(50) NOT NULL,
    `fax_date` timestamp DEFAULT CURRENT_TIMESTAMP,
    `total_pages` int unsigned DEFAULT 0,
    `note` varchar(1024) NULL,
    PRIMARY KEY  (`outbound_fax_cover_id`)
);

#
# When a file is uploaded, we need to convert and archive in TIFF format,
# this table indicates the conversion status
#
CREATE TABLE IF NOT EXISTS `fax_conversion_status` (
    `fax_conversion_status_id` int unsigned NOT NULL, 
    `fax_conversion_status_description` varchar(64),
    PRIMARY KEY  (`fax_conversion_status_id`)
);

INSERT INTO fax_conversion_status VALUES
(0, 'New'),
(1, 'Success'),
(2, 'Error');

#
# Records when user uploads file to the server for archive
#
CREATE TABLE IF NOT EXISTS `fax_file_repository` (
    `fax_file_repository_id` bigint unsigned NOT NULL auto_increment,
    `fax_orig_file_name` varchar(1024) NOT NULL,
    `fax_conversion_status_id` int unsigned NOT NULL DEFAULT 0 REFERENCES fax_conversion_status(fax_conversion_status_id),
    `fax_user_id` int unsigned NOT NULL REFERENCES fax_users(fax_user_id),
    `fax_file_type_id` int unsigned NOT NULL REFERENCES fax_file_types(fax_file_type_id),
    PRIMARY KEY  (`fax_file_repository_id`)
);

#
# Status when sending out faxes
#
CREATE TABLE IF NOT EXISTS `outbound_fax_status` (
    `outbound_fax_status_id` int unsigned NOT NULL,
    `outbound_fax_status_description` varchar(64)
);

INSERT INTO outbound_fax_status VALUES
(0, 'Pending'),
(1, 'In progress'),
(2, 'Finished');

#
# Records for each outbound fax requests
#
CREATE TABLE IF NOT EXISTS `outbound_faxes` (
    `outbound_fax_id` bigint unsigned NOT NULL auto_increment,
    `destination_number` varchar(50) NOT NULL,
    `source_number` varchar(50) NOT NULL,
    `max_attempts` int unsigned NOT NULL DEFAULT 5,
    `num_attempts` int unsigned NOT NULL DEFAULT 0,
    `sleep_time` int unsigned NOT NULL DEFAULT 60,
    `fax_file` varchar(1024) NOT NULL,
    `fax_timestamp` timestamp DEFAULT CURRENT_TIMESTAMP,
    `fax_user_id` int unsigned NOT NULL REFERENCES fax_users(fax_user_id),
    `outbound_fax_cover_id` int unsigned NULL REFERENCES outbound_fax_covers(outbound_fax_cover_id),
    `outbound_fax_status_id` int unsigned NOT NULL DEFAULT 0 REFERENCES outbound_fax_status(outbound_fax_status_id),
    PRIMARY KEY  (`outbound_fax_id`)
);

#
# Records on each failed/success outbound fax attempt
#
CREATE TABLE IF NOT EXISTS `outbound_fax_attempts` (
    `outbound_fax_attempt_id` bigint unsigned NOT NULL auto_increment,
    `attempt_timestamp` timestamp DEFAULT CURRENT_TIMESTAMP,
    `attempt_result_code` int NOT NULL DEFAULT 0,
    `attempt_result_message` varchar(256) NOT NULL DEFAULT '',
    `outbound_fax_id` int unsigned NOT NULL REFERENCES outbound_faxes(outbound_fax_id),
    PRIMARY KEY (`outbound_fax_attempt_id`) 
);

#####
# Create a database user to use for the service
#####
GRANT ALL ON `faxes`.* TO 'fax_user1'@'localhost' IDENTIFIED BY '97531';

