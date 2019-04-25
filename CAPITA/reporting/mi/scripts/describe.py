import argparse
import json
import sys
import boto3
import collections
from cloudformation_client_type_annotation import Client as CfClient
from iam_client_type_annotation import Client as IamClient


def dict_merge(dct: dict, merge_dct: dict):
    for k, _v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
           and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


cf_client: CfClient = boto3.client('cloudformation')
iam_client: IamClient = boto3.client("iam")


def list_stacks():
    return cf_client.list_stacks().get("StackSummaries", [])


def list_resources(stack_name):
    return cf_client.list_stack_resources(StackName=stack_name) \
                    .get("StackResourceSummaries", [])


def get_physical_resource_id(resources: list, logical_id: str):
    for resource in resources:
        if resource.get('LogicalResourceId') == logical_id:
            return resource.get('PhysicalResourceId')


def get_physical_id_from_stack(stack_name: str, logical_id: str):
    for resource in list_resources(stack_name):
        if resource.get('LogicalResourceId') == logical_id:
            return resource.get('PhysicalResourceId')


def describe_qi(env: str):
    env_fc = env[0:1].upper() + env[1:]
    qi_stack_name = f"stCapita-MI-{env_fc}-QueueIntervals"
    qi_stack_resources = list_resources(qi_stack_name)
    cross_acc_stack_name = f"stCapita-MI-{env_fc}-CrossAccountRole"
    customer_reporting_bucket_stack_name = f"stCapita-CCM-Customer-Connect-{env_fc}-ReportingBucket"
    kms_stack_name = f"stCapita-CCM-Customer-Connect-{env_fc}-Keys"

    qi_lambda = get_physical_resource_id(qi_stack_resources, "QueueIntervalLambda")
    qi_firehose = get_physical_resource_id(qi_stack_resources, "QueueIntervalParquetFirehose")
    qi_table = get_physical_resource_id(qi_stack_resources, "GlueQueueIntervalTable")

    account_alias = iam_client.list_account_aliases().get('AccountAliases', [])[0]
    cross_acc_role_name: str = get_physical_id_from_stack(cross_acc_stack_name,
                                                          'CrossAccountFirehoseRole')

    customer_reporting_bucket_name: str = get_physical_id_from_stack(customer_reporting_bucket_stack_name,
                                                                     'ReportingBucket')
    kms_master_alias: str = get_physical_id_from_stack(kms_stack_name, "ConnectKmsKeyAlias")
    # kms_calls_alias: str = get_physical_id_from_stack(kms_stack_name, "ConnectCallRecordingKmsKeyAlias")

    field_length = max(len(customer_reporting_bucket_name),
                    len(f"s3-capita-ccm-connect-common-{env}-reporting"))  + 2
    print(f"""

                                    QUEUE INTERVAL REPORTING SOLUTION
    -----------------------------------------------------------------------------------------------

    {account_alias.center(77)} |     Common Account
                                                                                  |
     ---------       -----------       ----------       ----------     -------    |      --------
    |         |     | Customer  |     |    QI    |     |    QI    |   | Cross |   |     | Common |
    | CONNECT | --> | Reporting | --> |  Lambda  | --> | Firehose | --| Accnt |-- | --> | Report |
    |         |     |  Bucket   |     |          |     |          |   | Role  |   |     | Bucket |
     ---------       -----------       ----------       ----------     -------    |      --------
         |                                                   ^  
         |                                                   |     
     ----------                                         ------------   
    |   KMS    |                                       |     QI     |  
    |  Master  |                                       | Glue Table |  
    |   Key    |                                        ------------   
     ----------                                                             

+------------------------------{'-' * field_length}+
+ Customer Reporting Bucket | {customer_reporting_bucket_name.ljust(field_length)} +
+ KMS Connect Master Key    | {kms_master_alias.ljust(field_length)} +
+ Queue Interval Lambda     | {qi_lambda.ljust(field_length)} +
+ Queue Interval Firehose   | {qi_firehose.ljust(field_length)} +
+ Cross Account Role        | {cross_acc_role_name.ljust(field_length)} +
+ Queue Interval Glue Table | {qi_table.ljust(field_length)} +
+ Common Reporting Bucket   | {f's3-capita-ccm-connect-common-{env}-reporting'.ljust(field_length)} +
+------------------------------{'-' * field_length}+

""")
    return {
        "Data Storage": {
            "Exported reports S3 Bucket": customer_reporting_bucket_name,
            "Exported reports S3 Prefix": "reports/",
            "Exported reports encryption Key": kms_master_alias
        }
    }


