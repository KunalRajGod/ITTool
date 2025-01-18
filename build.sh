#!/bin/bash

# Exit on error
set -e

echo "Cleaning previous builds..."
rm -rf build dist *.spec

echo "Creating icon..."
# Make sure icon script is executable
chmod +x make_icns.sh
./make_icns.sh

echo "Building application..."
pyinstaller PCRepairTool.spec

echo "Creating DMG..."
# Create directory for DMG
mkdir -p dist/dmg
cp -r "dist/PC Repair Tool.app" "dist/dmg/PC Repair Tool.app"

# Create Applications symlink
cd dist/dmg
ln -s /Applications Applications
cd ../..

# Create background image directory
mkdir -p dist/dmg/.background
cp assets/dmg_background.png dist/dmg/.background/background.png

# Create DMG
create-dmg \
  --volname "PC Repair Tool" \
  --volicon "PCRepairTool.icns" \
  --background "assets/dmg_background.png" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "PC Repair Tool.app" 200 190 \
  --icon "Applications" 600 190 \
  --hide-extension "PC Repair Tool.app" \
  --app-drop-link 600 185 \
  "dist/PC Repair Tool.dmg" \
  "dist/dmg/"

echo "Build complete!"
echo "Your application is at: dist/PC Repair Tool.app"
echo "The installer is at: dist/PC Repair Tool.dmg"