import luigi
from NormaliseDataT import NormaliseDataT
from ForceableTask import ForceableTask

class NormaliseAllDataWrapper(ForceableTask, luigi.WrapperTask):
    runDate      = luigi.DateParameter()
    multiFactor  = luigi.BoolParameter(default=False, parsing=luigi.BoolParameter.EXPLICIT_PARSING)
    lstCountries = ['AA', 'AN', 'FC', 'FH', 'FS', 'FA', 'FJ1', 'FJ2', 'FM', 'FT', 'FI', 'FL']

    def requires(self):
        for c in self.lstCountries:
            yield NormaliseDataT(runDate=self.runDate, country=c, multiFactor=self.multiFactor)
