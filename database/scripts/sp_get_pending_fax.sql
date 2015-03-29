#
# Geting one pending outbound fax request
#
USE faxes;

DELIMITER //

DROP PROCEDURE IF EXISTS get_pending_fax //
CREATE DEFINER = 'fax_user1'@'localhost' PROCEDURE get_pending_fax()
BEGIN
    DECLARE i_outbound_fax_id BIGINT DEFAULT -1;
    DECLARE i_max_attempts, i_num_attempts, i_sleep_time, i_fax_user_id INT;
    DECLARE vc_destination_number VARCHAR(50);
    DECLARE vc_source_number VARCHAR(50);
    DECLARE vc_fax_file VARCHAR(1024);

    START TRANSACTION;

    SELECT outbound_fax_id, destination_number, source_number, max_attempts, num_attempts, sleep_time, fax_file, fax_user_id
    INTO i_outbound_fax_id, vc_destination_number, vc_source_number, i_max_attempts, i_num_attempts, i_sleep_time, vc_fax_file, i_fax_user_id
    FROM faxes.outbound_faxes
    WHERE outbound_fax_status_id = 0
    LIMIT 1
    FOR UPDATE;

    UPDATE faxes.outbound_faxes SET outbound_fax_status_id = 1 WHERE outbound_fax_id = i_outbound_fax_id;
    COMMIT;

    SELECT i_outbound_fax_id AS outbound_fax_id, vc_destination_number AS destination_number, vc_source_number AS source_number, i_max_attempts AS max_attempts, i_num_attempts AS num_attempts, i_sleep_time AS sleep_time, vc_fax_file AS fax_file, i_fax_user_id AS fax_user_id;

END;
//
