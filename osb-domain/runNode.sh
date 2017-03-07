#!/bin/sh
# Pass in single number for managed server
# No parameter means admin server

NODE=$1
if [ "${NODE}" == "" ] ; then NODE=admin ; fi
if [ "${NODE}" ==  "admin" ]
then
	MS_NAME="AdminServer"
	MACHINE_NAME="AdminServerMachine"
	SCRIPT_NAME="createAndStartOSBDomain.sh"
	PORT_MAP="7001:7001"
else
	MS_NAME="osb_server${NODE}"
	MACHINE_NAME="OsbServer${NODE}Machine"
	SCRIPT_NAME="createAndStartManagedServer.sh"
	((eport=8009+2*${NODE}))
	PORT_MAP="${eport}:8011"
fi
SERVER_NAME="wls${NODE}"

echo Creating Container
echo MS_NAME=$MS_NAME
echo MACHINE_NAME=$MACHINE_NAME
echo SCRIPT_NAME=$SCRIPT_NAME
echo PORT_MAP=$PORT_MAP
echo SERVER_NAME=$SERVER_NAME
docker run -d -it \
	-e "MS_NAME=${MS_NAME}" \
	-e "MACHINE_NAME=${MACHINE_NAME}" \
	--name ${SERVER_NAME} \
	--add-host osbdb:172.17.0.2 \
	--add-host wlsadmin:172.17.0.3 \
	--add-host wls1:172.17.0.4 \
	--add-host wls2:172.17.0.5 \
	--add-host wls3:172.17.0.6 \
	--add-host wls4:172.17.0.7 \
	--hostname ${SERVER_NAME} \
	-p ${PORT_MAP} \
	oracle/osb_domain:12.2.1.2 \
	/u01/oracle/container-scripts/${SCRIPT_NAME}
