#docker run -d --name wlsadmin --hostname wlsadmin --network weblogic-net -p 8001:8001 weblogic-domain:12.2.1.2-generic
#docker service create --replicas 3 --name my-web --network weblogic-net nginx
docker service create --replicas 1 --name wlsadmin --network weblogic-net --publish 8001:8001 10.0.2.10:5000/weblogic-domain
