# This file is part of Certifier.
# Copyright 2014, Behance Ops.

"""Some common testing functionality."""

# Use unittest2 on Python < 2.7.
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os
import sys

sys.path.append("../../certifier")

class CertifierTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
