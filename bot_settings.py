""" Функции отвечающие за настройки бота """

import json


def read_settings(key):
    with open("/projects/sb_bot/data/settings.json", 'r') as f:
        settings = json.load(f)
        for old_key in settings:

            if old_key == key:
                print(f"Returned {settings[f'{key}']}")
                return settings[f'{key}']


def read_settings_all():
    with open("/projects/sb_bot/data/settings.json", 'r') as f:
        settings = json.load(f)
    return settings


def update_settings(key, value):
    with open("/projects/sb_bot/data/settings.json", 'r') as f:
        settings = json.load(f)
    for old_key in settings:
        if old_key == key:

            if value in {'True', 'False'}:


                value = eval(value)
            else:
                value = int(value)
            settings[old_key] = value
            with open("/projects/sb_bot/data/settings.json", 'w') as f:
                json.dump(settings, f, indent=4)
            print(f"UPDATED {old_key} with value {settings[old_key]}")


def add_key(key, value):
    with open("/projects/sb_bot/data/settings.json", 'r') as f:
        settings = json.load(f)
    print(settings)
    settings[key] = value
    with open("/projects/sb_bot/data/settings.json", 'w') as f:
        json.dump(settings, f, indent=4)


if __name__ == "__main__":
    # read_settings('alert_timer')
    print('Hello World')
