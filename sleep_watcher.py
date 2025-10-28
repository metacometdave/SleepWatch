"""Sleep/wake event detection for macOS."""
import threading
from Foundation import NSWorkspace, NSNotificationCenter


class SleepWatcher:
    """Watches for system sleep and wake events using macOS NSWorkspace notifications."""

    def __init__(self, on_sleep=None, on_wake=None):
        """
        Initialize the sleep watcher.

        Args:
            on_sleep: Callback function to call when system goes to sleep
            on_wake: Callback function to call when system wakes up
        """
        self.on_sleep = on_sleep
        self.on_wake = on_wake
        self.notification_center = None
        self.workspace = None
        self._running = False

    def start(self):
        """Start watching for sleep/wake events."""
        if self._running:
            return

        self._running = True

        # Get shared workspace and notification center
        self.workspace = NSWorkspace.sharedWorkspace()
        self.notification_center = self.workspace.notificationCenter()

        # Register for sleep notification
        self.notification_center.addObserver_selector_name_object_(
            self,
            'systemWillSleep:',
            'NSWorkspaceWillSleepNotification',
            None
        )

        # Register for wake notification
        self.notification_center.addObserver_selector_name_object_(
            self,
            'systemDidWake:',
            'NSWorkspaceDidWakeNotification',
            None
        )

        print("SleepWatcher started")

    def stop(self):
        """Stop watching for sleep/wake events."""
        if not self._running:
            return

        if self.notification_center:
            self.notification_center.removeObserver_(self)

        self._running = False
        print("SleepWatcher stopped")

    def systemWillSleep_(self, notification):
        """Called by macOS when system is about to sleep."""
        if self.on_sleep and callable(self.on_sleep):
            # Run callback in separate thread to not block notification
            threading.Thread(target=self.on_sleep, daemon=True).start()

    def systemDidWake_(self, notification):
        """Called by macOS when system wakes from sleep."""
        if self.on_wake and callable(self.on_wake):
            # Run callback in separate thread to not block notification
            threading.Thread(target=self.on_wake, daemon=True).start()
