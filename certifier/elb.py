
from certifier import aws_credentials
import boto.ec2.elb

def certify_elbs(aws_credentials, region='ue1'):

    return get_elbs(aws_credentials)

def get_elbs(aws_credentials, region='us-east-1'):

    conn = boto.ec2.elb.connect_to_region('us-east-1',
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

