from textbase import bot, Message
from typing import List
from pytube import YouTube
import os
import requests

def save_audio(url):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download()
    base, ext = os.path.splitext(out_file)
    file_name = base + '.mp3'
    os.rename(out_file, file_name)
    print(yt.title + " has been successfully downloaded.")
    print(file_name)
    return yt.title, file_name, yt.thumbnail_url

# def chapter_generation():


@bot()
async def on_message(message_history: List[Message], state: dict = None):

    video_title, save_location, video_thumbnail = await save_audio('https://www.youtube.com/watch?v=Mmt936kgot0')
    print(video_title, save_location, video_thumbnail)

    response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": "DOne"
                }
            ],
            "state": state
        },
        "errors": [
            {
                "message": ""
            }
        ]
    }

    return {
        "status_code": 200,
        "response": response
    }