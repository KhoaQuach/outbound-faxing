"""
get_pending_faxes.py:
    This script is supposed to be scheduled in the cron jobs to launch 
    periodically, in which, it would be query the database for any
    pending jobs, if so, hand the jobs to other script to handle.
"""

from db import DB
import ob_logger
import ob_handler
import ob_global_vars

__author__      = ob_global_vars.AUTHORS
__copyright__   = ob_global_vars.COPYRIGHT
__credits__     = ob_global_vars.CREDITS
__license__     = ob_global_vars.LICENSE
__version__     = ob_global_vars.VERSION
__maintainer__  = ob_global_vars.MAINTAINER
__email__       = ob_global_vars.EMAIL
__status__      = ob_global_vars.STATUS

db_conn = DB(ob_global_vars.DB_HOST, ob_global_vars.DB_USERNAME, ob_global_vars.DB_PASSWORD, ob_global_vars.DB_NAME)

# Get the list of pending requests
rows = db_conn.select("START TRANSACTION; \
    SELECT \
    outbound_fax_id, \
    destination_number, \
    source_number, \
    max_attempts, \
    num_attempts, \
    sleep_time, \
    fax_file, \
    fax_user_id \
    FROM faxes.outbound_faxes \
    WHERE \
        outbound_fax_status_id = 0 FOR UPDATE;")

# Change those request to in progress status
db_conn.execute("UPDATE faxes.outbound_faxes SET faxes.outbound_fax_status_id = 1 WHERE faxes.outbound_fax_status_id = 0; COMMIT;")

if 0 < len(rows):
    ob_logger.info("Entering " + __file__)    

    #
    # Handle requests here
    #
    threads = []
    for r in rows:
        ob_logger.debug(str(r))

        # Spawn a thread for each request
        h = ob_handler.OB_Handler(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7])
        threads.append(h)
        h.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()

    ob_logger.info("Exiting " + __file__)    
