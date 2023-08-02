from flask import request, jsonify
import regex as re
import requests
from dotenv import load_dotenv
import os


def get_video_data(bv_number):
    api_url = f'https://api.bilibili.com/x/web-interface/view?bvid={bv_number}'
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_player_data(aid, cid):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Host': 'api.bilibili.com',
        'Cookie': f"SESSDATA={os.getenv('SESSDATA')}",
    }
    api_url = f'https://api.bilibili.com/x/player/v2?aid={aid}&cid={cid}'
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_video_info(video_url):
    # Regular expression to match Bilibili video link pattern
    bilibili_pattern = r'^https?://(?:www\.)?bilibili\.com/video/(?:av|BV)(\w+)'

    # Check if the input matches the Bilibili video link pattern
    match = re.match(bilibili_pattern, video_url)
    if not match:
        return None

    # Extract the Bilibili video ID from the input
    bv_id = match.group(1)

    # Fetch video data using the Bilibili video ID
    video_data = get_video_data(bv_id)
    if not video_data:
        return None

    # Extract necessary data from the video data
    title = video_data['data']['title']
    desc = video_data['data']['desc']
    aid = video_data['data']['aid']
    cid = video_data['data']['cid']

    # Fetch player data using the video data
    player_data = get_player_data(aid, cid)
    if not player_data:
        return None

    # Check if the video has subtitle
    subtitles_data = player_data['data']['subtitle']['subtitles']
    if len(subtitles_data) == 0:
        return None

    # Extract the subtitle URL from the player data
    subtitle_url = subtitles_data[0]['subtitle_url']
    if not subtitle_url:
        return None

    # Complete the subtitle URL and fetch the subtitles
    subtitle_url = 'https:' + subtitle_url
    response = requests.get(subtitle_url)

    # Check if the subtitle request was successful
    if response.status_code != 200:
        return None 
    
    # Process the subtitles data and prepare the response
    subtitles_data = response.json()
    subtitles_list = [
        {
            'timestamp': item['from'],
            'text': item['content']
        }
        for item in subtitles_data['body']
    ]

    video_info = {
            'title': title,
            'description': desc,
            'subtitles': subtitles_list
    }

    return video_info