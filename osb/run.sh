#!/bin/sh
docker run -d --name wlsadmin --add-host osbdb:172.17.0.2 --add-host wls1:172.17.0.4 --add-host wls2:172.17.0.5 --hostname wlsadmin -p 7001:7001 oracle/osb:12.2.1.2
