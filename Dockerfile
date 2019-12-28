FROM alpine:3.11

RUN apk add python3 \
    && pip3 install boto3 \
    && ln -s /usr/bin/python3 /usr/local/bin/python

COPY aws-saml.py /usr/local/bin/aws-saml

ENTRYPOINT [ "/usr/local/bin/aws-saml" ]
