import asyncio


async def get_user_inputs(input_prompts):
    """
    Prompts the user for inputs based on a list of dictionaries, where each dictionary contains details of a prompt.

    Parameters:
    - input_prompts: A list of dictionaries, where each dictionary represents a prompt. The 'name' key in each dictionary is used as the prompt for user input.

    Returns:
    - A dictionary where keys are the 'name' values from the input dictionaries and values are the user inputs.
    """
    user_responses = {}
    for prompt_dict in input_prompts:
        prompt_name = prompt_dict.get('name')
        if prompt_name:
            user_input = input(f"Enter a value for {prompt_name}: ")
            user_responses[prompt_name] = user_input

    return user_responses


# Example usage
if __name__ == "__main__":
    prompts = [
        {
            "id": 334,
            "variable_id": 518,
            "name": "DATA_1010",
            "value": "Get a great description.",
            "data_type": "unknown",
            "source_type": "action_default",
            "destination_type": "action_function_arg",
            "is_dynamic": False
        },
        {
            "id": 335,
            "variable_id": 519,
            "name": "PRE_PROCESSED_DATA_1002",
            "value": "",
            "data_type": "unknown",
            "source_type": "action_function_return",
            "destination_type": "dynamic_action_variable",
            "is_dynamic": True
        },
        {
            "id": 336,
            "variable_id": 520,
            "name": "IMAGE_SOURCE_1003",
            "value": "",
            "data_type": "str",
            "source_type": "user_input",
            "destination_type": "action_function_arg",
            "is_dynamic": False
        }
    ]

    user_inputs = asyncio.run(get_user_inputs(prompts))

    print(user_inputs)
