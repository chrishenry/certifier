# This file is part of Certifier.
# Copyright 2015, Behance Ops.

"""Tests for the the certifier helper functions"""

import os
import sys
import time
import ConfigParser
from tests.unit import CertifierTestCase
import sure
import mock
import datetime
from mock import patch
from mock import Mock
from nose.plugins.attrib import attr

from certifier import *

class CertifierHelperTestCase(CertifierTestCase):

    def setUp(self):
        super(CertifierHelperTestCase, self).setUp()

    @attr(helper=True)
    def test_format_arn(self):

        cert_arn_name = "arn:aws:iam::11234552345:server-certificate/cloudfront/wildcard.domain.biz-cloudfront"

        retval = format_arn(cert_arn_name)
        retval.should.equal("server-certificate/cloudfront/wildcard.domain.biz-cloudfront")

    @attr(helper=True)
    def test_format_elb_dns_name(self):

        elb_dns_name = "elb-name-regions-11234552345.us-east-1.elb.amazonaws.com"

        retval = format_elb_dns_name(elb_dns_name)
        retval.should.equal("elb-name-regions-11234552345")

    @attr(helper=True)
    def test_within_danger(self):

        my_none = within_danger(None)
        my_none[0].should.equal(False)
        my_none[1].should.equal('NA')

        expiry = datetime.now() + timedelta(days=12)
        within_danger(expiry)[0].should.equal(True)

        expiry = datetime.now() + timedelta(days=120)
        within_danger(expiry)[0].should.equal(False)
