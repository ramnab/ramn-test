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
    print("Variable being searched for = " + event['Details']['Parameters']['DialledDDI'])

    if response['Count'] > 0:
        print("Returned data" + json.dumps(response["Items"]))

        connectPayload["variableValue"] = response["Items"][0]["VariableValue"]
        connectPayload["closureVariable"] = response["Items"][0]["ClosureVariable"]
        print("connectPayload = " + json.dumps(connectPayload))
        return connectPayload
    else:
        connectPayload["variableValue"] = "Variable not found"
        print("Variable not found")
        return connectPayload