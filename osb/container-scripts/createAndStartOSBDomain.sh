#!/bin/bash
#
# Copyright (c) 2014-2015 Oracle and/or its affiliates. All rights reserved.
#
########### SIGTERM handler ############
function _term() {
   echo "Stopping container."
   echo "SIGTERM received, shutting down database!"
   sqlplus / as sysdba <<EOF
   shutdown immediate;
EOF
   lsnrctl stop
}

########### SIGKILL handler ############
function _kill() {
   echo "SIGKILL received, shutting down database!"
   sqlplus / as sysdba <<EOF
   shutdown abort;
EOF
   lsnrctl stop
}

# Set SIGTERM handler
trap _term SIGTERM

# Set SIGKILL handler
trap _kill SIGKILL

# If AdminServer.log does not exists, container is starting for 1st time
# So it should start NM and also associate with AdminServer
# Otherwise, only start NM (container restarted)
DOMAIN_HOME=/u01/oracle/domains/osb_domain
ADD_DOMAIN=1
ADMIN_PASSWORD=Welcome1
if [ ! -f ${DOMAIN_HOME}/servers/AdminServer/logs/AdminServer.log ]; then
    ADD_DOMAIN=0
fi

# Create Domain only if 1st execution
if [ $ADD_DOMAIN -eq 0 ]; then
	#Absolute path of current file
	DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
	#run RCU
	$DIR/rcuOSB.sh
	
	echo ""
	echo "    Oracle WebLogic Server Auto Generated Empty OSB Domain:"
	echo ""
	echo "      ----> 'weblogic' admin password: $ADMIN_PASSWORD"
	echo ""
	
	sed -i -e "s|ADMIN_PASSWORD|$ADMIN_PASSWORD|g" /u01/oracle/create-osb-domain.py
	
	# Create an OSB domain
	wlst.sh -skipWLSModuleScanning /u01/oracle/create-osb-domain.py
	mkdir -p ${DOMAIN_HOME}/servers/AdminServer/security/ 
	echo "username=weblogic" > /u01/oracle/user_projects/domains/$DOMAIN_NAME/servers/AdminServer/security/boot.properties 
	echo "password=$ADMIN_PASSWORD" >> /u01/oracle/user_projects/domains/$DOMAIN_NAME/servers/AdminServer/security/boot.properties 
	${DOMAIN_HOME}/bin/setDomainEnv.sh 
fi


# Start Admin Server and tail the logs
${DOMAIN_HOME}/startWebLogic.sh
touch ${DOMAIN_HOME}/servers/AdminServer/logs/AdminServer.log
tail -f ${DOMAIN_HOME}/servers/AdminServer/logs/AdminServer.log &

childPID=$!
wait $childPID

