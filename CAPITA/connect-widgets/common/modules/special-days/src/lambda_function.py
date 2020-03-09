import boto3
import time
import json
import os

def lambda_handler(event, context):
    connectPayload = {}
    connectPayload["description"] = "other"
    tableName = os.environ["DynamoDBTableName"]

    dynamoDB = boto3.resource('dynamodb')
    table = dynamoDB.Table(tableName)

    response = table.scan(
        TableName=tableName,
        FilterExpression=":dateNow BETWEEN StartTime AND EndTime",
        ExpressionAttributeValues={
            ':dateNow': str(int(time.time()))
        }
    )

    print ("Scan filter = " + str(int(time.time())) + " BETWEEN StartTime and EndTime")
    print ("Scan response = " + json.dumps(response['Items']))

    if response['Count'] > 0:
        connectPayload["holidayFound"] = "true"
        for x in response['Items']:
            if x["Description"] == "RemembranceDay":
                connectPayload["description"] = "remembranceDay"

    else:
        connectPayload["holidayFound"] = "false"
        connectPayload["description"] = "noHoliday"

    print ("Lambda response = " + json.dumps(connectPayload))
    return connectPayload