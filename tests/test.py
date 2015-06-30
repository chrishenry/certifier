#!/usr/bin/env python
#
# This file is part of Certifier
# Copyright 2015, Behance Ops.

import logging
import sys
import os
import argparse
from nose.core import run

def main():
    description = ("Runs unit and/or integration tests. "
                   "Arguments will be passed on to nosetests. "
                   "See nosetests --help for more information.")
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-t', '--service-tests', action="append", default=[],
                        help="Run tests for a given service.  This will "
                        "run any test tagged with the specified value, "
                        "e.g -t clusters -t instances")
    known_args, remaining_args = parser.parse_known_args()
    attribute_args = []
    for service_attribute in known_args.service_tests:
        attribute_args.extend(['-a', '!notdefault,' + service_attribute])
    if not attribute_args:
        # If the user did not specify any filtering criteria, we at least
        # will filter out any test tagged 'notdefault'.
        attribute_args = ['-a', '!notdefault']
    all_args = [__file__] + attribute_args + remaining_args
    print "nose command:", ' '.join(all_args)
    if run(argv=all_args):
        # run will return True is all the tests pass.  We want
        # this to equal a 0 rc
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
