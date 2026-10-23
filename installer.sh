#!/bin/sh
# Installer usable only after ALL repo files are published on GitHub.
set -eu
BASE=https://raw.githubusercontent.com/OliOli2013/OpenCamView-Plugin/main/packages
PKG=enigma2-plugin-extensions-opencamview_2.0.1_all
if ! command -v python3 >/dev/null 2>&1;then echo 'Wymagany Python 3' >&2;exit 1;fi
if command -v opkg >/dev/null 2>&1;then EXT=ipk
elif command -v dpkg >/dev/null 2>&1;then EXT=deb
else echo 'Brak opkg/dpkg' >&2;exit 1;fi
if ! command -v sha256sum >/dev/null 2>&1;then echo 'Brak sha256sum' >&2;exit 1;fi
TMP=$(mktemp -d /tmp/ocv.XXXXXX)
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
if command -v wget >/dev/null 2>&1;then
    wget -q -O "$TMP/SHA256SUMS" "$BASE/SHA256SUMS"
    wget -q -O "$TMP/$PKG.$EXT" "$BASE/$PKG.$EXT"
else
    curl -fsSL "$BASE/SHA256SUMS" -o "$TMP/SHA256SUMS"
    curl -fsSL "$BASE/$PKG.$EXT" -o "$TMP/$PKG.$EXT"
fi
(cd "$TMP" && grep "  $PKG.$EXT\$" SHA256SUMS | sha256sum -c -)
if [ "$EXT" = ipk ];then opkg install "$TMP/$PKG.$EXT";else dpkg -i "$TMP/$PKG.$EXT";fi
echo 'Restartuj GUI Enigma2 po instalacji OpenCamView 2.0.1'
