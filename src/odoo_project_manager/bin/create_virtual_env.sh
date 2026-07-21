#!/bin/bash

if [ "$#" -lt 1 ]; then
  exit 1
fi

PYTHON_VERSION="3"
VENV_DIR="${1}/.venv"
PYTHON_BIN="/usr/bin/python${PYTHON_VERSION}"

$PYTHON_BIN -m venv $VENV_DIR

if [ $? -ne 0 ]; then
  exit 1
fi
