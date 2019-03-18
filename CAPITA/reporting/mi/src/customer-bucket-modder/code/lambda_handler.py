import boto3


def handler(event, _context):
    print(f"@lambda_handler|handler|got event: {str(event)}")

    bucket = event.get("bucket")
    prefix = event.get("prefix", "")
    lambda_name = event.get("lambda")

    if not bucket or not lambda_name:
        return

    account_id = boto3.client('sts').get_caller_identity().get('Account')
    lambda_arn = f"arn:aws:lambda:eu-central-1:{account_id}:function:{lambda_name}"

    s3 = boto3.resource('s3')
    notifications = s3.BucketNotification(bucket)
    if event.get("clean"):
        all_lambda_notifications = []
    else:
        notifications.load()
        print(f"Lambda notifications existing for bucket: "
              f"{str(notifications.lambda_function_configurations)}")

        if notifications.lambda_function_configurations:
            for notification in notifications.lambda_function_configurations:
                existing_lamdab_arn = notification.get('LambdaFunctionArn')
                existing_filter_rules = notification.get('Filter', {}) \
                                                    .get('Key', {})\
                                                    .get('FilterRules', [])
                print(f"Existing filter rules: {str(existing_filter_rules)}")
                existing_prefix = next(rule.get('Value') for rule in existing_filter_rules
                                       if rule.get('Name') == 'Prefix')

                if existing_lamdab_arn == lambda_arn or existing_prefix == prefix:
                    print(f"Removing existing config for {existing_lamdab_arn}: {str(notification)}")
                    notifications.lambda_function_configurations.remove(notification)

        all_lambda_notifications = notifications.lambda_function_configurations or []

    lambda_notification = {
        'LambdaFunctionArn': lambda_arn,
        'Events': [
            's3:ObjectCreated:*'
        ],
        'Filter': {
            'Key': {
                'FilterRules': [
                    {
                        'Name': 'Prefix',
                        'Value': prefix
                    }
                ]
            }
        }
    }

    all_lambda_notifications.append(lambda_notification)

    # remove Id from all notifications
    for n in all_lambda_notifications:
        n.pop("Id", None)

    print(f"updated lambda notifications: {str(all_lambda_notifications)}")

    response = notifications.put(
        NotificationConfiguration={
            'LambdaFunctionConfigurations': all_lambda_notifications
        }
    )
    print(f"Notification response: {response}")
