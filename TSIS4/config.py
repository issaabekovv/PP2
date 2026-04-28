import json
import os

DEFAULT_SETTINGS = {
    "snake_color": [0, 255, 0],
    "grid_overlay": True,
    "sound": True
}

def load_settings():
    if not os.path.exists('settings.json'):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    with open('settings.json', 'r') as f:
        return json.load(f)

def save_settings(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)