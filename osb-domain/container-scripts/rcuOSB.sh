#!/bin/bash
# 
# This script will wait until Admin Server is available.
# There is no timeout!
#
echo Run rcu for SOA Infrastucture
export ORACLE_HOME=/u01/oracle/weblogic
export RCU_OSB_RSP=rcuResponseFile.properties
export RCU_OSB_PWD=rcuOSBPasswords.txt
export RCU_INSTALL_HOME=/u01/oracle

$ORACLE_HOME/oracle_common/bin/rcu -silent -responseFile $RCU_INSTALL_HOME/$RCU_OSB_RSP -f < $RCU_INSTALL_HOME/$RCU_OSB_PWD