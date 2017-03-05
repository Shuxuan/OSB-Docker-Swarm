
# add global mode to make sure run docker service on every node but only 1 per node
#docker service create --name managedserver --network weblogic-net --mode global --publish 7001:7001 10.0.2.10:5000/weblogic-domain createServer.sh

# running as relicas mode, 
docker service create --replicas 3 --name wlsmanagedserver --network weblogic-net 10.0.2.10:5000/weblogic-domain createServer.sh
