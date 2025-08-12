#!/bin/bash

set -e  # Exit on any error

APP_DIR="dist/secan"
MAIN_EXEC="dist/secan"
DMG_NAME="secan-installer"
VERSION="0.1.0"

# Validate input directory
if [ ! -d "$APP_DIR" ]; then
    print_error "Application directory '$APP_DIR' does not exist"
    exit 1
fi

APP_NAME=$(basename "$MAIN_EXEC")

# Create temporary working directory
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

APP_BUNDLE="$TEMP_DIR/${APP_NAME}.app"
DMG_TEMP="$TEMP_DIR/dmg_temp"
DMG_PATH="$PWD/${DMG_NAME}.dmg"

# Create the .app bundle structure
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"

# Copy the PyInstaller directory contents to MacOS
cp -R "$APP_DIR"/* "$APP_BUNDLE/Contents/MacOS/"

# Create Info.plist
cat > "$APP_BUNDLE/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>$APP_NAME</string>
    <key>CFBundleIdentifier</key>
    <string>com.local.${APP_NAME}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>$APP_NAME</string>
    <key>CFBundleDisplayName</key>
    <string>$APP_NAME</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>$VERSION</string>
    <key>CFBundleVersion</key>
    <string>$VERSION</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSAppleScriptEnabled</key>
    <false/>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
</dict>
</plist>
EOF

# Make the main executable file executable
chmod +x "$APP_BUNDLE/Contents/MacOS/$APP_NAME"

# Sign all executable files and dylibs in the bundle
find "$APP_BUNDLE" -type f \( -name "*.dylib" -o -name "*.so" -o -perm +111 \) -exec codesign --force --sign - {} \; 2>/dev/null || true

# Sign the main app bundle
codesign --force --deep --sign - "$APP_BUNDLE"

# Verify the signature
codesign --verify --verbose=2 "$APP_BUNDLE" 2>/dev/null

# Create DMG staging directory
mkdir -p "$DMG_TEMP"
cp -R "$APP_BUNDLE" "$DMG_TEMP/"

# Create Applications symlink for easy installation
ln -sf /Applications "$DMG_TEMP/Applications"

# Calculate size needed for DMG (add 20% padding)
SIZE_KB=$(du -sk "$DMG_TEMP" | cut -f1)
SIZE_KB=$((SIZE_KB + SIZE_KB / 5))

print_status "Creating DMG image..."

# Remove existing DMG if it exists
[ -f "$DMG_PATH" ] && rm "$DMG_PATH"

# Create the DMG
hdiutil create -srcfolder "$DMG_TEMP" \
    -format UDZO \
    -compression 9 \
    -volname "$APP_NAME Installer" \
    -size ${SIZE_KB}k \
    "$DMG_PATH"
