import boto3
import json
import os
import time
from datetime import datetime
import decimal
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
            return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    
    try:
        tableName = os.environ["DynamoDBTableName"]
        dynamoDB = boto3.resource('dynamodb')
        table = dynamoDB.Table(tableName)
    	
        #Get current GMT time
        timestamp1 = int(time.mktime(datetime.now().timetuple()))
        
        timestamp2 = int(time.mktime(datetime.now().timetuple())) - (int(os.environ["DurationInDaysForSurvey"])*86400)
        
        print("Getting survey data for epoch time between " + str(timestamp2) + " and " + str(timestamp1))
        
        response = table.scan(
                TableName = tableName,
                FilterExpression=Attr('CallDateTime').between(timestamp2, timestamp1)
            )
            
    except Exception as e:
        print("Something went wrong when getting the records from table")
        raise e
        
    else:
        if response['Count'] > 0:
            print("Total rows returned " + str(response['Count']))
            
            #convert json object to string and eliminate decimal word from json
            surveyData = json.dumps(response["Items"], cls=DecimalEncoder)
            
            #convert string into a list to loop through
            data = json.loads(surveyData)
            
            surveyHeader = "Customers Number" + ',' + "Call DateTime" + ',' + "Called Number" + ',' + "Dialled DDI" + ',' + "Option Selected" + '\n'
            #print(surveyHeader)
            survey_data = ''
            cNum = ''
            dNum = ''
            
            for j in data:
                cNum = j['CustomerNumber']
                dNum = j['CalledNumber']
                
                if 'NGN' in j:
                    NGNumber = j['NGN']
                else:
                    NGNumber = '-'
                    
                if 'OptionSelected' in j:
                    Option = j['OptionSelected']
                else:
                    Option = '-'
                
                if j['CustomerNumber'].startswith('+44'):
                    cNum = '0' + j['CustomerNumber'][3:]
                else:
                    cNum = j['CustomerNumber']
                    
                if j['CalledNumber'].startswith('+44'):
                    dNum = j['CalledNumber'][1:]
                else:
                    dNum = j['CalledNumber']
                
                survey_data = survey_data + cNum + ',' + datetime.fromtimestamp(int(j['CallDateTime'])).strftime("%d-%b-%Y %H:%M") + ',' + NGNumber+ ','  + dNum+ ','  + Option + '\n'
                cNum = ''
                dNum = ''
                
            try:
                #set file name as SurveyData_dd-mmd-yyyy.csv
                print("Generating survey data on s3 bucket")
                file_name = "SurveyData_" + datetime.fromtimestamp(timestamp1).strftime("%d-%b-%Y") + ".csv"
                file_path = "SurveyFiles/" + file_name
                s3 = boto3.resource('s3')
                obj = s3.Object(os.environ["SurveyS3Bucket"], file_path)
                obj.put(Body = surveyHeader + survey_data)
                print("Survey data with file name " + file_name + " has been generated successfully")
                
            except Exception as e:
                print("Something went wrong when writing to the file on S3 ")
                raise e
        else:
            print("There is no Survey Data")