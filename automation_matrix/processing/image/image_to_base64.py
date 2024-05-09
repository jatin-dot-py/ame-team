import base64
import requests
from PIL import Image
from io import BytesIO
import os
#import firebase_admin
#from firebase_admin import credentials, storage
#from google_integrations.auth.firebase_manager import get_service_account_details


def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode()
    return image_base64

def handle_url_image(url):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        return convert_image_to_base64(image)
    except Exception as e:
        raise ValueError(f"Failed to process URL image: {e}")

def handle_local_image(file_path):
    try:
        with Image.open(file_path) as image:
            return convert_image_to_base64(image)
    except Exception as e:
        raise ValueError(f"Failed to process local image: {e}")

def parse_firebase_storage_url(storage_url):
    path = storage_url[5:]  # Remove 'gs://' prefix
    bucket_name, file_path = path.split('/', 1)
    return bucket_name, file_path

def handle_firestore_image(storage_url):
    try:
        bucket_name, file_path = parse_firebase_storage_url(storage_url)
        bucket = storage.bucket(bucket_name)
        blob = bucket.blob(file_path)
        image_bytes = blob.download_as_bytes()
        image = Image.open(BytesIO(image_bytes))
        return convert_image_to_base64(image)
    except Exception as e:
        raise ValueError(f"Failed to process Firestore image: {e}")

def convert_image_source_to_base64(source: str) -> str:
    """
    Converts an image from a web URL, Firestore URL, or local path to base64 encoded string.

    Args:
        source (str): The source URL or path of the image.

    Returns:
        str: The base64 encoded string representation of the image if successful,
             or an error message detailing any issues encountered during processing.
    """
    try:
        if source.startswith("http"):
            image_base64 = handle_url_image(source)
        elif source.startswith("gs://"):
            image_base64 = handle_firestore_image(source)
        else:
            # Correctly escape backslashes for Windows file paths
            source = source.replace("\\", "\\\\")
            image_base64 = handle_local_image(source)
        return image_base64
    except ValueError as e:
        # Handle specific errors raised in the processing functions
        return str(e)
    except Exception as e:
        # Catch-all for any unexpected errors
        return f"An error occurred while processing the image: {e}"


if __name__ == "__main__":
    # Example usage:
    # source = r"D:\OneDrive\Downloads\Dr. Sheila Nazarian.webp"
    # source = "https://nazarianplasticsurgery.com/wp-content/uploads/2020/05/voluma-juvederm-a.jpg"
    source = "https://cosmeticinjectables.com/wp-content/uploads/2023/12/old-woman-touching-her-skin.jpeg"

    # from  photo_editing.utils_images.image_to_base64 import convert_image_source_to_base64
    # Source can be https, local folder (D:\\files\\image.jpg) or impage bucket address
    base64_string = convert_image_source_to_base64(source)
    print(base64_string)

# https://chat.openai.com/share/e/44f863c6-caee-4de7-9af9-312721d00018



    """
    Convert an image source (URL, local path, or Firebase storage path) to base64.
    There is also an Async version of this function called convert_image_source_to_base64_async.

    This synchronous function serves as the entry point for processing various types of image sources
    for further analysis. It identifies the source type and delegates to the appropriate handler
    (for URL, local, or Firebase storage images). The conversion facilitates the integration of the image
    within a broader analysis model that also processes text, supporting a range of tasks like image tagging,
    recognition, and combined text and image analysis.

    Args:
        source (str): The source of the image, which can be a public URL, a local file path, or a Firebase storage path.

    Returns:
        str: A base64-encoded representation of the image, ready for analysis in conjunction with text or for other
             image-related tasks within the script's broader functional scope.

    Raises:
        ValueError: If the source is not a valid URL, local path, or Firebase storage path.
        IOError: If there is an issue retrieving or reading the image from the specified source.

    """
