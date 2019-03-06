import time
import boto3
import yaml
import re
import random
import argparse
import json


STACK_FAILED_STATUSES = [
    'CREATE_FAILED',
    'ROLLBACK_IN_PROGRESS',
    'ROLLBACK_FAILED',
    'ROLLBACK_COMPLETE',
    'DELETE_FAILED',
    'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS',
    'UPDATE_ROLLBACK_IN_PROGRESS',
    'UPDATE_ROLLBACK_FAILED',
    'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS',
    'UPDATE_ROLLBACK_COMPLETE'
]


def re_factory(config):
    def replacer(match):
        word = match.group(1)
        return config.get(word, word)

    return replacer


def update_config(session, config):
    cf = session.client('cloudformation')

    stacks = dict()
    for s in cf.describe_stacks()['Stacks']:
        stacks[s['StackName']] = s.get('Outputs')

    p = re.compile(r'\|Ref\|(st.+)\.(o.+)')
    for key, val in config.items():
        m = p.match(val)
        if m:
            stack = m.group(1)
            output = m.group(2)
            if stacks.get(stack):
                replaced = next(o['OutputValue']
                                for o in stacks.get(stack)
                                if o['OutputKey'] == output)

                config[key] = replaced


def who_me(session):
    sts = session.client('sts')
    return sts.get_caller_identity()


def stack_exists(session, stack_name):
    cf = session.client('cloudformation')
    stacks = cf.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == "DELETE_COMPLETE":
            continue
        if stack['StackName'] == stack_name:
            return True
    return False


def run_stack(session, template, stack_name, config, auto_accept):
    identity = who_me(session)
    update_config(session, config)
    print(f"\nAs user {identity['UserId']}, in account {identity['Account']}")

    change_type = 'CREATE'
    if stack_exists(session, stack_name):
        change_type = 'UPDATE'

    result = get_change_set(session, template, stack_name, config, change_type)

    if result:
        changes = result.get('Changes')
        change_set = result.get('ChangeSetName')
        print(f"\n\nChange set: {change_set}\n\nChanges:")
        print(changes)
        do_change = "y"
        if not auto_accept:
            do_change = input("Apply changes? y/n (n) ")

        if do_change.lower() == "y":
            print("Updating stack...")
            apply_change_set(session, change_set, stack_name)
            print("Change set completed")
    else:
        print("\nNo changes...")
    update_config(session, config)


def apply_change_set(session, change_set, stack_name):
    cf = session.client('cloudformation')
    cf.execute_change_set(ChangeSetName=change_set,
                          StackName=stack_name)
    wait_for_change_set_exec(cf, change_set, stack_name)
    wait_for_stack(cf, stack_name, False)


def extract_params(template, config):
    template_body = json.load(open(template, 'r'))

    nconfig = {}
    for pkey, _pval in template_body.get('Parameters').items():
        if config.get(pkey):
            nconfig[pkey] = config.get(pkey)
    print(f"Parameters for template '{template}'")
    print(json.dumps(nconfig, indent=2))
    return nconfig


def expand_params(params):

    expanded = []
    for key, val in params.items():
        expanded.append({
            'ParameterKey': key,
            'ParameterValue': val
        })
    return expanded


def get_change_set(session, template, stack_name, config, change_type):

    template_body = open(template, 'r').read()
    cf = session.client('cloudformation')
    r = str(random.randint(1001, 2000))
    change_set_name = stack_name + r + change_type

    print(f"Creating change set {change_set_name}")
    cf.create_change_set(
        StackName=stack_name,
        TemplateBody=template_body,
        Parameters=expand_params(extract_params(template, config)),
        Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
        ChangeSetName=change_set_name,
        ChangeSetType=change_type
    )
    return wait_for_change_set_created(cf, change_set_name, stack_name)


def wait_for_change_set_created(cf, change_set_name, stack_name):
    print(f"\n\nWaiting for stack change set to be created...")
    time.sleep(3)
    result = cf.describe_change_set(ChangeSetName=change_set_name,
                                    StackName=stack_name)

    if result.get('Status') == 'FAILED':
        changes = result.get('Changes')
        nchanges = len(changes)
        if changes is not None and nchanges == 0:
            return None
        status_reason = result.get('StatusReason')
        print(f"Change set failed: {status_reason}")
        raise Exception(f"Unable to create change set: {status_reason}")
    if result.get('Status') == 'CREATE_COMPLETE':
        return result
    return wait_for_change_set_created(cf, change_set_name, stack_name)


def wait_for_change_set_exec(cf, change_set_name, stack_name):
    print(f"\n\nWaiting for stack change set to complete")
    time.sleep(5)
    try:
        result = cf.describe_change_set(ChangeSetName=change_set_name,
                                        StackName=stack_name)

        if result.get('ExecutionStatus') == 'EXECUTE_FAILED':
            status_reason = result.get('StatusReason')
            print(f"Change set failed: {status_reason}")
            raise Exception(f"Change set execution failed: {status_reason}")

        if result.get('ExecutionStatus') == 'EXECUTE_COMPLETE':
            return True
        return wait_for_change_set_created(cf, change_set_name, stack_name)
    except Exception:
        return True


def wait_for_stack(cf, stack_name, retry):
    print(f"\n\nWaiting for stack {stack_name} to update")
    time.sleep(5)
    result = cf.describe_stacks(StackName=stack_name)

    status = result.get('StackStatus')
    print(f"Stack status: {status}")

    if status and status in STACK_FAILED_STATUSES:
        raise Exception(f"{status}: {result.get('StackStatusReason')}")

    if status and 'IN_PROGRESS' in status:
        wait_for_stack(cf, stack_name, False)

    if status is None and not retry:
        wait_for_stack(cf, stack_name, True)


def get_session(role_arn, region):
    sts = boto3.client('sts')
    session_name = 'role_'+str(random.randint(1001, 2000))
    auth = sts.assume_role(RoleArn=role_arn,
                           RoleSessionName=session_name)['Credentials']

    akey1 = auth['AccessKeyId']
    skey1 = auth['SecretAccessKey']
    sess1 = auth['SessionToken']

    session = boto3.session.Session(aws_access_key_id=akey1,
                                    aws_secret_access_key=skey1,
                                    aws_session_token=sess1,
                                    region_name=region)
    return session


def get_opts():
    parser = argparse.ArgumentParser('''
        Set up a customer Connect account linked to a Common account
    ''')
    parser.add_argument(
        '-c', '--config', help='Path to customer account config file',
        required=True
    )
    parser.add_argument(
        '-d', '--defaults', help='Path to customer account config file',
        required=False, default='KCOM/customer-account/defaults.yaml'
    )
    parser.add_argument(
        '--one', help='Run only the specified stack',
        required=False
    )
    parser.add_argument(
        '-y', help='Auto accept changes', action='store_true'
    )
    args = parser.parse_args()
    config = yaml.safe_load(open(args.defaults))
    config.update(yaml.safe_load(open(args.config)))
    print(config)

    pattern = r'\[([_a-zA-Z0-9-\s]+)\]'
    replacer = re_factory(config)

    for key, val in config.items():
        config[key] = re.sub(pattern, replacer, val)

    return {'config': config, 'auto_accept': args.y, 'one': args.one}
