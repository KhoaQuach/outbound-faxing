#!/usr/bin/env python
 
"""
fssocket.py:
    Wrapper class to provide all the communication to and from Freeswitch; 
    this is used only for inbound socket which basically means the inbound 
    connection socket to Freeswitch server does not associate with any 
    call session.
"""

import ESL

class FSSocket:

    def __init__(self, host='127.0.0.1', port=8021, password='ClueCon'):
        self._host = str(host)
        self._port = int(port)
        self._password = str(password)

        self._conn = ESL.ESLconnection(self._host, self._port, self._password)
        
    def connected(self):
        """
            This function returns the connection status to Freeswitch server 
        """
        return self._conn.connected()

    def disconnect(self):
        """
            Disconnect from Freeswitch
        """
        self._conn.disconnect()

    def sendApiCommand(self, api_command):
        """
            Send an API command to Freeswitch.
            Return a ESLEvent object upon success.  
            This function will block the script execution upon returned.
        """
        return self._conn.api(api_command)

    def sendBgApiCommand(self, api_command, command_arguments='', uuid=''):
        """
            Send an API command to Freeswitch.
            This function will return right away with empty ESLEvent and the 
            api command will continue executing in the background in 
            Freeswitch.
        """
        if str(uuid) == '':
            return self._conn.bgapi(api_command, command_arguments)
        else:
            return self._conn.bgapi(api_command, command_arguments, uuid)

    def sendDialPlanCommand(self, dialplan_command, command_arguments, \
        uuid, aSync=False):
        """
            Send a dialplan command to Freeswitch.
            This command is used for when we would like to interact with 
            a call session, as the result, the uuid of the call channel
            is required.
        """
        if aSync:
            return self._conn.executeAsync(dialplan_command, \
                command_arguments, uuid)
        else:                
            return self._conn.execute(dialplan_command, command_arguments, \
                uuid)


"""
    Unit tests
"""
if __name__ == '__main__':
    gw_provider = "callcentric.com"
    test_phone_number = "18553922666"
    test_fax_file = "/tmp/test_fax.tiff"

    conn = FSSocket('localhost', 8021, 'ClueCon')
    print("Connected: ", conn.connected())
    if conn.connected():
        # Run a command
        e = conn.sendApiCommand("sofia status")
        if e:
            print e.getBody()

        # Run another command
        command = "originate sofia/gateway/" + gw_provider + "/" + test_phone_number + " &txfax('" + test_fax_file + "')"
        print(command)
        e = conn.sendApiCommand(command)
        if e:
            print e.getBody()

        conn.disconnect()
