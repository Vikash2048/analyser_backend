from googleapiclient.discovery import build

from urllib.parse import urlparse, parse_qs
import re
from datetime import datetime
from html import unescape
import os

from dotenv import load_dotenv
load_dotenv()

# YouTube API setup
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.getenv("API_KEY")  # Replace YOUR_API_KEY with your actual YouTube Data API key.
youtube = build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

def get_video_id(url):
    """Extract the video ID from a YouTube URL."""
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    elif parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        query_params = parse_qs(parsed_url.query)
        return query_params.get('v', [None])[0]
    return None

def parse_duration(duration):
    """Parse ISO 8601 duration format to a more readable form."""
    pattern = re.compile(r'P(?:(\d+)D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    days, hours, minutes, seconds = pattern.match(duration).groups()
    duration_str = " ".join(f"{value} {unit}" for value, unit in zip(
        [days, hours, minutes, seconds], ['days', 'hours', 'minutes', 'seconds']) if value)
    return duration_str.strip()

def format_datetime(date_str):
    """Format the ISO 8601 date string into a more readable date format."""
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d %Y, %I:%M %p")

def fetch_video_details(url):
    """Fetch details of a YouTube video using the YouTube Data API."""
    video_id = get_video_id(url)
    if not video_id:
        return "Invalid YouTube URL or Video ID not found."
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()
    if not response['items']:
        return "No details found for the video."
    video = response['items'][0]
    snippet, content_details, statistics = video['snippet'], video['contentDetails'], video['statistics']
    video_details = {
        "URL": url,
        "Title": snippet['title'],
        "Channel": snippet['channelTitle'],
        "Resolution": content_details.get('definition', 'N/A').upper() + 'D',
        "Language": snippet.get('defaultAudioLanguage', 'Unknown'),
        "Duration": parse_duration(content_details['duration']),
        "Views": statistics['viewCount'],
        "Likes": statistics.get('likeCount', '0'),
        "Comments": statistics.get('commentCount', '0'),
        "Upload Date": format_datetime(snippet['publishedAt'])
    }
    return video_details

def fetch_all_comments(url):
    """Retrieve all comments from a YouTube video."""
    video_id = get_video_id(url)
    if not video_id:
        return "Invalid YouTube URL or Video ID not found."
    comments = []
    next_page_token = None
    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['updatedAt'],
                comment['likeCount'],
                comment['textDisplay']
            ])
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    return comments
