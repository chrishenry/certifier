# This file is part of Certifier.
# Copyright 2015, Behance Ops.

"""Tests for the the Certificate service class"""

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
from certifier.certificate import *

class CertificateTestCase(CertifierTestCase):

    def setUp(self):
        super(CertificateTestCase, self).setUp()

    def test_pyopenssl_callback(self):

        pyopenssl_check_callback(None, None, None, None, None).should.be.ok
