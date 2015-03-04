# outbound-faxing
Outbound faxing services and clients

This project includes the database and Freeswitch outbound faxing engine 
written in Python to provide the outbound faxing feature.

A separate restful server, utilized Python flask framework, would provide
the the mobile/web clients to submit the outbound request fax and query
for job status.

It's currently only running in Linux environment.

How it works:
* A client (web/mobile) would submit a outbound fax request.
* A new record in the database would be created with the PENDING status.
* A system cron job would launch a Python script every 30 seconds,
which checks the database if there is/are new outbound fax in PENDING state.
* If there is/are new outbound fax requests, another Python script will 
attemp to convert the uploaded file to TIFF format; the uploaded file could be 
in pdf, gif, jpeg, png formats. Sorry no doc format yet, because I use the
open source library so have not figured it out to convert doc to tiff yet.
* Build the appropriate outbound fax header template and combine the header
and documents files into one big TIFF file.
* Another Python script would connect to Freeswitch using socket, initiates
a new dial out session to request outbound fax phone number, and attempts to
deliver the fax.
* Update the SUCCESS or FAILURE status in database, with detail error message
if failure encounters.
