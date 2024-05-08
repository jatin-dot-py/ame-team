from typing import List, Dict, Optional, Any
from asgiref.sync import sync_to_async, async_to_sync


async def items_to_string_async(items: List[str]) -> str:
    """
    Convert a list of items to a single string asynchronously.

    Args:
        items: A list of items as strings.

    Returns:
        A single string representing the joined items.
    """
    result_list = '\n'.join(items)
    return result_list


def items_to_string_sync(items: List[str]) -> str:
    """
    Synchronously convert a list of items to a single string.

    Args:
        items: A list of items as strings.

    Returns:
        A single string representing the joined items.
    """
    item_text = async_to_sync(items_to_string_async)(items)
    return item_text


async def complex_items_to_string_async(data: dict) -> str:
    """
    Convert complex data structure to a formatted string asynchronously.

    Args:
        data: A dictionary with keys mapping to dictionaries of lists.

    Returns:
        A formatted string representing the complex data structure.
    """
    result_strings = []
    for key, value in data.items():
        result_strings.append(key)
        for sub_key, items in value.items():
            result_strings.append(f"  {sub_key}:")
            for item in items:
                result_strings.append(f"    - {item}")
    formatted_result = '\n'.join(result_strings)
    return formatted_result


def convert_complex_data_to_string(data: Dict[str, Dict[str, List[str]]]) -> str:
    """
    Synchronously convert a complex data structure to a formatted string.

    Args:
        data: A dictionary with keys mapping to dictionaries of lists.

    Returns:
        A formatted string representing the complex data structure.
    """
    text = async_to_sync(complex_items_to_string_async)(data)
    return text


async def complex_items_to_string_by_level_async(data: dict, key_to_get: str = None, level: int = None) -> str:
    """
    Asynchronously convert complex data with options for specific key or level to a formatted string.

    Args:
        data: A dictionary representing the complex data structure.
        key_to_get: Optional; Key to narrow down the conversion.
        level: Optional; Level to narrow down the conversion.

    Returns:
        A formatted string representing the complex data according to the key or level specified.
    """
    result_strings = []
    if key_to_get and level is None:
        updated_data = data.get(key_to_get, {})
        if isinstance(updated_data, dict):
            for sub_key, items in updated_data.items():
                result_strings.append(f"{sub_key}:")
                for item in items:
                    result_strings.append(f"  - {item}")
        else:
            result_strings.append(str(updated_data))
    elif key_to_get and level is not None:
        for key, value in data.items():
            if key == key_to_get:
                continue
            for sub_key, items in value.items():
                if sub_key == key_to_get:
                    result_strings.append(f"{sub_key}:")
                    for item in items:
                        result_strings.append(f"  - {item}")
    else:
        for key, value in data.items():
            result_strings.append(key)
            for sub_key, items in value.items():
                result_strings.append(f"  {sub_key}:")
                for item in items:
                    result_strings.append(f"    - {item}")

    formatted_result = '\n'.join(result_strings)
    return formatted_result


def convert_complex_data_to_string_by_level(data: Dict[str, Any], key_to_get: Optional[str] = None, level: Optional[int] = None) -> str:
    """
    Synchronously convert complex data with options for specific key or level to a formatted string.

    Args:
        data: A dictionary representing the complex data structure.
        key_to_get: Optional; Key to narrow down the conversion.
        level: Optional; Level to narrow down the conversion.

    Returns:
        A formatted string representing the complex data according to the key or level specified.
    """
    text = async_to_sync(complex_items_to_string_by_level_async)(data, key_to_get, level)
    return text




if __name__ == "__main__":
    example_items = [
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
]

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

    print(items_to_string_sync(example_items))


    print(complex_items_to_string_async(data_lsis))
