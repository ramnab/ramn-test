import json
import boto3
import os
import time
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    #print (json.dumps(event))
    connectPayload = {}
    
    Number=(event['Details']['ContactData']['CustomerEndpoint']['Address'])
    calledNumber = event['Details']['ContactData']['Attributes']['CalledNumber']
    NGN = event['Details']['ContactData']['Attributes']['NGN']
    OptionSelected = event['Details']['Parameters']['SelectedOption']

    #current epoch time 
    timestamp1 = int(time.mktime(datetime.now().timetuple()))
    
    #expiry time for the current record 
    timestamp2 = int(time.mktime(datetime.now().timetuple())) + (int(os.environ["ExpirationTimeInDays"])*86400)
 
    try:
        tableName = os.environ["DynamoDBTableName"]
        dynamoDB = boto3.resource('dynamodb')
        table = dynamoDB.Table(tableName)
        table.put_item(
            TableName= tableName,
             Item={
                 'CustomerNumber':Number,
                 'CallDateTime' :timestamp1,
                 'CalledNumber' : calledNumber,
                 'ExpirationTime' :timestamp2,
                 'NGN' : NGN,
                 'OptionSelected' : OptionSelected
                 
             }
        )
        return {"success":"Customers details have been inserted successfully"}
        
    except Exception as e:
        print("Something went wrong when inserting the records into the table")
        raise e
    