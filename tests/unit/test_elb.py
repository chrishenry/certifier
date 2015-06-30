# This file is part of Certifier.
# Copyright 2015, Behance Ops.

"""Tests for the the EC2 service class"""

import os
import sys
import time
import ConfigParser
from tests.unit import CertifierTestCase
import mock
from mock import patch
from mock import Mock
from nose.plugins.attrib import attr

from moto import mock_elb

from certifier.elb import *

class ElbTestCase(CertifierTestCase):

    def setUp(self):
        super(ElbTestCase, self).setUp()

    @attr(elb=True)
    @mock_elb
    def test_get_elbs(self):

        creds = {
            'aws_access_key_id': '',
            'aws_secret_access_key': ''
        }

        elbs = get_elbs(creds)
