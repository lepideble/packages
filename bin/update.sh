#!/bin/sh

set -e

cd $(dirname $(cd $(dirname $0) && pwd))

export PYTHONPATH=".:./packaging:$PYTHONPATH"

python3 apps/$1.py update feeds/$1.xml
