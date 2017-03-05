#Swarm initialized: current node (51tjyixnckdw2xjtpv90lic1a) is now a manager.
#
#To add a worker to this swarm, run the following command:
#
#    docker swarm join \
#    --token SWMTKN-1-0s61uwhyu3sconrk53hnlmyk7s4yu4c5i9zy7zmxns04q9mvrf-cf8pd5h9zdppjf3ikqhrytujo \
#    10.0.2.10:2377

#To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.


docker swarm init --advertise-addr 10.0.2.10
