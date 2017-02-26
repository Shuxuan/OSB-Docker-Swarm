#!/bin/bash
# 
# This script will wait until Admin Server is available.
# There is no timeout!
#
echo Run rcu for SOA Infrastucture
export ORACLE_HOME=/u01/oracle/weblogic
$ORACLE_HOME/oracle_common/bin/rcu -silent -createRepository -connectString localhost:1521:OSB -dbUser sys -dbRole sysdba -useSamePasswordForAllSchemaUsers true -schemaPrefix DEV -variables SOA_PROFILE_TYPE=LARGE <components> -f < password.txt


export RCU_SOA_RSP=rcuOSB.rsp
export RCU_SOA_PWD=rcuPasswords.txt
$ORACLE_HOME/oracle_common/bin/rcu -silent -responseFile $RCU_INSTALL_HOME/$RCU_SOA_RSP -f < $RCU_INSTALL_HOME/$RCU_SOA_PWD