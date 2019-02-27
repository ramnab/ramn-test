import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
import logging
import os
from time import sleep


logger = logging.getLogger()
# INFO = 20
# DEBUG = 10
LOGGING_LEVEL = int(os.environ.get("LOGGING_LEVEL", "20"))
logger.setLevel(LOGGING_LEVEL)

dynamodb = boto3.resource('dynamodb')

class DbTable():

    items = []

    def __init__(self, tablename):
        self.tablename = tablename
        logger.info(f"Creating new DbTable '{tablename}''")
        self.load()

    def load(self):
        table = dynamodb.Table(self.tablename)
        response = table.scan(ConsistentRead=True)
        logger.debug(f"get_history response = {str(response)}")
        self.items = response.get("Items", [])

    def write(self, entries):
        logger.info(f"db write to table {self.tablename}: {entries}")
        
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

    def update(self, key, field_name, new_value):
        table = dynamodb.Table(self.tablename)
        response = table.update_item(
            Key=key,
            UpdateExpression=f"set {field_name} = :d",
            ExpressionAttributeValues={
                ':d': new_value
            }
        )
        logger.info(f"@DB|update {key}, {field_name} = {new_value};"
                     f"response = {str(response)}")
        self.load()

    def run_updates(self, updates):
        table = dynamodb.Table(self.tablename)
        with table.batch_writer() as batch:
            for update in updates:
                sleep(0.1)
                if update.get("type") == "put":
                    item = update.get("item")
                    response = batch.put_item(Item=item)
                    logger.info(f"@DB|PUT|Item={str(item)}|"
                                f"Response={str(response)}")
                elif update.get("type") == "delete":
                    key = update.get("key")
                    response = batch.delete_item(Key=key)
                    logger.info(f"@DB|DEL|Key={str(key)}|"
                                f"Response={str(response)}")
                elif update.get("type") == "update":
                    key = update.get("key")
                    field = update.get("field")
                    val = update.get("val")
                    response = table.update_item(Key=key,
                                                 UpdateExpression=f"set {field} = :d",
                                                 ExpressionAttributeValues={
                                                    ':d': val
                                                 })
                    logger.info(f"@DB|UPDATE|Key={str(key)}|Field={str(field)}|val={str(val)}"
                                f"Response={str(response)}")
                else:
                    logger.info(f"@DB|UNK|{str(update)}")
