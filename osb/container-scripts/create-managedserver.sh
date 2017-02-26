#!/bin/sh
docker run -d --name managedserver1 --link wlsadmin:wlsadmin -p 7001:7001 weblogic-domain:12.2.1.2-generic createServer.sh

