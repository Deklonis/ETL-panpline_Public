import json
DB_PATH = 'components/db.db'

def get_settings_data():
    with open('settings/settings.json', "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings_data(data):
    with open('settings/settings.json', "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)