import boto3
import sys
import os
from pathlib import Path
import argparse


def main():
    parser = argparse.ArgumentParser(description='''

Usage:
    python create_views.py -e ENV [VIEW]
    
Creates all or specified view VIEW in the environment ENV
ENV: required, one of 'dev', 'test' or 'prod'
VIEW: optional, if none specified then all views are created

For example:
    python create_views.py -e test agent_daily

    ''')

    parser.add_argument('-e', '--env', help='one of dev, test or prod', required=True)
    parser.add_argument('view', nargs='?', help='name of view, e.g. agent_daily')

    views = [
        'agent_daily',
        'agent_event',
        'agent_interval',
        'contact_record',
        'queue_daily',
        'queue_interval'
    ]

    args = parser.parse_args()
    if args.view:
        views = [args.view]
    athena_client = boto3.client('athena')
    account_id = boto3.client('sts').get_caller_identity()['Account']
    account_alias = boto3.client('iam').list_account_aliases()['AccountAliases'][0]
    print(f"Creating views in account {account_alias} ({account_id}) "
          f"in database 'ccm_connect_reporting_{args.env}':\n")

    for view in views:
        query = load_query(view, args.env)
        run_query(athena_client, view, query,
                  f"ccm_connect_reporting_{args.env}",
                  account_id)


def load_query(view_name, env):
    dll_path = Path(os.path.dirname(os.path.realpath(__file__))) / '../ddls/'
    dll_file = dll_path / f'{view_name}_view.sql.template'
    if dll_file.is_file():
        with open(dll_file, 'r') as f:
            return f.read().replace('[env]', env)
    raise FileNotFoundError(f"Query script '{dll_file}' not found")


def run_query(client, view_name, query, db, account_id):
    print(f"Creating/replacing view: {view_name}")
    output_location = f"s3://aws-athena-query-results-{account_id}-eu-central-1/"
    client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': db
        },
        ResultConfiguration={
            'OutputLocation': output_location
        }
    )


if __name__ == '__main__':
    sys.exit(main())
