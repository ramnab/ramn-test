import json
import logging
import boto3
import datetime
import os

logger = logging.getLogger()
# INFO = 20
# DEBUG = 10
LOGGING_LEVEL = int(os.environ.get("LOGGING_LEVEL", "20"))
logger.setLevel(LOGGING_LEVEL)


def handler(event, context):
    logger.info("event: "+json.dumps(event, indent=2))

    rule_name = os.environ.get("HB")
    logger.info(f"Rule Name: {rule_name}")

    if rule_name and event.get("schedule") == "start":
        logger.info(f"Starting heart beats at {datetime.datetime.now()}")
        client = boto3.client('events')
        response = client.enable_rule(Name=rule_name)
        logger.debug(response)

    if rule_name and event.get("schedule") == "stop":
        logger.info(f"Stopping heart beats at {datetime.datetime.now()}")
        client = boto3.client('events')
        response = client.disable_rule(Name=rule_name)
        logger.debug(response)

    return {}
