# outbound-faxing
Outbound faxing services and clients

Implementing a restful server and back-end engine written in Python to provide
clients, web or mobile apps, the capability to send fax.

It's utilizing Freeswitch as the outbound faxing engine and bunch of Python
scripts to interactive with it. 

The restful server, utilized Python flask framework, would provide
the the mobile/web clients to submit the outbound request fax and query
for job status.

Support environments: Linux/Unix. Python 2.7+.

How it works:
============

* A client (web/mobile) would submit a outbound fax request through 
restful APIs.
* A new record would be added into fax file repository table with NEW status.
* A system cron job would launch a Python script every 30 seconds,
which checks the database if there is/are new fax file(s) in repository with 
the NEW state. 
* If found, above script would attempt to convert the file to TIFF format; 
the uploaded file could be in pdf, gif, jpeg, png formats. Sorry no doc 
format yet because I use the open source library so have not figured it 
out to convert doc to tiff yet.
* If the file is converted successfully, it would build the appropriate
outbound fax header template, and combine the header and document files into
one big TIF file. Once done, it would insert new record into database table
containing all the requests, with PENDING status.
* Another Python script would be launched by cron job every 30 seconds,
and check the database if there is/are PENDING status records.  
* If there is/are records returned from above script, it would connect to 
Freeswitch using socket, initiates a new dial out session to outbound 
fax phone number, and attempts to deliver the fax.  
* Either if the fax is sent or encountered error, the database record would 
be updated with SUCCESS or ERROR status, with detail error message if 
failured.

How to install and run:
======================

* This project requires a few component before it can be launched:
    - Flask framework:
    - Freeswitch: please consult freeswitch.org website on how to download
        and configure bare-bone Freeswitch system.
        The python scripts utilize the library ESL.py modules so
        make sure above file is installed and in your python path file; it
        should be automatically included as part of python package
        installation in most Linux distributions, I said most here...
    - MySQL: database backend to keep track of all requests and status.
    - File conversion tools: convert and imagematick library.
* Clone the project from github
    git clone https://github/KhoaQuach/outbound-faxing
* Run the setup script, setup.sh; this script will attemp to setup the system
to support outbound faxing.

** One important note: in order to dial out to send fax, I include a sample
sip profile, callcentric.xml, which utilizes the callcentric voip provider to
dial out and deliver the fax. Yours might be different so use it as reference
and configure your own accordingly. If you support a lot of outbound sessions,
you might need a sip trunk provider so the sip profile might be different as well.
Please consult the Freeswitch document for more information.

Design to consider:
==================

- The web services api and database might be hosted in Google app engine or
Amazon EC2 environment.
- Freeswitch might be running in the Amazon EC2 hosted server as well but I have 
heard it's not running very well with voice/fax protocols because sensitivity
of latency, jitter and packet loss.

