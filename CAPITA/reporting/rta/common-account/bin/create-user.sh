#!/usr/bin/env bash

USERNAME=$1
EMAIL=$2

echo "Creating user: username=${USERNAME}, email=${EMAIL}"
aws cognito-idp admin-create-user --user-pool-id eu-central-1_5vpngTHt2 --username $USERNAME --user-attributes Name=email,Value=${EMAIL} Name=email_verified,Value=true --temporary-password Let.me.in1
