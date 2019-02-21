import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
import logging
import os

logger = logging.getLogger()
# INFO = 20
# DEBUG = 10
LOGGING_LEVEL = int(os.environ.get("LOGGING_LEVEL", "20"))
logger.setLevel(LOGGING_LEVEL)


class DbTable():

    items = []

    def __init__(self, tablename):
        self.tablename = tablename
        logger.info(f"Creating new DbTable '{tablename}''")
        self.load()

    def load(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(self.tablename)
        response = table.scan(ConsistentRead=True)
        logger.debug(f"get_history response = {str(response)}")
        self.items = response.get("Items", [])

    def write(self, entries):
        logger.info(f"db write to table {self.tablename}: {entries}")
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(self.tablename)
        with table.batch_writer() as batch:
            for h in entries:
                response = batch.put_item(Item=h)
        self.load()

    def get(self, username, prop=None):
        if prop:
            for item in self.items:
                if item.get("username") == username and \
                   item.get("prop") == prop:
                    return item
            return {}

        return [item for item in self.items
                if item.get("username") == username]

    def get_m(self, usernames):
        return [item for item in self.items
                if item.get("username") in usernames]

    def delete_item(self, key):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(self.tablename)
        response = table.delete_item(Key=key)
        logger.debug(f"delete_item {key} response = {str(response)}")
        self.load()

    def update(self, key, field_name, new_value):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(self.tablename)
        response = table.update_item(
            Key=key,
            UpdateExpression=f"set {field_name} = :d",
            ExpressionAttributeValues={
                ':d': new_value
            }
        )
        logger.debug(f"update {key}, {field_name} = {new_value};"
                     f"response = {str(response)}")
        self.load()
