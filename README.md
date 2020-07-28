# Luigi Daemon

- depends on Python-daemon - can only reliably work in Linux/Mac
- started by:
```
luigid --background --logdir <path_to_logs>
```
- visit http://localhost:8082/ to access the UI

# Luigi Daemon using Docker image
- https://hub.docker.com/r/axiom/docker-luigi/
- run the following
```
docker run -d -p 8082:8082 --name docker-luigi -v luigistate:/luigi/state -v /mnt/c/Users/tungm/Projects/luigi-examples/luigi.cfg:/etc/luigi/luigi.cfg -v /mnt/c/Users/tungm/Projects/luigi-examples/luigid-start.sh:/bin/run axiom/docker-luigi:2.8.13-alpine --logdir /var/log/luigi
```
- visit http://localhost:8082/ to access the UI
- Note that we gave to pass in our own config file luigi.cfg
