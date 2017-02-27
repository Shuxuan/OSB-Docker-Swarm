#!/bin/sh
docker run -d --name wlsadmin --hostname wlsadmin -p 8001:8001 oracle/osb:12.2.1.2
