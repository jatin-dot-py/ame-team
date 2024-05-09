import os
import cv2
from moviepy.editor import VideoFileClip


def format_size(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0


def estimate_new_size(bitrate, duration):
    bitrate_kbps = int(bitrate[:-1]) if bitrate[-1].lower() == 'k' else int(bitrate[:-1]) * 1000
    estimated_size_bytes = (bitrate_kbps * 1000 * duration) / 8  # Convert from kilobits to bytes
    return format_size(estimated_size_bytes)


def resize_frame(frame, newsize):
    height, width = frame.shape[:2]
    original_aspect_ratio = width / height

    # Calculate new dimensions while preserving aspect ratio
    if width > height:  # Landscape orientation
        new_width = newsize[0]
        new_height = int(new_width / original_aspect_ratio)
    else:  # Portrait orientation
        new_height = newsize[1]
        new_width = int(new_height * original_aspect_ratio)

    return cv2.resize(frame, (new_width, new_height))


def compress_video(input_path, codec='libx264', bitrate='1000k', resolution=(1920, 1080), fps=30, preset='ultrafast',
                   audio_bitrate='128k'):
    """
    Compresses an MP4 video file with various settings.

    :param input_path: Path to the input video file
    :param codec: Video codec to use for compression
    :param bitrate: Bit rate for video compression
    :param resolution: New resolution for video (width, height) tuple
    :param fps: New frames per second for video
    :param preset: Compression speed/quality trade-off (slower presets give better compression)
    :param audio_bitrate: Bit rate for audio compression
    """
    # Ensure the input path is in a valid format
    input_path = os.path.abspath(input_path)

    # Load video clip
    clip = VideoFileClip(input_path)

    # Apply settings
    if resolution:
        clip = clip.fl_image(lambda frame: resize_frame(frame, resolution))
    if fps:
        clip = clip.set_fps(fps)

    # Construct output file path
    directory, filename = os.path.split(input_path)
    name, ext = os.path.splitext(filename)
    settings = f"{codec}_{bitrate}_{resolution[0]}x{resolution[1]}_{fps}fps_{preset}_{audio_bitrate}bit"
    output_path = os.path.join(directory, f"{name}-compressed_{settings}{ext}")

    # Compress video
    clip.write_videofile(output_path, codec=codec, bitrate=bitrate, preset=preset, audio_bitrate=audio_bitrate)

    print(f"Video compressed and saved to {output_path}")


if __name__ == "__main__":
    input_video_path = input("Enter the path to the video file: ").strip().strip('"')
    input_video_path = os.path.abspath(input_video_path)

    # Analyze original video
    clip = VideoFileClip(input_video_path)
    original_size = os.path.getsize(input_video_path)
    print(f"Current Size: {format_size(original_size)}")

    # Estimate new size with default settings
    estimated_size = estimate_new_size('1000k', clip.duration)
    print(f"Estimated New Size with Default Settings: {estimated_size} --> Proceed? [Y/n]")

    proceed = input().strip().lower()
    if proceed != 'n':
        compress_video(input_video_path)
    else:
        # Get custom settings from user
        codec = input("Enter video codec [default: libx264]: ").strip() or "libx264"
        bitrate = input("Enter video bitrate [default: 1000k]: ").strip() or "1000k"
        resolution_input = input("Enter video resolution as width x height [default: 1920x1080]: ").strip()
        resolution = tuple(map(int, resolution_input.split('x'))) if 'x' in resolution_input else (1920, 1080)
        fps = int(input("Enter frames per second [default: 30]: ").strip() or "30")
        preset = input("Enter compression preset [default: ultrafast]: ").strip() or "ultrafast"
        audio_bitrate = input("Enter audio bitrate [default: 128k]: ").strip() or "128k"

        # Estimate new size with custom settings
        estimated_size = estimate_new_size(bitrate, clip.duration)
        print(f"Estimated New Size with Custom Settings: {estimated_size} --> Proceed? [Y/n]")

        proceed = input().strip().lower()
        if proceed != 'n':
            compress_video(input_video_path, codec, bitrate, resolution, fps, preset, audio_bitrate)
