#!/bin/bash
#
# Copyright (c) 2014-2015 Oracle and/or its affiliates. All rights reserved.
#
########### SIGTERM handler ############
function _term() {
 echo "Stopping container."
 echo "SIGTERM received, shutting down weblogic!" 
}

########### SIGKILL handler ############
function _kill() {
echo "SIGKILL received, shutting down weblogic!"
}

# Set SIGTERM handler
trap _term SIGTERM

# Set SIGKILL handler
trap _kill SIGKILL

#Absolute path of current file
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DOMAIN_HOME=/u01/oracle/domains/osb_domain
MS_LOGS=$DOMAIN_HOME/servers/${MS_NAME}/logs
ADMIN_PASSWORD=Welcome1

# If domain directory does not exist, container is starting for 1st time
# So it should start NM and also associate with AdminServer
# Otherwise, only start NM (container restarted)
ADD_DOMAIN=1
if [ ! -d ${DOMAIN_HOME} ]; then
    ADD_DOMAIN=0
fi

# Create Managed Domain and Add Server only if 1st execution
if [ $ADD_DOMAIN -eq 0 ]; then
	# Create a Managed Server OSB domain
	wlst.sh -skipWLSModuleScanning $DIR/addManaged.py
	mkdir -p ${MS_LOGS}
fi


# Start Managed Server
${DOMAIN_HOME}/bin/startManagedWebLogic.sh $MS_NAME  http://wlsadmin:7001 &> ${MS_LOGS}/${MS_NAME}.out &

touch ${MS_LOGS}/${MS_NAME}.out
tail -f ${MS_LOGS}/${MS_NAME}.out &

childPID=$!
wait $childPID
