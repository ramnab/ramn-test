import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import os

def lambda_handler(event, context):
    print ("The connect variable being updated is: " + json.dumps(event))
    allowedValues = ["true","false", "0","10","20","30","40","50","60","70","80","90","100"]

    try:
        if event['variableValue'] in allowedValues:
            tableName = os.environ["VariablesDB"]
            dynamoDB = boto3.resource('dynamodb')
            table = dynamoDB.Table(tableName)
            
            table.update_item(
                TableName = tableName,
                Key = {
                    'VariableName': event['variableName']
                },  
                UpdateExpression = "SET VariableValue = :a",
                ConditionExpression = Attr('VariableName').exists(),
                ExpressionAttributeValues = {
                    ':a': event['variableValue']
                }
            )
            return {"success":"Variable has been updated successfully"}
        else:
            print ("The update request is failed. The value entered is " + event['variableValue'] + " which is not a valid Variable Value")

    except Exception as e:
        print ("Something went wrong when updating the records in the table")
        raise e