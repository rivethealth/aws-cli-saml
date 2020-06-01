# AWS SAML CLI

[![PyPi](https://img.shields.io/pypi/v/awscli-saml)](https://pypi.org/project/awscli-saml/)

Authenticate AWS CLI with SAML.

## Install

### [Pip](https://pypi.org/project/awscli-saml/)

```sh
pip install awscli-saml
```

Run as

```sh
aws-saml
```

### [Docker](https://hub.docker.com/r/rivethealth/aws-saml)

```sh
docker pull rivethealth/aws-saml
```

Run as

```sh
docker run -it -v ~/.aws:/root/.aws rivethealth/aws-saml
```

## Usage

1. Obtain a SAML authentication response (e.g. using Chrome extension https://github.com/rivethealth/chrome-saml).

2. Run `aws-saml` command, providing the base64-encoded SAML response.

Credentials are now saved to `~/.aws/credentials`, which will be used by the AWS CLI.

## Options

Options may be provided on the command line, or be saved in the profile configuration in `~/.aws/config`.

```
usage: aws-saml [-h] [-p PROFILE] [-e REGION] [-d SESSION_DURATION] [-i IDP_ARN]
                [-r ROLE_ARN] [-v]
                [saml]

positional arguments:
  saml                  Base64 encoded SAML assertion. Defaults to
                        SAML_ASSERTION, or stdin.

optional arguments:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        AWS profile name. Defaults to AWS_PROFILE or
                        'default'.
  -e REGION, --region   REGION
                        AWS region. Defaults to AWS_DEFAULT_REGION.
  -d SESSION_DURATION, --session-duration SESSION_DURATION
                        Session duration in seconds. Defaults to
                        saml.session_duration or 3600.
  -i IDP_ARN, --idp-arn IDP_ARN
                        Authenticating SAML provider ARN. Defaults to
                        saml.idp_arn.
  -r ROLE_ARN, --role-arn ROLE_ARN
                        Assumed IAM role ARN. Defaults to saml.role_arn.
  -v, --version         show program's version number and exit
```
