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

cd ${TESTS}

pipenv run ${COVERAGE} erase

pipenv run ${COVERAGE} run -a --omit ${VENV}/'*' -m unittest discover
pipenv run ${COVERAGE} report --omit ${VENV}/'*'
pipenv run ${COVERAGE} html --omit ${VENV}/'*'
pipenv run ${COVERAGE} xml --omit ${VENV}/'*'


pipenv run ${COVERAGE_BADGE} -fo ${PROJECT_ROOT}/coverage.svg

exit 0


