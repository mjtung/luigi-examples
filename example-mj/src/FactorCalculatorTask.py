
from datetime import datetime
import luigi
from NormaliseDataT import NormaliseDataT
from NormaliseAllDataWrapper import NormaliseAllDataWrapper
from DownloadRawDataT import DownloadRawDataT
import os 

class FactorCalculatorTask(luigi.Task) :
    runDate      = luigi.DateParameter()
    multiFactor  = luigi.BoolParameter(default = False, parsing=luigi.BoolParameter.EXPLICIT_PARSING)
    logDir  = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'output')

    def requires(self):
        requiredLst = [NormaliseAllDataWrapper(runDate=self.runDate, multiFactor=self.multiFactor), DownloadRawDataT(runDate=self.runDate)]
        return requiredLst

    def run(self):
        with self.output().open('w') as hello_file :
            hello_file.write('Hello')
    
    def output(self):
        return luigi.LocalTarget(os.path.join(
            self.logDir, 
            'FactorCalculatorTask_{}.txt'.format(self.runDate.strftime('%Y%m%d'))
            ))

if __name__ == '__main__':
    # luigi.build([FactorCalculatorTask(runDate=datetime.strptime('2016-01-10', '%Y-%m-%d'), multiFactor=False)]) #datetime.strptime('2013-01-05','%Y-%m-%d')])
    # luigi.run(['FactorCalculatorTask', '--runDate', '2016-02-01', 
    #     '--multiFactor', 'True',
    #     '--logging-conf-file', '/Users/mjtung/Projects/luigi-examples/example-mj/debug-macos/luigi-logging.conf'])
    luigi.run()