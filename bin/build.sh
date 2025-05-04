#!/bin/sh

cd $(dirname $(cd $(dirname $0) && pwd))

BASE_URL=$(python3 -c "import config; print(config.base_url)")
SIGNING_KEY=$(python3 -c "import config; print(config.signing_key)")

cp icons/*.png public/

for FILE in feeds/*.xml; do
    NAME="$(basename "$FILE" .xml)"
    DEST="public/$NAME.xml"

    cat "$FILE" \
        | sed '1a<?xml-stylesheet href="resources/feed.xsl" type="text/xsl"?>' \
        | sed "s#../icons/#$BASE_URL#" \
        > "$DEST"

    SIGNATURE=$(gpg --default-key=$SIGNING_KEY --detach-sign < $DEST | base64)

    echo "<!-- Base64 Signature" >> $DEST
    echo "$SIGNATURE" >> $DEST
    echo "-->" >> $DEST
done
