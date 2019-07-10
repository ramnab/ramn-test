import boto3
import re
import sys
from datetime import datetime


"""
List all versions for an S3 object with the ability to download and save locally a specific version

Example use:

python scripts/get_versions.py \
       s3://s3-capita-ccm-common-test-rta-agentschedules/uploads/TUK-ASPECT-LIVE-20190404-CPT.csv
"""


def from_path(path: str):
    """Returns tuple of bucket and path from pattern s3://bucket/path """
    (bucket, key) = re.match('s3://(.+?)/(.+)', path).groups()
    filename = key[key.rfind("/")+1:]
    has_extension = filename.rfind('.')
    extension = ""
    if has_extension > -1:
        file = filename[0:has_extension]
        extension = filename[filename.rfind('.')+1:]
    else:
        file = filename

    return bucket, key, file, extension


def find_version(versions, version_id):
    for version in versions:
        if version.get('VersionId') == version_id:
            return version


def main():
    (bucket, key, filename, extension) = from_path(sys.argv[1])
    print(f"Bucket: {bucket}, key: {key}, filename: {filename}, extension: {extension}")

    s3 = boto3.client("s3")

    response = s3.list_object_versions(Bucket=bucket, Prefix=key)
    for version in response.get("Versions"):
        print(f"key: {version.get('Key')}  versionId: {version.get('VersionId')}   "
              f"ts: {version.get('LastModified')}  size: {version.get('Size')}")

    s3_resource = boto3.resource('s3')
    s3_bucket = s3_resource.Bucket(bucket)

    while True:
        version_id = input("\nEnter versionId to download or enter to finish: ")
        if not version_id:
            break
        version = find_version(response.get("Versions"), version_id)
        if not version:
            print(f"Can't find version: {version_id}")
            continue
        ts = datetime.strftime(version.get('LastModified'), "%Y-%m-%dT%H%M%S")

        version_file_name = f"{filename}-{str(ts)}"
        if extension:
            version_file_name += f".{extension}"

        with open(version_file_name, 'wb') as data:
            print(f"""
Writing:
    s3://{bucket}/{key}  versionId: {version_id}  to  ./{version_file_name}

""")
            s3_bucket.download_fileobj(key, data, ExtraArgs={'VersionId': version_id})


if __name__ == '__main__':
    sys.exit(main())
