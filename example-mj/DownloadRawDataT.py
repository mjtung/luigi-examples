from datetime import datetime
import os
import luigi
import pandas as pd
import numpy as np

class DownloadRawDataT(luigi.Task) :
    runDate      = luigi.DateParameter()
    # country      = luigi.Parameter()
    # lstCountries = ['AA', 'AN', 'FC', 'FH', 'FS', 'FA', 'FJ1', 'FJ2', 'FM', 'FT', 'FI', 'FL']
    logDir       = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')

    # def __init__(self, date):
    #     self.runDate = date

    def requires(self):
        return None

    def run(self):
         with self.output().open('w') as outfile:
            pd.DataFrame(np.random.randn(100,1)).to_csv(outfile, header=False, index=False, line_terminator='\n')          
    
    def output(self) :
        return luigi.LocalTarget(os.path.join(
            self.logDir, 
            'DownloadRawData_{}.txt'.format(self.runDate.strftime('%Y%m%d'))
            ))


if __name__ == '__main__':
    luigi.run()