#!/usr/bin/env bash

ENV=$2
DIRECTORY=$(dirname $0)

python ${DIRECTORY}/describe.py -e ${ENV}
