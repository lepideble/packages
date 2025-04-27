#!/bin/sh

set -e

cd $(dirname $(cd $(dirname $0) && pwd))

export PYTHONPATH=".:$PYTHONPATH"

for FILE in apps/*.py; do
    echo "Updating $FILE"

    python3 $FILE
done
