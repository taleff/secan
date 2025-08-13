#!/bin/macos_installer.sh

mkdir -p dist/dmg
rm -r dist/dmg/*
cp -r "dist/secan.app" dist/dmg

create-dmg \
  --volname "Secan" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon "secan.app" 175 120 \
  --hide-extension "secan.app" \
  --app-drop-link 425 120 \
  "dist/secan-installer.dmg" \
  "dist/dmg/"

