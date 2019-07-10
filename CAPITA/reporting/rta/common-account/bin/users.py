import click
import boto3
from botocore.exceptions import ClientError
import csv


cognito_client = boto3.client("cognito-idp")
iam_client = boto3.client('iam')


def get_attribute_value(user: dict, attribute_name: str):
    for attribute in user.get('Attributes', []):
        if attribute.get('Name') == attribute_name:
            return attribute.get('Value')
    return ''


def get_max(f: list, attr: str, floor: int = 0):
    max_entry = max(f, key=lambda x: len(x.get(attr)))
    max_len = len(max_entry.get(attr, ''))
    if max_len < floor:
        return floor
    return max_len


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
    print(f"process_user kwargs = {kwargs}")
    username = kwargs.get("username")
    if get_user(pool, username):
        clients = kwargs.get("clients")
        clients = clients.replace(" ", ",")
        update_client(pool, username, clients)
    else:
        add_user(pool, **kwargs)


@click.group()
@click.pass_context
def cli(ctx):
    account_alias = iam_client.list_account_aliases().get('AccountAliases', [])[0]
    ctx.obj['account_alias'] = account_alias


def get_pools():
    response = cognito_client.list_user_pools(MaxResults=20)
    pools = []
    for pool in response.get('UserPools', []):
        pools.append({
            'id': pool['Id'],
            'name': pool['Name']
        })
    return pools


@cli.command()
@click.pass_context
def list_pools(ctx):
    pools = get_pools()
    max_id = max(pools, key=lambda x: len(x.get('id'))).get('id')
    max_id_length = len(max_id)

    max_name = max(pools, key=lambda x: len(x.get('name'))).get('name')
    max_name_length = len(max_name)
    account_alias = ctx.obj['account_alias']

    print(f"""
+{'-' * max_id_length}---{'-' * max_name_length}--+
+{('User Pools in ' + account_alias).center(max_id_length + max_name_length + 5)}+""")
    print(f"+{'-' * max_id_length}--+{'-' * max_name_length}--+")
    for pool in pools:
        pool_id: str = pool['id']
        name: str = pool['name']
        print(f"+ {pool_id.ljust(max_id_length)} + {name.center(max_name_length)} +")
    print(f"+{'-' * max_id_length}--+{'-' * max_name_length}--+\n\n")


@cli.command()
@click.option('--export', help='export to given csv file')
@click.pass_context
@click.argument('pool-id')
def list_users(ctx, export, pool_id):
    """ Display list of users in the specified pool """
    response = cognito_client.list_users(
        UserPoolId=pool_id
    )

    users = []
    for user in response.get('Users', []):
        users.append({
            'username': user['Username'],
            'email': get_attribute_value(user, 'email'),
            'clients': get_attribute_value(user, 'custom:client')
        })
    max_username_length = get_max(users, 'username', len('username'))
    max_email_length = get_max(users, 'email')
    max_clients_length = get_max(users, 'clients', len('clients'))

    table_width = max_username_length + max_email_length + max_clients_length + 8
    header = f"Users in account {ctx.obj['account_alias']}, pool {pool_id}"

    if export:
        export_file = open(export, 'w')
        export_file.write("username,email,clients\n")

    print(f"""

{header}

+{'-' * table_width}+
+ {'username'.center(max_username_length)} + {'email'.center(max_email_length)} + {'clients'.ljust(max_clients_length)} +
+{'-' * (max_username_length + 2)}+{'-' * (max_email_length + 2)}+{'-' * (max_clients_length + 2)}+""")

    for user in users:
        username = user.get('username')
        email = user.get('email')
        clients = user.get('clients')

        print(f"+ {username.center(max_username_length)} + {email.center(max_email_length)} + {clients.center(max_clients_length)} + ")
        if export:
            export_file.write(f"{username},{email},{clients.replace(',', ' ')}\n")

    print(f"+{'-' * table_width}+\n")
    if export:
        export_file.close()


def create_user_command():
    class CreateUserCommandClass(click.Command):

        def invoke(self, ctx):
            options = [p1 for (p1, p2) in ctx.params.items() if p2 is not None]

            if 'pool_id' not in options:
                raise click.ClickException("You must specify the pool-id")
            if 'csv' not in options:
                if 'username' not in options or 'email' not in options:
                    raise click.ClickException("You must specify either the csv import file or "
                                               "an individual user by username and email")
            super(CreateUserCommandClass, self).invoke(ctx)

    return CreateUserCommandClass


@cli.command(cls=create_user_command())
@click.option('--csv', help="path to csv file of users")
@click.option('--pool-id', help="id of the user pool to create/update users")
@click.option('--username', help="username, e.g. P0001")
@click.option('--email', help="user's email address")
@click.option('--clients', help='comma-delimited list of client codes that this user can access')
@click.pass_context
def create_user(ctx, csv, pool_id, username, email, clients):
    """ Create/update a user from the command line or specify a csv file """

    print(f"Creating / updating users in account {ctx.obj.get('account_alias')} in pool {pool_id}")
    if csv:
        print(f"Importing from file: {csv}")
        users = load_csv(csv)
    else:
        users = [
            {
                'username': username,
                'email': email,
                'clients': clients
            }
        ]
    for user in users:
        print(f"USER = {user}")
        process_user(pool_id, **user)


if __name__ == '__main__':
    cli(obj={})
