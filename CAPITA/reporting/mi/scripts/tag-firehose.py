import argparse
import sys
import boto3


def add_tags(args):
    stream = args.firehose
    tags = args.tags
    tags_list = []

    for tag in tags:
        tag: str = tag
        key = tag[0:tag.rfind(":")]
        val = tag[tag.rfind(":")+1:]
        tags_list.append({
            'Key': key,
            'Value': val
        })

    all_keys = [tag.get("Key") for tag in tags_list]
    max_key_len = len(max(all_keys, key=len))
    all_vals = [tag.get("Value") for tag in tags_list]
    max_val_len = len(max(all_vals, key=len))

    print(f"\n\nAdding tags to firehose {stream}:\n")
    print('+' + '-' * (max_key_len + 2) + '+' + '-' * (max_val_len + 2) + '+')
    for tag in tags_list:
        print(f"| {tag.get('Key').center(max_key_len)} | {tag.get('Value').center(max_val_len)} |")
    print('+' + '-' * (max_key_len + 2) + '+' + '-' * (max_val_len + 2) + '+')

    client = boto3.client("firehose", region_name=args.region)
    client.tag_delivery_stream(
        DeliveryStreamName=stream,
        Tags=tags_list
    )
    print(f"\nAdded tags to {stream}")
    response = client.list_tags_for_delivery_stream(
        DeliveryStreamName=stream
    )
    tags_pretty_printed = str.join('\n', [f"\t{tag.get('Key')}:{tag.get('Value')}" for tag in response.get('Tags')])
    print(f"""
+----------------------------+
Delivery Stream: {stream}
Tags:
{tags_pretty_printed}

""")


def main():
    parser = argparse.ArgumentParser(description='''

Usage:
    python tag-firehose.py -r REGION -f FIREHOSE -t TAG1 TAG2 TAG3
    
For example:
    python tag-firehose.py -r eu-central-1 -f kfh-ccm-agent-events-dev -t bus:ClientName tech:Environment
     
'''
                                     )
    parser.add_argument('-r', '--region',
                        help='AWS Region',
                        required=True)
    parser.add_argument('-f', '--firehose',
                        help='The name of the firehose, e.g. kfh-ccm-agent-events-dev',
                        required=True)

    parser.add_argument('-t', '--tags',
                        nargs='+',
                        help=('List of tags in the form TAG1 TAG2 TAG3, '
                              'e.g. bus:ClientName tech:Environment'),
                        required=True)

    args = parser.parse_args()
    add_tags(args)
    print(f"Successfully completed")


if __name__ == '__main__':
    sys.exit(main())
