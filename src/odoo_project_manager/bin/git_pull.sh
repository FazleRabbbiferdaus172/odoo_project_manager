#!/bin/bash

# repository is should be the first argument and second argument is project director

if [ "$#" -lt 2 ]; then
  exit 1
fi

git clone -q --recursive $1 $2
