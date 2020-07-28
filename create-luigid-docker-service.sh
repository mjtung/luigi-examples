#!/bin/sh
    # create service (ie. swarm mode)
    # can add repliacas=X flag to make it run X instances
    # mount volume to persist state
    # mount custom config file
    # mount folder for longs
    # pass in custom run script
    # get image: TODO: can keep a copy of it somewhere
    # pass in logdir args to luigid command
docker service create -d -p 8082:8082 --name docker-luigid-service \
    --mount type=volume,source=luigistate,destination=/luigi/state \
    --mount type=bind,source=/mnt/c/Users/tungm/Projects/luigi-examples/luigi.cfg,destination=/etc/luigi/luigi.cfg \
    --mount type=bind,source=/mnt/c/Users/tungm/Projects/luigi-examples/luigid-start.sh,destination=/bin/run \
    --mount type=bind,source=/mnt/c/Users/tungm/Projects/luigi-server/log,destination=/var/log/luigi \
    axiom/docker-luigi:2.8.13-alpine \
    --logdir /var/log/luigi  