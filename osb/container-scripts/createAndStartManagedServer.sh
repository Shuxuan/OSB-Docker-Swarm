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
export DOMAIN_HOME=/u01/oracle/domains/osb_domain
export MS_NAME=osb_server1
export ADMIN_PASSWORD=Welcome1

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
fi


# Start Managed Server
${DOMAIN_HOME}/bin/startManagedWebLogic.sh $MS_NAME
