#!/bin/bash
# Installer for SleepWatch.app (standalone version)

set -e

echo "🌙 SleepWatch App Installer"
echo "=============================="
echo ""

APP_NAME="SleepWatch.app"
APP_SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/dist/$APP_NAME"
APP_DEST="/Applications/$APP_NAME"

# Check if built app exists
if [ ! -d "$APP_SOURCE" ]; then
    echo "❌ $APP_NAME not found in dist/"
    echo "   Run ./build.sh first to create the app"
    exit 1
fi

# Check for blueutil
if ! command -v blueutil &> /dev/null; then
    echo "⚠️  blueutil not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install blueutil
        echo "✅ blueutil installed"
    else
        echo "⚠️  Homebrew not found."
        echo "   You'll need to install blueutil manually:"
        echo "   brew install blueutil"
        echo ""
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
else
    echo "✅ blueutil found"
fi

# Copy app to Applications
echo ""
echo "📦 Installing $APP_NAME..."
if [ -d "$APP_DEST" ]; then
    echo "⚠️  $APP_NAME already exists in /Applications"
    read -p "Replace it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$APP_DEST"
    else
        echo "Installation cancelled"
        exit 0
    fi
fi

cp -R "$APP_SOURCE" "$APP_DEST"
echo "✅ Copied to /Applications"

# Add to login items
echo ""
echo "🚀 Adding to login items..."
osascript -e "tell application \"System Events\" to delete every login item whose name is \"$APP_NAME\"" 2>/dev/null || true
osascript -e "tell application \"System Events\" to make login item at end with properties {path:\"$APP_DEST\", hidden:false}"
echo "✅ Added to login items"

# Launch the app
echo ""
echo "🎉 Launching SleepWatch..."
open "$APP_DEST"
sleep 2

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Installation complete!"
echo ""
echo "SleepWatch should now be running in your menu bar (black lightning bolt icon)"
echo "It will automatically start on login."
echo ""
echo "To uninstall:"
echo "  1. Go to System Settings → General → Login Items"
echo "  2. Remove SleepWatch from the list"
echo "  3. Delete /Applications/$APP_NAME"
echo ""
echo "Config file: ~/.sleepwatch.json"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
