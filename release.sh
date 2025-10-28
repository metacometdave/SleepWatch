#!/bin/bash
# Release script for SleepWatch
# Usage: ./release.sh <version>
# Example: ./release.sh 1.1.0

set -e

if [ -z "$1" ]; then
    echo "Usage: ./release.sh <version>"
    echo "Example: ./release.sh 1.1.0"
    exit 1
fi

VERSION="$1"
TAG="v$VERSION"

echo "🚀 Creating release for SleepWatch v$VERSION"
echo ""

# Check if version.py exists
if [ ! -f "version.py" ]; then
    echo "❌ version.py not found"
    exit 1
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  You have uncommitted changes:"
    git status --short
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update version in version.py
echo "📝 Updating version.py to $VERSION..."
sed -i '' "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" version.py

# Show the change
echo "Updated version:"
grep "__version__" version.py

echo ""
read -p "Does this look correct? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborting."
    git checkout version.py
    exit 1
fi

# Commit version bump
echo ""
echo "📦 Committing version bump..."
git add version.py
git commit -m "Bump version to $VERSION"

# Build the app
echo ""
echo "🔨 Building app..."
./build.sh

# Check if build succeeded
if [ ! -f "dist/SleepWatch.zip" ]; then
    echo "❌ Build failed - dist/SleepWatch.zip not found"
    exit 1
fi

echo ""
echo "✅ Build successful!"
echo "📦 Package: dist/SleepWatch.zip ($(du -h dist/SleepWatch.zip | cut -f1))"

# Create git tag
echo ""
read -p "Create git tag $TAG? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🏷️  Creating tag $TAG..."
    git tag -a "$TAG" -m "Release $TAG"
    echo "✅ Tag created"

    # Push
    echo ""
    read -p "Push commit and tag to GitHub? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push && git push origin "$TAG"
        echo "✅ Pushed to GitHub"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Release v$VERSION ready!"
echo ""
echo "Next steps:"
echo "1. Go to: https://github.com/metacometdave/SleepWatch/releases/new"
echo "2. Select tag: $TAG"
echo "3. Title: SleepWatch v$VERSION"
echo "4. Upload: dist/SleepWatch.zip"
echo "5. Write release notes and publish"
echo ""
echo "The app's auto-updater will detect the new version automatically!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
