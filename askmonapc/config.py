import os

CONFIG_PATH = os.path.join(os.environ.get("APPDATA", os.path.join(os.environ.get("HOME"), ".config")), "askmonapc")
CACHE_PATH = os.path.join(CONFIG_PATH, "cache")

if not os.path.exists(CONFIG_PATH):
    os.mkdir(CONFIG_PATH)
if not os.path.exists(CACHE_PATH):
    os.mkdir(CACHE_PATH)