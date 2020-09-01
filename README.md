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
- Note that we gave to pass in our own config file [luigi.cfg](luigi.cfg)
- This can also be specified as a Docker service

## Notes
- bind mounts mean that if I change the file that it is mounted to, the Docker container automatically picks up the changes

# Luigi Tasks

Inside the [example-mj](example-mj) folder, is an example app which uses Luigi Tasks to run a workflow.

## Example-mj App

- idea is that we use Luigi to run a workflow of tasks, where each task takes some input, and writes some output to file.  A downstream task reads the output from an upstream task, and does something else to the data, and writes the output to file.  Etc, etc.
- the head task/final downstream task is [FactorCalculatorTask](example-mj/src/FactorCalculatorTask.py)
- to run the head task, issue a command similar to the following:
```
PYTHONPATH='src' luigi --module FactorCalculatorTask FactorCalculatorTask --runDate 2016-01-28 --multiFactor True --logging-conf-file /Users/mjtung/Projects/luigi-examples/example-mj/debug-macos/luigi-logging.conf --workers 10
```
- the tasks here write files to S3 buckets, and downstream tasks read from these files and do further calculations / transformations
- see description of flags below

### Flags

- runDate: specify runDate.  Yesterday, by default
- multiFactor: True/False.  In multiFactor mode, the tasks CalcDataT and NormaliseDataT output a single file, containing the paths pointing to multiple "factors" (ie. outputs) that it had written to in the main `run()` function
- country: eg. FJ1. Used for NormaliseDataT and CalcDataT: these tasks run an instance per country
- force: (no value, just a flag). Forces a re-run of a task.  Uses the custom class [ForceableTask](example-mj/src/ForceableTask.py) to do so (see https://github.com/spotify/luigi/issues/595)
- forceUpstream: (no value, just a flag). Forces re-runs of upstream ForceableTasks
    - By default, Luigi will not re-run tasks if they are successful.  This is because Luigi tasks are meant to be idempotent - meaning that everytime you run them, you should get the same result, and therefore they never need to be re-run.
    - However, real life is less idealistic, and there could be many cases where a task needs to be re-run even if it was at first successful (or marked as successful)
    - The custom `ForceableTask` class allows for reruns.  The `ForceableTask` constructor removes all outputs that are currently in existence, thereby forcing tasks to be rerun, as Luigi checks for the existence of outputs to determine whether a task has already been run or not

# Deployment

- I have currently deployed both a Luigi daemon/server and the example workflow app above to AWS ECS.  AWS ECS keeps a Luigi daemon/server running as a Service at  http://54.245.23.5:8082/ (note that the IP address may change from time to time)
- The app is deployed as a Scheduled Task in the same ECS cluster.  It is scheduled to run once a day
    - The app uses an nginx Docker image as a reverse proxy that maps `localhost` to the IP-address of the Luigi daemon/server above
- The Luigi daemon/server will show the results of the tasks that have run, for up to 48 hours (configure that in [luigi.cfg](luigi.cfg))
- TODO: the deployment process was manual, and should be streamlined and automated.  By doing so, the IP-address of the Luigi Service could also be linked to the nginx reverse proxy, instead of being manually coded

