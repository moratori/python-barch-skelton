#!/bin/bash

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
CURRENT=$(cd $(dirname $0) && pwd)
PROJECT_ROOT="$(cd ${CURRENT%/}/../../ && pwd)"
BIN="${PROJECT_ROOT}/bin"
ENVIRON="dev"
ENVIRON_FILE="environ"

if [ -f "${PROJECT_ROOT}/${ENVIRON_FILE}" ]; then
    content="`cat ${PROJECT_ROOT}/${ENVIRON_FILE} | tr '[:upper:]' '[:lower:]' | tr -d '\n'`"
    case "${content}" in 
        "dev") ENVIRON="dev";;
        "prod") ENVIRON="prod";;
    esac
fi

. ${PROJECT_ROOT}/conf/${ENVIRON}/batch/shell/common.sh

SELF="`basename $0`"
SELF_CONF="${PROJECT_ROOT}/conf/batch/shell/${SELF}"

if [ -x "${SELF_CONF}" ]; then
    . ${SELF_CONF}
fi
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

find ${LOGS} -type f -mtime +${LOG_GZIP_PERIOD} -name "${ARCHIVE_TARGET_PATTERN}" ! -name "${ARCHIVED_PATTERN}" | xargs --no-run-if-empty ${ARCHIVE_CMD}
find ${LOGS} -type f -mtime +${LOG_REMOVE_PERIOD} -name "${ARCHIVED_PATTERN}" | xargs --no-run-if-empty rm
