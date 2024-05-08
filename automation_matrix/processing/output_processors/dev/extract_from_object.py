from matrix_utils import matrix_print

def extract_data(data, path=None, target_key=None, target_level=None, default=None, transformation=None):
    """
    Unified entry point for extracting data from complex dictionaries.

    :param data: The dictionary from which data is to be extracted.
    :param path: The path to the data within the dictionary, expressed as a dot-separated string or a list of keys.
    :param target_key: The key to search for at a specific level, used in level-based extraction.
    :param target_level: The level depth, STARTING FROM 0, for level-based extraction.
    :param default: The default value to return if the path does not exist or the key is not found at the target level.
    :param transformation: Optional function to apply to the extracted data.
    :return: The extracted and possibly transformed data, or the default value.
    """
    extracted_data = None  # Initialize extracted_data

    if path is not None:
        # Path-based extraction
        if isinstance(path, str):
            path = path.split('.')
        extracted_data = _extract_raw(data, path, default)
    elif target_key is not None and target_level is not None:
        # Level-based extraction
        extracted_data = _extract_by_level(data, target_key, 0, target_level, default)

    if extracted_data is None:
        return default

    # Apply transformation if specified
    if transformation:
        return _apply_transformation(extracted_data, transformation)

    return extracted_data


def _extract_by_level(data, target_key, current_level, target_level, default):
    """
    Helper function for level-based data extraction.

    :param data: Current level of the data dictionary.
    :param target_key: The target key to search for.
    :param current_level: Current depth level in the recursive search.
    :param target_level: The target depth level where the key is expected to be found.
    :param default: The default value to return if the key is not found at the target level.
    :return: The extracted data or the default value.
    """
    print(f"Entering _extract_by_level: current_level={current_level}, target_level={target_level}, data keys={list(data.keys()) if isinstance(data, dict) else 'N/A'}")
    if current_level == target_level:
        print(f"At target level: {target_level}, looking for key: '{target_key}'")
        return data.get(target_key, default)

    if isinstance(data, dict):
        for key, value in data.items():
            print(f"Current key in _extract_by_level: {key}")
            if isinstance(value, (dict, list)):
                result = _deep_search(value, target_key, current_level + 1, target_level, default)
                if result is not default:
                    return result
    return default

def _deep_search(data, target_key, current_level, target_level, default):
    """
    Performs a deep search in dictionaries and lists for the target_key at the target_level.

    :param data: The current data structure (dict or list) being searched.
    :param target_key: The target key to find.
    :param current_level: The current level in the search.
    :param target_level: The desired level to find the target_key.
    :param default: The default value to return if the target_key is not found.
    :return: The value of the target_key if found, else default.
    """
    print(f"Entering _deep_search: current_level={current_level}, target_level={target_level}, type={type(data).__name__}")
    if isinstance(data, list):
        for index, item in enumerate(data):
            print(f"List item index: {index}, type={type(item).__name__}")
            if isinstance(item, (dict, list)):
                result = _deep_search(item, target_key, current_level, target_level, default)  # Keep current_level for list items
                if result is not default:
                    return result
    elif isinstance(data, dict):
        if current_level == target_level:
            print(f"At target level in _deep_search: {target_level}, looking for key: '{target_key}'")
            return data.get(target_key, default)
        for key, value in data.items():
            print(f"Current key in _deep_search: {key}, type={type(value).__name__}")
            if isinstance(value, (dict, list)):
                result = _deep_search(value, target_key, current_level + 1, target_level, default)
                if result is not default:
                    return result
    return default


def _extract_raw(data, path, default):
    """
    Recursively navigate through the data based on the path to extract the raw data.

    :param data: The current level of the data dictionary.
    :param path: The remaining path as a list of keys.
    :param default: The default value to return if the path does not exist.
    :return: The extracted data or the default value.
    """
    if not path:
        return data

    key = path[0]
    if key in data:
        return _extract_raw(data[key], path[1:], default)
    else:
        return default


def _apply_transformation(data, transformation):
    """
    Apply a transformation function to the data.

    :param data: The data to transform.
    :param transformation: The transformation function to apply.
    :return: The transformed data.
    """
    try:
        return transformation(data)
    except Exception as e:
        # Handle or log the exception as necessary
        print(f"Error applying transformation: {e}")
        return data  # or handle the error as required


# Example transformation function
def capitalize_string(s):
    if isinstance(s, str):
        return s.capitalize()
    return s


# Example usage
if __name__ == "__main__":
    data = {
        "user": {
            "name": "john doe",
            "address": {
                "city": "new york",
                "zip": "10001"
            }
        }
    }

    data_lsis = {
  "Botox Injections": {
    "Parent LSIs": [
      "cosmetic injections",
      "facial rejuvenation procedures",
      "non-surgical aesthetics",
      "anti-aging treatments",
      "dermal fillers",
      "minimally invasive procedures",
      "injectable cosmetics",
      "medical aesthetic treatments"
    ],
    "Child LSIs": [
      "botulinum toxin type A",
      "wrinkle reduction",
      "forehead injections",
      "crow's feet treatment",
      "frown line injections",
      "bunny lines treatment",
      "gummy smile correction",
      "jawline contouring",
      "lip flip procedure",
      "hyperhidrosis treatment"
    ],
    "Natural LSIs": [
      "cosmetic injections",
      "facial rejuvenation",
      "anti-wrinkle treatment",
      "anti-aging injections",
      "wrinkle relaxers",
      "skin smoothing treatment",
      "smile line reduction",
      "aesthetic facial injections",
      "Botox cosmetic",
      "skin rejuvenation"
    ],
    "Related LSIs": [
      "cosmetic dermatology",
      "medical aesthetics clinic",
      "dermatologist",
      "aesthetic nurse",
      "injectable aesthetics",
      "cosmetic procedures",
      "skin care treatments",
      "beauty therapies",
      "esthetician",
      "skincare products"
    ]
  }
}

    natural_lsis = extract_data(data_lsis, target_key="Natural LSIs", target_level=1)
    print("\n\n")
    matrix_print(natural_lsis)
    print("\n\n")

    print(f"Debug: target_key= 'Natural LSIs', target_level=2\n")
    print(f"data_lsis: {data_lsis}")
    print(f"Natural LSIs: {natural_lsis}")


    # Extracting data without transformation
    # city = extract_data(data, "user.address.city")
    # print(f"City: {city}")

    # Extracting and transforming data
    # user_name = extract_data(data, "user.name", transformation=capitalize_string)
    # print(f"User Name: {user_name}")

