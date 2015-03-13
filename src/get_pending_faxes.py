"""
get_pending_faxes.py:
    This script is supposed to be scheduled in the cron jobs to launch 
    periodically, in which, it would be query the database for any
    pending jobs, if so, hand the jobs to other script to handle.
"""

from db import DB

conn = DB()
rows = conn.select("select outbound_fax_id, destination_number, \
    source_number, max_attempts, num_attempts, sleep_time, fax_file, \
    fax_timestamp, fax_user_id, outbound_fax_status_id from outbound_faxes")

if 0 < len(rows):
    #
    # Handle requests here
    #
    pass
