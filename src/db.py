#!/usr/bin/env python
 
"""
db.py - wrapper class to provide all database interaction functions
"""

import MySQLdb as mdb
import sys
import ob_global_vars

__author__      = ob_global_vars.AUTHORS
__copyright__   = ob_global_vars.COPYRIGHT
__credits__     = ob_global_vars.CREDITS
__license__     = ob_global_vars.LICENSE
__version__     = ob_global_vars.VERSION
__maintainer__  = ob_global_vars.MAINTAINER
__email__       = ob_global_vars.EMAIL
__status__      = ob_global_vars.STATUS

class DB:

    def __init__(self, host='localhost', username='fax_user1', password='97531', db='faxes'):
        self._host = str(host)
        self._username = str(username)
        self._password = str(password)
        self._db = str(db)
    
        self._db_conn = mdb.connect(host, username, password, db);

    def select(self, statement):
        """
            Execute the statement and return the result rows
        """
        with self._db_conn:
            try:
                cur = self._db_conn.cursor()
                cur.execute(statement)

                rows = cur.fetchall()

                return rows

            except mdb.Error, e:
                print "Error %d: %s" % (e.args[0],e.args[1])

            return []

    def execute(self, statement):
        """
            Execute the sql statement and return the affected rows number
        """
        with self._db_conn:
            cur = self._db_conn.cursor()
        
            cur.execute(statement)        
   
            return cur.rowcount


if __name__ == '__main__':
    """
        Unit tests
    """ 
    conn = DB()
    rows = conn.select("select * from fax_users")
    for r in rows:
        print(str(r))
