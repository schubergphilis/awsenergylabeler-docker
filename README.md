# awsenergylabeler-docker
```
docker pull ghcr.io/schubergphilis/awsenergylabeler:<VERSION>
```
Lists all SecurityHub findings and recommendations and calculate an Energy Label. 
Container image packaged with [awsenergylabelercli](https://pypi.org/project/awsenergylabelercli/)

This container needs to run with the right permissions to be able to list security findings and calculare the energy label. See [Permissions](#permissions) below.


## Energy Labels
|label|critical + high|medium|low|days open
|-|-|-|-|-
|A =>|0|up to 10|up to 20|less than 15|
|B ==>|up to 10|up to 20|up to 40|less than 30|
|C ===>|up to 15|up to 30|up to 60|less than 60|
|D ====>|up to 20|up to 40|up to 80|less than 90|
|E =====>|up to 25|up to 50|up to 100|less than 120|

## Arguments
Every command line argument is also reflected in an environment variable which gives flexibility. Command line arguments take precedence over environment variables.

|Environment variable name|CLI Argument|Required|Example value|Description|
|-------------------------|------------|--------|-------|-----------|
|AWS_LABELER_LOG_CONFIG|`--log-config` `-l`|No|~/log_config.json (default: `None`)|The location of the logging config json file|
|AWS_LABELER_LOG_LEVEL|`--log-level` `-L`|No|info (default)|Provide the log level. Defaults to info.|
|AWS_LABELER_LANDING_ZONE_NAME|`--landing-zone-name` `-n` |Either LANDING_ZONE_NAME or SINGLE_ACCOUNT_ID must be set|TEST (default: `None`)|Name of the landing zone being scored. This variable is mutually exclusive with SINGLE_ACCOUNT_ID|
|AWS_LABELER_SINGLE_ACCOUNT_ID|`--single-account-id` `-s`|Either SINGLE_ACCOUNT_ID or LANDING_ZONE_NAME must be set|123456789102 (default: `None`)|The AWS Account ID of the single account to score. This should only be used if scoring the entire landing zone is not an option.|
|AWS_LABELER_REGION|`--region` `-r`|Yes|`eu-west-1` (default)|The main region to run the labeler from|
|AWS_LABELER_FRAMEWORKS|`--frameworks` `-f`|No|aws-foundational-security-best-practices (default)|The frameworks to include in the score|
|AWS_LABELER_ALLOWED_ACCOUNT_IDS|`--allowed-account-ids` `-a`|No|123456789102,123456789103 (default: `None`)|A list of account IDs that should be scored. No accounts will be scored EXCEPT for accounts in this list. This variable is mutually exclusive with DENIED_ACCOUNT_IDS|
|AWS_LABELER_DENIED_ACCOUNT_IDS|`--denied-account-ids` `-d`|No|123456789102,123456789103 (default: `None`)|A list of account IDs that should NOT be scored. All accounts will be scored EXCEPT accounts in this list. This variable is mutually exclusive with ALLOWED_ACCOUNT_IDS|
|AWS_LABELER_ALLOWED_REGIONS|`--allowed-regions` `-ar`|No|eu-west-1,eu-central-1 (default: `None`)|A list of regions that should be included. No regions will be included EXCEPT for regions in this list. This variable is mutually exclusive with DENIED_REGIONS|
|AWS_LABELER_DENIED_REGIONS|`--denied-regions` `-dr`|No|eu-west-1,eu-central-1 (default: `None`)|A list of regionss that should NOT be included. All regions will be included EXCEPT regions in this list. This variable is mutually exclusive with ALLOWED_REGIONS|
|AWS_LABELER_EXPORT_PATH|`--export-path` `-p`|Yes if `export metrics` or `export all` is true|/tmp/aws_output (default: `None`)|The location where the output can be stored.|
|AWS_LABELER_EXPORT_METRICS|`--export-metrics` `-em`|No|`False` (default)|Exports metrics/statistics without sensitive findings data in JSON formatted files to the specified directory or S3 location.|
|AWS_LABELER_EXPORT_ALL|`--export-all` `-ea`|No|`True` (default)|Exports metrics/statistics along with sensitive findings data in JSON formatted files to the specified directory or S3 location.|
|AWS_LABELER_TO_JSON|`--to-json` `-j`|No|`False` (default)|Return the report in json format.|

## Permissions
Since the energylabeler can run on either a full Landing Zone, or a single account, different permissions are required.

### Landing zone
The following permissions are required to run on a landing zone.
```
"organizations:DescribeOrganization",
"organizations:ListAccounts",
"organizations:DescribeAccount",
"iam:ListAccountAliases",
"ec2:DescribeRegions",
"securityhub:ListFindingAggregators",
"securityhub:GetFindings"
```
A full example of a policy can be found in the file [EnergyLabelerPolicy_example.json](policy_examples/EnergyLabelerPolicy_example.json)

### Single account
The following permissions are required to run on a single account.
```
"iam:ListAccountAliases",
"ec2:DescribeRegions",
"securityhub:ListFindingAggregators",
"securityhub:GetFindings"
```

A full example of a policy can be found in the file [EnergyLabelerPolicySingle_example.json](policy_examples/EnergyLabelerPolicySingle_example.json)

## Examples

Running the container for your local machine (assuming you already setup `~/.aws` folder with your credentials and config)

```bash
docker run -v ~/.aws:/home/nonroot/.aws ghcr.io/schubergphilis/awsenergylabeler:<VERSION> -s <ACCOUNT_NUMBER>
```

Or running with environment variables set:

```bash
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN ghcr.io/schubergphilis/awsenergylabeler:<VERSION> -s <ACCOUNT_NUMBER> --region eu-west-1
```