def describe_ai(env: str):
    env_fc = env[0:1].upper() + env[1:]
    qi_stack_name = f"stCapita-MI-{env_fc}-AgentIntervals"
    qi_stack_resources = list_resources(qi_stack_name)
    cross_acc_stack_name = f"stCapita-MI-{env_fc}-CrossAccountRole"
    customer_reporting_bucket_stack_name = f"stCapita-CCM-Customer-Connect-{env_fc}-ReportingBucket"
    kms_stack_name = f"stCapita-CCM-Customer-Connect-{env_fc}-Keys"

    ai_lambda = get_physical_resource_id(qi_stack_resources, "AgentIntervalLambda")
    ai_firehose = get_physical_resource_id(qi_stack_resources, "AgentIntervalParquetFirehose")
    ai_table = get_physical_resource_id(qi_stack_resources, "GlueAgentIntervalTable")

    account_alias = iam_client.list_account_aliases().get('AccountAliases', [])[0]
    cross_acc_role_name: str = get_physical_id_from_stack(cross_acc_stack_name,
                                                          'CrossAccountFirehoseRole')

    customer_reporting_bucket_name: str = get_physical_id_from_stack(customer_reporting_bucket_stack_name,
                                                                     'ReportingBucket')
    kms_master_alias: str = get_physical_id_from_stack(kms_stack_name, "ConnectKmsKeyAlias")

    field_length = max(len(customer_reporting_bucket_name),
                       len(f"s3-capita-ccm-connect-common-{env}-reporting")) + 2
    print(f"""

                                    AGENT INTERVAL REPORTING SOLUTION
    -----------------------------------------------------------------------------------------------
    {account_alias.center(77)} |     Common Account
                                                                                  |
     ---------       -----------       ----------       ----------     -------    |      --------
    |         |     | Customer  |     |    AI    |     |    AI    |   | Cross |   |     | Common |
    | CONNECT | --> | Reporting | --> |  Lambda  | --> | Firehose | --| Accnt |-- | --> | Report |
    |         |     |  Bucket   |     |          |     |          |   | Role  |   |     | Bucket |
     ---------       -----------       ----------       ----------     -------    |      --------
         |                                                   ^  
         |                                                   |     
     ----------                                         ------------   
    |   KMS    |                                       |     AI     |  
    |  Master  |                                       | Glue Table |  
    |   Key    |                                        ------------   
     ----------                                                             

+------------------------------{'-' * field_length}+
+ Customer Reporting Bucket | {customer_reporting_bucket_name.ljust(field_length)} +
+ KMS Connect Master Key    | {kms_master_alias.ljust(field_length)} +
+ Queue Interval Lambda     | {ai_lambda.ljust(field_length)} +
+ Queue Interval Firehose   | {ai_firehose.ljust(field_length)} +
+ Cross Account Role        | {cross_acc_role_name.ljust(field_length)} +
+ Queue Interval Glue Table | {ai_table.ljust(field_length)} +
+ Common Reporting Bucket   | {f's3-capita-ccm-connect-common-{env}-reporting'.ljust(field_length)} +
+------------------------------{'-' * field_length}+


""")
    return {
        "Data Storage": {
            "Exported reports S3 Bucket": customer_reporting_bucket_name,
            "Exported reports S3 Prefix": "reports/",
            "Exported reports encryption Key": kms_master_alias
        }
    }


