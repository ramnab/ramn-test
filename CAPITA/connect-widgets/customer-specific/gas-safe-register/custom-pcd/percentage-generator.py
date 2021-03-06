import boto3
import json
import os
import random


def lambda_handler(event, context):
    connectPayload = {}
    print (json.dumps(event))

    ivrname = event['Details']['Parameters']['IVRName']

    if ivrname == "renewals":
        VariableName = "Installer Renewals % to IVR"
    elif ivrname == "find/check":
        VariableName = "Consumer Find/Check % to IVR"
    else:
        connectPayload["variableValue"] = "No valid ivrName (renewals, find, or check)"

    print (VariableName)

    try:
        tableName = os.environ["DynamoDBTableName"]
        dynamoDB = boto3.resource('dynamodb')
        table = dynamoDB.Table(tableName)

        response = table.scan(
            TableName=tableName,
            FilterExpression=":variable = VariableName",
            ExpressionAttributeValues={
                ':variable': VariableName
            }
        )

        print (json.dumps(response))

    except:
        print ("There has been an error in the function")
        connectPayload["variableValue"] = "Function error"

    variableValue = json.dumps(response["Items"][0]["VariableValue"])
    if variableValue.startswith('"') and variableValue.endswith('"'):
        variableValue = variableValue[1:-1]

    variableValue = int(variableValue)
    randomValue = random.randint(1, 100)
    print ("Variable value = " + str(variableValue))
    print ("Random value = " + str(randomValue))

    if randomValue <= variableValue:
        connectPayload["variableValue"] = "true"
    else:
        connectPayload["variableValue"] = "false"

    print (json.dumps(connectPayload))

    return connectPayload