"""
Version information for SleepWatch.
"""

__version__ = "1.0.0"
__version_info__ = tuple(int(i) for i in __version__.split('.'))

# GitHub repository information
GITHUB_REPO_OWNER = "metacometdave"
GITHUB_REPO_NAME = "SleepWatch"
GITHUB_REPO_URL = f"https://github.com/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}"
GITHUB_RELEASES_URL = f"{GITHUB_REPO_URL}/releases"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/releases/latest"
