#!/bin/sh

VERSION=0.2

# Build package
dpkg-deb --build snapclient-switcher

# Rename package
mv snapclient-switcher.deb snapclient-switcher-$VERSION.deb

exit 0
