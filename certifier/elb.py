
from collections import OrderedDict

import boto.ec2.elb

from socket import *
from certifier import aws_credentials, format_arn, format_elb_dns_name
from exception import CertifierException, CertifierWarningException
from certificate import get_expiry

from OpenSSL import SSL

def certify_elbs(aws_credentials, region='us-east-1'):

    elbs = get_elbs(aws_credentials, region=region)

    retval = []

    for elb in elbs:

        if elb.scheme != 'internet-facing':
            continue

        for listener in elb.listeners:
            if listener[2] != 'HTTPS':
                continue

            expiry = None
            error_msg = None

            try:

                expiry = get_expiry(elb.dns_name)

            except CertifierWarningException as e:
                print "CertifierWarningException"
                print e.host
                print e.message

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

            except timeout as e:
                # print e
                # print e.message
                # print e.args
                # print dir(e)
                # print type(e)

                error_msg = e.message

            retval.append(OrderedDict({
                            'dns_name': format_elb_dns_name(elb.dns_name),
                            'expiry': expiry,
                            'arn': format_arn(listener[4]),
                            'error': error_msg
                        }))

    return retval

def get_elbs(aws_credentials, region='us-east-1'):

    conn = boto.ec2.elb.connect_to_region(region,
                aws_access_key_id=aws_credentials['aws_access_key_id'],
                aws_secret_access_key=aws_credentials['aws_secret_access_key']
            )

    all_elbs = []
    marker = None

    while True:
        response = conn.get_all_load_balancers(marker=marker)

        # build our elb list
        all_elbs.extend(response)

        # ensure that we get every elb
        if response.next_marker:
            marker = response.next_marker
        else:
            break

    return all_elbs

