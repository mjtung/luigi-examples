#!/bin/sh
    # mount volume to persist state
    # mount custom config file
    # mount folder for longs
    # pass in custom run script
    # get image: TODO: can keep a copy of it somewhere
    # pass in logdir args to luigid command
docker run -d -p 8082:8082 --name docker-luigi \
    -v luigistate:/luigi/state \
    -v /mnt/c/Users/tungm/Projects/luigi-examples/luigi.cfg:/etc/luigi/luigi.cfg \
    -v /mnt/c/Users/tungm/Projects/luigi-examples/luigid-start.sh:/bin/run \
    -v /mnt/c/Users/tungm/Projects/luigi-server/log:/var/log/luigi \
    axiom/docker-luigi:2.8.13-alpine \
    --logdir /var/log/luigi  