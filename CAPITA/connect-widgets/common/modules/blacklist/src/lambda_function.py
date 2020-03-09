import json
import boto3
import os

def lambda_handler(event, context):
    connectPayload = {}
    tableName = os.environ["DynamoDBTableName"]

    dynamoDB = boto3.resource('dynamodb')
    table = dynamoDB.Table(tableName)

    response = table.scan(
        TableName=tableName,
        FilterExpression=":callingNum = CallingNumber",
        ExpressionAttributeValues={
            ':callingNum': event['Details']['ContactData']['CustomerEndpoint']['Address']
        }
    )

    print("Calling Number = " + event['Details']['ContactData']['CustomerEndpoint']['Address'])

    if response['Count'] > 0:
        connectPayload['blacklisted'] = "true"
        print("Caller is blacklisted")
        return connectPayload
    else:
        connectPayload['blacklisted'] = "false"
        print("Caller is not blacklisted")
        return connectPayload