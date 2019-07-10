#!/usr/bin/env bash

rm -rf generated

mkdir -p generated/transforms
mkdir -p generated/integration

cp -r transforms/* generated/transforms
cp -r integration/* generated/integration

PY=$(eval "pipenv run python scripts/token_replace.py")

find ./generated/ -type f -regex '.*/deployer.*\.sh' -exec bash -c 'eval {}' \;

if [[ ! -z ${PY} ]]; then
    echo "Success!"

else
    echo "Failure!"
fi