def describe_ctr(env: str):

    env_fc = env[0:1].upper() + env[1:]
    ctr_stack_name = f"stCapita-MI-{env_fc}-CTR"
    cross_acc_stack_name = f"stCapita-MI-{env_fc}-CrossAccountRole"
    customer_reporting_bucket_stack_name = f"stCapita-CCM-Customer-Connect-{env_fc}-ReportingBucket"

    ctr_resources = list_resources(ctr_stack_name)

    account_alias = iam_client.list_account_aliases().get('AccountAliases', [])[0]

    logical_ids = ['CtrKinesisStream', 'CustomerParquetFirehose', 'GlueCTRTable']
    physical_ids = {}
    for logical_id in logical_ids:
        physical_ids[logical_id] = get_physical_resource_id(ctr_resources, logical_id)

    cross_acc_role_name: str = get_physical_id_from_stack(cross_acc_stack_name,
                                                          'CrossAccountFirehoseRole')

    customer_reporting_bucket_name: str = get_physical_id_from_stack(customer_reporting_bucket_stack_name,
                                                                     'ReportingBucket')

    field_length = max(len(f"s3-capita-ccm-connect-common-{env}-reporting"),
                       len(customer_reporting_bucket_name)) + 2

    print(f"""

                                    CONTACT RECORDS REPORTING SOLUTION
    -----------------------------------------------------------------------------------------------

    {account_alias.center(62)} |     Common Account

     ---------       ---------        ----------      ---------    |      -----------
    |         |     |   CTR   |      |   CTR    |    |  Cross  |   |     |  Common   |
    | CONNECT | --> | Kinesis | -->  | Kinesis  | ---|  Accnt  |-- | --> | Reporting |
    |         |     | Stream  |      | Firehose |    |  Role   |   |     |  Bucket   |
     ---------       ---------        ----------      ---------    |      -----------
                                          ^    |
                                          |     -----------| (back up raw)
                                     ------------     -----------
                                    |     CTR    |   |  Customer |
                                    | Glue Table |   | Reporting |
                                     ------------    |   Bucket  |
                                                      -----------

+------------------------------{'-' * field_length}+
+ CTR Kinesis Stream        | {physical_ids.get('CtrKinesisStream').ljust(field_length)} +
+ CTR Kinesis Firehose      | {physical_ids.get('CustomerParquetFirehose').ljust(field_length)} +
+ Cross Account Role        | {cross_acc_role_name.ljust(field_length)} +
+ CTR Glue Table            | {physical_ids.get('GlueCTRTable').ljust(field_length)} +
+ Common Reporting Bucket   | {f's3-capita-ccm-connect-common-{env}-reporting'.ljust(field_length)} +
+ Customer Reporting Bucket | {customer_reporting_bucket_name.ljust(field_length)} + 
+------------------------------{'-' * field_length}+

""")
    return {
        "Data Streaming": {
            "Contact Trace Records Kinesis Stream": physical_ids.get('CtrKinesisStream')
        }
    }


def baseline(env: str):
    env_fc = env[0:1].upper() + env[1:]
    call_recordings_stack = f"stCapita-CCM-Customer-Connect-{env_fc}-CallRecordingsBucket"
    call_recordings_bucket = get_physical_id_from_stack(call_recordings_stack, "CallRecordingBucket")
    kms_stack_name = f"stCapita-CCM-Customer-Connect-{env_fc}-Keys"
    kms_calls_alias: str = get_physical_id_from_stack(kms_stack_name, "ConnectCallRecordingKmsKeyAlias")

    return {
        "Data Storage": {
            "Call Recordings Bucket": call_recordings_bucket,
            "Call Recordings Encryption Key": kms_calls_alias
        }
    }


def print_connect_config(cfg):

    lines = []
    for key, val in cfg.items():
        lines.append(f"\n  {key}\n  {'-' * len(key)}")
        if isinstance(val, dict):
            for key2, val2 in val.items():
                lines.append(f"  {key2.ljust(40)}: {val2}")
        else:
            lines.append(val)
    max_line_length = len(max(lines, key=len))
    print("CONNECT Instance Configuration".center(max_line_length))
    print("------------------------------".center(max_line_length))
    print("\n".join(lines))
    print(f"\n{'-' * max_line_length}")


def main():
    parser = argparse.ArgumentParser(description='''

    Usage:
        python describe.py -e ENV -s SOLUTION

    For example:
        python describe.py -e dev -s ctr

    ''')
    parser.add_argument('-e', '--env',
                        help='Environment, e.g. dev, test or prod',
                        required=True)

    parser.add_argument('-s', '--solution',
                        help='Solution, for example ctr, ai or qi',
                        required=False)

    args = parser.parse_args()
    connect_config = baseline(args.env.lower())

    if not args.solution or args.solution == "ctr":
        dict_merge(connect_config, describe_ctr(args.env.lower()))
    if not args.solution or args.solution == "qi":
        dict_merge(connect_config, describe_qi(args.env.lower()))
    if not args.solution or args.solution == "ai":
        dict_merge(connect_config, describe_ai(args.env.lower()))

    print_connect_config(connect_config)


if __name__ == '__main__':
    sys.exit(main())
