"""Configuration management for SleepWatch."""
import json
import os
from pathlib import Path

CONFIG_FILE = Path.home() / '.sleepwatch.json'

DEFAULT_CONFIG = {
    'wifi_enabled': True,
    'bluetooth_enabled': True,
    'auto_reconnect_wifi': True,
    'auto_reconnect_bluetooth': True,
    'favorite_devices': [],
    'last_wifi_network': None,
    'reconnect_mode': 'favorites'  # 'favorites', 'last', or 'all'
}


class Config:
    """Manages app configuration and preferences."""

    def __init__(self):
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from disk or create default."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults to handle new keys
                    config = DEFAULT_CONFIG.copy()
                    config.update(loaded)
                    return config
            except (json.JSONDecodeError, IOError):
                return DEFAULT_CONFIG.copy()
        return DEFAULT_CONFIG.copy()

    def save(self):
        """Save configuration to disk."""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            print(f"Failed to save config: {e}")

    def get(self, key, default=None):
        """Get a configuration value."""
        return self.config.get(key, default)

    def set(self, key, value):
        """Set a configuration value and save."""
        self.config[key] = value
        self.save()

    def toggle(self, key):
        """Toggle a boolean configuration value."""
        self.config[key] = not self.config.get(key, False)
        self.save()
        return self.config[key]

    def add_favorite(self, device_address):
        """Add a device to favorites."""
        favorites = self.config.get('favorite_devices', [])
        if device_address not in favorites:
            favorites.append(device_address)
            self.set('favorite_devices', favorites)

    def remove_favorite(self, device_address):
        """Remove a device from favorites."""
        favorites = self.config.get('favorite_devices', [])
        if device_address in favorites:
            favorites.remove(device_address)
            self.set('favorite_devices', favorites)

    def is_favorite(self, device_address):
        """Check if a device is in favorites."""
        return device_address in self.config.get('favorite_devices', [])
