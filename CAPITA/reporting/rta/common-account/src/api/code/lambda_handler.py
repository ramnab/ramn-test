import json
import boto3
import logging
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
import os


dynamodb = boto3.resource('dynamodb')
logger = logging.getLogger()
logger.setLevel(20)


class UnauthorisedException(Exception):
    pass


def handler(event, _context):
    """
    Handles API call from RTA dashboard

    """

    logger.info(f"Called with event: {str(event)}")

    authorisation_required = os.environ.get("AUTH", "true").lower() == "true"
    logger.info(f"Authorisation required for clients: {authorisation_required}")

    cors_header = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }

    try:
        filter_response = get_requested_filtered(event, authorisation_required)
        filtered = filter_response.get("filter")
        logger.info(f"Filter response: {filter_response}")
        tablename = os.environ.get("ALARM_DB")
        items = get_current_alarms(tablename, filtered)
        returned_clients = []

        # remove ttl - JSON doesn't like it
        for item in items:
            client = item.get("client")
            if client and client not in returned_clients:
                returned_clients.append(client)

            if item.get('ttl'):
                del item['ttl']

        filter_response['returned_clients'] = returned_clients

        response = {
            "items": items,
            "info": filter_response
        }
        return {
            "statusCode": 200,
            "body": json.dumps(response),
            "headers": cors_header
        }
    except UnauthorisedException as e:
        logger.error(e)
        return {
            "statusCode": 401,
            "body": str(e),
            "headers": cors_header
        }
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 500,
            "body": str(e),
            "headers": cors_header
        }


def get_requested_filtered(event: dict, authorisation_required: bool):
    """
    Returns the permitted clients the user is able to view

    A user has the custom attribute custom:client with either
    a list of clients (comma-delimited) or the wildcard 'all'

    A request to the API either specifies a client to view or has
    no client specified.

    If no client is specified then return only the clients listed
    in the custom attribute; in the case of the wildcard 'all',
    return the special filter ["*"]

    If a client is specified and either the user has the client
    listed in the custom attributes or the wildcard, return that
    client as the filter. If the user does not have the client
    listed, an exception is raised.

    Special case - authorisation not required, returns wildcard

    """

    body = json.loads(event.get('body', "{}"))
    requested_client = body.get("client", "*")
    auth = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
    permitted_clients = auth.get("custom:client", "").split(",")
    username = auth.get('cognito:username')

    response = {
        "username": username,
        "permitted": permitted_clients,
    }

    auth = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
    permitted_clients = auth.get("custom:client", "").split(",")

    if not authorisation_required:
        response['filter'] = [requested_client]
        response['authorisation_disabled'] = True
        return response

    if "all" in permitted_clients:
        response['filter'] = [requested_client]  # can be ["*"]
        return response

    if requested_client == "*":
        response['filter'] = permitted_clients
        return response

    if requested_client not in permitted_clients:
        raise UnauthorisedException(f"{auth.get('cognito:username')} not authorised to view {requested_client}")

    response['filter'] = [requested_client]
    return response


def get_current_alarms(tablename: str, filtered: list):
    """Returns the alarms given a list of clients or '*' returns all"""

    table = dynamodb.Table(tablename)
    try:
        kwargs = {}
        if filtered and "*" not in filtered:
            fe = Attr('client').eq(filtered[0])
            for client in filtered[1:]:
                fe = fe | Attr('client').eq(client)
            kwargs = {
                'FilterExpression': fe
            }
        response = table.scan(**kwargs)
        logger.info(f"get_current_alarms response={str(response)}")
        return response.get('Items', [])
    except ClientError as e:
        raise Exception(e)
