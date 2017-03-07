Swarm
==============================================================================
1 create docker swarm manager

docker swarm init --advertise-addr 10.0.2.7


#[oracle@swarm-master ~]$ docker swarm init --advertise-addr 10.0.2.7
#Swarm initialized: current node (5o4dgfqbvdlp7112mnyyi21j4) is now a manager.

#To add a worker to this swarm, run the following command:

#    docker swarm join \
#    --token SWMTKN-1-3qkfb6ny69pb278xrin9bb5g4am88lt2iobbr6yx7atduva494-c4meo6o1rn1fdepbdgn7k3ves \
#    10.0.2.7:2377

#To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.


2 on each swarm node, join the swarm 
docker swarm join --token SWMTKN-1-3qkfb6ny69pb278xrin9bb5g4am88lt2iobbr6yx7atduva494-c4meo6o1rn1fdepbdgn7k3ves 10.0.2.7:2377

3 on swarm manasger, create overlay network
docker network create -d overlay weblogic-net

private repo
==============================================================================
1 start private repo
docker run -d -p 8500:8500 --hostname=consul --restart=always --name consul -h consul progrium/consul -server -bootstrap
docker run -d -p 5000:5000 --hostname=registry --restart=always --name registry -h registry registry:latest

2 push docker images into repo

2.1 
vi /etc/systemd/system/docker.service.d/http-proxy.conf
Environment="NO_PROXY=localhost,127.0.0.1,{{10.0.2.14}}"
Environment="no_proxy=localhost,127.0.0.1,{{10.0.2.14}}"

2.2 
vi /usr/lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd --insecure-registry {{10.0.2.14}}:5000

2.3 
vi /etc/sysconfig/docker
INSECURE_REGISTRY='--insecure-registry 10.0.2.14:5000'


2.4 systemctl daemon-reload
2.5 systemctl restart docker
2.6 tag image and push image into private repo

199cfe67642f is the image id
docker tag 199cfe67642f 10.0.2.14:5000/oracle/database
docker push 10.0.2.14:5000/oracle/database

2.7 query from repo
curl -X GET http://10.0.2.14:5000/v2/_catalog
curl -v -s -X GET "10.0.2.14:5000/v2/oracle/database/tags/list"
curl -X GET http://10.0.2.14:5000/v2/oracle/database/manifests/latest

2.8 pull db images on master
docker pull 10.0.2.14:5000/oracle/database

create database swarm service
==============================================================================
#docker service create --replicas 1 --name Oracle12cDB --hostname osbdb --network weblogic-net --publish 1521:1521 --publish 5500:5500 -e ORACLE_SID=ORCL -e ORACLE_PDB=OSB 10.0.2.14:5000/oracle/database

docker service create --replicas 1 --name Oracle12cDB --hostname osbdb --network weblogic-net --hostname="{{.Node.ID}}-{{.Service.Name}}" --publish 1521:1521 --publish 5500:5500 -e ORACLE_SID=ORCL -e ORACLE_PDB=OSB 10.0.2.14:5000/oracle/database

--hostname="{{.Node.ID}}-{{.Service.Name}}"
--net-alias

docker inspect osbdb


docker-machine create --driver virtualbox --engine-insecure-registry registry:5000 --engine-storage-driver overlay --swarm-master swarm-master1
docker-machine create --driver virtualbox --engine-storage-driver overlay --swarm-master swarm-master1

docker-machine env swarm-master1
eval $(docker-machine env swarm-master1)
unset env
========
unset ${!DOCKER*}

