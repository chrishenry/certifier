
from collections import OrderedDict

import pprint

import botocore.session

import boto.cloudfront
from socket import *

from exception import CertifierException, CertifierWarningException
from certificate import get_expiry

from OpenSSL import SSL

def certify_distributions(aws_credentials):

    distributions = get_distributions(aws_credentials)

    retval = []

    for distribution in distributions['DistributionList']['Items']:

        expiry = None
        error_msg = None

        # If there's no CNAME, we're using the *.cloudfront cert
        if 'CloudFrontDefaultCertificate' in distribution['ViewerCertificate'].keys():
            continue


        try:

            cname = distribution['Aliases']['Items'][0]
            expiry = get_expiry(cname)

        except CertifierWarningException as e:
            # print "CertifierWarningException"
            # print e.host
            # print e.message

            error_msg = e.message

        except CertifierException as e:
            # print "CertifierException"
            # print e.host
            # print e.message

            error_msg = e.message

        except SSL.WantReadError as e:
            # print e
            # print e.message
            # print dir(e)
            # print "OpenSSL.SSL.WantReadError"

            error_msg = e.message

        except gaierror as e:
            # print e
            # print e.message
            # print e.args
            # print dir(e)
            # print type(e)

            error_msg = e

        except error as e:
            # print e
            # print e.message
            # print e.args
            # print dir(e)
            # print type(e)

            error_msg = e

        except timeout as e:
            # print e
            # print e.message
            # print e.args
            # print dir(e)
            # print type(e)

            error_msg = e.message


        retval.append(OrderedDict({
                        'dns_name': cname,
                        'expiry': expiry,
                        'arn': None,
                        'error': error_msg
                    }))

    return retval

def get_distributions(aws_credentials):

    session = botocore.session.get_session()
    client = session.create_client('cloudfront',
                region_name='us-east-1',
                aws_access_key_id=aws_credentials['aws_access_key_id'],
                aws_secret_access_key=aws_credentials['aws_secret_access_key'])

    distributions = client.list_distributions()

    return distributions

