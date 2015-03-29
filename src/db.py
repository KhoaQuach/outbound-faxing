#!/usr/bin/env python
 
"""
db.py - wrapper class to provide all database interaction functions
"""

import MySQLdb as mdb
import sys
import obf_global_vars

__author__      = obf_global_vars.AUTHORS
__copyright__   = obf_global_vars.COPYRIGHT
__credits__     = obf_global_vars.CREDITS
__license__     = obf_global_vars.LICENSE
__version__     = obf_global_vars.VERSION
__maintainer__  = obf_global_vars.MAINTAINER
__email__       = obf_global_vars.EMAIL
__status__      = obf_global_vars.STATUS

class DB:

    def __init__(self, host='localhost', username='fax_user1', password='97531', db='faxes'):
        self._host = str(host)
        self._username = str(username)
        self._password = str(password)
        self._db = str(db)
    
        self._db_conn = mdb.connect(host, username, password, db);

    def execute(self, statement):
        """
            Execute the sql statement and return the affected rows number
        """
        cur = self._db_conn.cursor()
        cur.execute(statement)        
   
        return cur.rowcount

    def execute_select(self, statement):
        """
            Execute the statement and return the result rows
        """
        try:
            cur = self._db_conn.cursor()
            cur.execute(statement)

            rows = cur.fetchall()

            return rows

        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])

        return []

    def execute_sp(self, sp):
        """
            Execute the stored procedure statement 
            and return the result row;
            NOT WORKING: use the execute or execute_select to
            call a stored procedure instead
        """
        try:
            cur = self._db_conn.cursor()
            cur.callproc(sp)
            rows = cur.stored_results()
            for r in rows:
                print(str(r))
  
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            
if __name__ == '__main__':
    """
        Unit tests
    """ 
    conn = DB()
    rows = conn.execute_select("call get_pending_fax();")
    for r in rows:
        print(str(r))
