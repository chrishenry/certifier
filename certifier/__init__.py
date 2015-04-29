
import os
import re
import platform
import argparse
import ConfigParser

from datetime import datetime, timedelta

import pygerduty

__version__ = '0.0.1'
__author__ = 'Behance Ops'

def format_arn(arn):
    return arn.split(':')[-1]

def format_elb_dns_name(dns_name):
    return dns_name.split('.')[0]

def within_danger(expiry, days_before_expiry=60):
    """Check that the expiration date is greater than `days_before_expiry` away"""

    if expiry is None:
        return (False, 'NA')

    # If today + `days_before_expiry` is after the expiry, scream.
    danger_date = datetime.now() + timedelta(days=days_before_expiry)

    # Calculate how many days until expiry
    diff = (expiry - datetime.now()).days

    if danger_date > expiry:
        return (True, diff)
    else:
        return (False, diff)

def pd_create_event(certification, resource_type):

    if not os.environ.get('PD_KEY') or not os.environ.get('PD_SERVICE_KEY'):
        raise Exception("Set PD_KEY and PD_SERVICE_KEY")

    # Send pager duty alert
    pd_key = os.environ.get('PD_KEY')
    pd_service_key = os.environ.get('PD_SERVICE_KEY')

    if resource_type == 'elb':

        description = "ELB %s's SSL cert expires soon." % certification['dns_name']
        incident_key = "ELB-%s/SSL_EXPIRY" % certification['dns_name']
        details = "ELB %s's' with cert %s, expires in %s days" % \
                    (certification['dns_name'], certification['arn'], certification['days_til_expiry'])

    if resource_type == 'cloudfront':

        description = "Distribution %s's SSL cert expires soon." % certification['dns_name']
        incident_key = "CDN-%s/SSL_EXPIRY" % certification['dns_name']
        details = "Distribution %s expires in %s days" % \
                    (certification['dns_name'], certification['days_til_expiry'])

    if resource_type == 'domain':
        description = "Domain %s's SSL cert expires soon." % certification['dns_name']
        incident_key = "DOMAIN-%s/SSL_EXPIRY" % certification['dns_name']
        details = "Distribution %s expires in %s days" % \
                    (certification['dns_name'], certification['days_til_expiry'])


    try:

        pager = pygerduty.PagerDuty("behance", pd_key)
        pager.create_event(
            pd_service_key,
            description,
            'trigger',
            details,
            incident_key
        )

    except Exception as e:
        print e
        raise


def aws_credentials(credentials_file, profile):
    """Try to get credentials"""

    try:
        return aws_credentials_env()
    except Exception as e:
        print e

    try:
        return aws_credentials_file(credentials_file, profile)
    except Exception as e:
        print e

    raise ValueError, 'No AWS credentials found'

def aws_credentials_env():

    if not os.environ.get('AWS_ACCESS_KEY_ID'):
        raise ValueError, 'No AWS_ACCESS_KEY_ID env var found'

    if not os.environ.get('AWS_SECRET_ACCESS_KEY'):
        raise ValueError, 'No AWS_SECRET_ACCESS_KEY env var found'

    return {
        'aws_access_key_id': os.environ.get('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': os.environ.get('AWS_SECRET_ACCESS_KEY')
    }

def aws_credentials_file(cfg, profile='Credentials'):
    """Return a dictionary containing aws_access_key_id and aws_secret_access_key, given a file to a credentials file
       in the format expected by AWS tools (as described at http://j.mp/qGGHNp).
    """

    if cfg is None:
        raise ValueError, 'No credentials file found'

    if profile != 'Credentials' and profile != 'default':
        profile = 'profile %s' % profile

    config = ConfigParser.RawConfigParser()

    # preserve case, which is important for cfn
    config.optionxform = str
    config.readfp(cfg)

    if not config.has_section(profile):
        raise ValueError, 'Profile %s doesn\'t exist' % profile

    return {
        'aws_access_key_id': config.get(profile, 'aws_access_key_id'),
        'aws_secret_access_key': config.get(profile, 'aws_secret_access_key')
    }

def add_args(parser):
    """Add arguments to the parser object"""

    parser.add_argument('-k', '--credentials-file',
        metavar='FILE', dest='credentials_file',
        type=argparse.FileType('r'), required=False,
        help='Path to your AWS credentials file (ie /etc/aws-credentials.txt)'
    )
    parser.add_argument('-p', '--profile',
        type=str, default='Credentials', dest='profile',
        help='If using a credentials profile, specify here'
    )
    parser.add_argument('-r', '--region',
        type=str, default='us-east-1',
        choices=['us-east-1', 'us-west-2', 'eu-west-1'],
        help='AWS region, defaults to ue1'
    )
    parser.add_argument('-d', '--days',
        type=int, default=60,
        help='How many days in advance of expiry to alert.'
    )
    parser.add_argument('-e', '--domain',
        type=str, default=None,
        help='A domain to check'
    )

