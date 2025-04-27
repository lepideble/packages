#!/bin/sh

cd $(dirname $(cd $(dirname $0) && pwd))

KEY=$(python3 -c "import config; print(config.signing_key)")

for FILE in feeds/*.xml; do
    DEST="public/$(basename $FILE)"

    cp "$FILE" "$DEST"

    0install run https://apps.0install.net/0install/0publish.xml --xmlsign --key=$KEY $DEST
done
