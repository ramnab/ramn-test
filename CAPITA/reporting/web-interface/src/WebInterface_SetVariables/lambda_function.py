import boto3
import json
import os

def lambda_handler(event, context):
    print ("The connect variable being updated is: " + json.dumps(event))

    try:
        tableName = os.environ["VariablesDB"]
        dynamoDB = boto3.resource('dynamodb')
        table = dynamoDB.Table(tableName)
        
        table.update_item(
            TableName = tableName,
            Key = {
                'VariableName': event['variableName']
            },
            UpdateExpression = "SET VariableValue = :a",
            ExpressionAttributeValues = {
                ':a': event['variableValue']
            }
        )
        return {"success":"Variable has been updated successfully"}

    except Exception as e:
        print ("Something went wrong when updating the records in the table")
        raise e