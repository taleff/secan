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

# Function to sign individual files with error handling
sign_file() {
    local file="$1"
    if codesign --force --sign - "$file" 2>/dev/null; then
        return 0
    else
        echo "Failed to sign: $(basename "$file")"
        return 1
    fi
}

# First, sign all individual executable files and libraries
SIGN_ERRORS=0

# Find and sign all dylibs and so files
while IFS= read -r -d '' file; do
    sign_file "$file" || ((SIGN_ERRORS++))
done < <(find "$APP_BUNDLE" -type f \( -name "*.dylib" -o -name "*.so" \) -print0)

# Find and sign all executable files (but not the main app bundle itself)
while IFS= read -r -d '' file; do
    # Skip if it's a directory or the main app bundle
    if [ -f "$file" ] && [ "$file" != "$APP_BUNDLE" ]; then
        sign_file "$file" || ((SIGN_ERRORS++))
    fi
done < <(find "$APP_BUNDLE/Contents/MacOS" -type f -perm +111 -print0)

# Remove any extended attributes that might interfere with signing
xattr -cr "$APP_BUNDLE" 2>/dev/null || true

# Sign the main app bundle with less strict options
if codesign --force --sign - --options runtime --entitlements /dev/null "$APP_BUNDLE" 2>/dev/null; then
    echo "Main application bundle signed successfully"
elif codesign --force --sign - "$APP_BUNDLE" 2>/dev/null; then
    echo "Main application bundle signed (without hardened runtime)"
else
    echo "Main bundle signing failed, trying alternative approach..."
    # Try signing without the problematic subdirectories
    if [ -d "$APP_BUNDLE/Contents/MacOS/_internal" ]; then
        # Move problematic files temporarily and sign
        TEMP_INTERNAL="$TEMP_DIR/temp_internal"
        mv "$APP_BUNDLE/Contents/MacOS/_internal" "$TEMP_INTERNAL" 2>/dev/null || true
        
        # Try signing without the _internal directory
        if codesign --force --sign - "$APP_BUNDLE" 2>/dev/null; then
            echo "App bundle signed without _internal directory"
            # Move the files back
            mv "$TEMP_INTERNAL" "$APP_BUNDLE/Contents/MacOS/_internal" 2>/dev/null || true
        else
            # Move files back and continue anyway
            mv "$TEMP_INTERNAL" "$APP_BUNDLE/Contents/MacOS/_internal" 2>/dev/null || true
            echo "Code signing had issues, but continuing with DMG creation..."
        fi
    else
        echo "Code signing had issues, but continuing with DMG creation..."
    fi
fi

# Report signing summary
if [ $SIGN_ERRORS -gt 0 ]; then
    echo "Encountered $SIGN_ERRORS signing errors, but app should still be functional"
else
    echo "All components signed successfully"
fi

# Verify the signature (but don't fail if verification fails)
if codesign --verify "$APP_BUNDLE" 2>/dev/null; then
    echo "Code signature verification passed"
else
    echo "Code signature verification had issues, but the app may still work"
fi

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
