import luigi

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
