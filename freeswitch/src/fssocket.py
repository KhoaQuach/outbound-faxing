#!/usr/bin/env python
 
"""
fssocket.py - wrapper class to provide all the communication 
to and from Freeswitch
"""

import ESL

class FSSocket:

    def __init__(self, host, port, password):
        self._host = str(host)
        self._port = int(port)
        self._password = str(password)

        self._conn = ESL.ESLconnection(self._host, self._port, self._password)
        
    def connect(self):
        if _conn.connected:
            con.events('plain', 'all')
        while 1:
            e = con.recvEvent()
            if e:
                print e.serialize()

    def connected(self):
        return _conn.connected
