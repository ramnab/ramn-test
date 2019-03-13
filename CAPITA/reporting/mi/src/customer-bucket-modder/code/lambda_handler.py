import boto3


def handler(event, _context):
    print(f"@lambda_handler|handler|got event: {str(event)}")

    bucket = event.get("bucket")
    prefix = event.get("prefix", "")
    lambda_arn = event.get("lambda")

    if not bucket or not lambda_arn:
        return

    s3 = boto3.resource('s3')
    notifications = s3.BucketNotification(bucket)
    notifications.load()
    print(f"Lambda notifications existing for bucket: "
          f"{str(notifications.lambda_function_configurations)}")

    lambda_notification = {
        'LambdaFunctionArn': lambda_arn,
        'Events': [
            's3:ObjectCreated:*'
        ],
        'Filter': {
            'Key': {
                'FilterRules': [
                    {
                        'Name': 'prefix',
                        'Value': prefix
                    }
                ]
            }
        }
    }
    all_lambda_notifications = notifications.lambda_function_configurations or []
    all_lambda_notifications.append(lambda_notification)
    print(f"updated lambda notifications: {str(all_lambda_notifications)}")

    notifications.put(
        NotificationConfiguration={
            'LambdaFunctionConfigurations': all_lambda_notifications
        }
    )
