FROM python:3.8-alpine

CMD pip install boto3

COPY aws-saml.py /usr/bin/local/aws-saml

ENTRYPOINT [ "/usr/bin/local/aws-saml" ]
