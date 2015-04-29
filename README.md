# Certifier

Manually maintaining lists of SSL certs that have been deployed to AWS is
tedious and error prone. This tool will check deployed ssl certs deployed to
Cloudfront distributions and ELBs.

## AWS Authentication

Certifier will will look for credentials in the following order;

* Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`).
* Configuration file, passed via the `-k` / `--credentials-file` option.

Config files follow the same structure as [AWS CLI config files](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-config-files)

```text
[default]
aws_access_key_id=KLJJHGKJHGKJHGKJHG
aws_secret_access_key=KJHGKJGKJHGKHGKHJGKJHGKHGKJHG
```

Additionally, configuration for multiple accounts can be stored in a single
file using profiles.

```text
[profile prod]
aws_access_key_id=KLJJHGKJHGKJHGKJHG
aws_secret_access_key=KJHGKJGKJHGKHGKHJGKJHGKHGKJHG
```

When using profiles, use the `-p` / `--profile` flag to pass the profile to
check.

## Pagerduty Authentication

Certifier uses environment variables for configuring PagerDuty.
PagerDuty requires that you have an API key, which can be found at
[https://you.pagerduty.com/api_keys](https://you.pagerduty.com/api_keys). This
allows you to make API calls.

In addition, you need a service key, which identifies the escalation policies
configured on the PagerDuty side. You can create a new service at
[https://you.pagerduty.com/services](https://you.pagerduty.com/services).

```bash
export PD_KEY=putyourrealapikeyhere
export PD_SERVICE_KEY=thisisyourservicekey
```

## Usage

```
± |initial ✓| → ./bin/certifier --help
usage: certifier (sub-commands ...) [options ...] {arguments ...}

CLI for Certifier.

commands:

  cloudfront
    Check CloudFront certs

  elb
    Check ELB certs

  test-pd
    Test the Pager Duty Integration

optional arguments:
  -h, --help            show this help message and exit
  --debug               toggle debug output
  --quiet               suppress all output
  -k FILE, --credentials-file FILE
                        Path to your AWS credentials file (ie /etc/aws-
                        credentials.txt)
  -p PROFILE, --profile PROFILE
                        If using a credentials profile, specify here
  -r {us-east-1,us-west-2,eu-west-1}, --region {us-east-1,us-west-2,eu-west-1}
                        AWS region, defaults to ue1
  -d DAYS, --days DAYS  How many days in advance of expiry to alert.
```

## Caveats

When certifier checks infrastructure, it may not necessarily know the correct
DNS name, so name-based checking can __not__ be a feature. However, the main
goal is to check expiration, which is entirely possible via an SSL connection.

When checking cloudfront, we __do__ need to use the cname provided via the api.
This is because Cloudfront will use it's own certificate (*.cloudfront.com) when
serving SSL over the default dns name.


