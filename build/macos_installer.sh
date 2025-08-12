#!/bin/bash
# build/macos_installer.sh

set -e  # Exit on error

APP_NAME="Secan"
APP_VERSION="0.1.0"
BUNDLE_ID="com.secan.secan"

echo "Creating macOS installer for $APP_NAME..."

# Install create-dmg
echo "Installing create-dmg..."
brew install create-dmg

# Create app bundle structure if not exists
if [ ! -d "dist/secan.app" ]; then
    echo "Creating .app bundle structure..."
    mkdir -p dist/secan.app/Contents/MacOS
    mkdir -p dist/secan.app/Contents/Resources
    
    # Move executable and resources
    mv dist/secan/* dist/secan.app/Contents/MacOS/
    
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
    
    echo "App bundle structure created"
fi

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
echo "Creating DMG..."
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

echo "macOS installer created successfully: secan-installer.dmg"

# Verify the DMG
if [ -f "secan-installer.dmg" ]; then
    echo "DMG size: $(du -h secan-installer.dmg | cut -f1)"
    echo "DMG creation completed successfully!"
else
    echo "Error: DMG file was not created"
    exit 1
fi
