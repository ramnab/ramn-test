import boto3
import sys

key_alias = sys.argv[1]

kms = boto3.client("kms")

aliases = kms.list_aliases().get("Aliases", [])

for alias in aliases:
    if alias.get("AliasName") == f"alias/{key_alias}":
        arn = alias.get("AliasArn")
        key = alias.get("TargetKeyId")
        key_arn = arn[0:arn.rfind(":")] + ":key/" + key
        print(key_arn)
        break
