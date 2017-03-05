#!/bin/sh
# docker run -e "MS_NAME=osb_server2" -e "MACHINE_NAME=osb2Machine" -d -it --name wls2 --add-host osbdb:172.17.0.2 --add-host wlsadmin:172.17.0.3 --hostname wls2 -p 8013:8011 oracle/osb_domain:12.2.1.2 /bin/bash
docker run -e "MS_NAME=osb_server2" -e "MACHINE_NAME=osb2Machine" -d -it --name wls2 --add-host osbdb:172.17.0.2 --add-host wlsadmin:172.17.0.3 --hostname wls2 -p 8013:8011 oracle/osb_domain:12.2.1.2 /u01/oracle/container-scripts/createAndStartManagedServer.sh
