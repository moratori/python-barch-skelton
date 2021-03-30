#!/bin/bash

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
CURRENT=$(cd $(dirname $0) && pwd)
PROJECT_ROOT="$(cd ${CURRENT%/}/.. && pwd)"
BIN="${PROJECT_ROOT}/bin"

. ${PROJECT_ROOT}/conf/shell/common.sh

if [ $# -lt 1 ]; then
    echo "specify executable main script name"
    exit 1
fi

EXEC_TARGET="`echo "${1}" | sed -e "s/.${TOPLEVEL_SCRIPT_EXT}$//g"`"
TOPLEVEL="${EXEC_TARGET}.${TOPLEVEL_SCRIPT_EXT}"
EXEC_TARGET_CONF="${PROJECT_ROOT}/conf/shell/${EXEC_TARGET}.sh"

if [ -x "${EXEC_TARGET_CONF}" ]; then
    . ${EXEC_TARGET_CONF}
fi

if [ ! -x "${SOURCES}/${TOPLEVEL}" ]; then
    echo "specify executable main script name"
    exit 1
fi
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 


cd ${PROJECT_ROOT}

mkdir -p "${LOCKS}"
if ! ln -s $$ "${LOCKS}/${EXEC_TARGET}" > /dev/null 2>&1; then
    echo "lockfile ${LOCKS}/${EXEC_TARGET} found"
    exit 1
fi

shift
pipenv run ${SOURCES}/${TOPLEVEL} $@
return_code=$?

rm "${LOCKS}/${EXEC_TARGET}"

exit ${return_code}
