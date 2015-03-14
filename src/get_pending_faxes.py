"""
get_pending_faxes.py:
    This script is supposed to be scheduled in the cron jobs to launch 
    periodically, in which, it would be query the database for any
    pending jobs, if so, hand the jobs to other script to handle.
"""

from db import DB
import ob_logger
import ob_handler

conn = DB()
rows = conn.select("select \
    outbound_fax_id, \
    destination_number, \
    source_number, \
    max_attempts, \
    num_attempts, \
    sleep_time, \
    fax_file, \
    fax_user_id \
    from faxes.outbound_faxes  \
    where \
        outbound_fax_status_id = 0")

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
