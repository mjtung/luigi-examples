from luigi.contrib.s3 import S3Target
import boto3
import botocore

BUCKET = 'mjtung-luigi-example'

def getCountryKeyForFactorS3(runDate, country, factor, isNorm):
    normOrCalc = 'Norm' if isNorm else 'Calc'
    return 'factors/{}/{}/{}Data_{}.csv'.format(runDate.strftime('%Y%m%d'), country, normOrCalc, factor)

def getS3Target(client, path):
    return S3Target('s3://' + BUCKET + '/' + path, client=client)

def s3FileExists(key):
    # return True if file exists and has file size
    # raise Exception if file exists and is empty
    # return False if file does not exist
    try:
        s3 = boto3.client('s3')
        response = s3.head_object(Bucket=BUCKET, Key=key)
        if response['ContentLength'] <= 0:
            raise Exception('Output file {} is empty'.format(key))       
    except botocore.exceptions.ClientError:
        # This error occurs if file does not exist
        return False  

    return True
