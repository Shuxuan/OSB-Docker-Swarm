#!/bin/sh
docker run -d -it --name wls1 --add-host osbdb:172.17.0.2 --add-host wlsadmin:172.17.0.3 --hostname wls1 -p 8011:8011 oracle/osb:12.2.1.2 /u01/oracle/container-scripts/createAndStartManagedServer.sh
