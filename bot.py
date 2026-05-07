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
    script = "Dosto, aaj hum Free Fire mein V-Badge ki journey shuru kar rahe hain. Subscribe karein Uzumaki-FF ko trending gameplay ke liye!"
    
    # Try Gemini
    if GEMINI_KEY:
        try:
            print("Fetching script from Gemini...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
            prompt = "Write a 1 line viral Free Fire Hindi status for YouTube Shorts."
            payload = {"contents": [{"parts":[{"text": prompt}]}]}
            res = requests.post(url, json=payload, timeout=10).json()
            if 'candidates' in res:
                script = res['candidates'][0]['content']['parts'][0]['text']
                print("✅ AI Script generated!")
        except Exception as e:
            print(f"Gemini failed: {e}, using backup script.")

    # 2. Voice-over banana
    print("Generating voice-over...")
    communicate = edge_tts.Communicate(script, "hi-IN-MadhurNeural")
    await communicate.save("voice.mp3")

    # 3. Image Generation
    print("Generating image...")
    img_url = f"https://pollinations.ai/p/free_fire_pro_player_neon_v_badge?width=1080&height=1920&seed={datetime.datetime.now().second}"
    with open("thumbnail.jpg", "wb") as f:
        f.write(requests.get(img_url).content)
    
    return script

def create_video(is_short=True):
    print("Encoding video with FFMPEG...")
    size = "1080:1920" if is_short else "1920:1080"
    # Simple FFMPEG command to merge image and audio
    cmd = f"ffmpeg -loop 1 -i thumbnail.jpg -i voice.mp3 -c:v libx264 -t 15 -pix_fmt yuv420p -vf 'scale={size}' video.mp4 -y"
    subprocess.run(cmd, shell=True)

def upload_to_youtube(title, description, is_short=True):
    try:
        youtube = get_youtube_client()
        request_body = {
            'snippet': {
                'title': title + (" #Shorts #FreeFire" if is_short else ""),
                'description': description,
                'categoryId': '20'
            },
            'status': {'privacyStatus': 'public'}
        }
        media = MediaFileUpload('video.mp4', mimetype='video/mp4', resumable=True)
        youtube.videos().insert(part='snippet,status', body=request_body, media_body=media).execute()
        print("🚀 YOUTUBE UPLOAD SUCCESSFUL!")
    except Exception as e:
        print(f"❌ Upload failed: {e}")

def main():
    today = datetime.datetime.now().strftime('%A')
    print(f"--- Process Started for {today} ---")
    
    script = asyncio.run(generate_assets())
    
    # Sunday aur Monday Full Video, Baaki din Shorts
    is_short_video = today not in ['Sunday', 'Monday']
    
    create_video(is_short=is_short_video)
    
    title = "Free Fire V-Badge Journey" if not is_short_video else "FF Viral Shorts"
    upload_to_youtube(title, script, is_short=is_short_video)

if __name__ == "__main__":
    main()
    
