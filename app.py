from flask import Flask, render_template, request, jsonify
import regex as re
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/get_subtitles', methods=['POST'])
def get_subtitles():
    data = request.get_json()
    bv_number = data.get('bv_number', '')

    # Regular expression to match Bilibili video link pattern
    bilibili_pattern = r'^https?://(?:www\.)?bilibili\.com/video/(?:av|BV)(\w+)'

    match = re.match(bilibili_pattern, bv_number)
    if match:
        bv_number = match.group(1)
        video_data = get_video_data(bv_number)

        if video_data:
            aid = video_data['data']['aid']
            cid = video_data['data']['cid']
            player_data = get_player_data(aid, cid)

            if player_data:
                subtitle_url = player_data['data']['subtitle']['subtitles'][0]['subtitle_url']
                subtitle_url = 'https:' + subtitle_url
                response = requests.get(subtitle_url)

                if response.status_code == 200:
                    subtitles_data = response.json()
                    subtitles_list = [
                        {
                            'from': item['from'],
                            'to': item['to'],
                            'content': item['content']
                        }
                        for item in subtitles_data['body']
                    ]
                    return jsonify(valid=True, subtitles=subtitles_list)
                
                else:
                    return jsonify(valid=False, error='Failed to fetch subtitles.')
            else:
                return jsonify(valid=False, error='Failed to fetch player data.')
        else:
            return jsonify(valid=False, error='Failed to fetch video data.')
    else:
        return jsonify(valid=False, error='Invalid link. Please enter a valid Bilibili video link.')

# @app.route('/')
# def get_api_content():
#     api_url = "https://api.bilibili.com/x/player/v2?aid=573502486&cid=1199820711"
    
#     headers = {
#         'Accept': 'application/json',
#         'Content-Type': 'application/json',
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
#         'Host': 'api.bilibili.com',
#         'Cookie': f"SESSDATA={os.getenv('SESSDATA')}",
#     }
    
#     response = requests.get(api_url, headers=headers)

#     if response.status_code == 200:
#         return jsonify(response.json())
#     else:
#         return "Error: Unable to fetch data from the API."
    
if __name__ == '__main__':
    app.run(debug=True)