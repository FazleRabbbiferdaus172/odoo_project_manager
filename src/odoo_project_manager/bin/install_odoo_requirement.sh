#!/bin/bash

PATH_TO_ODOO="$1"
VENV_DIR="$2"

if [ "$PATH_TO_ODOO" != false ]; then
  source $VENV_DIR/activate
  cd "$PATH_TO_ODOO"
  pip install -r requirements.txt
  pip freeze
fi
