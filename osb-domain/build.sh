#!/bin/sh
docker build --build-arg ADMIN_PASS="Welcome1" -t weblogic-domain:12.2.1.2-generic . 
