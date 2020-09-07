import luigi

# the ForceableTask has two flags, --force and --forceUpstream
# by default, Luigi runs tasks only once, if they were successful.  It marks them as "complete" (the complete() method returns true, if the outputs exist)
# the constructor of Forceable tasks removes outputs - which forces Luigi to run these tasks again, even if the outputs existed before, because removed outputs means that the complete() method will return False
# Flags:
# --force removes the outputs of the task that is called
# --forceUpstream removes the outputs of the current task, and all the tasks in the requires function (upstream tasks), and all the tasks upstream too (traversing upwards)
class ForceableTask(luigi.Task):
    force = luigi.BoolParameter(significant=False, default=False)
    forceUpstream = luigi.BoolParameter(significant=False, default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.forceUpstream:
            self.force = True
        
        # To force execution, we just remove all outputs before `complete()` is called
        if self.force is True:
            tasks = [self]
            while tasks:  #while tasks is not empty, pop tasks from list
                currentTask = tasks.pop(0) 
                if isinstance(currentTask, ForceableTask): #only remove outputs for ForceableTasks
                    outputs = luigi.task.flatten(currentTask.output())
                    [out.remove() for out in outputs if out.exists()]

                if self.forceUpstream is True:
                    tasks += luigi.task.flatten(currentTask.requires())  
