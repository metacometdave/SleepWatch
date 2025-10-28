#!/bin/bash
# Build script for SleepWatch.app

set -e

echo "🔨 Building SleepWatch.app..."

# Clean previous builds
rm -rf build dist

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install py2app jaraco.text
fi

# Build the app
echo "📦 Running py2app..."
python setup.py py2app

# Create distributable zip
echo "📦 Creating distribution package..."

cd dist
zip -r SleepWatch.zip SleepWatch.app -x "*.DS_Store"
cd ..

echo "✅ Build complete!"
echo "📁 App bundle: dist/SleepWatch.app"
echo "📦 Distribution: dist/SleepWatch.zip ($(du -h dist/SleepWatch.zip | cut -f1))"
echo ""
echo "To test the app, run:"
echo "  open dist/SleepWatch.app"
