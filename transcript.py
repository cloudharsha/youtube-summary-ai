import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, VideoUnavailable


def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def get_transcript(url):
    """Fetch transcript for a YouTube video."""
    video_id = extract_video_id(url)

    if not video_id:
        raise ValueError("Invalid YouTube URL")

    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)

        # Combine transcript segments into a single text
        text = ' '.join([segment['text'] for segment in transcript])

        # Limit transcript size (roughly 100k characters)
        max_length = 100000
        if len(text) > max_length:
            text = text[:max_length] + "..."

        return text, video_id

    except NoTranscriptFound:
        raise ValueError("No transcript available for this video")
    except VideoUnavailable:
        raise ValueError("Video is unavailable")
    except Exception as e:
        raise ValueError(f"Error fetching transcript: {str(e)}")
