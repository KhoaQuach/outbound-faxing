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

How to install and run:
* This project requires a few component before it can be setup:
    Freeswitch: please consult freeswitch.org website on how to download
        and configure bare-bone Freeswitch system.
    MySQL: database backend to keep track of all requests and status.
    File conversion tools:
* Clone the project from github
    git clone https://github/KhoaQuach/outbound-faxing
* Run the setup script, setup.sh; this script will attemp to setup the system
to support outbound faxing.

*** One important note: in order to dial out to send fax, I include a sample
sip profile, callcentric.xml, which utilizes the callcentric voip provider to
dial out and deliver the fax. Yours might be different so use it as reference
and configure your own accordingly. If you support a lot of outbound sessions,
you might need a sip trunk provider so the sip profile might be different as well.
Please consult the Freeswitch document for more information.

