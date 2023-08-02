from flask import Flask, render_template, request, jsonify

from bilibili_helper import get_video_info
from openai_helper import get_openAI_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def get_answer():
    # Get input data from the request
    data = request.get_json()
    video_url = data.get('video_url', '')

    video_info = get_video_info(video_url)

    if video_info is None:
        return jsonify(valid=False, error="video has no subtitles")

    # response = get_openAI_response(video_info)
    response = video_info

    return jsonify(valid=True, response=response)
    

if __name__ == '__main__':
    app.run(debug=True)