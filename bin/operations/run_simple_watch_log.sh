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


function get_log_file_name_from_tail_header(){
    local line="`cat -`"
    if [ ! -z "`echo "${line}" | /usr/bin/grep "${TAIL_LOG_FILE_PATTERN}"`" ]; then
        echo "${line}" | \
            /usr/bin/sed -e 's/^==> //g' | \
            /usr/bin/sed -e 's/ <==$//g'
    else
        echo ""
    fi
}

function get_log_level_from_log_line(){
    local line="`cat -`"
    local result=''
    for level in "${!LOG_LEVELS[@]}"; do
        local pattern="${LOG_LEVELS[${level}]}"
        if [ ! -z "`echo "${line}" | /usr/bin/grep "${pattern}"`" ]; then
            result="${level}"
            break
        fi
    done
    echo "${result}"
}

function notify_log_line(){
    local line="`cat -`"
    if [ $# -eq 2 ]; then
        local log_file_name="${1}"
        local log_level="${2}"

        echo "${line}" | notify_slack "${log_file_name}" "${log_level}"

        /usr/bin/sleep ${ALERT_NOTIFY_WAIT}
    fi
}

function notify_slack(){
    local message="`cat -`"
    local log_file_name="${1}"
    local log_level="${2}"
    local text="Level:${log_level}\nFile:${log_file_name}\nMessage:${message}"
    local body="{\"text\":\"${text}\"}"
    if [ ! -z "${ALERT_NOTIFY_SLACK_URL}" ]; then
        /usr/bin/curl -X POST -H 'Content-type: application/json' --data "${body}" ${ALERT_NOTIFY_SLACK_URL} > /dev/null 2>&1
    fi
}






target_log_file_cnt="`/usr/bin/find "${LOGS}" -type f -name '*.log' | wc -l`"
if [ ${target_log_file_cnt} -eq 0 ]; then
    echo "unable to find target log file: ${LOGS}"
    exit 1
fi


log_file_name=''
/usr/bin/tail -F -n0 ${WATCH_TARGET_PATTERN} 2> /dev/null | \
    while read line
    do
        is_fname="`echo "${line}" | get_log_file_name_from_tail_header`"
        if [ ! -z "${is_fname}" ]; then
            log_file_name="${is_fname}"
            continue
        fi

        log_level="`echo "${line}" | get_log_level_from_log_line`"
        if [ ! -z "${log_level}" ]; then
            echo "${line}" | \
                notify_log_line "${log_file_name}" "${log_level}"
        fi
    done
