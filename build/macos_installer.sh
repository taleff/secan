#!/bin/bash
# build/macos_installer.sh

set -e  # Exit on error

APP_NAME="Secan"
APP_VERSION="0.1.0"
BUNDLE_ID="com.secan.secan"

# Install create-dmg
brew install create-dmg

# Remove any existing .app bundle
rm -rf dist/secan.app

# Create new .app bundle structure
mkdir -p dist/secan.app/Contents/MacOS
mkdir -p dist/secan.app/Contents/Resources

# Copy all files from the PyInstaller directory to the .app bundle
cp -R dist/secan/* dist/secan.app/Contents/MacOS/
# Remove the original PyInstaller directory to avoid duplication in DMG
rm -rf dist/secan
    
# Create Info.plist
cat > dist/secan.app/Contents/Info.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>secan</string>
    <key>CFBundleIdentifier</key>
    <string>$BUNDLE_ID</string>
    <key>CFBundleName</key>
    <string>$APP_NAME</string>
    <key>CFBundleDisplayName</key>
    <string>$APP_NAME</string>
    <key>CFBundleVersion</key>
    <string>$APP_VERSION</string>
    <key>CFBundleShortVersionString</key>
    <string>$APP_VERSION</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSSupportsAutomaticGraphicsSwitching</key>
    <true/>
</dict>
</plist>
EOF

# Make sure the executable is actually executable
chmod +x dist/secan.app/Contents/MacOS/secan

# Self-sign the app with ad-hoc signature
codesign --force --deep --sign - dist/secan.app
codesign --verify --deep --strict --verbose=2 dist/secan.app

# Remove quarantine attribute that might be added during build
xattr -rd com.apple.quarantine dist/secan.app 2>/dev/null || true

# Display signing information
codesign -dv dist/secan.app 2>&1 | head -10

# Create DMG background image directory (optional)
mkdir -p dmg-resources

# Create a simple background image if it doesn't exist
if [ ! -f "dmg-resources/background.png" ]; then
    # Create a simple background using ImageMagick if available
    if command -v convert &> /dev/null; then
        convert -size 800x450 xc:'#f0f0f0' \
                -pointsize 24 -fill '#333333' \
                -gravity center -annotate +0-50 "Drag $APP_NAME to Applications" \
                dmg-resources/background.png
    fi
fi

# Create DMG
create-dmg \
    --volname "$APP_NAME Installer" \
    --window-pos 200 120 \
    --window-size 800 450 \
    --icon-size 100 \
    --icon "secan.app" 200 190 \
    --hide-extension "secan.app" \
    --app-drop-link 600 185 \
    --background "dmg-resources/background.png" \
    --hdiutil-quiet \
    "secan-installer.dmg" \
    "dist/" || {
    # Fallback without background if it fails
    echo "Retrying DMG creation without background..."
    create-dmg \
        --volname "$APP_NAME Installer" \
        --window-pos 200 120 \
        --window-size 800 450 \
        --icon-size 100 \
        --icon "secan.app" 200 190 \
        --hide-extension "secan.app" \
        --app-drop-link 600 185 \
        --hdiutil-quiet \
        "secan-installer.dmg" \
        "dist/"
}

# Verify the DMG
if [ -f "secan-installer.dmg" ]; then
    echo "DMG size: $(du -h secan-installer.dmg | cut -f1)"
    
    # Test mounting the DMG
    echo "Testing DMG..."
    hdiutil attach secan-installer.dmg -readonly -mountpoint /tmp/secan-test 2>/dev/null && {
        echo "DMG mounts successfully"
        hdiutil detach /tmp/secan-test 2>/dev/null
    } || echo "Warning: Could not test DMG mounting"
    
    echo "DMG creation completed successfully!"
else
    echo "Error: DMG file was not created"
    exit 1
fi
