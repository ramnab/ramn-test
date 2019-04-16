import boto3
import logging
from pythonjsonlogger import jsonlogger
import os
from datetime import datetime, timezone


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.propagate = False


def handler(event: dict, _context):
    logger.info("INVOKED", extra={"event": event})

    config = read_config_from_env()
    errors = []
    check_aspect_upload(config, errors)
    check_agent_schedule(config, errors)
    logger.info("Errors", extra={"errors": errors})
    if errors:
        report_errors(config, errors)


def read_config_from_env():
    conf = {
        'agent_schedule_bucket': os.environ.get("AGENT_SCHEDULE_BUCKET",
                                                "s3-capita-ccm-common-test-rta-agentschedules"),
        'aspect_prefix': os.environ.get("ASPECT_PREFIX", "uploads/TUK-ASPECT-LIVE-"),
        'aspect_freshness_threshold': int(os.environ.get("ASPECT_FRESH_THRESHOLD", "20")),
        'schedule_freshness_threshold': int(os.environ.get("SCHEDULE_FRESH_THRESHOLD", "60")),
        'reporting_bucket': os.environ.get("REPORTING_BUCKET", "s3-capita-ccm-connect-common-test-reporting"),
        'topic': os.environ.get("TOPIC", "stCapita-RTA-Dev-Verify-RtaVerifySnsTopic-SRC2JO0LAZ9D")
    }
    logger.info("Read config from env", extra={"config": conf})
    return conf


def check_aspect_upload(config: dict, errors: list):

    now = datetime.now(timezone.utc)
    today = now.strftime("%Y%m%d")
    prefix = f"{config.get('aspect_prefix')}{today}"
    bucket = config.get("agent_schedule_bucket")
    files = get_file_info(bucket, prefix)

    if not check_one_file_only(files, "ASPECT UPLOAD", errors):
        return

    threshold = config.get("aspect_freshness_threshold")
    if not check_freshness(files[0], threshold, "ASPECT UPLOAD", errors):
        return


def check_agent_schedule(config: dict, errors: list):

    prefix = "processed/agent_schedule.json"
    bucket = config.get("agent_schedule_bucket")
    files = get_file_info(bucket, prefix)

    if not check_one_file_only(files, "AGENT SCHEDULE", errors):
        return

    threshold = config.get("schedule_freshness_threshold")
    if not check_freshness(files[0], threshold, "AGENT SCHEDULE", errors):
        return


def get_file_info(bucket, prefix):
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )
    return response.get("Contents", [])


def check_one_file_only(files, check_set, errors):

    if not files:
        errors.append({
            "level": "CRITICAL",
            "check": check_set,
            "message": f"No file found"
        })
        return False

    number_of_files = len(files)
    if number_of_files > 1:
        errors.append({
            "level": "CRITICAL",
            "check": check_set,
            "message": f"Multiple files found: {files}"
        })
        return False

    return True


def check_freshness(file, threshold, checkset, errors):
    now = datetime.now(timezone.utc)
    last_modified = file.get("LastModified")
    age = now - last_modified
    age_in_minutes = int(age.total_seconds() / 60)
    logger.info(f"File {file.get('Key')} is {age_in_minutes} minutes old")

    if age_in_minutes > threshold:
        errors.append({
            "level": "WARNING",
            "check": checkset,
            "message": f"File is {age_in_minutes} minutes old: {file.get('Key')}"
        })
        return


def report_errors(config: dict, errors: list):
    sns = boto3.client("sns")
    message = f"""
There were the following errors reported from RTA:

"""
    for error in errors:
        message += f"[{error.get('level')}] for {error.get('check')}: {error.get('message')}\n\n"

    logger.warning(message, extra={"errors": errors})
    sns.publish(
        TopicArn=config.get("topic"),
        Message=message,
        Subject=f"RTA Health Check"
    )
