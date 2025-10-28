"""Bluetooth device management."""
import subprocess
import json
import os
import shutil

class BluetoothError(Exception):
    """Bluetooth operation error."""
    pass

class BluetoothManager:
    """Manages Bluetooth state and device connections."""
    
    @staticmethod
    def is_brew_installed():
        """Check if Homebrew is installed."""
        return bool(shutil.which('brew'))

    @staticmethod
    def is_blueutil_installed():
        """Check if blueutil is installed and accessible."""
        return bool(shutil.which('blueutil'))
    
    @staticmethod
    def get_blueutil_path():
        """Get the full path to blueutil."""
        # Check common homebrew locations
        paths = [
            shutil.which('blueutil'),  # Check PATH first
            '/usr/local/bin/blueutil',  # Intel Mac homebrew
            '/opt/homebrew/bin/blueutil',  # Apple Silicon homebrew
        ]
        for path in paths:
            if path and os.path.exists(path):
                return path
        return '/usr/local/bin/blueutil'  # fallback

    @staticmethod
    def get_power_state():
        """Get current Bluetooth power state (True = on, False = off)."""
        blueutil = BluetoothManager.get_blueutil_path()
        if not os.path.exists(blueutil):
            raise BluetoothError("blueutil not installed")
            
        try:
            result = subprocess.run(
                [blueutil, '--power'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                check=True
            )
            return result.stdout.strip() == '1'
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    @staticmethod
    def set_power(state):
        """Set Bluetooth power state (True = on, False = off)."""
        blueutil = BluetoothManager.get_blueutil_path()
        if not os.path.exists(blueutil):
            raise BluetoothError("blueutil not installed")
            
        try:
            subprocess.run(
                [blueutil, '--power', '1' if state else '0'],
                check=True,
                capture_output=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    @staticmethod
    def get_paired_devices():
        """Get list of paired Bluetooth devices."""
        blueutil = BluetoothManager.get_blueutil_path()
        if not os.path.exists(blueutil):
            raise BluetoothError("blueutil not installed")
            
        try:
            result = subprocess.run(
                [blueutil, '--paired', '--format', 'json'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                check=True
            )
            devices = json.loads(result.stdout)
            return devices
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def get_connected_devices():
        """Get list of currently connected Bluetooth devices."""
        devices = BluetoothManager.get_paired_devices()
        return [d for d in devices if d.get('connected', False)]

    @staticmethod
    def connect_device(address):
        """Connect to a specific Bluetooth device by address."""
        try:
            subprocess.run(
                ['blueutil', '--connect', address],
                check=True,
                capture_output=True,
                timeout=10
            )
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return False

    @staticmethod
    def disconnect_device(address):
        """Disconnect a specific Bluetooth device by address."""
        try:
            subprocess.run(
                ['blueutil', '--disconnect', address],
                check=True,
                capture_output=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    @staticmethod
    def reconnect_favorites(favorite_addresses):
        """Reconnect to favorite devices."""
        if not BluetoothManager.get_power_state():
            BluetoothManager.set_power(True)
            # Give Bluetooth time to power on
            import time
            time.sleep(1)

        success_count = 0
        for address in favorite_addresses:
            if BluetoothManager.connect_device(address):
                success_count += 1

        return success_count
