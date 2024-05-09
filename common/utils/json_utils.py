# common/utils/json_utils.py
import json
from ame_team.settings.base import BASE_DIR
from common import pretty_print, print_link
from datetime import datetime
timestamp = datetime.now().strftime("%y%m%d%H%M%S")

def clean_json_data(json_data):
    """
    Cleans up the JSON data by removing unnecessary escape characters
    and trying to parse it into a valid JSON object.
    """
    try:
        if json_data.startswith('"') and json_data.endswith('"'):
            json_data = json_data[1:-1]

        json_data = json_data.replace('\\"', '"').replace('\\\\', '\\')

        return json.loads(json_data)
    except Exception as e:
        return json_data


def get_json_data(file_path):
    with open(file_path, 'r') as file:
        original_data = json.load(file)
    return original_data


def save_to_json(data, new_file_path, add_datetime=False):
    if add_datetime:
        new_file_path = f"{new_file_path}_{timestamp}.json"
    with open(new_file_path, 'w') as file:
        json.dump(data, file, separators=(',', ':'), indent=None)
        print_link(new_file_path)


def get_json_data_from_base(path_from_base):
    file_path = BASE_DIR / path_from_base
    with open(file_path, 'r') as file:
        original_data = json.load(file)
    return original_data


def save_to_json_from_base(data, path_from_base, add_datetime=False):
    if add_datetime:
        path_from_base = f"{path_from_base}_{timestamp}.json"
    save_path = BASE_DIR / path_from_base
    with open(save_path, 'w') as file:
        json.dump(data, file, separators=(',', ':'), indent=None)
        print_link(save_path)
