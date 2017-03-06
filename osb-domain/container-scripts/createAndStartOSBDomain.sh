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

# If AdminServer.log does not exists, container is starting for 1st time
# So it should start NM and also associate with AdminServer
# Otherwise, only start NM (container restarted)
DOMAIN_HOME=/u01/oracle/domains/osb_domain
ADMIN_LOGS=$DOMAIN_HOME/servers/AdminServer/logs
ADD_DOMAIN=1
ADMIN_PASSWORD=Welcome1
if [ ! -f ${ADMIN_LOGS}/AdminServer.log ]; then
    ADD_DOMAIN=0
fi

# Create Domain only if 1st execution
if [ $ADD_DOMAIN -eq 0 ]; then
	#run RCU
	$DIR/rcuOSB.sh
	
	echo ""
	echo "    Oracle WebLogic Server Auto Generated OSB Domain:"
	echo ""
	echo "      ----> 'weblogic' admin password: $ADMIN_PASSWORD"
	echo ""
	
	#sed -i -e "s|ADMIN_PASSWORD|$ADMIN_PASSWORD|g" $DIR/create-osb-domain.py
	
	# Create an OSB domain
	wlst.sh -skipWLSModuleScanning $DIR/create-osb-domain.py
	${DOMAIN_HOME}/bin/setDomainEnv.sh 
	mkdir -p ${ADMIN_LOGS}
fi


# Start Admin Server

${DOMAIN_HOME}/startWebLogic.sh &> ${ADMIN_LOGS}/AdminServer.out &

touch ${ADMIN_LOGS}/AdminServer.out
tail -f ${ADMIN_LOGS}/AdminServer.out &

childPID=$!
wait $childPID

