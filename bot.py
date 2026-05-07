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
    script = "Free Fire V-Badge journey day 1. Subscribe Uzumaki-FF for more viral clips! 🔥"
    if GEMINI_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
            payload = {"contents": [{"parts":[{"text": "Write 1 viral Free Fire Hindi status line."}]}]}
            res = requests.post(url, json=payload, timeout=10).json()
            script = res['candidates'][0]['content']['parts'][0]['text']
        except: pass

    # Voice generation
    communicate = edge_tts.Communicate(script, "hi-IN-MadhurNeural")
    await communicate.save("voice.mp3")

    # Fast Image Generation
    img_url = f"https://pollinations.ai/p/free_fire_gaming_boy_v_badge?width=720&height=1280&seed={datetime.datetime.now().second}"
    with open("thumbnail.jpg", "wb") as f:
        f.write(requests.get(img_url).content)
    return script

def create_video(is_short=True):
    print("🚀 Fast Encoding Started...")
    size = "720:1280" if is_short else "1280:720"
    # '-preset ultrafast' is the key here for speed
    cmd = f"ffmpeg -loop 1 -i thumbnail.jpg -i voice.mp3 -c:v libx264 -preset ultrafast -t 10 -pix_fmt yuv420p -vf 'scale={size}' video.mp4 -y"
    subprocess.run(cmd, shell=True)

def upload_to_youtube(title, description, is_short=True):
    try:
        youtube = get_youtube_client()
        request_body = {
            'snippet': {'title': title + " #Shorts", 'description': description, 'categoryId': '20'},
            'status': {'privacyStatus': 'public'}
        }
        media = MediaFileUpload('video.mp4', mimetype='video/mp4', resumable=True)
        youtube.videos().insert(part='snippet,status', body=request_body, media_body=media).execute()
        print("✅ UPLOAD SUCCESSFUL!")
    except Exception as e: print(f"Error: {e}")

def main():
    today = datetime.datetime.now().strftime('%A')
    script = asyncio.run(generate_assets())
    create_video(is_short=(today not in ['Sunday', 'Monday']))
    upload_to_youtube("Free Fire Viral", script)

if __name__ == "__main__":
    main()
        
