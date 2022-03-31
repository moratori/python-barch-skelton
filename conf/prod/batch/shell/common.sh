#!/bin/bash

#######################################
BIN="${PROJECT_ROOT}/bin"
LOCKS="${PROJECT_ROOT}/jobs/locks"
SOURCES="${PROJECT_ROOT}/src"
LOGS="${PROJECT_ROOT}/logs"
TESTS="${PROJECT_ROOT}/test"
VENV="${PROJECT_ROOT}/.venv"
TOPLEVEL_SCRIPT_EXT="py"
#######################################

# write common setting

export PIPENV_VERBOSITY=-1
