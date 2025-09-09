#!/bin/macos_installer.sh
codesign --verify --deep --strict --verbose=2 dist/Secan.app

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
  "secan-installer.dmg" \
  "dist/dmg/"

