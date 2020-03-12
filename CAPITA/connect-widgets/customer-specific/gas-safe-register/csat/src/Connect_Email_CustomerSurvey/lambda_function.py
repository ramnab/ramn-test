import json
import boto3
import os
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def lambda_handler(event, context):
    
    s3Client = boto3.client("s3")
    #print("Event: ", event)
    fileObj = event["Records"][0]
    rawFileName = str(fileObj['s3']['object']['key'])
    fileName = rawFileName[12:]
    #print("File name is: ", fileName)
    bucketName = str(fileObj['s3']['bucket']['name'])
    #print("Bucket name is: ", bucketName)
    
    #Get the file from S3 to attach to the email
    #fileObj = s3Client.get_object(Bucket = bucketName, Key = fileName)
    #file_content = fileObj["Body"].read()
    
    downloadLink = "https://{0}/index.html?path={1}".format(os.environ["CloudFrontDomain"],fileName)
    #print("The link to download the file is: ", downloadLink)
    
    # This address must be verified with Amazon SES.
    SENDER = os.environ["FromEmailAddress"]
    
    # If your account is still in the sandbox, this address must be verified.
    
    ToRECIPIENT = (os.environ["ToEmailAddress"]).split(",")
    RECIPIENTS = ToRECIPIENT
    
    if os.environ["CcEmailAddress"]:
        CcRECIPIENT = (os.environ["CcEmailAddress"]).split(",")
        RECIPIENTS = RECIPIENTS + CcRECIPIENT
        #print("CcRECIPIENT are: ", CcRECIPIENT)
    
    #print("ToRECIPIENT are: ", ToRECIPIENT)
    
    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    ##CONFIGURATION_SET = "ConfigSet"
    
    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "eu-west-1"
    
    # The subject line for the email.
    SUBJECT = "Gas Safe Register Customer Survey"
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = "Hello,\r\n\nThe customer survey file ({0}) has been generated. Please log on to {1} to download the file.\r\n\nRegards,\r\nGas Safe Register".format(fileName,downloadLink)
    
    # The HTML body of the email.
    BODY_HTML = """\
    <html>
    <head></head>
    <body style='font-size:11.0pt;font-family:Calibri,sans-serif'>
    <p>Hello,</p>
    <p>The customer survey file ({0}) has been generated. Please log on <a href='{1}'>here</a> to download the file.</p>
    <p>Regards,<br>Gas Safe Register</p>
    </body>
    </html>
    """.format(fileName,downloadLink)
    
    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    
    msg = MIMEMultipart('mixed')
    
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = ', '.join(ToRECIPIENT)
    if os.environ["CcEmailAddress"]:
        msg['Cc'] = ', '.join(CcRECIPIENT)
    
    msg_body = MIMEMultipart('alternative')
    
    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
    
    #Removed attachment section
    #attachment = MIMEApplication(file_content)
    #attachment.add_header("Content-Disposition","attachment", filename = fileName)
    
    # Add the text and HTML parts to the child container.
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)
    
    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)
    #Removed attachment section
    #msg.attach(attachment)
    
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=RECIPIENTS,
                RawMessage={
                    'Data':msg.as_string(),
                    
                }
        )
    
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])