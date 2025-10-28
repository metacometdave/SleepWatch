#!/bin/bash
# Installation script for SleepWatch

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_PATH="$HOME/Library/LaunchAgents/com.sleepwatch.app.plist"

echo "🌙 SleepWatch Installer"
echo "========================="
echo ""

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found."
    echo "   Install it from python.org or via Homebrew: brew install python3"
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

# Check for blueutil
if ! command -v blueutil &> /dev/null; then
    echo "⚠️  blueutil not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install blueutil
        echo "✅ blueutil installed"
    else
        echo "❌ Homebrew not found. Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
else
    echo "✅ blueutil found"
fi

# Create virtual environment
echo ""
echo "📦 Setting up Python virtual environment..."
python3 -m venv "$SCRIPT_DIR/venv"
echo "✅ Virtual environment created"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
"$SCRIPT_DIR/venv/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"
echo "✅ Dependencies installed"

# Create LaunchAgent plist
echo ""
echo "🚀 Setting up auto-start at login..."

cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sleepwatch.app</string>
    <key>ProgramArguments</key>
    <array>
        <string>$SCRIPT_DIR/venv/bin/python</string>
        <string>$SCRIPT_DIR/sleepwatch.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardOutPath</key>
    <string>$HOME/Library/Logs/sleepwatch.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/Library/Logs/sleepwatch.error.log</string>
</dict>
</plist>
EOF

# Load the LaunchAgent
launchctl unload "$PLIST_PATH" 2>/dev/null || true
launchctl load "$PLIST_PATH"

echo "✅ Auto-start configured"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Installation complete!"
echo ""
echo "SleepWatch should now be running in your menu bar (⚡ icon)"
echo ""
echo "To manually start: $SCRIPT_DIR/venv/bin/python $SCRIPT_DIR/sleepwatch.py"
echo "To uninstall: launchctl unload $PLIST_PATH && rm $PLIST_PATH"
echo ""
echo "Logs: ~/Library/Logs/sleepwatch.log"
echo "Config: ~/.sleepwatch.json"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
