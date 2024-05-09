import os
import yt_dlp
import asyncio
import re
import uuid
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import shutil
from common import pretty_print
from ame_team.settings.base import BASE_DIR
AUDIO_EXT = 'flac'


class VideoProcessor:
    def __init__(self):
        self.output_parent_dir = BASE_DIR / "temp/videos"
        self.date_str = datetime.now().strftime("%y%m%d-%H%M")
        self.url = None
        self.full_results = {}
        self.video_id = None
        self.title = None
        self.output_path = None
        self.channel_id = None
        self.description = None
        self.channel_url = None
        self.duration = None
        self.view_count = None
        self.webpage_url = None
        self.base_filename = None
        self.audio_file_path = None
        self.extracted_info = {}
        self.return_params = {}
        self.cleaned_text = ""
        self.text_output_link = ""
        self.debug_save = None
        self.unique_id = uuid.uuid4()


    def process_and_return(self, url, return_params=None):
        self.return_params = return_params or {}
        self.url = url

        success = self.process()

        if success:
            keys_to_extract = ['id', 'title', 'thumbnail', 'description', 'channel_id', 'channel_url', 'channel', 'channel_follower_count', 'duration', 'view_count', 'webpage_url',
                                'comment_count', 'upload_date', 'playlist', 'playlist_index', 'tags', 'categories']
            self.extracted_info = {key: self.full_results.get(key, '') for key in keys_to_extract}

            if not self.cleaned_text:
                self.cleaned_text = "No subtitles found for this video."
                self.text_output_link = None
                self.debug_save = self.full_results

            response = {
                'signature': 'YouTubeProcessorResponse',
                "ame_id": self.unique_id,
                'status': "completed",  # completed, partial, failed
                "variable_name": self.return_params.get('variable_name', 'VIDEO_RESULTS_AUTO_1001'),
                'value': self.extracted_info,
                'processed_values': {
                    'directory': self.output_path,
                    'subtitles': self.cleaned_text,
                    'audio': self.audio_file_path,
                    'text': self.text_output_link,
                }
            }
            if self.debug_save is not None:
                response['processed_values']['debug_save'] = self.debug_save
                response['status'] = "partial"

        else:
            response = {
                'signature': 'YouTubeProcessorResponse',
                'processing': "failed",
                "variable_name": "",
                'value': "",
                'processed_values': {}
            }
        return response


    def process(self, url=None):
        self.url = url or self.url
        unique_id = uuid.uuid4()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        temp_output_path = self.output_parent_dir / f"temp_{unique_id}_{timestamp}"
        temp_filename = "temp"

        ydl_opts = {
            'outtmpl': {
                'default': str(temp_output_path / f"{temp_filename}.%(ext)s"),
                'audio': str(temp_output_path / f"{temp_filename}_audio.%(ext)s"),
            },
            'format': 'bestvideo+bestaudio/best',
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en', 'es', 'fr'],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'flac',
                'nopostoverwrites': False,
            }],
            'keepvideo': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                temp_output_path.mkdir(parents=True, exist_ok=True)

                self.full_results = ydl.extract_info(self.url, download=True)
                self.video_id = self.full_results.get('id')
                self.title = self.sanitize_filename(self.full_results.get('title'))
                self.channel_id = self.full_results.get('channel_id', "no_channel")

                self.base_filename = f"{self.video_id}_{self.title[:65]}"
                self.output_path = self.output_parent_dir / self.channel_id / self.base_filename
                self.output_path.mkdir(parents=True, exist_ok=True)

                temp_debug_path = self.output_parent_dir / "temp_debug"
                shutil.copytree(temp_output_path, temp_debug_path, dirs_exist_ok=True)

                if 'requested_subtitles' in self.full_results and self.full_results['requested_subtitles']:
                    subtitle_info = self.full_results['requested_subtitles'].get('en')
                    if subtitle_info:
                        subtitle_file = subtitle_info.get('filepath')
                        if subtitle_file:
                            self.clean_subtitles_to_paragraphs(subtitle_file)

                for temp_file in temp_output_path.iterdir():
                    extension = temp_file.suffix
                    original_name = temp_file.stem.replace("temp", "")

                    if extension == '.flac':
                        self.audio_file_path = self.output_path / f"{self.base_filename}{extension}"

                    final_name = f"{self.base_filename}{original_name}{extension}"
                    final_path = self.output_path / final_name

                    shutil.move(str(temp_file), str(final_path))

                shutil.rmtree(str(temp_output_path))

                return self.audio_file_path

            except Exception as e:
                print(f"Error during processing: {e}")

            finally:
                if temp_output_path.exists():
                    shutil.rmtree(str(temp_output_path))

    def sanitize_filename(self, title):
        """Sanitize the title to be used as a valid filename."""
        title = title.replace(' ', '_')
        title = re.sub(r'[^a-zA-Z0-9_]', '', title)
        return title

    def clean_subtitles_to_paragraphs(self, subtitle_file_path, max_paragraph_length=750):
        with open(subtitle_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if "Language:" in line:
                lines = lines[i + 1:]
                break

        self.cleaned_text = ""
        paragraph_text = ""
        previous_line = None

        for line in lines:
            if '-->' in line or any(c in line for c in '<>/') or line.strip().isdigit():
                continue
            if line.strip() and line.strip() != previous_line:
                cleaned_line = line.strip() + ' '
                self.cleaned_text += cleaned_line
                paragraph_text += cleaned_line
                previous_line = line.strip()

        paragraphs = []
        while len(paragraph_text) > max_paragraph_length:
            split_index = paragraph_text.rfind('.', 0, max_paragraph_length) + 1
            if split_index <= 0:
                split_index = paragraph_text.rfind(' ', 0, max_paragraph_length)
                if split_index <= 0:
                    split_index = max_paragraph_length
            paragraphs.append(paragraph_text[:split_index].strip())
            paragraph_text = paragraph_text[split_index:].strip()

        if paragraph_text:
            paragraphs.append(paragraph_text)

        self.text_output_link = os.path.join(self.output_path, self.base_filename + '_text.txt')
        self.text_output_link = os.path.normpath(self.text_output_link)

        with open(self.text_output_link, 'w', encoding='utf-8') as file:
            for paragraph in paragraphs:
                file.write(paragraph + '\n\n')

        print(f"Full text and paragraphs saved to: {self.text_output_link}")


async def process_single_download(url):
    processor = VideoProcessor()
    video_processor_dict = processor.process_and_return(url)

    return video_processor_dict

async def process_batch_download(urls):
    tasks = [process_single_download(url) for url in urls]
    video_processor_dicts = await asyncio.gather(*tasks)

    return video_processor_dicts



async def process_youtube_video(video_url: str, return_params: dict = None) -> dict:
    """
    Asynchronously processes an online video for various outputs such as video, audio, and text.
        Tested for YouTube, Vimeo and TikTok, but likely to work for X and other public content platforms as well. (Not IG)

    Args:
        video_url (str): The URL of the YouTube video to process.

        return_params (dict): Optional parameters affecting processing outcomes like saving video/audio/text and obtaining high-quality transcript.
            RETURN PARAMS NOT CURRENTLY SET UP AND WORKING SO IT ALWAYS RETURNS ALL, BUT NO HQ TRANSCRIPT
            {
                'variable_name': 'special_variable_name'
                'save_video': True,
                'save_audio': True,
                'save_text': True,
                'get_hq_transcript': True, # NOT SET UP!
            }

    Returns:
        dict: A dictionary with key information about the processing state and outcome. Contains 'signature', 'processing' status,
              'variable_name', 'value', and 'processed_values' keys detailing processing results and links to processed outputs.
                {
                    'signature': 'YouTubeProcessorResponse',
                    'processing': True,
                    "variable_name": self.return_params.get('variable_name', ''),
                    'value': self.cleaned_text,
                    'processed_values': {
                        'video': self.video_output_link,
                        'audio': self.audio_output_link,
                        'text': self.text_output_link,
                    }
                }
    """

    return_params = return_params if return_params is not None else {}

    processor = VideoProcessor()

    loop = asyncio.get_running_loop()
    processed_video_audio_and_text = await loop.run_in_executor(None, processor.process_and_return, video_url, return_params)

    pretty_print_data(processed_video_audio_and_text)

    return processed_video_audio_and_text

async def process_video_with_semaphore(semaphore, video_url, return_params):
    """
    A helper coroutine that uses a semaphore to limit the number of concurrent video processing tasks.
    """

    async with semaphore:
        try:
            return await process_youtube_video(video_url, return_params)
        except Exception as e:
            # If an error occurs, return a dictionary indicating failure for this URL
            return {
                'url': video_url,
                'error': str(e),
                'status': 'failed'
            }

async def process_batch_videos(video_urls: list, return_params: dict = None) -> list:
    """
    Asynchronously processes a batch of video URLs concurrently, up to 10 at a time.

    Args:
        video_urls (list): A list of video URLs to process.
        return_params (dict): Optional parameters affecting processing outcomes for each video.

    Returns:
        list: A list of dictionaries, each representing the result of processing for a video URL.
    """

    semaphore = asyncio.Semaphore(10)
    tasks = [process_video_with_semaphore(semaphore, url, return_params) for url in video_urls]
    results_dict = await asyncio.gather(*tasks, return_exceptions=True)

    return results_dict


if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=EaMHGdATLuY"
    return_params = {'variable_name': 'special_variable_name'}

    urls = [
        "https://www.youtube.com/watch?v=IeN05lD9p98",
        #"https://www.youtube.com/watch?v=vL-RlVSQgsk",
        #"https://www.youtube.com/watch?v=3lKbUHUBLvU",
        #"https://www.youtube.com/watch?v=zu6QJEC78jw",
    ]


    #processed_video_audio_and_text = asyncio.run(process_youtube_video(video_url, return_params))

    processed_video_audio_and_text_batch = asyncio.run(process_batch_videos(urls, return_params))

    pretty_print_data(processed_video_audio_and_text_batch)


"""
For rate limits:
Rate Limiting and IP Exposure
IP Address Exposure: Yes, when you use yt-dlp to download videos, your IP address is exposed to YouTube because yt-dlp makes requests to YouTube's servers as if you were browsing the site normally. Excessive usage can lead to your IP being temporarily blocked.
Rate Limits: YouTube doesn't publicly disclose specific rate limits, but it's known that they implement rate-limiting mechanisms. If you make too many requests in a short period, you might encounter HTTP 429 errors (Too Many Requests), leading to temporary IP bans.

Best Practices to Avoid Issues
Limit Concurrency: Avoid downloading too many videos simultaneously. You mentioned wanting to run up to 10 concurrent downloads; while this might be okay, closely monitor for any errors or blocks and adjust as necessary.
Respect Retry-After: If you hit a rate limit and receive a 429 error, it often includes a Retry-After header indicating how long to wait before making another request. Ensure your script respects this.
Use Sleep Intervals: Introduce delays between download requests to mimic human interaction patterns more closely. Randomizing these intervals can also be beneficial.
Rotate IPs: If possible, use a rotating proxy or VPN service to change your IP address periodically. This can help avoid rate limits and bans, especially for large-scale operations. However, ensure this aligns with your ethical guidelines and legal considerations.
Set a Custom User-Agent: Changing the default User-Agent of your requests to mimic a regular browser can sometimes help avoid detection, but use this sparingly and responsibly.
Limit Video Quality: Downloading videos in lower quality can reduce the bandwidth and may draw less attention.
Cookies: Using a cookies file (from a logged-in YouTube session) can sometimes help avoid rate limiting, but this should be used carefully and ethically, considering privacy implications.
Avoid Logged-In Actions: Actions like downloading private or age-restricted videos, which require a logged-in session, can be riskier and more likely to trigger blocks or account-related actions.
Comply with YouTube's Terms of Service: It's crucial to adhere to YouTube's terms and policies. Unauthorized downloading of content, especially copyrighted material for which you don't have permission, can lead to legal issues and violations of YouTube's terms.


"""
