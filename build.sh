#!/usr/bin/env bash

mkdir -p ./build/
rm -f ./build/*.teal # clean
set -e # die on error
python ./compile.py "$1" ./build/approval.teal ./build/clear.teal