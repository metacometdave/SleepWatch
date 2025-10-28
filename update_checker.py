"""
Auto-update checker for SleepWatch.
Checks GitHub releases for new versions.
"""
import urllib.request
import json
from version import __version__, GITHUB_API_URL, GITHUB_RELEASES_URL


def parse_version(version_string):
    """Parse version string to tuple of ints."""
    # Remove 'v' prefix if present
    version_string = version_string.lstrip('v')
    try:
        return tuple(int(i) for i in version_string.split('.'))
    except (ValueError, AttributeError):
        return (0, 0, 0)


def check_for_updates():
    """
    Check GitHub for updates.
    Returns: (has_update, latest_version, download_url) or (False, None, None) on error
    """
    try:
        # Make request to GitHub API
        req = urllib.request.Request(
            GITHUB_API_URL,
            headers={'User-Agent': 'SleepWatch'}
        )

        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())

        latest_version = data.get('tag_name', '').lstrip('v')
        download_url = None

        # Find the .zip asset
        for asset in data.get('assets', []):
            if asset.get('name', '').endswith('.zip'):
                download_url = asset.get('browser_download_url')
                break

        if not download_url:
            # Fallback to releases page
            download_url = GITHUB_RELEASES_URL

        # Compare versions
        current = parse_version(__version__)
        latest = parse_version(latest_version)

        has_update = latest > current

        return has_update, latest_version, download_url

    except Exception as e:
        print(f"Update check failed: {e}")
        return False, None, None


def get_current_version():
    """Get the current version string."""
    return __version__
