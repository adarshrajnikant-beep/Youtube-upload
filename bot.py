import os
import datetime
import requests
import asyncio
import edge_tts
import subprocess
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

# Configuration
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def get_youtube_client():
    creds = Credentials(
        None, refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
    )
    return build("youtube", "v3", credentials=creds)

async def generate_assets():
    # 1. AI se viral script lena
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    prompt = "Write a viral Free Fire Hindi script for a 30s YouTube Short. Focus on V-Badge journey."
    payload = {"contents": [{"parts":[{"text": prompt}]}]}
    res = requests.post(url, json=payload).json()
    script = res['candidates'][0]['content']['parts'][0]['text']

    # 2. Voice-over banana (Hindi Madhur)
    communicate = edge_tts.Communicate(script, "hi-IN-MadhurNeural")
    await communicate.save("voice.mp3")

    # 3. Viral Thumbnail/Background Image
    img_url = f"https://pollinations.ai/p/free_fire_epic_battle_thumbnail_v_badge_glow?width=1280&height=720&seed={datetime.datetime.now().second}"
    with open("thumbnail.jpg", "wb") as f:
        f.write(requests.get(img_url).content)
    
    return script

def create_video(is_short=True):
    # Image aur Audio ko jod kar video banana (FFMPEG)
    size = "1080:1920" if is_short else "1920:1080"
    cmd = f"ffmpeg -loop 1 -i thumbnail.jpg -i voice.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest -vf 'scale={size}' video.mp4 -y"
    subprocess.run(cmd, shell=True)

def upload_to_youtube(title, description, is_short=True):
    youtube = get_youtube_client()
    request_body = {
        'snippet': {
            'title': title + (" #Shorts" if is_short else ""),
            'description': description,
            'categoryId': '20' # Gaming
        },
        'status': {'privacyStatus': 'public'}
    }
    media = MediaFileUpload('video.mp4', chunksize=-1, resumable=True)
    youtube.videos().insert(part='snippet,status', body=request_body, media_body=media).execute()
    print("✅ Upload Successful!")

def main():
    today = datetime.datetime.now().strftime('%A')
    print(f"Starting Uzumaki-Bot for {today}...")
    
    script = asyncio.run(generate_assets())
    
    if today in ['Sunday', 'Monday']:
        print("Creating Full Video...")
        create_video(is_short=False)
        upload_to_youtube("Free Fire V-Badge Special Video", script, is_short=False)
    else:
        print("Creating Shorts Video...")
        create_video(is_short=True)
        upload_to_youtube("Free Fire Viral Shorts", script, is_short=True)

if __name__ == "__main__":
    main()
    
