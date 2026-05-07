import os
import datetime
import requests
import asyncio
import edge_tts
import subprocess
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

# Keys from GitHub Secrets
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def get_youtube_client():
    creds = Credentials(
        None, refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
    )
    return build("youtube", "v3", credentials=creds)

def get_viral_content():
    prompt = "Write a 1-line viral Free Fire Hindi status for YouTube Shorts about V-Badge journey. Use hashtags."
    if OPENROUTER_KEY:
        try:
            print("Trying OpenRouter (gpt-oss-120b)...")
            res = requests.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
                json={"model": "openai/gpt-oss-120b:free", "messages": [{"role": "user", "content": prompt}]}, timeout=15).json()
            return res['choices'][0]['message']['content']
        except: pass
    return "V-Badge journey day 1: Har har nahi manunga! 🔥 #FreeFire #VBadge"

async def generate_assets():
    script = get_viral_content()
    print(f"Final Script: {script}")

    # Voice generation - Fixed spelling and added fallback
    try:
        communicate = edge_tts.Communicate(script, "hi-IN-MadhurNeural")
        await communicate.save("voice.mp3")
    except:
        communicate = edge_tts.Communicate(script, "hi-IN-SwaraNeural")
        await communicate.save("voice.mp3")

    # Fast Image Generation
    img_url = f"https://pollinations.ai/p/free_fire_gaming_pro_v_badge_neon?width=720&height=1280&seed={datetime.datetime.now().second}"
    with open("thumbnail.jpg", "wb") as f:
        f.write(requests.get(img_url).content)
    return script

def create_video(is_short=True):
    print("🚀 Fast Encoding...")
    size = "720:1280" if is_short else "1280:720"
    cmd = f"ffmpeg -loop 1 -i thumbnail.jpg -i voice.mp3 -c:v libx264 -preset ultrafast -t 12 -pix_fmt yuv420p -vf 'scale={size}' video.mp4 -y"
    subprocess.run(cmd, shell=True)

def upload_to_youtube(title, description, is_short=True):
    try:
        youtube = get_youtube_client()
        request_body = {
            'snippet': {'title': title + (" #Shorts" if is_short else ""), 'description': description, 'categoryId': '20'},
            'status': {'privacyStatus': 'public'}
        }
        media = MediaFileUpload('video.mp4', mimetype='video/mp4', resumable=True)
        youtube.videos().insert(part='snippet,status', body=request_body, media_body=media).execute()
        print("✅ YOUTUBE UPLOAD SUCCESSFUL!")
    except Exception as e:
        print(f"❌ Upload Error: {e}")

def main():
    today = datetime.datetime.now().strftime('%A')
    print(f"--- Starting Uzumaki-Bot for {today} ---")
    script = asyncio.run(generate_assets())
    is_short = today not in ['Sunday', 'Monday']
    create_video(is_short=is_short)
    upload_to_youtube("Free Fire Viral Shorts", script, is_short=is_short)

if __name__ == "__main__":
    main()

