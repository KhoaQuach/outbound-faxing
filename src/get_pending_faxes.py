"""
get_pending_faxes.py:
    This script is supposed to be scheduled in the cron jobs to launch 
    periodically, in which, it would be query the database for any
    pending jobs, if so, hand the jobs to other script to handle.
"""

from db import DB
import obf_logger
import obf_handler
import obf_global_vars

__author__      = obf_global_vars.AUTHORS
__copyright__   = obf_global_vars.COPYRIGHT
__credits__     = obf_global_vars.CREDITS
__license__     = obf_global_vars.LICENSE
__version__     = obf_global_vars.VERSION
__maintainer__  = obf_global_vars.MAINTAINER
__email__       = obf_global_vars.EMAIL
__status__      = obf_global_vars.STATUS

obf_logger.info("Entering " + __file__)    

db_conn = DB(obf_global_vars.DB_HOST, obf_global_vars.DB_USERNAME, obf_global_vars.DB_PASSWORD, obf_global_vars.DB_NAME)

threads = []

while True:

    # Get one pending request
    rows = db_conn.execute_select("call get_pending_fax();")

    if 0 < len(rows):

        # Get only first row
        row = rows[0]

        # No more requests
        if len(row) == 0 \
            or row[0] is None \
            or int(row[0]) <= 0:
            break

        obf_logger.debug(str(row))

        #
        # Handle requests here
        #

        # Spawn a thread for each request
        try:
            h = obf_handler.OB_Handler(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            threads.append(h)
            h.start()
        except Exception, e:
            obf_logger.error(e.message)
            break

# Wait for all threads to complete
for t in threads:
    t.join()

obf_logger.info("Exiting " + __file__)    
