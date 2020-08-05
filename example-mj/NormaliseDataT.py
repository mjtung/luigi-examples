from datetime import datetime
import os
import luigi
import pandas as pd
import numpy as np
from CalcDataT import CalcDataT

class NormaliseDataT(luigi.Task) :
    runDate      = luigi.DateParameter()
    country      = luigi.Parameter(default = "")
    multiFactor  = luigi.BoolParameter(default = False, parsing=luigi.BoolParameter.EXPLICIT_PARSING)
    lstCountries = ['AA', 'AN', 'FC', 'FH', 'FS', 'FA', 'FJ1', 'FJ2', 'FM', 'FT', 'FI', 'FL']
    logDir       = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')
    factorDir    = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'factors')
    # def __init__(self, date):
    #     self.runDate = date

    def requires(self):
        lstRequiredTasks = []
        if not self.country:
            for x in self.lstCountries:
                lstRequiredTasks.append(NormaliseDataT(runDate=self.runDate, country=x, multiFactor=self.multiFactor))
        else:
            return CalcDataT(runDate=self.runDate, country=self.country, multiFactor=self.multiFactor)
        
        return lstRequiredTasks
    
    def getOutputFactorFilePath(self, factorName):
        return os.path.join(self.factorDir, self.country, 'norm' + factorName + '.csv')
    
    def getFactorNameFromPath(self, factorPath):
        return os.path.splitext(os.path.basename(factorPath))[0]

    def run(self):
        if self.country:            
            if self.multiFactor:
                factors = {}
                normFactors = {}
                # input file stores the list of factor files that are the requirements
                with self.input().open('r') as infile: 
                # with open('listOfFiles', 'r') as infile:
                    factorInFiles = pd.read_csv(infile)
                
                # loop through each factor in listed in the infile
                for factorPath in factorInFiles:                
                    fac = self.getFactorNameFromPath(factorPath)
                    # read factor CSV
                    factors[fac] = pd.read_csv(factorPath)
                    # normalise factors
                    normFactors[fac] = (factors[fac] - np.mean(factors[fac])) / np.std(factors[fac]) 
                    # write normalised data to output factor files
                    factorOutPath = self.getOutputFactorFilePath(fac)
                    if not os.path.exists(os.path.dirname(factorOutPath)):
                        os.mkdir(os.path.dirname(factorOutPath))
                    normFactors[fac].to_csv(factorOutPath, header=False, index=False, line_terminator='\n')
                                        
                # create list of out factor filenames
                factorOutFiles = [self.getOutputFactorFilePath(x) for x in normFactors.keys()]
                
                # write filenames to output file
                with self.output().open('w') as outfile:
                    pd.DataFrame(factorOutFiles).to_csv(outfile, header=False, index=False, line_terminator='\n')                
            else:
                # open the input file (determined by requirements), and normalise data
                with self.input().open('r') as infile:
                    rawData = np.loadtxt(infile)
                    outData = (rawData - np.mean(rawData)) / np.std(rawData)
                # write normalised data to output file
                with self.output().open('w') as outfile:
                    pd.DataFrame(outData).to_csv(outfile, header=False, index=False, line_terminator='\n')
        else:            
            with self.output().open('w') as outfile:
                outfile.write('NormData - All Countries done')            
    
    def output(self) :
        ctryStr = self.country if self.country else 'All'
        return luigi.LocalTarget(os.path.join(
            self.logDir, 
            'NormData_{}_{}.csv'.format(ctryStr, self.runDate.strftime('%Y%m%d'))
            ))


if __name__ == '__main__':
    luigi.build([NormaliseDataT(runDate=datetime.strptime('2013-01-08', '%Y-%m-%d'), country='FJ1', multiFactor=True)]) #datetime.strptime('2013-01-05','%Y-%m-%d')])
    # luigi.run()