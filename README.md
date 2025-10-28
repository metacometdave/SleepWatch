# SleepWatch ⚡

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: macOS](https://img.shields.io/badge/platform-macOS-blue.svg)](https://www.apple.com/macos)
[![GitHub release](https://img.shields.io/github/v/release/metacometdave/SleepWatch)](https://github.com/metacometdave/SleepWatch/releases)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A lightweight macOS menu bar app that automatically turns off WiFi and Bluetooth when your Mac goes to sleep, then reconnects to your favorite devices when it wakes up.

**Minimize battery drain when your MacBook lid is closed.**

## Features

- 🔋 **Auto-disable radios on sleep** - WiFi and Bluetooth turn off when lid closes
- 🔌 **Smart reconnection** - Auto-reconnect to favorite devices or most recent connections on wake
- ⭐ **Favorite devices** - Mark your preferred Bluetooth devices for auto-reconnection
- 📡 **WiFi management** - Automatically reconnect to your last WiFi network
- 🚀 **Launch at login** - One-click toggle in the menu to start automatically at login
- 🔄 **Auto-updates** - Automatic update checking with one-click downloads
- 🪶 **Lightweight** - Pure Python, minimal resource usage (~20MB RAM)
- 🎯 **Menu bar interface** - Simple, clean UI with status indicators

## Why SleepWatch?

By default, macOS keeps WiFi and Bluetooth partially active even when sleeping, causing significant battery drain. This app ensures true deep sleep by completely disabling radios when your lid closes.

**Typical battery savings:** 1-2% overnight vs 10-20% without it.

## Menu Preview

```
⚡️ SleepWatch
├─ Status: WiFi: On | BT: On | MyNetwork
├─ ────────────────────────
├─ WiFi Control
│  ├─ ✓ Disable WiFi on Sleep
│  └─ ✓ Auto-reconnect WiFi
├─ Bluetooth Control
│  ├─ ✓ Disable Bluetooth on Sleep
│  └─ ✓ Auto-reconnect Bluetooth
├─ Favorite Devices
│  ├─ ★ AirPods Pro
│  ├─ ☆ Magic Mouse
│  └─ ★ Keyboard
├─ Reconnect Mode
│  ├─ ✓ Favorites Only
│  └─   Most Recent
├─ ✓ Launch at Login
├─ Hide Menu Bar Icon
├─ ──────────────────────
├─ Version 1.0.0
├─ Check for Updates...
├─ Refresh
└─ Quit SleepWatch
```

## Installation

### Download & Install (Recommended)

1. **Download** the latest release: [SleepWatch.zip](https://github.com/metacometdave/SleepWatch/releases)
2. **Unzip** the downloaded file
3. **Move** `SleepWatch.app` to your `/Applications` folder
4. **Launch** SleepWatch from Applications
5. **Grant permissions** when macOS prompts for Accessibility access

That's it! The app will appear in your menu bar as a black lightning bolt icon

### Prerequisites

Before installing, you need `blueutil` for Bluetooth control:

```bash
# Install via Homebrew
brew install blueutil
```

### Auto-start on Login

**Method 1: Built-in Toggle (Easiest)**

Once the app is in `/Applications`:
1. Launch **SleepWatch**
2. Click the **lightning bolt icon** in menu bar
3. Click **"Launch at Login"** to enable
4. Done! ✓ The checkmark shows it's enabled

To disable, just click it again.

**Method 2: Automated Installer**
```bash
# Download the repo, then run:
./install-app.sh
```
This will:
- Copy the app to `/Applications`
- Add to login items automatically
- Install dependencies (blueutil)
- Launch the app

**Method 3: Manual via System Settings**
1. Move `SleepWatch.app` to `/Applications`
2. Go to **System Settings → General → Login Items**
3. Click the **+** button under "Open at Login"
4. Select **SleepWatch** from Applications folder

### Install from Source

If you prefer to run from source:

```bash
# Clone the repository
git clone https://github.com/metacometdave/SleepWatch.git
cd SleepWatch

# Install dependencies
brew install blueutil

# Create virtual environment and install Python packages
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the app
python sleepwatch.py
```

## Usage

### Basic Setup

1. **Launch the app** - Click the lightning bolt icon in your menu bar
2. **Enable controls** - Check "Disable WiFi on Sleep" and "Disable Bluetooth on Sleep"
3. **Pick favorites** - Click on device names to toggle ★ (favorite) status
4. **Choose mode:**
   - **Favorites Only** - Reconnect only to starred devices
   - **Most Recent** - Reconnect to whatever was connected before sleep

### Menu Options

| Option | Description |
|--------|-------------|
| **Disable WiFi on Sleep** | Turn off WiFi when lid closes |
| **Auto-reconnect WiFi** | Reconnect to last network on wake |
| **Disable Bluetooth on Sleep** | Turn off Bluetooth when lid closes |
| **Auto-reconnect Bluetooth** | Reconnect to devices on wake |
| **★ Device Name** | Starred = favorite (will auto-reconnect) |
| **☆ Device Name** | Not a favorite (click to star) |

## Configuration

Settings are stored in `~/.sleepwatch.json`:

```json
{
  "wifi_enabled": true,
  "bluetooth_enabled": true,
  "auto_reconnect_wifi": true,
  "auto_reconnect_bluetooth": true,
  "favorite_devices": ["00:1A:7D:DA:71:13", "00:1B:3F:22:44:55"],
  "last_wifi_network": "MyNetwork",
  "reconnect_mode": "favorites"
}
```

You can edit this file directly if needed.

## How It Works

1. **Sleep Detection** - Uses macOS `NSWorkspaceWillSleepNotification` to detect when lid closes
2. **Radio Control** - Calls `blueutil` and `networksetup` to toggle WiFi/Bluetooth
3. **Wake Handling** - Uses `NSWorkspaceDidWakeNotification` to detect wake events
4. **Smart Reconnection** - Restores WiFi and reconnects to favorite Bluetooth devices

## Comparison to Alternatives

| Feature | SleepWatch | Bluesnooze | SleepWatcher Scripts |
|---------|--------------|------------|----------------------|
| **WiFi Control** | ✅ | ❌ | ✅ (manual) |
| **Bluetooth Control** | ✅ | ✅ | ✅ (manual) |
| **Favorite Devices** | ✅ | ❌ | ❌ |
| **Smart Reconnection** | ✅ | ✅ | ⚠️ Basic |
| **Menu Bar UI** | ✅ | ✅ | ❌ |
| **In-App Settings** | ✅ | ❌ | ❌ |
| **Hide Icon** | ✅ | ✅ | ❌ |
| **Launch at Login Toggle** | ✅ | ❌ (manual) | ❌ |
| **Open Source** | ✅ | ✅ | ✅ |
| **Language** | Python | Swift | Shell |
| **Homebrew Install** | ⚠️ Coming | ✅ | N/A |

## Troubleshooting

### App doesn't start
```bash
# Check if blueutil is installed
which blueutil

# If not, install it
brew install blueutil

# Try running with verbose output
python3 sleepwatch.py
```

### Devices don't reconnect
- Make sure "Auto-reconnect Bluetooth" is checked
- Verify devices are starred (★) if using "Favorites Only" mode
- Check that devices are actually paired in System Settings

### WiFi doesn't turn off
- Check that "Disable WiFi on Sleep" is enabled
- Your WiFi interface might not be `en0` (rare) - check with:
  ```bash
  networksetup -listallhardwareports
  ```

### Permissions Issue
SleepWatch needs accessibility permissions on newer macOS versions:
1. Go to **System Settings → Privacy & Security → Accessibility**
2. Add **Terminal** or **Python** to the allowed apps

## Development

### Project Structure

```
sleepwatch/
├── sleepwatch.py          # Main menu bar app
├── bluetooth_manager.py     # Bluetooth device control
├── wifi_manager.py          # WiFi network control
├── sleep_watcher.py         # Sleep/wake event detection
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── install.sh               # Auto-start installer
└── README.md
```

### Running from Source

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python sleepwatch.py
```

### Building Standalone App (Optional)

```bash
# Install py2app
pip3 install py2app

# Create standalone .app bundle
python3 setup.py py2app
```

## Contributing

Contributions are welcome! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Merge Request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Credits

Built with:
- [rumps](https://github.com/jaredks/rumps) - Ridiculously Uncomplicated macOS Python Statusbar apps
- [blueutil](https://github.com/toy/blueutil) - CLI for Bluetooth on macOS
- macOS `networksetup` - Built-in WiFi management

Inspired by [Bluesnooze](https://github.com/odlp/bluesnooze) but extended to handle WiFi and favorite device management.

## FAQs

### Can I hide the menu bar icon?

Yes! Two ways:

**Option 1: Use the menu (easiest)**
1. Click the lightning bolt icon
2. Click **"Hide Menu Bar Icon"**
3. Confirm

**Option 2: Terminal command**
```bash
defaults write com.sleepwatch.app hideIcon -bool true && killall SleepWatch
```

The app continues running in the background even when hidden.

### How can I restore the menu bar icon?

Run this command in Terminal:

```bash
defaults delete com.sleepwatch.app hideIcon && killall SleepWatch
```

When you next relaunch the application, it should appear in the menu bar.

### Why can't this be distributed via the App Store?

SleepWatch uses system-level APIs to control WiFi and Bluetooth which requires special permissions that App Store apps cannot request. However, the app is open source and the release builds can be notarized by Apple for security.

### Can I customize which devices auto-reconnect?

Yes! Use the menu to star (★) your favorite devices. Set the reconnect mode to "Favorites Only" and only starred devices will reconnect on wake.

### Does this work with third-party Bluetooth devices?

Yes! Any Bluetooth device that pairs with your Mac can be managed by SleepWatch.

### How do updates work?

SleepWatch automatically checks for updates on startup (you'll get a notification if a new version is available). You can also manually check via the menu: **Check for Updates...**

Updates are downloaded from GitHub Releases. The app will open your browser to the download page.

## Contributing

Contributions are welcome! Whether it's:
- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 💡 Ideas and suggestions

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get started.

## Support

- 🐛 **Bug reports:** [GitHub Issues](https://github.com/metacometdave/SleepWatch/issues)
- 💬 **Questions:** [Discussions](https://github.com/metacometdave/SleepWatch/discussions)
- ⭐ **Star the repo** if you find it useful!

---

Made with 🌙 to save your battery life
