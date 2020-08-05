from datetime import datetime
import os
import luigi
import pandas as pd
import numpy as np
from DownloadRawDataT import DownloadRawDataT

class CalcDataT(luigi.Task) :
    runDate      = luigi.DateParameter()
    country      = luigi.Parameter()
    multiFactor  = luigi.BoolParameter(default = False, parsing=luigi.BoolParameter.EXPLICIT_PARSING)    
    # lstCountries = ['AA', 'AN', 'FC', 'FH', 'FS', 'FA', 'FJ1', 'FJ2', 'FM', 'FT', 'FI', 'FL']
    logDir       = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')
    factorDir    = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'factors')
    factorList   = ['factor1', 'factor2', 'factor3', 'factor4'] # for multiFactor only
    # def __init__(self, date):
    #     self.runDate = date

    def requires(self):
        return DownloadRawDataT(runDate=self.runDate)

    def run(self):
        # if self.country=='FJ1':
        #     raise ValueError('There is an error with FJ1')
        if self.multiFactor:
            listFactorOutPaths = []
            for fac in self.factorList:
                data = pd.DataFrame(np.random.randn(10,1)*100)
                path = os.path.join(self.factorDir, self.country, fac + '.csv')
                if not os.path.exists(os.path.dirname(path)):
                    os.mkdir(os.path.dirname(path))
                data.to_csv(path, header=False, index=False, line_terminator='\n')
                listFactorOutPaths.append(path)
            
            with self.output().open('w') as outfile:
                # print list of factor paths to the outfile
                pd.DataFrame(listFactorOutPaths).to_csv(outfile, header=False, index=False, line_terminator='\n')
        else:
            with self.output().open('w') as outfile:
                # output 10 random numbers per country, multiplied by 100
                pd.DataFrame(np.random.randn(10,1)*100).to_csv(outfile, header=False, index=False, line_terminator='\n')
    
    def output(self) :
        # ctryStr = self.country if self.country else 'All'
        return luigi.LocalTarget(os.path.join(
            self.logDir, 
            'CalcData_{}_{}.csv'.format(self.country, self.runDate.strftime('%Y%m%d'))
            ))


if __name__ == '__main__':
    luigi.run()