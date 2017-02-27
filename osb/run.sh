#!/bin/sh
docker run -d --name wlsadmin --add-host osbdb:172.17.0.2 --hostname wlsadmin -p 7001:7001 oracle/osb:12.2.1.2
