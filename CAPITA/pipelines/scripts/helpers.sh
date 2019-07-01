#!/usr/bin/env bash

function config_exists {

    local CONFIG_FILE=${1}
    if [[ -f ${CONFIG_FILE} ]]; then
        echo "Using config file: ${CONFIG_FILE}"
    else
        echo "Config file: ${CONFIG_FILE} does not exist"
        exit 1
    fi
}

function prop {
    # extracts named property from config file
    # if no value then default is used instead
    local PROPERTY=${1}
    local DEFAULT=${2}
    V=$(grep "${PROPERTY}" ${CONF}|cut -d'=' -f2)
    if [[ $? -ne 0 ]]; then exit 1; fi
    if [[ -z ${V} ]]; then echo ${DEFAULT}; else echo ${V}; fi
}
die2() { echo >&2 -e "\nERROR: $@\n"; exit 1; }
run() { "$@"; code=$?; [[ ${code} -ne 0 ]] && die2 "command [$*] failed with error code $code"; }

