# This file is part of Certifier.
# Copyright 2015, Behance Ops.

"""Tests for the the EC2 service class"""

import os
import sys
import time
import ConfigParser
from tests.unit import CertifierTestCase
import sure
import mock
from mock import patch
from mock import Mock
from nose.plugins.attrib import attr

import boto.ec2.elb as elb


from moto import mock_elb

from certifier.elb import *

class ElbTestCase(CertifierTestCase):

    creds = {
        'aws_access_key_id': '',
        'aws_secret_access_key': ''
    }

    def setUp(self):
        super(ElbTestCase, self).setUp()

    @attr(elb=True)
    @mock_elb
    def test_get_empty_elbs(self):

        elbs = get_elbs(self.creds)
        elbs.should.be.empty

        elbs = get_elbs(self.creds, region='us-west-2')
        elbs.should.be.empty

    @attr(elb=True)
    @mock_elb
    def test_get_elbs(self):

        for x in range(0,50):
            self.create_elb()

        elbs = get_elbs(self.creds)
        len(elbs).should.equal(50)

    def create_elb(self, scheme='internet-facing'):

        name = self.random_name()

        conn = elb.connect_to_region('us-east-1')

        zones = ['us-east-1a', 'us-east-1b']
        ports = [(80, 80, 'http'), (443, 80, 'https', 'arn:aws:iam::1234567890123:server-certificate/my.nifty.cert.net')]
        lb = conn.create_load_balancer(name, zones, ports, scheme=scheme)

