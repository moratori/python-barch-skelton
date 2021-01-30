#!/bin/bash

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
CURRENT=$(cd $(dirname $0) && pwd)
PROJECT_ROOT="$(cd ${CURRENT%/}/../../ && pwd)"
BIN="${PROJECT_ROOT}/bin"

. ${PROJECT_ROOT}/conf/shell/common.sh

SELF="`basename $0`"
SELF_CONF="${PROJECT_ROOT}/conf/shell/${SELF}"

if [ -x "${SELF_CONF}" ]; then
    . ${SELF_CONF}
fi
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

find ${LOGS} -type f -mtime +${LOG_GZIP_PERIOD} -name "${ARCHIVE_TARGET_PATTERN}" ! -name "${ARCHIVED_PATTERN}" | xargs --no-run-if-empty ${ARCHIVE_CMD}
find ${LOGS} -type f -mtime +${LOG_REMOVE_PERIOD} -name "${ARCHIVED_PATTERN}" | xargs --no-run-if-empty rm
