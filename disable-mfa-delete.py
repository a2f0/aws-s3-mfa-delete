#!/usr/bin/env python3
import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
s3_bucket = boto3.resource('s3')
bucket_name = input('Bucket: ')
mfa_token = input('<deviceSerialNumber> <tokenCode>: ')

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
                                    'MFADelete' : 'Disabled',
                                    'Status' : 'Suspended'
                                    }
                                )
except ClientError as e:
    print(e)