import os
import ffmpeg
from video_compression_2 import format_size


# Not that great yet, but I think we can get it there.

def analyze_video(input_path):
    try:
        probe = ffmpeg.probe(input_path)
        video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
        audio_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']

        if not video_streams:
            raise Exception("No video stream found")

        video_stream = video_streams[0]

        bitrate = int(video_stream['bit_rate']) if 'bit_rate' in video_stream else None
        duration = float(video_stream['duration']) if 'duration' in video_stream else None

        return {
            'bitrate': bitrate,
            'duration': duration,
            'video_streams': video_streams,
            'audio_streams': audio_streams
        }
    except ffmpeg.Error as e:
        print('Error:', e)
        return None


def estimate_file_size(video_info, new_bitrate=None):
    if new_bitrate is None:
        new_bitrate = video_info['bitrate']

    if new_bitrate is None or video_info['duration'] is None:
        return "Cannot estimate size without bitrate and duration"

    estimated_size_bytes = (new_bitrate * video_info['duration']) / 8  # Convert from bits to bytes
    return format_size(estimated_size_bytes)


if __name__ == "__main__":
    input_video_path = input("Enter the path to the video file: ").strip().strip('"')
    input_video_path = os.path.abspath(input_video_path)

    video_info = analyze_video(input_video_path)

    if video_info:
        print("Video Information:")
        print("Bitrate:", video_info['bitrate'], "bps")
        print("Duration:", video_info['duration'], "seconds")

        estimated_size = estimate_file_size(video_info)
        print("Estimated Current Size:", estimated_size)
