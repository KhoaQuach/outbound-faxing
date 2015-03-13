#!/usr/bin/env python
 
"""
db.py - wrapper class to provide all database interaction functions
"""

class DB:

    def __init__(self, host, port, username, password):
        self._host = str(host)
        self._port = int(port)
        self._username = str(username)
        self._password = str(password)

    def connect(self):
        pass

    def connected(self):
        pass
