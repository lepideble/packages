#!/bin/sh

cd $(dirname $(cd $(dirname $0) && pwd))

KEY=$(python3 -c "import config; print(config.signing_key)")

for FILE in feeds/*.xml; do
    DEST="public/$(basename $FILE)"

    cat "$FILE" | sed '1a<?xml-stylesheet href="resources/feed.xsl" type="text/xsl"?>' > "$DEST"

    SIGNATURE=$(gpg --default-key=$KEY --detach-sign < $DEST | base64)

    echo "<!-- Base64 Signature" >> $DEST
    echo "$SIGNATURE" >> $DEST
    echo "-->" >> $DEST
done
