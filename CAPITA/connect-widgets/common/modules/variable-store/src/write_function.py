import boto3
import json
import os

def lambda_handler(event, context):
    print (json.dumps(event))
    connectPayload = {}

    try:
        tableName = os.environ["DynamoDBTableName"]
        dynamoDB = boto3.resource('dynamodb')
        table = dynamoDB.Table(tableName)

        table.update_item(
            TableName = tableName,
            Key = {
                'VariableName': event['Details']['Parameters']['VariableName']
            },
            UpdateExpression = "SET VariableValue = :a",
            ExpressionAttributeValues = {
                ':a': event['Details']['Parameters']['VariableValue']
            }
        )

    except:
        print ("There has been an error updating the table")

    return connectPayload
