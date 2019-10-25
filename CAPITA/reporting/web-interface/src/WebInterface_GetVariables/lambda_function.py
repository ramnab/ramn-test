import json
import boto3
import os

def lambda_handler(event, context):
    apiPayload = {}
    
    try:
        tableName = os.environ["VariablesDB"]
        dynamoDB = boto3.resource('dynamodb')
        table = dynamoDB.Table(tableName)
        
        response = table.scan(
                TableName = tableName,
                # FilterExpression = ":variable = VariableName",
                #ExpressionAttributeValues = {
                # ':variable': event['Details']['Parameters']['VariableName']
                # }
                Select='ALL_ATTRIBUTES'
            )
        
        if response['Count'] > 0:
            j = response['Items']
            response = sorted(j, key=lambda k: k.get('VariableName', 0), reverse=False)
            
            apiPayload["variables"] = response
            return apiPayload
        else:
            connectPayload["variables"] = "Variables not found"
            print("Variables not found")
            return apiPayload

    except Exception as e:
        print("Something went wrong when reading the records from the table")
        raise e