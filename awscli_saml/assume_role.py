import boto3
import botocore
import botocore.config
import configparser
import os
import os.path
import readline  # needed for terminal raw mode (> 4096 characters)

try:
    input = raw_input
except NameError:
    pass


def run(profile=None, session_duration=None, idp_arn=None, role_arn=None, saml=None, legacy_support=False):
    profile_name = profile or os.environ.get("AWS_PROFILE", "default")
    section_name = (
        profile_name if profile_name == "default" else "profile {}".format(profile_name)
    )

    config_path = os.path.expanduser("~/.aws/config")
    cred_path = os.path.expanduser("~/.aws/credentials")

    config = configparser.RawConfigParser()
    config.read(config_path)

    session_duration = session_duration or config.getint(
        section_name, "saml.session_duration"
    )
    principal_arn = idp_arn or config.get(section_name, "saml.idp_arn")
    role_arn = role_arn or config.get(section_name, "saml.role_arn")

    # would use getpass, but truncates to terminal max 4096
    saml_assertion = (
        saml
        or os.environ.get("SAML_ASSERTION")
        or input("Base64 encoded SAML response:\n")
    )

    sts = boto3.client(
        "sts", config=botocore.config.Config(signature_version=botocore.UNSIGNED)
    )
    response = sts.assume_role_with_saml(
        DurationSeconds=session_duration,
        PrincipalArn=principal_arn,
        RoleArn=role_arn,
        SAMLAssertion=saml_assertion,
    )

    cred = configparser.RawConfigParser()
    cred.read(cred_path)

    if not cred.has_section(profile_name):
        cred.add_section(profile_name)

    cred.set(profile_name, "aws_access_key_id", response["Credentials"]["AccessKeyId"])
    cred.set(
        profile_name,
        "aws_secret_access_key",
        response["Credentials"]["SecretAccessKey"],
    )
    cred.set(profile_name, "aws_session_token", response["Credentials"]["SessionToken"])
    if legacy_support:
        # Duplicate aws_session_token to aws_security_token to support legacy AWS clients.
        cred.set(profile_name, "aws_security_token", response["Credentials"]["SessionToken"])
    else:
        # Clear out any existing value if legacy support not enabled
        cred.remove_option(profile_name, "aws_security_token")

    cred.set(
        profile_name, 
        "aws_session_expiration", 
        response["Credentials"]["Expiration"].strftime('%Y-%m-%dT%H:%M:%S%z')
    )

    with open(cred_path, "w+") as f:
        cred.write(f)

    print(
        "Credentials saved for {}. Expire {}.".format(
            profile_name, response["Credentials"]["Expiration"]
        )
    )
