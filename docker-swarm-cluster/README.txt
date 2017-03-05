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

