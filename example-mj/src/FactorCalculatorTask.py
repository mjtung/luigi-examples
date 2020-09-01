
from datetime import datetime, timedelta
import luigi
# from NormaliseDataT import NormaliseDataT
from NormaliseAllDataWrapper import NormaliseAllDataWrapper
from DownloadRawDataT import DownloadRawDataT
from ForceableTask import ForceableTask
import os 

class FactorCalculatorTask(ForceableTask) :
    runDate      = luigi.DateParameter(default=datetime.today() + timedelta(-1))
    multiFactor  = luigi.BoolParameter(default=True, parsing=luigi.BoolParameter.EXPLICIT_PARSING)
    logDir  = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'output')

    def requires(self):
        requiredLst = [NormaliseAllDataWrapper(runDate=self.runDate, multiFactor=self.multiFactor), DownloadRawDataT(runDate=self.runDate)]
        return requiredLst

    def run(self):
        print('Running FactorCalculatorTask!')
        with self.output().open('w') as outfile:
            outfile.write('FactorCalculatorTask done for {}'.format(self.runDate.strftime('%Y%m%d')))
    
    def output(self):
        # return luigi.LocalTarget(os.path.join(
            # self.logDir, 
            # 'FactorCalculatorTask_{}.txt'.format(self.runDate.strftime('%Y%m%d'))
            # ))
        return luigi.LocalTarget(is_tmp=True)

if __name__ == '__main__':
    # luigi.build([FactorCalculatorTask(runDate=datetime.strptime('2016-01-10', '%Y-%m-%d'), multiFactor=False)]) #datetime.strptime('2013-01-05','%Y-%m-%d')])
    # luigi.run(['FactorCalculatorTask', '--runDate', '2016-02-01', 
    #     '--multiFactor', 'True',
    #     '--logging-conf-file', '/Users/mjtung/Projects/luigi-examples/example-mj/debug-macos/luigi-logging.conf'])
    luigi.run()