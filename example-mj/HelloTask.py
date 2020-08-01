
from datetime import datetime
import luigi
from NormaliseDataT import NormaliseDataT
from DownloadRawDataT import DownloadRawDataT
import os 

class HelloTask(luigi.Task) :
    runDate = luigi.DateParameter()
    logDir  = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')

    def requires(self):
        requiredLst = [NormaliseDataT(runDate=self.runDate), DownloadRawDataT(runDate=self.runDate)]
        return requiredLst
        # return wtf(otherA = 'hello')

    def run(self):
        with self.output().open('w') as hello_file :
            hello_file.write('Hello')
    
    def output(self):
        return luigi.LocalTarget(os.path.join(
            self.logDir, 
            'hello_{}.txt'.format(self.runDate.strftime('%Y%m%d'))
            ))


if __name__ == '__main__':
    # luigi.run([HelloTask(runDate=datetime.strptime('2013-01-07', '%Y-%m-%d'))]) #datetime.strptime('2013-01-05','%Y-%m-%d')])
    luigi.run()