import asyncio
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
import aiofiles
import json


# Initializes MarkdownIt with default settings
def init_markdown_parser():
    md = MarkdownIt("commonmark")
    return md

# Synchronously parses Markdown text
def parse_markdown(text):
    if not text:
        print("ERROR: parse_markdown received empty text.")
        return {}
    md = init_markdown_parser()
    tokens = md.parse(text)
    root_node = SyntaxTreeNode(tokens)
    return build_simple_structure(root_node.children)

# Builds a simplified content structure from Markdown tokens
def build_simple_structure(nodes, content_dict=None, current_key='root'):
    if content_dict is None:
        content_dict = {current_key: []}

    for node in nodes:
        if node.type.startswith('heading'):
            current_key = get_text_content(node).strip()
            content_dict[current_key] = []
        elif node.type in ['paragraph', 'inline', 'text']:
            text = get_text_content(node).strip()
            if text:
                content_dict[current_key].append(text)
        elif node.type in ['bullet_list', 'ordered_list']:
            for child in node.children:
                if child.type == 'list_item':
                    list_item_text = get_text_content(child).strip()
                    if list_item_text:
                        content_dict[current_key].append(list_item_text)

    return content_dict

# Retrieves text content from a node
def get_text_content(node):
    if node.type == 'text':
        return node.content
    elif node.children:
        return ' '.join(get_text_content(child) for child in node.children)
    return ''

# Asynchronously wraps the synchronous parse_markdown function
async def parse_markdown_async(main_function_returns: dict, **kwargs) -> dict:
    """
    Asynchronously parses markdown text into its components.

    Args:
        main_function_returns (dict): A dictionary potentially containing a 'value' key with markdown text.
        **kwargs: Additional keyword arguments passed to the function.

    Returns:
        dict: A dictionary with an added 'processed_value' key containing parsed markdown components if successful.
              In case of an error, it contains 'error' and 'message' keys detailing the issue.
    """
    text = main_function_returns.get('value')

    if text is None:
        print("ERROR: parse_markdown_async received None as text input.")
        main_function_returns["error"] = True
        main_function_returns["message"] = "No text provided for markdown parsing."
        return main_function_returns

    loop = asyncio.get_running_loop()
    try:
        result_dict = await loop.run_in_executor(None, parse_markdown, text)
        if not result_dict:
            print("ERROR: parse_markdown returned an empty dictionary.")
            main_function_returns["error"] = True
            main_function_returns["message"] = "Markdown parsing resulted in an empty dictionary."
        else:
            main_function_returns['processed_value'] = result_dict

    except Exception as e:
        print(f"ERROR during markdown parsing: {str(e)}")
        main_function_returns["error"] = True
        main_function_returns["message"] = f"Markdown parsing error: {str(e)}"

    return main_function_returns

# This allows you to get a specific key by the count, such as the third key.
async def extract_by_level_from_markdown(markdown_content: dict, count: int = 1) -> dict:
    """
    Asynchronously extracts specified structure from markdown content by level.

    Args:
        markdown_content (dict): Dictionary containing markdown content to process.
        count (int, optional): 1-based index to specify which structure to extract from the 'root' list. Defaults to 1.

    Returns:
        dict: The specific structure from the 'root' list if count is within range.
              The entire 'processed_value' if count is None.
              A dictionary with 'error' and 'message' in case of an error or invalid count.
    """
    structured_data = {
        'signature': 'post_processing',
        "value": None,
        "data_type": "unknown",
        "error": False,
        "message": ""
    }

    # Prepare the input dictionary expected by parse_markdown_async
    main_function_input = {'value': markdown_content}

    # Call parse_markdown_async with the markdown content
    result = await parse_markdown_async(main_function_input)

    if result.get("error"):
        # Populate the structured_data with error details if parsing failed
        structured_data.update({
            "error": True,
            "message": result.get("message", "An error occurred during markdown parsing.")
        })
        return structured_data

    # Extract 'processed_value' which contains the structured content
    structured_content = result.get('processed_value', {})
    root_list = structured_content.get('root', [])

    if count is not None:
        # Validate the count
        if count <= 0 or count > len(root_list):
            structured_data.update({
                "error": True,
                "message": f"Requested count {count} is out of range. There are only {len(root_list)} structures."
            })
            return structured_data

        # Set the specific structure by count (adjusting for 1-based indexing)
        structured_data["value"] = root_list[count - 1]
    else:
        # If no count is provided, set the entire 'processed_value'
        structured_data["value"] = structured_content

    # Set the data_type based on the type of 'value'
    structured_data["data_type"] = type(structured_data["value"]).__name__

    return structured_data


# Asynchronously reads and parses a markdown file
async def read_markdown_file_async(filepath):
    print(f"Attempting to read file at {filepath}")
    structured_data = {
        'signature': 'post_processing',
        "value": None,
        "data_type": "unknown",
        "error": False,
        "message": ""
    }

    async with aiofiles.open(filepath, 'r', encoding='utf-8') as file:
        content = await file.read()

    if not content:
        print(f"ERROR: File at {filepath} is empty or could not be read.")
        structured_data["error"] = True
        structured_data["message"] = "File is empty or could not be read."
        return structured_data

    print(f"File read successfully: {filepath}")
    structured_data["value"] = content
    return await parse_markdown_async(structured_data)


async def save_object_as_text(filepath, obj):
    """Serializes an object to a text file in JSON format."""
    async with aiofiles.open(filepath, 'w', encoding='utf-8') as file:
        await file.write(json.dumps(obj, indent=2))


async def load_text_as_object(filepath):
    """Deserializes a text file containing JSON back into an object."""
    async with aiofiles.open(filepath, 'r', encoding='utf-8') as file:
        content = await file.read()
    return json.loads(content)


# Main function to demonstrate async file reading and parsing
async def main_async():
    filepath = r'D:\OneDrive\dev\PycharmProjects\aidream\a_sample\matrix_steps\response_handling\sample_text.txt'
    use_serialized_object = True  # Toggle this to switch between plain text or serialized object

    if use_serialized_object:
        # Load the serialized object from the text file and process it
        structured_data = await load_text_as_object(filepath)
        processed_results_object = await parse_markdown_async(structured_data)
    else:
        # Process the file content as plain text
        processed_results_object = await read_markdown_file_async(filepath)

    # Print results based on the processing
    if processed_results_object.get("error"):
        print("Error occurred:", processed_results_object.get("message"))
    else:
        print(json.dumps(processed_results_object.get("processed_value", {}), indent=2))

async def get_structure_from_file(filepath, count=None):

    async with aiofiles.open(filepath, 'r', encoding='utf-8') as file:
        content = await file.read()

    final_result = await extract_by_level_from_markdown(content, count)
    print(final_result['value'])

    return



if __name__ == "__main__":
    filepath = r'D:\OneDrive\dev\PycharmProjects\aidream\a_sample\matrix_steps\response_handling\sample_text.txt'
    #asyncio.run(main_async(filepath=filepath))

    asyncio.run(get_structure_from_file(filepath=filepath, count=2))

    #asyncio.run(main_async())




