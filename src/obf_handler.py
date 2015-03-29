#!/usr/bin/env python
 
"""
obf_handler.py:
    Outbound faxing handler object which is responsible to deliver the fax;
    each handler will run on its own little thread environment so multiple
    requests could be handle at the same time.
    Note: this class will NOT utilize any locking mechanism since each
    instance should be handle separate unique outbound faxing request
    which corresponding to each record in outbound_faxes table in datbase 
"""

from threading import Thread
from fs_socket import FS_Socket
from db import DB
import obf_logger
import obf_global_vars

__author__      = obf_global_vars.AUTHORS
__copyright__   = obf_global_vars.COPYRIGHT
__credits__     = obf_global_vars.CREDITS
__license__     = obf_global_vars.LICENSE
__version__     = obf_global_vars.VERSION
__maintainer__  = obf_global_vars.MAINTAINER
__email__       = obf_global_vars.EMAIL
__status__      = obf_global_vars.STATUS

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

        # These settings affect the fax call or fax pages
        self._fax_disable_v17 = False
        self._fax_enable_t38 = True
        self._fax_ident = ""
        self._fax_header = ""
        self._fax_use_ecm = True

        # Fax call result codes and texts; they are in string type
        self._fax_result_code = "0"
        self._fax_result_text = ""
        self._fax_success = "0"
        self._fax_document_total_pages = "0"
        self._fax_document_transferred_pages = "0"
        self._fax_image_resolution = ""
        self._fax_image_size = ""
        self._fax_local_station_id = ""
        self._fax_remote_station_id = ""
        self._fax_transfer_rate = ""
        self._fax_bad_rows = ""
        self._t38_gateway_format = ""
        self._t38_peer = ""
        self._hangup_cause = ""

        self._socket = FS_Socket(obf_global_vars.FS_HOST, obf_global_vars.FS_SOCKET_PORT, obf_global_vars.FS_SOCKET_PASSWORD)

        if not self._socket.connected():
            raise Exception("Can not establish connection to Freeswitch")

        self._socket.filter_events("plain","all");

        self._orig_uuid = self._socket.send_api_command("create_uuid").getBody();
        self._job_uuid = ""

    def build_fs_obf_fax_command(self, voip_gw, destination_number, fax_file):
        """
            Build a Freeswitch command to send out the fax
        """ 
        return "\{outbound_fax_id={0}\}sofia/gateway/{1}/{2} &txfax({3})".format(self._outbound_fax_id, voip_gw, destination_number, fax_file)

    def hangup_cause_call_failed(hangup_cause_code):
        return False

    def run(self):
        """
            Main entry function to handle each outbound fax request
        """
        obf_logger.debug("Start run function, outbound_fax_id: " \
            + str(self._outbound_fax_id))
     
        # Send out the fax 
        send_out_fax()

        # Check sending fax evens for progress and hangup events
        wait_for_hangup_events()

        self._socket.disconnect()

        obf_logger.debug("End run function, outbound_fax_id: " \
            + str(self._outbound_fax_id))

    def send_out_fax(self):
        """
            This function submits a background task to Freeswitch to dial, connect
            and try to deliver the fax
        """
        obf_logger.debug("Connected: " + str(self._socket.connected()))

        if self._socket.connected():
            command_args = build_fs_obf_fax_command_args(obf_global_vars.VOIP_GW, self._destination_number, self._fax_file)
            obf_logger.debug(command_args)
            e = conn.send_bg_api_command("originate", command_args, self._orig_uuid)

            # Save the background job uuid in case we need it later
            self._job_uuid = e.getHeader("Job-UUID")

    def update_obf_fax_status(self, outbound_fax_id, outbound_fax_status_id, num_attempts, result_code, result_message):
        """
            Update the database outbound fax record with appropriate 
            progress and status
        """
        obf_logger.debug(__function__ + " entering")

        db_conn = DB(obf_global_vars.DB_HOST, obf_global_vars.DB_USERNAME, obf_global_vars.DB_PASSWORD, obf_global_vars.DB_NAME)

        db_conn.execute("INSERT INTO faxes.outbound_fax_attempts(attempt_result_code, attempt_result_message, outbound_fax_id) VALUES({0}, '{1}', {2})".format(attempt_result_code, attempt_result_message, outbound_fax_id))

        db_conn.execute("UPDATE faxes.outbound_faxes SET num_attempts={0}, outbound_fax_status_id={1} WHERE outbound_fax_id={2}".format(num_attempts, outbound_fax_status_id, outbound_fax_id))

        obf_logger.debug(__function__ + " exiting")

    def wait_for_hangup_events(self):
        """
            This function waits until the call ends, save some of the call hungup result events,
            and depend on what results of the fax call, update the database status accordingly
        """

        while True: 
            
            self._num_attempts += 1
            obf_logger.debug("Number of tries: " + str(self._num_attempts))
            if self._max_attemtps < self._num_attempts:
                obf_logger.warning("Max out number of attempts!")
                update_obf_fax_status(self._outbound_fax_id, 2, self._num_attempts, -1, '')
                return 

            if not self._socket.connected():
                obf_logger.error("Socket session disconnected!")
                update_obf_fax_status(self._outbound_fax_id, 2, self._num_attempts, -1, '')
                return 

            e = self._socket.recvEventTimed(10000);
            if e is not None:
                event_name = e.getHeader("Event-Name");
        
                # Should we check for the job_uuid to match the background job ?                      
                if event_name == "BACKGROUND_JOB":
                    if e.getHeader("Job-UUID") == self._job_uuid: 
                        call_result = e.getBody();
                        obf_logger.debug("Result of call is {0}".format(call_result))

                elif event_name == "CHANNEL_HANGUP" or event_name == "CHANNEL_HANGUP_COMPLETE":
                    obf_logger.debug("Call has been hung up")

                    # Result of the call
                    self._fax_result_code = e.getHeader("fax_result_code")
                    self._fax_result_text = e.getHeader("fax_result_text")
                    self._fax_success = e.getHeader("fax_success")
                    self._fax_document_total_pages = e.getHeader("fax_document_total_pages")
                    self._fax_document_transferred_pages = e.getHeader("fax_document_transferred_pages")
                    self._fax_image_resolution = e.getHeader("fax_image_resolution")
                    self._fax_image_size = e.getHeader("fax_image_size")
                    self._fax_local_station_id = e.getHeader("fax_local_station_id")
                    self._fax_remote_station_id =e.getHeader("fax_remote_station_id")
                    self._fax_transfer_rate = e.getHeader("fax_transfer_rate")
                    self._fax_bad_rows = e.getHeader("fax_bad_rows")
                    self._t38_gateway_format = e.getHeader("t38_gateway_format")
                    self._t38_peer = e.getHeader("t38_peer")
                    self._hangup_cause = e.getHeader("hangup_cause");

                    obf_logger.debug("fax_result_code: " + self._fax_result_code)
                    obf_logger.debug("fax_result_text: " + self._fax_result_text)
                    obf_logger.debug("fax_success: " + self._fax_success)
                    obf_logger.debug("fax_document_total_pages: " + self._fax_document_total_pages)
                    obf_logger.debug("fax_document_transferred_pages: " + self._fax_document_transferred_pages)
                    obf_logger.debug("fax_image_resolution: " +  self._fax_image_resolution)
                    obf_logger.debug("fax_image_size: " + self._fax_image_size )
                    obf_logger.debug("fax_local_station_id: " +  self._fax_local_station_id )
                    obf_logger.debug("fax_remote_station_id: " + self._fax_remote_station_id)
                    obf_logger.debug("fax_transfer_rate: " + fax_transfer_rate)
                    obf_logger.debug("fax_bad_rows: " + fax_bad_rows)
                    obf_logger.debug("t38_gateway_format: " + t38_gateway_format)
                    obf_logger.debug("t38_peer: " + t38_peer)
                    obf_logger.debug("hangup_cause: " + self._hangup_cause)

                    update_obf_fax_status(self._outbound_fax_id, 1, self._num_attempts, self._fax_result_code, self._fax_result_text)

                    # Examine hangup cause code here since some of the codes caused by the call
                    # could not be established, if so, don't re-try to send out the fax again
                    # but end the handle function instead
                    if hangup_cause_call_failed(self._hangup_cause):
                        return

                    # Finally, if we have successfully delivered the fax, we exit the function as well
                    if self._fax_success == "1" or self._fax_success == True:
                        return

                else:
                    obf_logger.debug(e.getBody())

        return 
