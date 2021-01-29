#!/bin/bash

#######################################
CURRENT=$(cd $(dirname $0) && pwd)
PROJECT_ROOT="$(cd ${CURRENT%/}/../../ && pwd)"
BIN="${PROJECT_ROOT}/bin"

. ${BIN}/common.sh

LOG_GZIP_PERIOD=3
LOG_REMOVE_PERIOD=120
ARCHIVE_TARGET_PATTERN="*.log.*"
ARCHIVE_CMD="gzip"
ARCHIVED_PATTERN="*.gz"
#######################################

find ${LOGS} -type f -mtime +${LOG_GZIP_PERIOD} -name "${ARCHIVE_TARGET_PATTERN}" ! -name "${ARCHIVED_PATTERN}" | xargs --no-run-if-empty ${ARCHIVE_CMD}
find ${LOGS} -type f -mtime +${LOG_REMOVE_PERIOD} -name "${ARCHIVED_PATTERN}" | xargs --no-run-if-empty rm
