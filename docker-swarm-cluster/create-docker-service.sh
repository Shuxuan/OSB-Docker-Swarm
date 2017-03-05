#docker service create --replicas 3 --name my-web --network weblogic-net nginx
#docker service ps my-web
docker service create --replicas 1 --name weblogic --network weblogic-net 10.0.2.10:5000/weblogic
