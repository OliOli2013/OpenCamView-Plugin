#!/bin/sh
# OpenCamView Enigma2 installer - downloads and verifies SHA-256 before installing.
set -eu
NAME=enigma2-plugin-extensions-opencamview
VERSION=2.0.3
BASE=https://raw.githubusercontent.com/OliOli2013/OpenCamView-Plugin/main/packages
PKG=${NAME}_${VERSION}_all
if ! command -v python3 >/dev/null 2>&1; then
  echo 'OpenCamView requires Python 3' >&2; exit 1
fi
if command -v opkg >/dev/null 2>&1; then
  EXT=ipk
  INSTALLED=$(opkg status "$NAME" 2>/dev/null | sed -n 's/^Version: *//p' | head -n 1 || true)
elif command -v dpkg >/dev/null 2>&1; then
  EXT=deb
  INSTALLED=$(dpkg-query -W -f='${Version}' "$NAME" 2>/dev/null || true)
else
  echo 'No opkg/dpkg package manager found' >&2; exit 1
fi
if [ "$INSTALLED" = "$VERSION" ]; then
  echo "OpenCamView $VERSION is already installed. No update required."
  exit 0
fi
if ! command -v sha256sum >/dev/null 2>&1; then
  echo 'sha256sum is required for download verification' >&2; exit 1
fi
if ! command -v wget >/dev/null 2>&1 && ! command -v curl >/dev/null 2>&1; then
  echo 'wget or curl is required' >&2; exit 1
fi
TMP=$(mktemp -d /tmp/ocv.XXXXXX)
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
if command -v wget >/dev/null 2>&1; then
  wget -q -O "$TMP/SHA256SUMS" "$BASE/SHA256SUMS"
  wget -q -O "$TMP/$PKG.$EXT" "$BASE/$PKG.$EXT"
else
  curl -fsSL "$BASE/SHA256SUMS" -o "$TMP/SHA256SUMS"
  curl -fsSL "$BASE/$PKG.$EXT" -o "$TMP/$PKG.$EXT"
fi
(cd "$TMP" && grep "  $PKG.$EXT\$" SHA256SUMS | sha256sum -c -)
if [ "$EXT" = ipk ]; then
  opkg install "$TMP/$PKG.$EXT"
else
  dpkg -i "$TMP/$PKG.$EXT"
fi
echo "OpenCamView $VERSION installed successfully. Restart Enigma2 GUI."
