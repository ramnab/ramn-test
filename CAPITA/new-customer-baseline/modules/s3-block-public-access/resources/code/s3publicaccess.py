import json
import logging
import requests
import boto3
import os

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

client = boto3.client('s3control')


def handle_create():
        client.put_public_access_block(
            AccountId=os.environ['ACCOUNT_ID'],
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        LOGGER.info('Successfully set public S3 to none public access')


def handle_delete():
    client.delete_public_access_block(
        AccountId=os.environ['ACCOUNT_ID']
    )

    LOGGER.info('Successfully removed public S3 to none public access')


def send_response(event, context, response_status, response_data):
    '''Send a resource manipulation status response to CloudFormation'''
    response_body = {
        "Status": response_status,
        "Reason": "See the details in CloudWatch Log Stream: " + context.log_stream_name,
        "PhysicalResourceId": context.log_stream_name,
        "StackId": event['StackId'],
        "RequestId": event['RequestId'],
        "LogicalResourceId": event['LogicalResourceId'],
        "Data": response_data
    }

    try:
        req = requests.put(event['ResponseURL'],
                           data=json.dumps(response_body))
        if req.status_code != 200:
            print(req.text)
            raise Exception('Received non 200 response while sending response')
        return
    except requests.exceptions.RequestException as exc:
        print(exc)
        raise


def handler(event, context):
    try:
        LOGGER.info('REQUEST RECEIVED:\n %s', event)
        LOGGER.info('REQUEST RECEIVED:\n %s', context)
        if event['RequestType'] == 'Create':
            LOGGER.info('CREATE!')
            handle_create()
            send_response(event, context, "SUCCESS",
                          {"Message": "Resource creation successful!"})
        elif event['RequestType'] == 'Update':
            LOGGER.info('UPDATE!')
            handle_create()
            send_response(event, context, "SUCCESS",
                          {"Message": "Resource creation successful!"})
        elif event['RequestType'] == 'Delete':
            LOGGER.info('DELETE!')
            handle_delete()
            send_response(event, context, "SUCCESS",
                          {"Message": "Resource deletion successful!"})
        else:
            LOGGER.info('FAILED!')
            send_response(event, context, "FAILED",
                          {"Message": "Unexpected event received from CloudFormation"})
    except Exception as exc:
        LOGGER.info(exc)
        LOGGER.info('FAILED!')
        send_response(event, context, "FAILED", {
            "Message": "Exception during processing"})
