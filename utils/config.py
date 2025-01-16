import os

# Configuration constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_FILE = os.path.join(BASE_DIR, 'settings.json')

# Default settings
DEFAULT_SETTINGS = {
    'music_folder': '',
    'volume': 0.7,
    'selected_days': [],
    'schedules': []
}
