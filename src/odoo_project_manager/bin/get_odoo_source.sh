#!/bin/bash

target_version=$1
path_to_odoo=false

while read -r release_file; do
  found_version=$(grep "version_info = " $release_file | awk '{print $3}' | tr -d '(,')
  if [ "$target_version" == "$found_version" ]; then
    path_to_odoo="${release_file%/*/*}"
  fi
done < <(find ~ -path "*/odoo/release.py")

echo "$path_to_odoo"
