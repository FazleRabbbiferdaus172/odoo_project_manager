#!/bin/bash

target_version=$1
VENV_DIR="$2"
path_to_odoo=false

while read -r release_file; do
  echo $release_file
  found_version=$(grep "version_info = " $release_file | awk '{print $3}' | tr -d '(,')
  if [ "$target_version" == "$found_version" ]; then
    path_to_odoo="${release_file%/*/*}"
    echo "$path_to_odoo"
  fi
done < <(find ~ -path "*/odoo/release.py")

if [ "$path_to_odoo" != false ]; then
  source $VENV_DIR/activate
  cd "$path_to_odoo"
  pip install -r requirements.txt
  pip freeze
fi
