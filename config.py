import os


class Config:
    root_folder = os.path.dirname(os.path.realpath(__file__))
    api_root = "http://127.0.0.1:8000/api/"


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
PPO_LOCATIONS_PATH = os.path.join(BASE_PATH, r"resources/ppo_specific_data/locations.json")

RARITY_MAPPING = {
    "c": "Common",
    "uc": "Uncommon",
    "r": "Rare",
    "vr": "Very Rare",
    "er": "Extremely Rare",
    "l": "Legendary"
}
