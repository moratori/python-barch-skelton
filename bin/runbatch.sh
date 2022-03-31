#!/bin/bash

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
CURRENT=$(cd $(dirname $0) && pwd)
PROJECT_ROOT="$(cd ${CURRENT%/}/.. && pwd)"
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
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
if [ $# -lt 1 ]; then
    echo "specify executable main script name"
    exit 1
fi
EXEC_TARGET="`echo "${1}" | sed -e "s/.${TOPLEVEL_SCRIPT_EXT}$//g"`"
TOPLEVEL="${EXEC_TARGET}.${TOPLEVEL_SCRIPT_EXT}"
EXEC_TARGET_CONF="${PROJECT_ROOT}/conf/${ENVIRON}/batch/shell/${EXEC_TARGET}.sh"

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
