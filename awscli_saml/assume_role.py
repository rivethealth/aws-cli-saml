import boto3
import botocore
import botocore.config
import configparser
import os
import os.path
import traceback

try:
    input = raw_input
except NameError:
    pass


def run(profile=None, region=None, session_duration=None, idp_arn=None, role_arn=None, saml=None):
    profile_name = profile or os.environ.get("AWS_PROFILE", "default")
    region_name = region or os.environ.get("AWS_DEFAULT_REGION", None)
    section_name = (
        profile_name if profile_name == "default" else "profile {}".format(profile_name)
    )

    config_path = os.environ.get("AWS_CONFIG_FILE") or os.path.expanduser("~/.aws/config")
    cred_path = os.environ.get("AWS_SHARED_CREDENTIALS_FILE") or os.path.expanduser("~/.aws/credentials")

    config = configparser.RawConfigParser()
    config.read(config_path)


    try:
        session_duration = session_duration or config.getint(
            section_name, "saml.session_duration")
    except configparser.NoOptionError:
        session_duration = 3600

    principal_arn = idp_arn or config.get(section_name, "saml.idp_arn")
    role_arn = role_arn or config.get(section_name, "saml.role_arn")
    try:
        region_name = region_name or config.get(section_name, "region")
    except configparser.NoOptionError:
        pass

    # would use getpass, but truncates to terminal max 4096
    saml_assertion = saml or os.environ.get("SAML_ASSERTION")
    if not saml_assertion:
        try:
            import readline  # needed for terminal raw mode (> 4096 characters)
        except:
            print("Failed to load readline\n{}".format(traceback.format_exc()))
        saml_assertion = input("Base64 encoded SAML response:\n")

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
    if region_name is not None:
        cred.set(profile_name, "region", region_name)
    else:
        cred.remove_option(profile_name, "region")
    cred.set(
        profile_name,
        "aws_secret_access_key",
        response["Credentials"]["SecretAccessKey"],
    )
    cred.set(profile_name, "aws_session_token", response["Credentials"]["SessionToken"])
    # Duplicate aws_session_token to aws_security_token to support legacy AWS clients.
    cred.set(
        profile_name, "aws_security_token", response["Credentials"]["SessionToken"]
    )

    cred.set(
        profile_name,
        "aws_session_expiration",
        response["Credentials"]["Expiration"].strftime("%Y-%m-%dT%H:%M:%S%z"),
    )

    with open(cred_path, "w+") as f:
        cred.write(f)

    print(
        "Credentials saved for {}. Expire {}.".format(
            profile_name, response["Credentials"]["Expiration"]
        )
    )
