#!/bin/bash

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
CURRENT=$(cd $(dirname $0) && pwd)
PROJECT_ROOT="$(cd ${CURRENT%/}/.. && pwd)"
BIN="${PROJECT_ROOT}/bin"

. ${PROJECT_ROOT}/conf/shell/common.sh

SELF="`basename $0`"
SELF_CONF="${PROJECT_ROOT}/conf/shell/${SELF}"

if [ -x "${SELF_CONF}" ]; then
    . ${SELF_CONF}
fi

TOPLEVEL="`echo "${SELF}" | sed -e "s/\.sh$/.${TOPLEVEL_SCRIPT_EXT}/g"`"
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

cd ${PROJECT_ROOT}

# If exclusive control is required, please comment out the following
mkdir -p "${LOCKS}"
if ! ln -s $$ "${LOCKS}/${SELF}" > /dev/null 2>&1; then
    exit 1
fi

/usr/bin/timeout ${TIMEOUT_DURATION} pipenv run ${SOURCES}/${TOPLEVEL} $@
return_code=$?

# If exclusive control is required, please comment out the following
rm "${LOCKS}/${SELF}"

exit ${return_code}
