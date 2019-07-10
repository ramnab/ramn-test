import boto3
import argparse
import sys
import re


def from_path(path: str):
    return re.match('s3://(.+?)/(.*)', path).groups()


def list_files(bucket, prefix):
    s3 = boto3.client('s3')
    files = []
    token = None
    while True:
        if token:
            response = s3.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix,
                ContinuationToken=token
            )
        else:
            response = s3.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix
            )
        for file in response.get("Contents"):
            files.append(file.get("Key"))
        if response.get("IsTruncated"):
            token = response.get("NextContinuationToken")
        else:
            break
    return files


def copy(source_bucket: str, keys: list, target_bucket: str, target_prefix: str):
    s3 = boto3.resource('s3')

    for key in keys:
        file_name = key[(key.rfind('/')+1):]

        if not target_bucket:
            print(f"Downloading {file_name} to local directory")
            s3.Bucket(source_bucket).download_file(key, file_name)
        else:
            source = {
                'Bucket': source_bucket,
                'Key': key
            }
            print(f"Copying from s3://{source.get('Bucket')}/{source.get('Key')} to "
                  f"s3://{target_bucket}/{target_prefix}{file_name}")
        # s3.meta.client.copy(source, target_bucket, target_prefix + file_name)


def main():
    parser = argparse.ArgumentParser(description='''
    Usage:
        python copy_source.py -s SOURCE_PATH -t TARGET_PATH

        Copies files found recursively in SOURCE_PATH are then copied to
        TARGET_PATH with original filename but in a single directory,
        i.e. flattens the folder in source.
        
        Note that files with the same name will overwrite each other 

    ''')

    parser.add_argument('-s', '--source',
                        help='Source path in the form s3://bucket/path/',
                        required=True)

    parser.add_argument('-t', '--target',
                        help='Target path in the form s3://bucket/path/',
                        required=False)

    args = parser.parse_args()
    print(f"source path: {args.source}")
    print(f"target path: {args.target}")
    (source_bucket, source_prefix) = from_path(args.source)
    try:
        (target_bucket, target_prefix) = from_path(args.target)
    except Exception:
        target_bucket = None
        target_prefix = None

    keys = list_files(source_bucket, source_prefix)
    print(f"Got {len(keys)} files from s3://{source_bucket}/{source_prefix}")

    copy(source_bucket, keys, target_bucket, target_prefix)

    print("Completed")


if __name__ == '__main__':
    sys.exit(main())
