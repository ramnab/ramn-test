
import os
from republish import process
import logging
from urllib.parse import unquote

logger = logging.getLogger()
# INFO = 20
# DEBUG = 10
LOGGING_LEVEL = int(os.environ.get("LOGGING_LEVEL", "20"))
logger.setLevel(LOGGING_LEVEL)


def handler(event, _context):
    logger.info(f"@lambda_handler|handler|received event: {str(event)}")

    s3 = event.get("Records", [{}])[0].get("s3")
    if not s3:
        logger.error(f"@lambda_handler|handler|"
                     f"Lambda triggered with incorrect event: {str(event)}")
        return

    bucket = s3.get("bucket", {}).get("name")
    key = unquote(s3.get("object", {}).get("key"))
    firehose = event.get("Firehose", os.environ.get("FIREHOSE"))

    if not firehose:
        logger.error(f"@lambda_handler|handler|"
                     f"No Firehose specified in environment vars for lambda")
    logger.info(f"@lambda_handler|handler|firehose={firehose}")

    config = os.environ.get("CONFIG", "").split(",")
    logger.info(f"@lambda_handler|handler|config={str(config)}")

    if not bucket or not key:
        logger.error(f"@lambda_handler|handler|"
                     f"No bucket or key found in event: {str(event)}")
        return

    try:
        logger.info(f"@lambda_handler|handler|bucket={bucket}")
        logger.info(f"@lambda_handler|handler|key={key}")
        process(bucket, key, firehose, config)
    except Exception as e:
        logger.error(f"@lambda_handler|handler|{str(e)}")

    return
