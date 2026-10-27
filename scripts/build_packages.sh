#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
NAME=enigma2-plugin-extensions-opencamview
VER=2.0.2
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/data/usr/lib/enigma2/python/Plugins/Extensions/OpenCamView" "$TMP/control" "$TMP/deb/DEBIAN" "$ROOT/packages"
cp "$ROOT/OpenCamView"/*.py "$ROOT/OpenCamView/plugin.png" "$TMP/data/usr/lib/enigma2/python/Plugins/Extensions/OpenCamView/"
cat > "$TMP/control/control" <<EOF
Package: $NAME
Version: $VER
Section: extensions
Priority: optional
Architecture: all
Maintainer: Paweł Pawełek <msisystem@t.pl>
Depends: enigma2
Description: OpenCamView 2.0.2 - Home IP camera viewer for Enigma2 Python3
 RTSP playback, ONVIF, PTZ, JPEG overlay, camera wall and patrol,
 RTSP LAN discovery, optional PiP, intercom, backups and bouquets.
EOF
(cd "$TMP/control" && tar -czf "$TMP/control.tar.gz" control)
(cd "$TMP/data" && tar -czf "$TMP/data.tar.gz" .)
printf '2.0\n' > "$TMP/debian-binary"
rm -f "$ROOT/packages/${NAME}_${VER}_all.ipk"
(cd "$TMP" && ar qc "$ROOT/packages/${NAME}_${VER}_all.ipk" debian-binary control.tar.gz data.tar.gz)
cp "$TMP/control/control" "$TMP/deb/DEBIAN/control"
mkdir -p "$TMP/deb/usr"
cp -a "$TMP/data/usr/." "$TMP/deb/usr/"
dpkg-deb -Zgzip --build "$TMP/deb" "$ROOT/packages/${NAME}_${VER}_all.deb" >/dev/null
(cd "$ROOT/packages" && sha256sum "${NAME}_${VER}_all.ipk" "${NAME}_${VER}_all.deb" > SHA256SUMS)
echo 'Pakiety OpenCamView gotowe:'
ls -lh "$ROOT/packages"/*
