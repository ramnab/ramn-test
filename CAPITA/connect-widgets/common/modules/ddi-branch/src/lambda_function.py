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
        FilterExpression=":variable = DialledDDI",
        ExpressionAttributeValues={
            ':variable': event['Details']['Parameters']['DialledDDI']
        }
    )

    print(json.dumps(event))
    print("DDI being searched for = " + event['Details']['Parameters']['DialledDDI'])

    if response['Count'] > 0:
        print("Returned data" + json.dumps(response["Items"]))

        connectPayload["queueARN"] = response["Items"][0]["QueueARN"]
        print("connectPayload = " + json.dumps(connectPayload))
        return connectPayload
    else:
        connectPayload["queueARN"] = "Queue not found"
        print("Queue not found")
        return connectPayload