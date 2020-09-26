# AWS MFA Delete Operations

## Setup

This is a simple example of how to enable MFA delete on an Amazon S3 bucket.

Note: these instructions have been tested on MacOS.

Install the Python virtualenv

    ./venv.sh

Activate the virtualenv

    source ./.venv/bin/activate

Install dependencies

    pip3 install -r freeze.txt

## Enabling MFA Delete

First, authenticate MFA:

    export AWS_ACCESS_KEY_ID=<key>
    export AWS_SECRET_ACCESS_KEY=<secret_access_key>

Obtain the device serial number.  The string without the quotes should be copied, for example `arn:aws:iam::123456789012:mfa/root-account-mfa-device`

    aws iam list-mfa-devices

Run `enable-mfa-delete.py`

    > ./enable-mfa-delete.py
    Bucket: mfadeletetestdevopsrockstars
    <deviceSerialNumber> <tokenCode>: arn:aws:iam::123456789012:mfa/root-account-mfa-device 123456

Verify that it is enabled

    > aws s3api get-bucket-versioning --bucket mfadeletetestdevopsrockstars
    {
    "Status": "Enabled",
    "MFADelete": "Enabled"
    }

Deactivate the virtualenv

    deactivate

## Disabling MFA Delete

First, authenticate MFA:

    export AWS_ACCESS_KEY_ID=<key>
    export AWS_SECRET_ACCESS_KEY=<secret_access_key>

Obtain the device serial number.  The string without the quotes should be copied, for example `arn:aws:iam::123456789012:mfa/root-account-mfa-device`

    aws iam list-mfa-devices

Run `disable-mfa-delete.py`

    > ./disable-mfa-delete.py
    Bucket: mfadeletetestdevopsrockstars
    <deviceSerialNumber> <tokenCode>: arn:aws:iam::123456789012:mfa/root-account-mfa-device 123456

Verify that it is enabled

    > aws s3api get-bucket-versioning --bucket mfadeletetestdevopsrockstars
    {
    "Status": "Suspended",
    "MFADelete": "Disabled"
    }

Deactivate the virtualenv

    deactivate

## Testing MFA delete (can't permanetly delete without MFA)

Create, upload, delete an object, then verify its deleted.

    echo test > test.txt
    aws s3 cp test.txt s3://mfadeletetestdevopsrockstars
    aws s3 ls s3://mfadeletetestdevopsrockstars/test.txt
    aws s3 rm s3://mfadeletetestdevopsrockstars/test.txt

See the deleted version and delete marker

    aws s3api list-object-versions --bucket mfadeletetestdevopsrockstars

Try to delete the deleted version (or the delete marker)

    aws s3api delete-object --bucket mfadeletetestdevopsrockstars --key test.txt --version-id=OcBXW1i5.roITx9Zo58jasvMnu7RWCkj
    An error occurred (AccessDenied) when calling the DeleteObject operation: Mfa Authentication must be used for this request

## Restore of deleted file when MFA delete is enabled

Essentially delete all `DeleteMarker` entries from `aws s3api list-object-versions --bucket mfadeletetestdevopsrockstars`

    aws s3api delete-object --bucket mfadeletetestdevopsrockstars --key test.txt --version-id=XhJwYocN_4pGw6uolmVdd0CQ7DYpSS7i --mfa 'arn:aws:iam::123456789012:mfa/root-account-mfa-device 123456'
