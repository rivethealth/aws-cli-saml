#!/usr/bin/env python3
import setuptools
import os

version = {}
with open("awscli_saml/version.py", "r") as f:
    exec(f.read(), version)

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    author="Rivet Health",
    author_email="ops@rivethealth.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
    ],
    description="Authenticate AWS CLI with SAML",
    entry_points={"console_scripts": ["aws-saml=awscli_saml.main:main",]},
    install_requires=["boto3"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="awscli-saml",
    packages=setuptools.find_packages(),
    project_urls={"Issues": "https://github.com/rivethealth/aws-saml-cli/issues",},
    url="https://github.com/rivethealth/aws-saml-cli",
    version=version["__version__"],
)
