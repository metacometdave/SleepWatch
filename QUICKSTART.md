# Quick Start Guide ⚡

## What You Have Now

**SleepWatch** is running in your menu bar! Look for the ⚡ icon.

## Testing It Right Now

### 1. Click the ⚡ Icon
You should see a dropdown menu with:
- WiFi and Bluetooth status
- Control toggles
- List of Bluetooth devices

### 2. Try These Features

**Mark a device as favorite:**
- Click on any Bluetooth device in the "Favorite Devices" section
- ☆ (not favorite) → ★ (favorite)
- Click again to toggle back

**Enable auto-control:**
- Check "Disable WiFi on Sleep" ✓
- Check "Disable Bluetooth on Sleep" ✓
- Check "Auto-reconnect WiFi" ✓
- Check "Auto-reconnect Bluetooth" ✓

**Test sleep/wake:**
1. Note which devices are currently connected
2. Close your MacBook lid for 10 seconds
3. Open it back up
4. Your favorite devices should reconnect automatically!

### 3. Check It's Working

After testing sleep/wake, run:
```bash
cat ~/.sleepwatcher.log
```

You should see entries like:
```
Tue Oct 28 12:30:15 2025: System going to sleep
WiFi disabled
Bluetooth disabled
Tue Oct 28 12:30:45 2025: System waking up
WiFi enabled
Bluetooth enabled
Reconnected 2/2 favorite devices
```

## Next Steps

### Make It Start Automatically

Run the installer to make SleepWatch start at login:
```bash
cd /Users/dhunt/code/Sleepwatch
./install.sh
```

This creates a Launch Agent so SleepWatch always runs.

### Clean Up Old Tools

Since SleepWatch replaces them, you can uninstall:

```bash
# Remove Bluesnooze
brew uninstall bluesnooze

# Stop SleepWatcher (if you were using it for this)
brew services stop sleepwatcher
brew uninstall sleepwatcher

# Remove old scripts
rm ~/.sleep ~/.wakeup ~/.sleepwatcher.log
```

### GitLab Repository

Your project is ready to push! Files included:
- ✅ Full source code
- ✅ README.md with documentation
- ✅ LICENSE (MIT)
- ✅ .gitignore
- ✅ requirements.txt
- ✅ install.sh

Initialize git and push:
```bash
cd /Users/dhunt/code/Sleepwatch
git init
git add .
git commit -m "Initial commit: SleepWatch - Lightweight macOS power management"
git remote add origin https://gitlab.com/yourusername/sleepwatch.git
git push -u origin main
```

## Configuration File

Settings are stored in: `~/.sleepwatch.json`

Example:
```json
{
  "wifi_enabled": true,
  "bluetooth_enabled": true,
  "auto_reconnect_wifi": true,
  "auto_reconnect_bluetooth": true,
  "favorite_devices": [
    "00:1A:7D:DA:71:13",
    "00:1B:3F:22:44:55"
  ],
  "last_wifi_network": "MyNetwork",
  "reconnect_mode": "favorites"
}
```

## Troubleshooting

**App not in menu bar?**
```bash
cd /Users/dhunt/code/Sleepwatch
source venv/bin/activate
python sleepwatch.py
```

**Devices not showing up?**
```bash
blueutil --paired --format json
```

**Check if it's running:**
```bash
ps aux | grep sleepwatch
```

**View logs:**
```bash
cat ~/Library/Logs/sleepwatch.log
```

## Customization Ideas

Want to customize? Edit `sleepwatch.py`:

**Change the icon:**
Line 19: Change `"⚡"` to any emoji

**Add notifications:**
Add `rumps.notification()` calls in the sleep/wake handlers

**Add menu items:**
Add new `rumps.MenuItem()` in the menu list

**Change reconnect delay:**
Edit the `time.sleep(2)` values in `_reconnect_wifi` and `_reconnect_bluetooth`

---

**Enjoy your battery savings!** 🔋
