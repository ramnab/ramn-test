#!/usr/bin/env bash

# code to deploy idp... see https://docs.aws.amazon.com/cli/latest/reference/iam/create-saml-provider.html

# get Identity Provider ARN and save to
IDP=replaceme

cf sync -y -t ../../../transforms/config-dept-customer \
           -p stCapita-AD-[env]-Permissions.pIdentityProviderArn=${IDP} \
           ad.stacks
