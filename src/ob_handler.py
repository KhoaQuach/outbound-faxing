#!/usr/bin/env python
 
"""
ob_handler.py:
    Outbound faxing handler object which is responsible to deliver the fax;
    each handler will run on its own little thread environment so multiple
    requests could be handle at the same time.
    Note: this class will NOT utilize any locking mechanism since each
    instance should be handle separate unique outbound faxing request
    which corresponding to each record in outbound_faxes table in datbase 
"""

from threading import Thread
from fs_socket import FS_Socket
import ob_logger
import ob_global_vars

class OB_Handler(Thread):

    def __init__(self, outbound_fax_id, destination_number, source_number, \
        max_attempts, num_attempts, sleep_time, fax_file, fax_user_id):

        Thread.__init__(self)

        self._outbound_fax_id = int(outbound_fax_id)
        self._destination_number = str(destination_number)
        self._source_number = str(source_number)
        self._max_attempts = int(max_attempts)
        self._num_attempts = int(num_attempts)
        self._sleep_time = int(sleep_time)
        self._fax_file = str(fax_file)
        self._fax_user_id = int(fax_user_id)

        self._conn = FS_Socket('localhost', 8021, 'ClueCon')

    def build_fs_ob_fax_command(self, voip_gw, destination_number, fax_file):
        """
            Build a Freeswitch command to send out the fax
        """ 
        return "originate sofia/gateway/" + voip_gw + "/" + destination_number + " &txfax('" + fax_file + "')"

    def run(self):
        """
            Main entry function to handle each outbound fax request
        """
        ob_logger.debug("Start run function, outbound_fax_id: " \
            + str(self._outbound_fax_id))
     
        # Send out the fax 
        send_out_fax()

        # Check sending fax evens for progress and hangup events
        wait_for_hangup_events()

        self._conn.disconnect()

        ob_logger.debug("End run function, outbound_fax_id: " \
            + str(self._outbound_fax_id))

    def send_out_fax(self):
        ob_logger.debug("Connected: ", self._conn.connected())

        if self._conn.connected():
            command = build_fs_ob_fax_command(ob_global_vars.VOIP_GW, self._destination_number, self._fax_file)
            ob_logger.debug(command)
            e = conn.sendApiCommand(command)

    def wait_for_hangup_events(self):
