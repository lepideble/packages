#!/bin/sh

cd $(dirname $(cd $(dirname $0) && pwd))

BASE_URL=$(python3 -c "import config; print(config.base_url)")
SIGNING_KEY=$(python3 -c "import config; print(config.signing_key)")

LAST_MESSAGE=$(cd public && git log -1 --pretty=%B)
LAST_BUILT_COMMIT=${LAST_MESSAGE#"Update to "}

CURRENT_COMMIT=$(git rev-parse HEAD)

CHANGED_FEEDS=$(git diff --name-only $LAST_BUILT_COMMIT $CURRENT_COMMIT -- feeds)

if [ -z "$CHANGED_FEEDS" ]; then
    exit 0
fi

cp icons/*.png public/

for FILE in $CHANGED_FEEDS; do
    NAME=${FILE#"feeds/"}
    NAME=${NAME%".xml"}

    DEST="public/$NAME.xml"

    cat "$FILE" \
        | sed '1a<?xml-stylesheet href="resources/feed.xsl" type="text/xsl"?>' \
        | sed "s#../icons/#$BASE_URL#" \
        > "$DEST"

    SIGNATURE=$(gpg --default-key=$SIGNING_KEY --detach-sign < $DEST | base64)

    echo "<!-- Base64 Signature" >> $DEST
    echo "$SIGNATURE" >> $DEST
    echo "-->" >> $DEST

    (cd public && git add "$NAME.xml")
done

(cd public && git commit -m "Update to $CURRENT_COMMIT")
