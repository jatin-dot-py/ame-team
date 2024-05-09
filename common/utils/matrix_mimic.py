import asyncio
import json
import os
import pickle
from datetime import datetime
from decimal import Decimal

# Directory for saving data
save_dir = "D:/OneDrive/_dev/data/mimic"

def append_datetime(identifier):
    """Appends the current date and time to the given identifier."""
    return f"{identifier}_{datetime.now().strftime('%y%m%d_%H%M%S')}"

def convert_to_json_compatible(data):
    """
    Recursively converts various data types into JSON-compatible formats.
    Returns the converted data.
    """
    if isinstance(data, (str, int, float, bool, type(None))):
        return data
    elif isinstance(data, (list, tuple)):
        return [convert_to_json_compatible(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_to_json_compatible(value) for key, value in data.items()}
    elif isinstance(data, datetime):
        return data.isoformat()
    elif isinstance(data, Decimal):
        return float(data)
    elif hasattr(data, '__dict__'):
        return {key: convert_to_json_compatible(value) for key, value in data.__dict__.items()}
    else:
        try:
            return str(data)
        except Exception as e:
            print(f"Error converting data: {e}")
            return None
def save_data_sync(data, identifier):
    """Saves data synchronously in both pickle and JSON formats."""
    identifier_with_datetime = append_datetime(identifier)

    # Save as pickle
    try:
        pickle_filename = os.path.join(save_dir, f"{identifier_with_datetime}.pkl")
        with open(pickle_filename, 'wb') as file:
            pickle.dump(data, file)
        print(f"Data saved to {pickle_filename}")
    except Exception as e:
        print(f"Error saving pickle file: {e}")

    # Convert to JSON-compatible format and save as JSON
    try:
        processed_data = convert_to_json_compatible(data)
        json_filename = os.path.join(save_dir, f"{identifier_with_datetime}.json")
        with open(json_filename, 'w', encoding='utf-8') as file:
            json.dump(processed_data, file, ensure_ascii=False, indent=4)
        print(f"Data saved to file:///{json_filename.replace('\\', '/')}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

async def save_data_async(data, identifier):
    """Saves data asynchronously by calling the synchronous save function in an executor."""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, save_data_sync, data, identifier)

def retrieve_data_sync(identifier):
    """Retrieves data synchronously using the full identifier, including the datetime."""
    filename = os.path.join(save_dir, f"{identifier}.pkl")
    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print(f"No saved data found for identifier '{identifier}'.")

async def retrieve_data_async(identifier):
    """Retrieves data asynchronously by calling the synchronous retrieve function in an executor."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, retrieve_data_sync, identifier)
