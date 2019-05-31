# Enabling MFA Delete

This is a simple example of how to enable MFA delete on an Amazon S3 bucket.

Note: these instructions have been tested on MacOS.

Install the Python virtualenv

    ./venv.sh

Activate the virtualenv

    source ./.venv/bin/activate

Obtain the device serial number.  The string without the quotes should be copied, for example `arn:aws:iam::123456789012:mfa/root-account-mfa-device`

    aws iam list-mfa-devices

Run `enable-mfa-delete.py`

    > ./enable-mfa-delete.py
    Enter the name of the bucket that you want to enable MFA-delete on: mfadeletetestdevopsrockstars
    Enter your MFA serial number and token code, e.g. <deviceSerialNumber> <tokenCode>: arn:aws:iam::123456789012:mfa/root-account-mfa-device 123456

Verify that it is enabled

    > aws s3api get-bucket-versioning --bucket mfadeletetestdevopsrockstars
    {
    "Status": "Enabled",
    "MFADelete": "Enabled"
    }
   
Deactivate the virtualenv

    deactivate

