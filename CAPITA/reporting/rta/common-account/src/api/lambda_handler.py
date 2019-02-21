import json


def handler(event, context):
    """
    Handles API call from RTA dashboard

    """

    print("Called with event:" + json.dumps(event, indent=2))

    return {
        "statusCode": 200,
        "body": json.dumps({'message': 'Hello World'}),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
    }
