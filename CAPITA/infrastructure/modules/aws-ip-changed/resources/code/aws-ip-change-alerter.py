import boto3
import requests
import json
import os
import logging
from botocore.exceptions import ClientError

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def publishToSNSTopic(ConnectIps, url):
    message = {"Name": "Empty"}
    arn = os.environ['SnsTopic']
    client = boto3.client('sns')
    response = client.publish(
        TargetArn=arn,
        Message=json.dumps({'default': json.dumps(message),
                            'email': 'Connect IPs changed:\n ' +
                            '\n'.join(ConnectIps) + '\n'
                            'URL to view all changes is: \n' +
                            url}),
        Subject='Connect IPs changed in EU-CENTRAL-1',
        MessageStructure='json'
    )


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    message = json.loads(event['Records'][0]['Sns']['Message'])
    r = requests.get(message['url'])
    data = json.loads(r.content)
    connect_ranges = [x['ip_prefix'] for x in data['prefixes']
                      if x['region'] == 'eu-central-1' and
                      x['service'] == 'AMAZON_CONNECT']

    ssm = boto3.client('ssm')
    parameter = os.environ['SsmParameter']

    # Check the parameter exists, if not create it
    # Or catch the error
    try:
        param = ssm.get_parameter(Name=parameter)
        currentIps = param['Parameter']['Value']
    except ClientError as e:
        if 'ParameterNotFound' in e.response['Error']['Code']:
            LOGGER.info(f'SSM Parameter {parameter} not found, creating')
            currentIps = []
        else:
            LOGGER.info(e.response['Error']['Code'])
            raise

    if str(connect_ranges) == currentIps:
        LOGGER.info("No changes to connect")
    else:
        # Upload to SSM:
        try:
            ssm.put_parameter(Name=parameter,
                              Value=str(connect_ranges),
                              Type='StringList',
                              Overwrite=True)
            LOGGER.info("SSM parameter updated.")
        except ClientError as e:
            LOGGER.info(e.response['Error']['Code'])
        # Send to SNS
        publishToSNSTopic(connect_ranges, message['url'])
