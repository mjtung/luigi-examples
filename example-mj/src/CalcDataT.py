from datetime import datetime
import os
import luigi
import pandas as pd
import numpy as np
from DownloadRawDataT import DownloadRawDataT
from luigi.contrib.s3 import S3Client
# import boto3
# import botocore
import utilFuncs
from ForceableTask import ForceableTask

class CalcDataT(ForceableTask) :
    runDate      = luigi.DateParameter()
    country      = luigi.Parameter()
    multiFactor  = luigi.BoolParameter(default = False, parsing=luigi.BoolParameter.EXPLICIT_PARSING)    
    # lstCountries = ['AA', 'AN', 'FC', 'FH', 'FS', 'FA', 'FJ1', 'FJ2', 'FM', 'FT', 'FI', 'FL']
    # logDir       = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'output')
    # factorDir    = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'factors')
    factorList   = ['factor1', 'factor2', 'factor3', 'factor4'] # for multiFactor only
    # bucket       = utilFuncs.BUCKET
    # def __init__(self, date):
    #     self.runDate = date

    def requires(self):
        return DownloadRawDataT(runDate=self.runDate)

    def run(self):
        if self.country=='FJ1':
            raise ValueError('There is an error with FJ1')
        with self.input().open('r') as inFile:
            inData = pd.read_csv(inFile, header=None)

        if self.multiFactor:
            listFactorOutPaths = []

            # write individual factor files to the proper date/country key/path
            client = S3Client()
            for n, fac in enumerate(self.factorList):
                data = pd.DataFrame(inData[n*10:(n+1)*10] * 100) # read data from inData
                # path = os.path.join(self.factorDir, self.country, fac + '.csv')
                # if not os.path.exists(os.path.dirname(path)):
                    # os.mkdir(os.path.dirname(path))
                path = utilFuncs.getCountryKeyForFactorS3(self.runDate, self.country, fac, isNorm=False)
                target = utilFuncs.getS3Target(client, path)
                with target.open('w') as targetBuf:
                    data.to_csv(targetBuf, header=False, index=False, line_terminator='\n')
                listFactorOutPaths.append(path)
            
            # write the list of keys/paths to the main output file
            with self.output().open('w') as outfile:
                # print list of factor paths to the outfile
                pd.DataFrame(listFactorOutPaths).to_csv(outfile, header=False, index=False, line_terminator='\n')
            
            self.checkMultiFactorDone(listFactorOutPaths)

        else:
            with self.output().open('w') as outfile:
                # multiply first 10 numbers in inData by 100
                pd.DataFrame(inData[0,10] * 100).to_csv(outfile, header=False, index=False, line_terminator='\n')
    
    def checkMultiFactorDone(self, keys):
        # call s3FileExists on all keys.  s3FileExists will throw exception if file is incomplete
        for key in keys:
            utilFuncs.s3FileExists(key)

    # MJ: perhaps the complete function is not really needed.  As long as the check is done in the run() function
    # def complete(self):
    #     isComplete = self.s3FileExists(key=self.getKeyS3())
        
    #     if self.multiFactor & isComplete:
    #         # open s3 file
    #         # factorFileList = pd.read_csv(self.getKeyS3(), header=None)
    #         # try:
    #         with self.output().open('r') as listFile:
    #             factorFileList = pd.read_csv(listFile, header=None)
    #         # except:
    #             # return False

    #         # read contents
    #         for f in factorFileList.values.squeeze():
    #             try:    
    #                 # check each factor file
    #                 if not self.s3FileExists(f):
    #                     raise Exception('Factor output file {} is missing!'.format(f))
    #                     # returnVal = False 
    #             except:
    #                 print('{} is missing'.format(f))
    #                 isComplete = False
    #     return isComplete

    def output(self):
        # return luigi.LocalTarget(os.path.join(
        #     self.logDir, 
        #     'CalcData_{}_{}.csv'.format(self.country, self.runDate.strftime('%Y%m%d'))
        #     ))
        # client = S3Client()
        # return self.getS3Target(client, self.getKeyS3())
        return utilFuncs.getS3Target(S3Client(), self.getKeyS3())

    def getCountryKeyForFactorS3(self, factor):
        return utilFuncs.getCountryKeyForFactorS3(self.runDate, self.country, factor, isNorm=False)
        # return 'factors/{}/{}/CalcData_{}.csv'.format(self.runDate.strftime('%Y%m%d'), self.country, factor)

    def getKeyS3(self):
        return 'fileLists/CalcData_{}_{}.csv'.format(self.country, self.runDate.strftime('%Y%m%d'))

if __name__ == '__main__':
    luigi.run()