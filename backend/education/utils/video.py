import os
import subprocess
import re
from urllib.parse import urlparse
from django.conf import settings


def is_url(path):
    """Check if the path is a URL"""
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except:
        return False


def get_video_duration(video_file_path):
    """
    Get video duration in seconds using ffmpeg
    Supports both local files and remote URLs (S3, cloud storage, etc.)
    Returns duration in seconds or None if unable to determine
    """
    # Check if it's a URL or local file
    if is_url(video_file_path):
        # For URLs
        input_source = video_file_path
    else:
        # For local files
        if not os.path.exists(video_file_path):
            return None
        input_source = video_file_path
    
    try:
        result = subprocess.run(
            ["ffmpeg", "-i", input_source],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=60 
        )
        
        match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", result.stdout)
        if match:
            hours, minutes, seconds = match.groups()
            hours = int(hours)
            minutes = int(minutes)
            seconds = float(seconds)
            total_seconds = hours * 3600 + minutes * 60 + seconds
            return int(total_seconds)
        
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError, OSError):
        pass
    
    return None


def calculate_package_total_duration(package):
    """
    Calculate total duration of all videos in a package
    Supports both local files and cloud storage URLs
    Returns total duration in seconds
    """
    total_duration = 0
    
    for video in package.videos.all():
        if video.video_file:
            video_file_str = str(video.video_file)
            
            # Check if it's a URL (cloud storage) or local file
            if is_url(video_file_str):
                # Direct URL
                video_path = video_file_str
            else:
                # Local file
                video_path = os.path.join(settings.MEDIA_ROOT, video_file_str)
            
            duration = get_video_duration(video_path)
            if duration:
                total_duration += duration
    
    return total_duration
