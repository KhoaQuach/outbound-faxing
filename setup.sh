#!/bin/sh

#
# This script would attemp to verify all neccessary components in order to
# support outbound faxing feature. Once done, it would attempt to configure
# Freeswitch, database, restful server and cron job. Final step, it will
# copy all neccessary Python scripts to correct location.
#

FS_CONF_DIR=/usr/local/freeswitch/conf

if [[ ${1} != "" ]]; then
    FS_CONF_DIR=${1}
fi

if [[ -d ${FS_CONF_DIR} ]]
    print "Freeswitch conf directory does not exist!"
    exit 1
fi
