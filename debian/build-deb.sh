#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
PACKAGE_NAME=${PACKAGE_NAME:-changeme}
VERSION_FILE="$ROOT_DIR/VERSION"
CONTROL_TEMPLATE="$ROOT_DIR/debian/control.template"
LAUNCHER_FILE="$ROOT_DIR/debian/changeme.launcher"
BUILD_DIR=${BUILD_DIR:-"$ROOT_DIR/build/deb"}
DIST_DIR=${DIST_DIR:-"$ROOT_DIR/dist"}
DEB_ARCH=${DEB_ARCH:-$(dpkg --print-architecture)}

if [[ ! -f "$VERSION_FILE" ]]; then
    echo "Missing VERSION file: $VERSION_FILE" >&2
    exit 1
fi

VERSION=$(tr -d '[:space:]' < "$VERSION_FILE")
if [[ ! "$VERSION" =~ ^[0-9][A-Za-z0-9.+:~_-]*$ ]]; then
    echo "Invalid Debian package version in VERSION: $VERSION" >&2
    exit 1
fi

PKG_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}_${DEB_ARCH}"
OPT_DIR="$PKG_ROOT/opt/$PACKAGE_NAME"
BIN_DIR="$OPT_DIR/bin"
DEBIAN_DIR="$PKG_ROOT/DEBIAN"
USR_BIN_DIR="$PKG_ROOT/usr/bin"
MAN_DIR="$PKG_ROOT/usr/share/man/man1"
DOC_DIR="$PKG_ROOT/usr/share/doc/$PACKAGE_NAME"
DEB_PATH="$DIST_DIR/${PACKAGE_NAME}_${VERSION}_${DEB_ARCH}.deb"

rm -rf "$PKG_ROOT"
mkdir -p "$OPT_DIR" "$BIN_DIR" "$DEBIAN_DIR" "$USR_BIN_DIR" "$MAN_DIR" "$DOC_DIR" "$DIST_DIR"

cp -a \
    "$ROOT_DIR/changeme.py" \
    "$ROOT_DIR/changeme" \
    "$ROOT_DIR/creds" \
    "$ROOT_DIR/requirements.txt" \
    "$ROOT_DIR/VERSION" \
    "$ROOT_DIR/COPYING" \
    "$ROOT_DIR/README.md" \
    "$OPT_DIR/"

install -m 0755 "$LAUNCHER_FILE" "$BIN_DIR/changeme"
ln -s "/opt/$PACKAGE_NAME/bin/changeme" "$USR_BIN_DIR/changeme"

gzip -c "$ROOT_DIR/changeme.1" > "$MAN_DIR/changeme.1.gz"
cp "$ROOT_DIR/COPYING" "$DOC_DIR/copyright"


sed \
    -e "s/@VERSION@/$VERSION/g" \
    -e "s/@ARCH@/$DEB_ARCH/g" \
    "$CONTROL_TEMPLATE" > "$DEBIAN_DIR/control"

cat > "$DEBIAN_DIR/postinst" <<POSTINST
#!/bin/sh
set -e
if [ "\$1" = "configure" ]; then
    chmod +x /opt/$PACKAGE_NAME/bin/changeme
    python3 -m venv /opt/$PACKAGE_NAME/.venv
    /opt/$PACKAGE_NAME/.venv/bin/python3 -m pip install -r /opt/$PACKAGE_NAME/requirements.txt
fi
exit 0
POSTINST
chmod 0755 "$DEBIAN_DIR/postinst"

cat > "$DEBIAN_DIR/postrm" <<POSTRM
#!/bin/sh
set -e
if [ "\$1" = "purge" ]; then
    rm -rf /opt/$PACKAGE_NAME/.venv
fi
exit 0
POSTRM
chmod 0755 "$DEBIAN_DIR/postrm"

dpkg-deb --build --root-owner-group "$PKG_ROOT" "$DEB_PATH"
echo "Built $DEB_PATH"
