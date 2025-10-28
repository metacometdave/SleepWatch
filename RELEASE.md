# Release Process

This document describes how to create a new release of SleepWatch.

## Version Numbering

SleepWatch uses [Semantic Versioning](https://semver.org/):
- **Major** (X.0.0): Breaking changes or major new features
- **Minor** (x.X.0): New features, backward compatible
- **Patch** (x.x.X): Bug fixes, backward compatible

## Creating a Release

### 1. Update Version Number

Edit `version.py` and update `__version__`:

```python
__version__ = "1.1.0"  # Update this
```

### 2. Update Changelog

Add release notes to the commit message or CHANGELOG.md (if you create one).

### 3. Commit Changes

```bash
git add version.py
git commit -m "Bump version to 1.1.0"
git push
```

### 4. Build the App

```bash
./build.sh
```

This creates:
- `dist/SleepWatch.app` - The application bundle
- `dist/SleepWatch.zip` - Distributable package

### 5. Create Git Tag

```bash
git tag -a v1.1.0 -m "Release v1.1.0: Add auto-updates and hide icon feature"
git push origin v1.1.0
```

### 6. Create GitHub Release

1. Go to: https://github.com/metacometdave/SleepWatch/releases/new
2. Select the tag you just created: `v1.1.0`
3. Title: `SleepWatch v1.1.0`
4. Description: Write release notes (what's new, bug fixes, etc.)
5. Upload `dist/SleepWatch.zip`
6. Check "Set as the latest release"
7. Click "Publish release"

### 7. Test Auto-Update

After publishing:
1. Install an older version on a test Mac
2. Launch it
3. Wait 3 seconds for auto-check or click "Check for Updates..."
4. Verify it detects the new version
5. Verify download link works

## Example Release Notes Template

```markdown
## What's New in v1.1.0

### New Features
- 🔄 Auto-update checking on startup
- 🙈 Hide menu bar icon option
- ✨ [Other new feature]

### Improvements
- Better error handling for Bluetooth reconnection
- Improved menu layout

### Bug Fixes
- Fixed issue with WiFi reconnection on wake
- [Other bug fix]

### Requirements
- macOS 10.13 or later
- blueutil (install via: `brew install blueutil`)

## Installation

Download `SleepWatch.zip`, unzip, and move to `/Applications`.

For auto-start, use the built-in "Launch at Login" toggle in the menu.
```

## Automation Ideas (Future)

Consider creating a GitHub Actions workflow to:
- Auto-build the .app on new tags
- Auto-create GitHub releases
- Run tests before release
