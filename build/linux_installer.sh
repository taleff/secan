#!/bin/bash
# build/linux_installer.sh

set -e  # Exit on error

APP_NAME="Secan"
APP_VERSION="0.1.0"
DESCRIPTION="Secan Application"
CATEGORIES="Utility;"

echo "Creating Linux AppImage for $APP_NAME..."

# Install AppImage tools
echo "Downloading linuxdeploy..."
wget -q https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
chmod +x linuxdeploy-x86_64.AppImage

# Create AppDir structure
echo "Creating AppDir structure..."
mkdir -p secan.AppDir/usr/bin
mkdir -p secan.AppDir/usr/share/applications
mkdir -p secan.AppDir/usr/share/icons/hicolor/256x256/apps
mkdir -p secan.AppDir/usr/share/metainfo

# Copy application files
echo "Copying application files..."
cp -r dist/secan/* secan.AppDir/usr/bin/

# Create desktop entry
cat > secan.AppDir/usr/share/applications/secan.desktop << EOF
[Desktop Entry]
Name=$APP_NAME
Comment=$DESCRIPTION
Exec=secan
Icon=secan
Type=Application
Categories=$CATEGORIES
Terminal=false
StartupNotify=true
EOF

# Create AppStream metainfo (for software centers)
cat > secan.AppDir/usr/share/metainfo/secan.appdata.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop">
    <id>secan</id>
    <name>$APP_NAME</name>
    <summary>$DESCRIPTION</summary>
    <description>
        <p>
            $APP_NAME is a powerful application that provides 
            essential functionality for users.
        </p>
    </description>
    <url type="homepage">https://github.com/your-username/secan</url>
    <metadata_license>CC0-1.0</metadata_license>
    <project_license>MIT</project_license>
    <releases>
        <release version="$APP_VERSION" date="$(date +%Y-%m-%d)"/>
    </releases>
</component>
EOF

# Create AppRun script
cat > secan.AppDir/AppRun << 'EOF'
#!/bin/bash

# Get the directory containing this script
HERE="$(dirname "$(readlink -f "${0}")")"

# Set up environment
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"

# Change to the application directory
cd "${HERE}/usr/bin"

# Execute the application with all arguments
exec "./secan" "$@"
EOF

chmod +x secan.AppDir/AppRun

# Create app icon (replace with your actual icon)
if command -v convert &> /dev/null; then
    echo "Creating application icon..."
    convert -size 256x256 xc:'#4CAF50' \
            -fill white -pointsize 72 -gravity center \
            -annotate +0+0 "S" \
            secan.AppDir/usr/share/icons/hicolor/256x256/apps/secan.png
elif command -v magick &> /dev/null; then
    echo "Creating application icon with magick..."
    magick -size 256x256 xc:'#4CAF50' \
           -fill white -pointsize 72 -gravity center \
           -annotate +0+0 "S" \
           secan.AppDir/usr/share/icons/hicolor/256x256/apps/secan.png
else
    echo "Warning: ImageMagick not available, using placeholder icon"
    # Create a simple SVG icon as fallback
    cat > secan.AppDir/usr/share/icons/hicolor/256x256/apps/secan.svg << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">
    <rect width="256" height="256" fill="#4CAF50"/>
    <text x="128" y="140" font-family="sans-serif" font-size="72" 
          fill="white" text-anchor="middle">S</text>
</svg>
EOF
    # Convert SVG to PNG if possible
    if command -v rsvg-convert &> /dev/null; then
        rsvg-convert -w 256 -h 256 \
            secan.AppDir/usr/share/icons/hicolor/256x256/apps/secan.svg \
            -o secan.AppDir/usr/share/icons/hicolor/256x256/apps/secan.png
    fi
fi

# Copy icon to AppDir root for linuxdeploy
cp secan.AppDir/usr/share/icons/hicolor/256x256/apps/secan.png secan.AppDir/ 2>/dev/null || \
cp secan.AppDir/usr/share/icons/hicolor/256x256/apps/secan.svg secan.AppDir/secan.png 2>/dev/null || \
echo "Warning: Could not copy icon to AppDir root"

# Build AppImage
echo "Building AppImage..."
./linuxdeploy-x86_64.AppImage --appdir secan.AppDir --output appimage

# Find the generated AppImage
APPIMAGE_FILE=$(find . -name "*.AppImage" -not -name "linuxdeploy-*" | head -1)

if [ -n "$APPIMAGE_FILE" ]; then
    echo "AppImage created successfully: $APPIMAGE_FILE"
    echo "AppImage size: $(du -h "$APPIMAGE_FILE" | cut -f1)"
    
    # Make it executable
    chmod +x "$APPIMAGE_FILE"
    
    # Test the AppImage
    echo "Testing AppImage..."
    if "$APPIMAGE_FILE" --help &>/dev/null || "$APPIMAGE_FILE" --version &>/dev/null; then
        echo "AppImage test successful!"
    else
        echo "Warning: AppImage test failed, but file was created"
    fi
else
    echo "Error: No AppImage file was created"
    exit 1
fi
