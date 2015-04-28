# Certifier

Manually maintaining lists of SSL certs that have been deployed to AWS is
tedious and error prone. This tool will check deployed ssl certs deployed to
Cloudfront distributions and ELBs.

## AWS Authentication

Certifier will take AWS creds will look for credentials in the following order;

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
