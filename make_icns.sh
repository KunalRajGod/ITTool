#!/bin/bash

# Create iconset directory
mkdir PCRepairTool.iconset

# Generate icon files at different sizes
sips -z 16 16     assets/icon.png --out PCRepairTool.iconset/icon_16x16.png
sips -z 32 32     assets/icon.png --out PCRepairTool.iconset/icon_16x16@2x.png
sips -z 32 32     assets/icon.png --out PCRepairTool.iconset/icon_32x32.png
sips -z 64 64     assets/icon.png --out PCRepairTool.iconset/icon_32x32@2x.png
sips -z 128 128   assets/icon.png --out PCRepairTool.iconset/icon_128x128.png
sips -z 256 256   assets/icon.png --out PCRepairTool.iconset/icon_128x128@2x.png
sips -z 256 256   assets/icon.png --out PCRepairTool.iconset/icon_256x256.png
sips -z 512 512   assets/icon.png --out PCRepairTool.iconset/icon_256x256@2x.png
sips -z 512 512   assets/icon.png --out PCRepairTool.iconset/icon_512x512.png
sips -z 1024 1024 assets/icon.png --out PCRepairTool.iconset/icon_512x512@2x.png

# Convert to icns file
iconutil -c icns PCRepairTool.iconset

# Clean up
rm -rf PCRepairTool.iconset