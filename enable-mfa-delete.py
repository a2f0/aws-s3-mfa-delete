#!/usr/bin/env python
import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
s3_bucket = boto3.resource('s3')
bucket_name = input('Enter the name of the bucket that you want to enable MFA-delete on: ')
mfa_token = input('Enter your MFA serial number and token code, e.g. <deviceSerialNumber> <tokenCode>: ')

try:
    s3_bucket.meta.client.head_bucket(Bucket=bucket_name)
except ClientError as e:
    if int(e.response['Error']['Code']) == 404:
        print('Bucket does not exist')
        exit()

try:
    s3_client.put_bucket_versioning(Bucket = bucket_name,
                                MFA = mfa_token,
                                VersioningConfiguration = {
                                    'MFADelete' : 'Enabled',
                                    'Status' : 'Enabled'
                                    }
                                )
except ClientError as e:
    print(e)