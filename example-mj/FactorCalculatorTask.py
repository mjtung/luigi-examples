
from datetime import datetime
import luigi
from NormaliseDataT import NormaliseDataT
from DownloadRawDataT import DownloadRawDataT
import os 

class FactorCalculatorTask(luigi.Task) :
    runDate      = luigi.DateParameter()
    multiFactor  = luigi.BoolParameter(default = False, parsing=luigi.BoolParameter.EXPLICIT_PARSING)
    logDir  = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')

    def requires(self):
        requiredLst = [NormaliseDataT(runDate=self.runDate, multiFactor=self.multiFactor), DownloadRawDataT(runDate=self.runDate)]
        return requiredLst
        # return wtf(otherA = 'hello')

    def run(self):
        with self.output().open('w') as hello_file :
            hello_file.write('Hello')
    
    def output(self):
        return luigi.LocalTarget(os.path.join(
            self.logDir, 
            'FactorCalculatorTask_{}.txt'.format(self.runDate.strftime('%Y%m%d'))
            ))


if __name__ == '__main__':
    luigi.build([FactorCalculatorTask(runDate=datetime.strptime('2013-01-07', '%Y-%m-%d'), multiFactor=True)]) #datetime.strptime('2013-01-05','%Y-%m-%d')])
    # luigi.run()