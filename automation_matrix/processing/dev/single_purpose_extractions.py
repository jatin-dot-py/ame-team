def find_value_by_key(data: dict, key: str) -> any:
    """
    Searches recursively for a value by its key in a nested dictionary or list structure.

    Args:
        data (dict): The dictionary or list to search through.
        key (str): The key for which to search the value.

    Returns:
        any: The value found for the specified key, or None if the key is not found.
    """
    #print(f"\n********** WORKFLOW FUNCTION: find_value_by_key START **********")
    #print("Arguments Received:")
    #print(f"Argument 1... data:\n{data}")
    #print(f"Argument 2... key:\n{key}")
    result = None

    def search(data, key):
        nonlocal result
        if isinstance(data, dict):
            if key in data:
                result = data[key]
                return
            for value in data.values():
                if result is None:
                    search(value, key)
        elif isinstance(data, list):
            for item in data:
                if result is None:
                    search(item, key)

    search(data, key)
    #print(f"Result: {result}")
    #print(f"\n********** WORKFLOW FUNCTION: find_value_by_key END **********")
    return result


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
  "Chemical Peel": {
    "Parent LSIs": [
      "skin rejuvenation",
      "cosmetic dermatology",
      "facial treatments",
      "aesthetic procedures",
      "skin resurfacing",
      "dermatological services",
      "medical aesthetics",
      "skin care treatments",
      "skin regeneration",
      "skin health"
    ],
    "Child LSIs": [
      "glycolic acid peel",
      "salicylic acid peel",
      "lactic acid peel",
      "TCA peel",
      "phenol peel",
      "enzyme peel",
      "beta peel",
      "retinoic acid peel",
      "professional chemical peel",
      "superficial chemical peel"
    ],
    "Natural LSIs": [
      "skin treatment",
      "facial peel",
      "dermal peel",
      "chemical exfoliation",
      "skin renewal",
      "skin resurfacing treatment",
      "skin texture improvement",
      "age spots reduction",
      "hyperpigmentation treatment",
      "acne scar treatment"
    ],
    "Related LSIs": [
      "skin clinic",
      "dermatologist",
      "beauty treatments",
      "medical spa",
      "skin analysis",
      "cosmeceuticals",
      "skincare regimen",
      "cosmetic procedures",
      "pre and post-peel care",
      "topical skincare products"
    ]
  }
}

    example_dict = '''{
        "level1": {
            "level2": {
                "username": "john_doe"
            },
            "other_key": ["item1", {
                "username": "jane_doe"
            }]
        },
        "top_level_username": "admin"
    }'''

    # Search for the 'username' key
    result = find_value_by_key(example_dict, "username")
    print("Found value:", result)

    result = find_value_by_key(data_lsis, "Natural LSIs")
    print("Found value:", result)
