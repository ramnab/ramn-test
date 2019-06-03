#!/usr/bin/env bash


SCRIPT_DIR=$(dirname "$0")
ROOT_DIR=${SCRIPT_DIR}/..
DIST_DIR=${ROOT_DIR}/dist

rm -r ${DIST_DIR}
mkdir -p ${DIST_DIR}/scripts
mkdir -p ${DIST_DIR}/src/connectmetrics/code
mkdir -p ${DIST_DIR}/docs

cp -r ${SCRIPT_DIR}/connect-metrics-cli.ps1 ${DIST_DIR}/scripts/connect-metrics-cli.ps1

cp -r ${ROOT_DIR}/src/connectmetrics/code ${DIST_DIR}/src/connectmetrics

cp ${ROOT_DIR}/requirements.txt ${DIST_DIR}
cp ${ROOT_DIR}/CHANGELOG.md ${DIST_DIR}

cp -r ${ROOT_DIR}/config ${DIST_DIR}/config
cp ${ROOT_DIR}/docs/*.pdf ${DIST_DIR}/docs


pushd ${DIST_DIR}
zip -r connect-dashboard-metrics.zip *
popd
