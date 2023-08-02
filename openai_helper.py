import json
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
prompt = "I would like you to act as a professional video content editor. You will help students summarize the essence of the video in Chinese. Please start by summarizing the whole video in one short sentence (there may be typos in the subtitles, please correct them). Then, please summarize the video subtitles, each subtitle should has the start timestamp (e.g. 12.4 -) so that students can select the video part. Please return in an unordered list format, make sure all sentences are concise, clear, and complete. Good luck!"

messages = [
    {"role": "user", "content": "tell me a interesting fact about physics."}
]

def get_openAI_response(video_info):
    # Convert the JSON object to a JSON-formatted string
    video_info = json.dumps(video_info)
    
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": video_info}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response['choices'][0]['message']['content']