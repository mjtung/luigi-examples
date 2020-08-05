# Luigi Daemon

- depends on Python-daemon - can only reliably work in Linux/Mac
- started by:
```
luigid --background --logdir <path_to_logs>
```
- visit http://localhost:8082/ to access the UI

# Luigi Daemon using Docker image
- https://hub.docker.com/r/axiom/docker-luigi/
- run the script in [start-luigi-docker.sh](start-luigi-docker.sh)
- visit http://localhost:8082/ to access the UI
- Note that we gave to pass in our own config file luigi.cfg

# Further integrations

## This example does the following:
1. Single output - single input
2. NormaliseDataT normalises data from input and writes output as CSV