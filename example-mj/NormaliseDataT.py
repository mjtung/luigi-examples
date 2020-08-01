from datetime import datetime
import os
import luigi
import pandas as pd
import numpy as np
from CalcDataT import CalcDataT

class NormaliseDataT(luigi.Task) :
    runDate      = luigi.DateParameter()
    country      = luigi.Parameter(default = "")
    lstCountries = ['AA', 'AN', 'FC', 'FH', 'FS', 'FA', 'FJ1', 'FJ2', 'FM', 'FT', 'FI', 'FL']
    logDir       = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')

    # def __init__(self, date):
    #     self.runDate = date

    def requires(self):
        lstRequiredTasks = []
        if not self.country:
            for x in self.lstCountries:
                lstRequiredTasks.append(NormaliseDataT(runDate = self.runDate, country=x))
        else:
            return CalcDataT(runDate = self.runDate, country = self.country)
        
        return lstRequiredTasks

    def run(self):
        if self.country:
            # open the input file (determined by requirements), and normalize data
            with self.input().open('r') as infile:
                rawData = np.loadtxt(infile)
                outData = (rawData - np.mean(rawData)) / np.std(rawData)
                # write normalized data to output file
                with self.output().open('w') as outfile:
                    pd.DataFrame(outData).to_csv(outfile, header=False, index=False, line_terminator='\n')
        else:            
            with self.output().open('w') as outfile:
                outfile.write('NormData')            
    
    def output(self) :
        ctryStr = self.country if self.country else 'All'
        return luigi.LocalTarget(os.path.join(
            self.logDir, 
            'NormData_{}_{}.csv'.format(ctryStr, self.runDate.strftime('%Y%m%d'))
            ))


if __name__ == '__main__':
    luigi.build([NormaliseDataT(runDate=datetime.strptime('2013-01-08', '%Y-%m-%d'), country='FJ1')]) #datetime.strptime('2013-01-05','%Y-%m-%d')])
    # luigi.run()