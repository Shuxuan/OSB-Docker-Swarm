#!/bin/sh
docker run -d --name wlsadmin --hostname wlsadmin -p 8001:8001 weblogic-domain:12.2.1.2-generic
