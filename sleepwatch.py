#!/usr/bin/env python3
"""
SleepWatch - Lightweight macOS menu bar app to manage WiFi and Bluetooth on sleep/wake.
"""
import rumps
import threading
import os
import sys
import subprocess
from datetime import datetime
from config import Config
from bluetooth_manager import BluetoothManager
from wifi_manager import WiFiManager
from sleep_watcher import SleepWatcher
from version import __version__, GITHUB_RELEASES_URL
from update_checker import check_for_updates


class SleepWatchApp(rumps.App):
    """Main menu bar application."""
    
    @staticmethod
    def log_to_system(msg):
        """Log a message to the system log."""
        try:
            # Print to stdout for development debugging
            print(f"[SleepWatch] {msg}")
            # Log to system log
            result = os.system(f'logger -t SleepWatch "{msg}"')
            if result != 0:
                print(f"[SleepWatch] Warning: logger command failed with code {result}")
        except Exception as e:
            print(f"[SleepWatch] Error logging message: {e}")

    def install_blueutil(self):
        """Install blueutil using Homebrew."""
        # Check if Homebrew is installed first
        if not BluetoothManager.is_brew_installed():
            response = rumps.alert(
                "Homebrew Required",
                "blueutil requires Homebrew to install.\n\n"
                "Terminal will open to install Homebrew first, then blueutil.\n\n"
                "This may take a few minutes.",
                ok="Install",
                cancel="Cancel"
            )
            if response != 1:
                return

            # Open Terminal to install Homebrew first, then blueutil
            script = '''
tell application "Terminal"
    activate
    do script "echo 'Installing Homebrew...' && /bin/bash -c \\"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\\" && echo '\\nInstalling blueutil...' && brew install blueutil && echo '\\nInstallation complete! You can close this window.' && exit"
end tell
'''
        else:
            # Just install blueutil
            response = rumps.alert(
                "Install blueutil",
                "Terminal will open to install blueutil.\n\n"
                "The window will close automatically when done.",
                ok="Install",
                cancel="Cancel"
            )
            if response != 1:
                return

            script = '''
tell application "Terminal"
    activate
    do script "echo 'Installing blueutil...' && brew install blueutil && echo '\\nInstallation complete! You can close this window.' && exit"
end tell
'''

        try:
            subprocess.run(['osascript', '-e', script], check=True)
            rumps.notification(
                "Installing blueutil",
                "Terminal is open",
                "Please wait for installation to complete, then restart SleepWatch."
            )
        except Exception as e:
            rumps.alert("Error", f"Failed to open Terminal:\n{e}")

    def __init__(self):
        # Get path to icon file
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')

        # Check if blueutil is installed - if not, prompt to install
        if not BluetoothManager.is_blueutil_installed():
            # Show dialog asking user to install
            response = rumps.alert(
                "blueutil Required",
                "SleepWatch needs blueutil for Bluetooth features.\n\n"
                "Terminal will open to install it via Homebrew.\n"
                "This may take a few minutes.\n\n"
                "The app will start after installation completes.",
                ok="Install Now",
                cancel="Skip (Limited Features)"
            )

            if response == 1:  # Install clicked
                # Get app path for restart (check if running from app bundle)
                if getattr(sys, 'frozen', False):
                    # Running from py2app bundle
                    app_path = os.path.abspath(os.path.join(os.path.dirname(sys.executable), '..', '..'))
                elif os.path.exists('/Applications/SleepWatch.app'):
                    app_path = '/Applications/SleepWatch.app'
                else:
                    app_path = '/Applications/SleepWatch.app'  # Default fallback

                # Open Terminal with install command that restarts the app
                if not BluetoothManager.is_brew_installed():
                    script = f'''
tell application "Terminal"
    activate
    set currentTab to do script "echo 'Installing Homebrew...' && /bin/bash -c \\"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\\" && echo '\\nInstalling blueutil...' && brew install blueutil && echo '\\nInstallation complete! Restarting SleepWatch...' && sleep 1 && open '{app_path}' && exit"
end tell
'''
                else:
                    script = f'''
tell application "Terminal"
    activate
    set currentTab to do script "echo 'Installing blueutil...' && brew install blueutil && echo '\\nInstallation complete! Restarting SleepWatch...' && sleep 1 && open '{app_path}' && exit"
end tell
'''
                try:
                    subprocess.run(['osascript', '-e', script], check=True)
                    # Quit this instance since we're restarting
                    import time
                    time.sleep(2)  # Give Terminal time to start
                    rumps.quit_application()
                except Exception as e:
                    print(f"Error opening Terminal: {e}")

        # Use actual icon file for solid black rendering
        super(SleepWatchApp, self).__init__(
            "SleepWatch",
            icon=icon_path if os.path.exists(icon_path) else None,
            template=True,
            quit_button=None
        )

        self.config = Config()
        self.bt_manager = BluetoothManager()
        self.wifi_manager = WiFiManager()
        self.sleep_watcher = None

        # Track state before sleep
        self.devices_before_sleep = []
        self.wifi_before_sleep = None

        # Build menu
        self.menu = [
            rumps.MenuItem("Status", callback=None),
            None,  # Separator
            rumps.MenuItem("WiFi Control", callback=None),
            rumps.MenuItem("  Disable WiFi on Sleep", callback=self.toggle_wifi_control),
            rumps.MenuItem("  Auto-reconnect WiFi", callback=self.toggle_wifi_reconnect),
            None,
            rumps.MenuItem("Bluetooth Control", callback=None),
            rumps.MenuItem("  Disable Bluetooth on Sleep", callback=self.toggle_bt_control),
            rumps.MenuItem("  Auto-reconnect Bluetooth", callback=self.toggle_bt_reconnect),
            None,
            rumps.MenuItem("Favorite Devices", callback=None),
            # Device list will be populated by update_device_list()
            None,
            rumps.MenuItem("Bluetooth Reconnect Mode", callback=None),
            rumps.MenuItem("  Favorites Only", callback=self.set_mode_favorites),
            rumps.MenuItem("  Most Recent", callback=self.set_mode_recent),
            None,
            rumps.MenuItem("Launch at Login", callback=self.toggle_launch_at_login),
            rumps.MenuItem("Hide Menu Bar Icon", callback=self.hide_icon),
            None,
            rumps.MenuItem(f"Version {__version__}", callback=None),
            rumps.MenuItem("Check for Updates...", callback=self.check_updates),
            rumps.MenuItem("Refresh", callback=self.refresh_menu),
            rumps.MenuItem("Quit SleepWatch", callback=self.quit_app)
        ]

        self.update_menu_state()
        self.update_device_list()  # Populate device list on startup
        self.start_sleep_watcher()

        # Check for updates on startup (in background)
        if self.config.get('check_updates_on_startup', True):
            threading.Thread(target=self._check_updates_background, daemon=True).start()

    def start_sleep_watcher(self):
        """Start watching for sleep/wake events."""
        self.sleep_watcher = SleepWatcher(
            on_sleep=self.on_system_sleep,
            on_wake=self.on_system_wake
        )
        self.sleep_watcher.start()

    def on_system_sleep(self):
        """Called when system is about to sleep."""
        print(f"{datetime.now()}: System going to sleep")

        # Save current state
        if self.config.get('bluetooth_enabled'):
            self.devices_before_sleep = self.bt_manager.get_connected_devices()

        if self.config.get('wifi_enabled'):
            self.wifi_before_sleep = self.wifi_manager.get_current_network()
            if self.wifi_before_sleep:
                self.config.set('last_wifi_network', self.wifi_before_sleep)

        # Turn off radios
        if self.config.get('wifi_enabled'):
            self.wifi_manager.set_power(False)
            print("WiFi disabled")

        if self.config.get('bluetooth_enabled'):
            self.bt_manager.set_power(False)
            print("Bluetooth disabled")

    def on_system_wake(self):
        """Called when system wakes from sleep."""
        print(f"{datetime.now()}: System waking up")

        # Turn on WiFi
        if self.config.get('wifi_enabled'):
            self.wifi_manager.set_power(True)
            print("WiFi enabled")

            if self.config.get('auto_reconnect_wifi') and self.wifi_before_sleep:
                threading.Thread(
                    target=self._reconnect_wifi,
                    args=(self.wifi_before_sleep,),
                    daemon=True
                ).start()

        # Turn on Bluetooth and reconnect devices
        if self.config.get('bluetooth_enabled'):
            self.bt_manager.set_power(True)
            print("Bluetooth enabled")

            if self.config.get('auto_reconnect_bluetooth'):
                threading.Thread(
                    target=self._reconnect_bluetooth,
                    daemon=True
                ).start()

    def _reconnect_wifi(self, ssid):
        """Reconnect to WiFi network (runs in thread)."""
        import time
        time.sleep(2)  # Give WiFi time to initialize

        if self.wifi_manager.connect_to_network(ssid):
            print(f"Reconnected to WiFi: {ssid}")
        else:
            print(f"Failed to reconnect to WiFi: {ssid}")

    def _reconnect_bluetooth(self):
        """Reconnect to Bluetooth devices (runs in thread)."""
        import time
        time.sleep(2)  # Give Bluetooth time to initialize

        mode = self.config.get('reconnect_mode', 'favorites')

        if mode == 'favorites':
            favorites = self.config.get('favorite_devices', [])
            if favorites:
                count = self.bt_manager.reconnect_favorites(favorites)
                print(f"Reconnected {count}/{len(favorites)} favorite devices")
        elif mode == 'last':
            # Reconnect to devices that were connected before sleep
            for device in self.devices_before_sleep:
                address = device.get('address', '')
                if address:
                    self.bt_manager.connect_device(address)
                    print(f"Reconnected to: {device.get('name', address)}")

    @rumps.clicked("  Disable WiFi on Sleep")
    def toggle_wifi_control(self, sender):
        """Toggle WiFi control on/off."""
        self.config.toggle('wifi_enabled')
        self.update_menu_state()

    @rumps.clicked("  Auto-reconnect WiFi")
    def toggle_wifi_reconnect(self, sender):
        """Toggle WiFi auto-reconnect."""
        self.config.toggle('auto_reconnect_wifi')
        self.update_menu_state()

    @rumps.clicked("  Disable Bluetooth on Sleep")
    def toggle_bt_control(self, sender):
        """Toggle Bluetooth control on/off."""
        self.config.toggle('bluetooth_enabled')
        self.update_menu_state()

    @rumps.clicked("  Auto-reconnect Bluetooth")
    def toggle_bt_reconnect(self, sender):
        """Toggle Bluetooth auto-reconnect."""
        self.config.toggle('auto_reconnect_bluetooth')
        self.update_menu_state()

    @rumps.clicked("  Favorites Only")
    def set_mode_favorites(self, sender):
        """Set reconnect mode to favorites only."""
        self.config.set('reconnect_mode', 'favorites')
        self.update_menu_state()

    @rumps.clicked("  Most Recent")
    def set_mode_recent(self, sender):
        """Set reconnect mode to most recent."""
        self.config.set('reconnect_mode', 'last')
        self.update_menu_state()

    @rumps.clicked("Refresh")
    def refresh_menu(self, sender):
        """Refresh the menu and device list."""
        self.update_menu_state()
        self.update_device_list()

    def update_menu_state(self):
        """Update menu item states (checkmarks)."""
        # Check if blueutil is installed
        if not self.bt_manager.is_blueutil_installed():
            # Rebuild menu without Bluetooth features, showing install option
            self.menu.clear()
            self.menu.update([
                rumps.MenuItem("Status", callback=None),
                None,
                rumps.MenuItem("⚠️ Bluetooth Support Missing", callback=None),
                rumps.MenuItem("Install blueutil", callback=self.install_blueutil),
                None,
                rumps.MenuItem("WiFi Control", callback=None),
                rumps.MenuItem("  Disable WiFi on Sleep", callback=self.toggle_wifi_control),
                rumps.MenuItem("  Auto-reconnect WiFi", callback=self.toggle_wifi_reconnect),
                None,
                rumps.MenuItem("Launch at Login", callback=self.toggle_launch_at_login),
                rumps.MenuItem("Hide Menu Bar Icon", callback=self.hide_icon),
                None,
                rumps.MenuItem(f"Version {__version__}", callback=None),
                rumps.MenuItem("Check for Updates...", callback=self.check_updates),
                rumps.MenuItem("Refresh", callback=self.refresh_menu),
                rumps.MenuItem("Quit SleepWatch", callback=self.quit_app)
            ])
            # Update WiFi control states
            self.menu["  Disable WiFi on Sleep"].state = self.config.get('wifi_enabled', True)
            self.menu["  Auto-reconnect WiFi"].state = self.config.get('auto_reconnect_wifi', True)
            return
        
        # WiFi controls
        self.menu["  Disable WiFi on Sleep"].state = self.config.get('wifi_enabled', True)
        self.menu["  Auto-reconnect WiFi"].state = self.config.get('auto_reconnect_wifi', True)

        # Bluetooth controls
        self.menu["  Disable Bluetooth on Sleep"].state = self.config.get('bluetooth_enabled', True)
        self.menu["  Auto-reconnect Bluetooth"].state = self.config.get('auto_reconnect_bluetooth', True)

        # Reconnect mode
        mode = self.config.get('reconnect_mode', 'favorites')
        self.menu["  Favorites Only"].state = (mode == 'favorites')
        self.menu["  Most Recent"].state = (mode == 'last')

        # Launch at login - can't check state without code signing, so we don't show a checkbox

        # Update status
        wifi_status = "On" if self.wifi_manager.get_power_state() else "Off"
        bt_status = "On" if self.bt_manager.get_power_state() else "Off"
        current_wifi = self.wifi_manager.get_current_network() or "Not connected"

        self.menu["Status"].title = f"WiFi: {wifi_status} | BT: {bt_status} | {current_wifi}"

    def update_device_list(self):
        """Update the list of Bluetooth devices in menu."""
        # Find the "Favorite Devices" section
        favorite_index = None
        for i, item in enumerate(self.menu):
            if item and hasattr(item, 'title'):
                # title is a method in rumps, need to call it
                title = item.title() if callable(item.title) else item.title
                if title == "Favorite Devices":
                    favorite_index = i
                    break

        if favorite_index is None:
            return

        # Remove old device items (everything between "Favorite Devices" and "Bluetooth Reconnect Mode")
        # Iterate through menu items directly instead of using integer indices
        items_to_remove = []
        found_favorite_devices = False

        for item in self.menu:
            if item and hasattr(item, 'title'):
                title = item.title() if callable(item.title) else item.title
                if title == "Favorite Devices":
                    found_favorite_devices = True
                    continue
                # Stop when we reach the next fixed menu section
                if found_favorite_devices and title == "Bluetooth Reconnect Mode":
                    break

            if found_favorite_devices:
                # Only add items with valid titles (not separators or auto-generated names)
                if item and hasattr(item, 'title'):
                    title = item.title() if callable(item.title) else item.title
                    # Skip auto-generated separator names
                    if not title.startswith('Separatormenuitem'):
                        items_to_remove.append(item)

        for item in items_to_remove:
            # title is a method in rumps, need to call it
            title = item.title() if callable(item.title) else item.title
            try:
                del self.menu[title]
            except KeyError:
                # Item might have been deleted or title changed, skip it
                # This can happen due to case differences in device names
                pass

        # Add device items - get recently connected devices first, then all paired
        try:
            devices = self.bt_manager.get_paired_devices()
        except Exception:
            device_item = rumps.MenuItem("  Error loading devices", callback=None)
            self.menu.insert_after("Favorite Devices", device_item)
            return

        connected_devices = [d for d in devices if d.get('connected', False)]

        # Sort: connected first, then by name
        devices_sorted = sorted(devices, key=lambda d: (not d.get('connected', False), d.get('name', '')))

        if not devices:
            device_item = rumps.MenuItem("  No devices found", callback=None)
            self.menu.insert_after("Favorite Devices", device_item)
        else:
            insert_after = "Favorite Devices"
            for device in devices_sorted[:10]:  # Limit to 10 devices
                name = device.get('name', 'Unknown')
                address = device.get('address', '')
                is_fav = self.config.is_favorite(address)
                is_connected = device.get('connected', False)

                # Show connection status and use checkmark for favorites
                status_icon = "🟢 " if is_connected else ""

                device_item = rumps.MenuItem(
                    f"  {status_icon}{name}",
                    callback=lambda sender, addr=address: self.toggle_favorite(addr)
                )
                # Set checkmark state for favorites
                device_item.state = is_fav

                self.menu.insert_after(insert_after, device_item)
                # title is a method in rumps, need to call it
                insert_after = device_item.title() if callable(device_item.title) else device_item.title

    def toggle_favorite(self, device_address):
        """Toggle a device as favorite."""
        if self.config.is_favorite(device_address):
            self.config.remove_favorite(device_address)
        else:
            self.config.add_favorite(device_address)

        self.update_device_list()

    def is_login_item(self):
        """Check if app is in login items."""
        try:
            import Foundation
            
            app_path = self._get_app_path()
            self.log_to_system(f"Checking login item status for app at path: {app_path}")
            
            if not app_path:
                self.log_to_system("No app path found")
                return False
                
            # Use SMAppService to check login item status
            SMAppService = Foundation.NSClassFromString('SMAppService')
            self.log_to_system(f"SMAppService class: {SMAppService}")
            
            mainApp = SMAppService.mainAppService()
            self.log_to_system(f"Main app service: {mainApp}")
            
            # Get status and debug info
            status = mainApp.status()
            self.log_to_system(f"SMAppService status: {status}")
            self.log_to_system(f"Status type: {type(status)}")
            
            # Check if enabled (status == SMAppServiceStatusEnabled)
            enabled = (status == 1)  # 1 = SMAppServiceStatusEnabled
            self.log_to_system(f"Login item enabled: {enabled}")
            return enabled
        except Exception as e:
            print(f"Error checking login items: {e}")
            return False

    def _get_app_path(self):
        """Get the path to the .app bundle if running as an app."""
        import sys
        # Check if running from an app bundle
        if getattr(sys, 'frozen', False):
            # Running from py2app bundle
            # sys.executable is at: SleepWatch.app/Contents/MacOS/SleepWatch
            # We need to go up 2 directories to get to SleepWatch.app
            return os.path.abspath(os.path.join(os.path.dirname(sys.executable), '..', '..'))
        else:
            # Running from source - check if in /Applications
            if os.path.exists('/Applications/SleepWatch.app'):
                return '/Applications/SleepWatch.app'
        return None

    @rumps.clicked("Launch at Login")
    def toggle_launch_at_login(self, sender):
        """Open System Settings to configure launch at login."""
        import subprocess

        self.log_to_system("Opening System Settings for Launch at Login")

        app_path = self._get_app_path()

        if not app_path:
            rumps.alert(
                "App Not in Applications",
                "Please move SleepWatch.app to /Applications first.\n\n"
                "Launch at Login only works when the app is installed in /Applications."
            )
            return

        # Show instructions
        response = rumps.alert(
            "Configure Launch at Login",
            "System Settings will open to Login Items.\n\n"
            "To enable:\n"
            "1. Click the '+' button under 'Open at Login'\n"
            "2. Navigate to Applications\n"
            "3. Select SleepWatch.app\n\n"
            "To disable:\n"
            "• Select SleepWatch in the list and click '-'",
            ok="Open Settings",
            cancel="Cancel"
        )

        if response == 1:  # OK button clicked
            try:
                # Open System Settings to Login Items
                subprocess.run([
                    'open',
                    'x-apple.systempreferences:com.apple.LoginItems-Settings.extension'
                ])
                self.log_to_system("Opened System Settings")
            except Exception as e:
                self.log_to_system(f"Error opening settings: {e}")
                rumps.alert("Error", f"Failed to open System Settings:\n{e}")

    def _check_updates_background(self):
        """Check for updates in background and notify if available."""
        import time
        time.sleep(3)  # Wait a bit after startup

        has_update, latest_version, download_url = check_for_updates()

        if has_update and latest_version:
            rumps.notification(
                f"SleepWatch v{latest_version} Available",
                "A new version is available!",
                f"Click to download or use 'Check for Updates' menu"
            )

    @rumps.clicked("Check for Updates...")
    def check_updates(self, sender):
        """Check for updates manually."""
        # Run directly on main thread since this is a manual check from menu
        # Network calls are usually fast enough to not block UI
        has_update, latest_version, download_url = check_for_updates()

        if has_update and latest_version:
            response = rumps.alert(
                f"Update Available: v{latest_version}",
                f"A new version of SleepWatch is available!\n\n"
                f"Current version: v{__version__}\n"
                f"Latest version: v{latest_version}\n\n"
                f"Would you like to download it?",
                ok="Download",
                cancel="Later"
            )

            if response == 1:  # Download clicked
                import subprocess
                subprocess.run(['open', download_url])
        elif latest_version is None:
            rumps.alert(
                "Update Check Failed",
                "Could not check for updates.\n\n"
                "Please check your internet connection and try again."
            )
        else:
            rumps.alert(
                "You're Up to Date!",
                f"SleepWatch v{__version__} is the latest version."
            )

    @rumps.clicked("Hide Menu Bar Icon")
    def hide_icon(self, sender):
        """Hide the menu bar icon."""
        import subprocess

        response = rumps.alert(
            "Hide Menu Bar Icon?",
            "This will hide SleepWatch from the menu bar.\n\n"
            "The app will continue running in the background.\n\n"
            "To restore the icon, run this command in Terminal:\n"
            "defaults delete com.sleepwatch.app hideIcon && killall SleepWatch",
            ok="Hide Icon",
            cancel="Cancel"
        )

        if response == 1:  # OK was clicked
            try:
                # Set the preference to hide icon
                subprocess.run(
                    ['defaults', 'write', 'com.sleepwatch.app', 'hideIcon', '-bool', 'true'],
                    check=True,
                    timeout=5
                )

                rumps.notification(
                    "Icon Hidden",
                    "",
                    "SleepWatch is still running. Use Terminal to restore icon."
                )

                # Restart the app to apply changes
                import sys
                import os
                python = sys.executable
                os.execl(python, python, *sys.argv)
            except Exception as e:
                rumps.alert("Error", f"Failed to hide icon:\n{e}")

    @rumps.clicked("Quit SleepWatch")
    def quit_app(self, sender):
        """Quit the application."""
        if self.sleep_watcher:
            self.sleep_watcher.stop()
        rumps.quit_application()


def main():
    """Entry point for the application."""
    # Start the app - if blueutil is not installed, the menu will show an install option
    app = SleepWatchApp()
    app.run()


if __name__ == '__main__':
    main()
