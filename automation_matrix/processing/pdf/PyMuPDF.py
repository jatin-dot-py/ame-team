import asyncio
import aiohttp
from aiofiles import open as aioopen
import fitz  # Ensure PyMuPDF is installed
import os

from common import print_link
# from google_integrations.cloud_storage.storage_manager import upload_content_to_bucket
from aiomultiprocess import Pool  # Ensure aiomultiprocess is installed
import urllib.parse

output_dir = "text_output"
os.makedirs(output_dir, exist_ok=True)


async def fetch_or_load_pdf(path_or_url):
    if urllib.parse.urlparse(path_or_url).scheme in ('http', 'https'):
        return await download_pdf(path_or_url)
    elif os.path.isfile(path_or_url):
        return path_or_url.replace('\\', '/')  # Ensure path uses forward slashes
    else:
        print(f"File does not exist: {path_or_url}")
        return None


async def download_pdf(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                filename = os.path.basename(urllib.parse.urlparse(url).path)
                filepath = os.path.join(output_dir, filename).replace('\\', '/')
                async with aioopen(filepath, 'wb') as file:
                    await file.write(await response.read())
                return filepath
            else:
                print(f"Failed to download {url}")
                return None


async def extract_text(filepath):
    try:
        doc = fitz.open(filepath)
        text = "".join(page.get_text() for page in doc)
        doc.close()
        return text
    except Exception as e:
        print(f"Error extracting text from {filepath}: {e}")
        return ""


async def save_to_file(content, filename):
    async with aioopen(filename, 'w', encoding='utf-8') as file:
        await file.write(content)


def upload_to_firebase(filepath):
    filepath = filepath.replace('\\', '/')  # Ensure filepath uses forward slashes
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as file:
        # upload_content_to_bucket(file, "ai-matrix-engine-text", f"text_output/{filename}", content_type='text/plain')
        print("disabled for now")
        pass


async def process_pdf(args):
    filepath, use_text, _ = args  # Ignore use_tables as it's not used anymore
    if use_text:
        text = await extract_text(filepath)
        text_filename = f"{output_dir}/{os.path.splitext(os.path.basename(filepath))[0]}_text.txt"
        print_link(text_filename)
        await save_to_file(text, text_filename)
        upload_to_firebase(text_filename)
        return text


async def process_pdf_save_and_return_text(paths_or_urls, use_text=True):
    tasks = [fetch_or_load_pdf(path_or_url) for path_or_url in paths_or_urls]
    filepaths = await asyncio.gather(*tasks)

    process_tasks = [(path, use_text, False) for path in filepaths if path]  # False for use_tables, which is now irrelevant

    async with Pool() as pool:
        text = await pool.map(process_pdf, process_tasks)

    return text


if __name__ == "__main__":
    paths_or_urls = [
        r"D:\a_starter\ama\Book pdf\ama_legal_book.pdf",
        # Add more paths or URLs here
    ]
    text = asyncio.run(process_pdf_save_and_return_text(paths_or_urls, use_text=True))

# vasaro account: https://chat.openai.com/share/e/5ec5788d-8151-4c7e-ab1e-68d84a80b79f
