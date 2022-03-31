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
SELF_CONF="${PROJECT_ROOT}/conf/${ENVIRON}/batch/shell/${SELF}"

if [ -x "${SELF_CONF}" ]; then
    . ${SELF_CONF}
fi
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

cd ${TESTS}

pipenv run ${COVERAGE} erase

pipenv run ${COVERAGE} run -a --omit ${VENV}/'*' -m unittest discover -v
pipenv run ${COVERAGE} report --omit ${VENV}/'*'
pipenv run ${COVERAGE} html --omit ${VENV}/'*'
pipenv run ${COVERAGE} xml --omit ${VENV}/'*'


pipenv run ${COVERAGE_BADGE} -fo ${PROJECT_ROOT}/coverage.svg

exit 0


