# Republishing Agent Interval, Queue Interval Reports and CTR records

### Overview

`s3://bucket/source/ <-- republish*.py --> firehose --> s3://bucket/transformed/`

The Firehose used (and associated role) is created using republish_setup.sh 
which in turn uses historic-intervals.yml

```bash
# in target customer account:
# from working directory: reporting/mi/
scripts/republish/setup.py CLIENT ENV
```

* `CLIENT` is the client name, e.g. `tradeuk`
* `ENV` is the envionment, one of `dev`, `test` or `prod`

This will create 3 temporary firehoses that use the existing Glue db and table definitions
to map the records, for example:

* `kfh-ccm-historic-ai-dev` will use the definition in db/table `gl_ccm_dev.glt_agent_intervals_dev`
* `kfh-ccm-historic-qi-dev` will use the definition in db/table `gl_ccm_dev.glt_queue_intervals_dev`
* `kfh-ccm-historic-ctr-dev` will use the definition in db/table `gl_ccm_dev.glt_agent_intervals_dev`

### Interval Reports

```bash
python republish_intervals.py -t TYPE -f FIREHOSE -p PATH -s START [-e END]
```

* `TYPE` is either `agent` or `queue`
* `FIREHOSE` is the firehose created by `republish_setup.sh` to send to, 
e.g. `kfh-ccm-historic-ai-dev`
* `PATH` is the s3 path to the source files, up to the date component of the filename,
for example: 
`s3://s3-capita-ccm-connect-tradeuk-dev-reporting/historic/agent_interval/source/AgentHistoricInterval-`
* `START` and `END` are the start and end date (inclusive) for files to be retrieved and processed against
and are in the format `YYYY-MM-DD`, for example `2019-03-01`

Note that if the `END` is not specified, then the script will only process the `START` date


### CTR Records

The CTR records will need to be put into a single (flat) source directory.
To help, the script `copy_source.py` can copy them either to the current working
directory or to another bucket/prefix in the same account.

```bash
python copy_source.py -s SOURCE -t TARGET
``` 

* `SOURCE` is the path to the root folder containing the files to copy,
for example `s3://s3-ccm-prod-tradeuk-connect-prod01-raw-ctr/myfiles/` - note that the `/` at the
end is important
* `TARGET` is the path to folder to copy the files to,
for example `s3://s3-ccm-prod-tradeuk-connect-prod01-raw-ctr/mycopy/` - note that the `/` at the
end is important

Note that if no `TARGET` is specified, the script will download the files to the current working
directory.

```bash
python republish_ctrs.py -f FIREHOSE -p PATH -s START -e END
```

* `FIREHOSE` is the firehose created by `republish_setup.sh` to send to, 
e.g. `kfh-ccm-historic-ai-dev`
* `PATH` is the s3 path to the source files, up to the date component of the filename,
for example: 
`s3://s3-capita-ccm-connect-tradeuk-dev-reporting/historic/ctrs/source/TradeUK_Prod_CTRFirehose-1-`
* `START` and `END` are the start and end date (inclusive) for files to be retrieved and processed against
and are in the format `YYYY-MM-DD`, for example `2019-03-01`

Note that if the `END` is not specified, then the script will only process the `START` date

### Adding to Athena

The scripts will produce parquet files in the specified bucket in the client account under

`historic/TYPE/transformed/NOW/clientname=CLIENT/rowdate=DATE/`

for example:

`historic/agent_interval/transformed/2019-03-27/clientname=tradeuk/rowdate=2019-03-01/`

 These will then need to be copied into the appropriate Common bucket, for example:
 
 `s3-capita-ccm-connect-common-prod-reporting/historic/ctrs/transformed/`
 
 To do this, update the bucket policy on the source bucket 
 (e.g. `s3-capita-ccm-connect-tradeuk-dev-reporting`) to allow access from
 the common-prod account, for example:
 
 ```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DelegateS3Access",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::808647995970:role/ccm_common_prod_admin"
            },
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::s3-capita-ccm-connect-tradeuk-dev-reporting/*",
                "arn:aws:s3:::s3-capita-ccm-connect-tradeuk-dev-reporting"
            ]
        }
    ]
}
```

This example allows anyone using the `ccm_common_prod_admin` role to access the 
bucket `s3-capita-ccm-connect-tradeuk-dev-reporting`
 
Once the bucket policy is in place, run the following commands
(example given for CTRs):
 
 ```bash
 # in common account, e.g. common-prod

aws s3 sync s3://s3-capita-ccm-connect-tradeuk-dev-reporting/historic/ctrs/transformed/2019-03-27/ \
            s3://s3-capita-ccm-connect-common-prod-reporting/historic/ctrs/transformed/
```

Once happy with the files in `historic/`, copy over to the final target directory
(example given for CTRs):

```bash
aws s3 sync s3://s3-capita-ccm-connect-common-prod-reporting/historic/ctrs/transformed/ \
            s3://s3-capita-ccm-connect-common-prod-reporting/contact_record/

``` 