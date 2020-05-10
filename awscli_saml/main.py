import argparse
from .version import __version__

def main():
    parser = argparse.ArgumentParser("aws-saml")
    parser.add_argument(
        "-p",
        "--profile",
        help="AWS profile name. Defaults to AWS_PROFILE or 'default'.",
    )
    parser.add_argument(
        "-d",
        "--session-duration",
        type=int,
        help="Session duration in seconds. Defaults to saml.session_duration or 3600.",
    )
    parser.add_argument(
        "-i",
        "--idp-arn",
        help="Authenticating SAML provider ARN. Defaults to saml.idp_arn.",
    )
    parser.add_argument(
        "-r", "--role-arn", help="Assumed IAM role ARN. Defaults to saml.role_arn."
    )
    parser.add_argument(
        "-s",
        "--saml",
        help="Base64 encoded SAML assertion. Defaults to SAML_ASSERTION, or stdin.",
    )
    parser.add_argument(
        "-l",
        "--legacy",
        action="store_true",
        help="Adds backward compatible aws_security_token value to support legacy clients.",
    )

    args = parser.parse_args()

    import awscli_saml.assume_role as assume_role

    assume_role.run(
        profile=args.profile,
        session_duration=args.session_duration,
        idp_arn=args.idp_arn,
        role_arn=args.role_arn,
        saml=args.saml,
    )
