#!/bin/sh
docker run -e "MS_NAME=osb_server1" -e "MACHINE_NAME=osb1Machine" -d -it --name wls1 --add-host osbdb:172.17.0.2 --add-host wlsadmin:172.17.0.3 --hostname wls1 -p 8011:8011 oracle/osb_domain:12.2.1.2 /u01/oracle/container-scripts/createAndStartManagedServer.sh
