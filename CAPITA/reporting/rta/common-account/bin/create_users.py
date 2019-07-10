import boto3
import argparse
import csv
from botocore.exceptions import ClientError


cognito_client = boto3.client("cognito-idp")


def verify_user_pool(pool):
    response = cognito_client.list_user_pools(MaxResults=10)
    pools = [p.get('Id') for p in response.get('UserPools', [])]
    if pool not in pools:
        print(f"\nUserpool {pool} not found. Available pools (IDs) are: ")
        print("\n".join([f"\t{p.get('Name')} ({p.get('Id')})" for p in response.get('UserPools', [])]))
        print("\n")
        raise Exception(f"Pool not found: {pool}")


def load_csv(file):
    with open(file, 'r') as f:
        reader = csv.DictReader(f.read().splitlines())
        lst = []
        for line in reader:
            lst.append(dict(line))
        return lst


def get_user(pool, username):
    try:
        return cognito_client.admin_get_user(
            UserPoolId=pool,
            Username=username
        )
    except ClientError:
        return None


def update_client(pool, username, clients):
    try:
        cognito_client.admin_update_user_attributes(
            UserPoolId=pool,
            Username=username,
            UserAttributes=[
                {
                    'Name': 'custom:client',
                    'Value': clients
                }
            ]
        )
        print(f"Updated {username} for {clients}")
    except ClientError:
        print(f"Unable to update {username} to {clients}")


def add_user(pool, **kwargs):

    user_attributes = [
        {
            'Name': 'email',
            'Value': kwargs.get('email')
        },
        {
            'Name': 'email_verified',
            'Value': "true"
        }
    ]
    if kwargs.get("clients"):
        clients = kwargs.get("clients")
        clients = clients.replace(" ", ",")
        user_attributes.append({
            'Name': 'custom:client',
            'Value': clients
        })

    try:
        response = cognito_client.admin_create_user(
            UserPoolId=pool,
            Username=kwargs.get("username"),
            UserAttributes=user_attributes,
            TemporaryPassword='Let.me.in1'
        )
        print(f"Created user: {response.get('User', {}).get('Username')}")
    except ClientError as e:
        if e.response.get("Error").get("Code") == "UsernameExistsException":
            print(f"Username {kwargs.get('username')} already exists... skipping")


def process_user(pool, **kwargs):
    username = kwargs.get("username")
    if get_user(pool, username):
        clients = kwargs.get("clients")
        clients = clients.replace(" ", ",")
        update_client(pool, username, clients)
    else:
        print(f"Processing: kwargs={kwargs}")
        add_user(pool, **kwargs)


def main():
    parser = argparse.ArgumentParser('''
    Add Users to Cognitio User Pool or updates an existing user

    usage:
        python create_users.py --pool POOLID --username USERNAME --email EMAIL --clients CLIENTS 
        
    Alternative:
        python create_users.py --pool POOLID --file CSV

    Where
        POOLID is the cognito pool id, for example eu-central-1_5vpngTHt2 (REQUIRED)
        EMAIL is the user's email address
        CLIENTS is a space-delimited list of customer accounts, e.g. tradeuk firstgroup
          (note that this option needs to be last)
        
        USERNAME is the username, e.g. P0001
        CSV is a csv list containing headers: 
            * username
            * email
            * clients (space delimited)

    ''')

    parser.add_argument(
        '-p', '--pool',
        help='Pool ID, for example eu-central-1_5vpngTHt2',
        required=True
    )
    parser.add_argument(
        '-m', '--email',
        help='Email address'
    )
    parser.add_argument(
        '-c', '--clients',
        help='List of clients, e.g. tradeuk firstgroup',
        nargs='+'
    )
    parser.add_argument(
        '-n', '--username',
        help='Username, e.g. P0001'
    )
    parser.add_argument(
        '-f', '--file',
        help='File to CSV list of users'
    )
    args = parser.parse_args()

    if args.file:
        users = load_csv(args.file)
    else:
        users = [
            {
                'username': args.username,
                'email': args.email,
                'clients': ','.join(args.clients)
            }
        ]
    verify_user_pool(args.pool)
    for user in users:
        process_user(args.pool, **user)


if __name__ == '__main__':
    main()

