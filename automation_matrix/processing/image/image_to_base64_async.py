import base64
import aiohttp
from PIL import Image
from io import BytesIO
import asyncio
import firebase_admin
from firebase_admin import credentials, storage
from google.cloud import storage as gcs_storage  # For accessing Google Cloud Storage


async def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


async def handle_url_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise ValueError(f"Failed to fetch image from URL: {url}, Status: {response.status}")
            content = await response.read()
    image = Image.open(BytesIO(content))
    return await convert_image_to_base64(image)


async def handle_local_image(file_path):
    try:
        with Image.open(file_path) as image:
            return await convert_image_to_base64(image)
    except IOError as e:
        raise ValueError(f"Failed to process local image: {e}")


def parse_firebase_storage_url(storage_url):
    path = storage_url[5:]  # Remove 'gs://' prefix
    bucket_name, file_path = path.split('/', 1)
    return bucket_name, file_path


async def handle_firestore_image(storage_url):
    try:
        bucket_name, file_path = parse_firebase_storage_url(storage_url)
        # Initialize Google Cloud Storage client synchronously
        client = gcs_storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        # Download the blob as bytes synchronously
        image_bytes = await asyncio.get_event_loop().run_in_executor(None, blob.download_as_bytes)
        image = Image.open(BytesIO(image_bytes))
        return await convert_image_to_base64(image)
    except Exception as e:
        raise ValueError(f"Failed to process Firestore image: {e}")


async def convert_image_source_to_base64_async(image_source: str) -> str:
    """
    Converts an image from a URL, Firestore path, or local path to a Base64 string.

    Args:
        image_source (str): The source of the image. It can be a URL (http...), a Firestore path (gs://), or a local file path.

    Returns:
        str: A Base64-encoded string of the image if successful, or an error message.
    """
    try:
        if image_source.startswith("http"):
            image_base64 = await handle_url_image(image_source)
        elif image_source.startswith("gs://"):
            image_base64 = await handle_firestore_image(image_source)
        else:
            image_base64 = await handle_local_image(image_source)
        return image_base64
    except ValueError as e:
        # Handle specific errors raised in the processing functions
        return str(e)
    except Exception as e:
        # Catch-all for any unexpected errors
        return f"An error occurred while processing the image: {e}"


async def main():
    image_source = "gs://ai-matrix-engine.appspot.com/resizeImage/Arman-Sadeghi-Titanium-Success-215x300.jpg/Arman-Sadeghi-Titanium-Success-215x300_600x600.webp"
    base64_string = await convert_image_source_to_base64_async(image_source)
    print(base64_string)


if __name__ == "__main__":
    asyncio.run(main())
