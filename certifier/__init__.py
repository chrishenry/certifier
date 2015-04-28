
import os
import re
import platform
import argparse
import ConfigParser

__version__ = '0.0.1'
__author__ = 'Behance Ops'

USER_AGENT = 'BehanceOps Certifier/%s Python/%s %s/%s' % (
    __version__,
    platform.python_version(),
    platform.system(),
    platform.release()
)

def parse_aws_credentials_file(cfg):
    """Return a dictionary containing aws_access_key_id and aws_secret_access_key, given a file to a credentials file
       in the format expected by AWS tools (as described at http://j.mp/qGGHNp).
    """

    if os.path.isfile(cfg) is False:
        raise ValueError, 'File %s doesn\'t exist' % cfg

    pass

def add_args(parser):
    """Add arguments to the parser object"""

    parser.add_argument('-k', '--credentials-file',
        metavar='FILE', dest='credentials_file',
        type=argparse.FileType('r'), required=False,
        help='Path to your AWS credentials file (ie /etc/aws-credentials.txt)'
    )
    parser.add_argument('-p', '--profile',
        type=str, default=None,
        help='If using a credentials profile, specify here'
    )
    parser.add_argument('-r', '--region',
        type=str, default='ue1',
        choices=['ue1', 'uw2', 'ew1', 'an1'],
        help='AWS region, defaults to ue1'
    )
