"""WiFi network management."""
import subprocess
import re


class WiFiManager:
    """Manages WiFi state and connections."""

    INTERFACE = 'en0'  # Default WiFi interface on most Macs

    @staticmethod
    def get_power_state():
        """Get current WiFi power state (True = on, False = off)."""
        try:
            result = subprocess.run(
                ['networksetup', '-getairportpower', WiFiManager.INTERFACE],
                capture_output=True,
                text=True,
                check=True
            )
            # Output format: "Wi-Fi Power (en0): On" or "Wi-Fi Power (en0): Off"
            return 'On' in result.stdout
        except subprocess.CalledProcessError:
            return None

    @staticmethod
    def set_power(state):
        """Set WiFi power state (True = on, False = off)."""
        try:
            subprocess.run(
                ['networksetup', '-setairportpower', WiFiManager.INTERFACE, 'on' if state else 'off'],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def get_current_network():
        """Get currently connected WiFi network name (SSID)."""
        try:
            result = subprocess.run(
                ['networksetup', '-getairportnetwork', WiFiManager.INTERFACE],
                capture_output=True,
                text=True,
                check=True
            )
            # Output format: "Current Wi-Fi Network: NetworkName"
            match = re.search(r'Current Wi-Fi Network: (.+)', result.stdout)
            if match:
                return match.group(1).strip()
            return None
        except subprocess.CalledProcessError:
            return None

    @staticmethod
    def connect_to_network(ssid):
        """Connect to a specific WiFi network."""
        try:
            subprocess.run(
                ['networksetup', '-setairportnetwork', WiFiManager.INTERFACE, ssid],
                check=True,
                capture_output=True,
                timeout=15
            )
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            return False

    @staticmethod
    def get_preferred_networks():
        """Get list of preferred (saved) WiFi networks."""
        try:
            result = subprocess.run(
                ['networksetup', '-listpreferredwirelessnetworks', WiFiManager.INTERFACE],
                capture_output=True,
                text=True,
                check=True
            )
            # Skip the first line (header) and strip whitespace
            networks = [line.strip() for line in result.stdout.split('\n')[1:] if line.strip()]
            return networks
        except subprocess.CalledProcessError:
            return []
