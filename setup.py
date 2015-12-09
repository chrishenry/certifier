#!/usr/bin/env python
from __future__ import unicode_literals
from setuptools import setup, find_packages

install_requires = [
    "clint==0.3.4",
    "boto3==1.2.2",
    "boto==2.38.0",
    "cement==2.4.0",
    "tabulate==0.7.3",
    "pygerduty==0.28",
    "pyopenssl==0.13.0",
    "termcolor==1.1.0",
]

setup(
    name='certifier',
    version='0.0.1',
    description='Automated SSL Cert Checker',
    author='Behance Ops',
    author_email='devops-behance@adpbe.com',
    url='https://github.com/behanceops/certifier',
    packages=find_packages(exclude=("tests", "tests.*")),
    install_requires=install_requires,
    license="Apache",
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Testing",
    ],
)
