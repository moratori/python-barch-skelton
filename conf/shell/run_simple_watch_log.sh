#!/bin/bash

ALERT_NOTIFY_WAIT="1"
ALERT_NOTIFY_SLACK_URL=""
TAIL_LOG_FILE_PATTERN='^==> .*\.log <==$'
WATCH_TARGET_PATTERN="${LOGS}/main_*.log"

declare -A LOG_LEVELS=(
    ['CRITICAL']='^20..-..-.. ..:..:..,... \[CRITICAL\] '
    ['ERROR']='^20..-..-.. ..:..:..,... \[ERROR\] '
    ['WARNING']='^20..-..-.. ..:..:..,... \[WARNING\] '
)

