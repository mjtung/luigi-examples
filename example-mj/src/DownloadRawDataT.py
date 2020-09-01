from datetime import datetime
import os
import luigi
import pandas as pd
import numpy as np
from luigi.contrib.s3 import S3Client
import boto3
import botocore
import utilFuncs
# import sys
from ForceableTask import ForceableTask

class DownloadRawDataT(luigi.Task) :
    runDate      = luigi.DateParameter()
    # country      = luigi.Parameter()
    # lstCountries = ['AA', 'AN', 'FC', 'FH', 'FS', 'FA', 'FJ1', 'FJ2', 'FM', 'FT', 'FI', 'FL']
    logDir       = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'output')
    # bucket       = utilFuncs.BUCKET

    def requires(self):
        return None

    def run(self):
        with self.output().open('w') as outfile:
            pd.DataFrame(np.random.randn(100,1)).to_csv(outfile, header=False, index=False, line_terminator='\n')          
    
    def complete(self):
        try:
            s3 = boto3.client('s3')
            response = s3.head_object(Bucket=utilFuncs.BUCKET, Key=self.getKeyS3())
            if response['ContentLength'] <= 0:
                raise Exception('Output file {} is empty'.format(self.getKeyS3()))          
        except botocore.exceptions.ClientError:
            # This error occurs when the task is not yet complete
            return False
        except Exception as e:
            # All other errors
            print(e)
            return False   

        return True

    def output(self) :
        # return luigi.LocalTarget(os.path.join(
        #     self.logDir, 
        #     'DownloadRawData_{}.txt'.format(self.runDate.strftime('%Y%m%d'))
        #     ))
        # client = S3Client()
        # return S3Target('s3://' + self.bucket + '/' + self.getKeyS3(), client=client)
        return utilFuncs.getS3Target(S3Client(), self.getKeyS3())

    def getKeyS3(self):
        return 'rawdata/downloadedDataFor{}.csv'.format(self.runDate.strftime('%Y%m%d'))


if __name__ == '__main__':
    luigi.run()