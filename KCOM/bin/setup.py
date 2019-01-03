import stacks


def main():

    opts = stacks.get_opts()
    config = opts['config']
    auto_accept = opts['auto_accept']
    one = opts.get('one')

    customer_session = stacks.get_session(config['role'], 'eu-central-1')
    common_session = stacks.get_session(config['commonRole'], 'eu-central-1')

    acc = f"{config['customer']}-{config['env']}"
    print(f"""

SETTING UP FOR ACCOUNT {acc}
-----------------------{'-' * len(acc)}
AUTO ACCEPT CHANGES = {auto_accept}

""")

    common_resources = 'CAPITA/cloudformation/common-account/resources'
    customer_resources = 'CAPITA/cloudformation/customer-account/resources'

    # Create / Update VPC for Customer Account
    if not one or one == 'vpc':
        print("\nConfiguring VPC")
        print("---------------")
        stacks.run_stack(customer_session,
                         customer_resources + '/vpc.template',
                         config['stVpcName'], config, auto_accept)

    # Create / Update Subnets for Customer Account
    if not one or one == 'subnets':
        print("\nConfiguring Subnets")
        print("-------------------")
        stacks.run_stack(customer_session,
                         customer_resources + '/subnets.template',
                         config['stSubnetsName'], config, auto_accept)

    # Create / Update Security Groups for Customer Account
    if not one or one == 'sg':
        print("\nConfiguring Security Groups")
        print("---------------------------")
        stacks.run_stack(customer_session,
                         customer_resources + '/security-groups.template',
                         config['stSecurityGroupsName'], config, auto_accept)

    # Create / Update Common Account with Peering to Common Account
    stacks.update_config(common_session, config)
    if not one or one == 'peering':
        print("\nConfiguring Peering in Common Account")
        print("-------------------------------------")
        stacks.run_stack(common_session,
                         common_resources + '/vpc-peering.template',
                         config['stPeeringName'], config, auto_accept)

    # NO LONGER REQUIRED
    # # Create / Update SQS for CTR records
    # if not one or one == 'sqs':
    #     print("\nConfiguring SQS")
    #     print("----------------------")
    #     stacks.run_stack(customer_session,
    #                      customer_resources + '/sqs.template',
    #                      config['stCTRSQS'], config, auto_accept)

    # Create / Update S3 Buckets for Customer Account
    if not one or one == 's3':
        print("\nConfiguring S3 Buckets")
        print("----------------------")
        stacks.run_stack(customer_session,
                         customer_resources + '/s3-for-connect.template',
                         config['stS3Buckets'], config, auto_accept)

    # Create / Update CTR S3 Bucket for Customer Account
    if not one or one == 'ctr':
        print("\nConfiguring S3 CTR Bucket")
        print("-------------------------")
        stacks.run_stack(customer_session,
                         customer_resources + '/s3-for-ctr.template',
                         config['stS3CTR'], config, auto_accept)


# Create / Update Connect Master Key
    if not one or one == 'kms':
        print("\nConfiguring Connect Master Key")
        print("------------------------------")
        stacks.run_stack(customer_session,
                         customer_resources + '/kms.template',
                         config['stConnectKMS'], config, auto_accept)

# Create / Update all Kinesis config
    if not one or one == 'kinesis':
        print("\nConfiguring Kinesis")
        print("-------------------")
        stacks.run_stack(customer_session,
                         customer_resources + '/kinesis.template',
                         config['stKinesis'], config, auto_accept)


if __name__ == '__main__':
    main()
