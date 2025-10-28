"""
Setup script for building SleepWatch as a standalone macOS application.
"""
from setuptools import setup

APP = ['sleepwatch.py']
DATA_FILES = [('', ['icon.png'])]
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'icon.png',
    'plist': {
        'CFBundleName': 'SleepWatch',
        'CFBundleDisplayName': 'SleepWatch',
        'CFBundleIdentifier': 'com.sleepwatch.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '10.13',
        'LSUIElement': True,  # Hide from Dock (menu bar app only)
        'NSHumanReadableCopyright': 'MIT License',
        'NSHighResolutionCapable': True,
    },
    'includes': [
        'rumps',
        'bluetooth_manager',
        'wifi_manager',
        'sleep_watcher',
        'config',
        'version',
        'update_checker',
    ],
    'packages': ['rumps'],
}

setup(
    name='SleepWatch',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'rumps>=0.4.0',
        'pyobjc-framework-Cocoa>=12.0',
        'Pillow>=12.0.0',
    ],
)
