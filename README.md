# AWS SAML CLI

Authenticate AWS CLI with SAML.

## Install

```sh
pip install boto3
```

Download [`aws-saml.py`](aws-saml.py).

## Usage

1. Obtain a SAML authentication response (e.g. using Chrome extension https://github.com/rivethealth/chrome-saml).

2. Run `aws-saml.py`, providing the base64-encoding SAML response.

Credentials are now saved to `~/.aws/credentials`, which will be used by the AWS CLI.

## Options

Options may be provided on the command line, or be saved in the profile configuration in `~/.aws/config`.

```
usage: aws-saml [-h] [-p PROFILE] [-d SESSION_DURATION] [-i IDP_ARN]
                [-r ROLE_ARN]

optional arguments:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        AWS profile name. Defaults to AWS_PROFILE or
                        'default'.
  -d SESSION_DURATION, --session-duration SESSION_DURATION
                        Session duration in seconds. Defaults to
                        saml.session_duration or 3600.
  -i IDP_ARN, --idp-arn IDP_ARN
                        Authenticating SAML provider ARN. Defaults to
                        saml.idp_arn.
  -r ROLE_ARN, --role-arn ROLE_ARN
                        Assumed IAM role ARN. Defaults to saml.role_arn.
```
