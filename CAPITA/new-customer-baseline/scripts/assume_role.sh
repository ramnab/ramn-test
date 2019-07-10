#!/usr/bin/env bash

ROLE_ARN=$1
echo "Using role: ${ROLE_ARN}"
sts=($(aws sts assume-role --role-arn ${ROLE_ARN} --role-session-name "ca_codebuild_deploy" --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' --output text))
AWS_ACCESS_KEY_ID="${sts[0]}"
AWS_SECRET_ACCESS_KEY="${sts[1]}"
AWS_SESSION_TOKEN="${sts[2]}"

mkdir -p ~/.aws/
touch ~/.aws/credentials
touch ~/.aws/config

cat <<EOF > ~/.aws/credentials
[default]
aws_access_key_id = ${AWS_ACCESS_KEY_ID}
aws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}
aws_session_token = ${AWS_SESSION_TOKEN}
EOF

cat <<EOF > ~/.aws/config
[default]
region = eu-central-1
EOF
