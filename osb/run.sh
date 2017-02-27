#!/bin/sh
docker run -d --name wlsadmin --hostname wlsadmin -p 7001:7001 oracle/osb:12.2.1.2
