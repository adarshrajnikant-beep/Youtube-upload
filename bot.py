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
    
    # 1. Try Groq (Fastest)
    if GROQ_KEY:
        try:
            res = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_KEY}"},
                json={"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}]}, timeout=10).json()
            return res['choices'][0]['message']['content']
        except: pass

    # 2. Try OpenRouter (gpt-oss-120b)
    if OPENROUTER_KEY:
        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
                json={"model": "openai/gpt-oss-120b:free", "messages": [{"role": "user", "content": prompt}]}, timeout=10).json()
            return res['choices'][0]['message']['content']
        except: pass

    return "V-Badge journey: Haar nahi manunga, jab tak V-Badge nahi mil jata! 🔥 #FreeFire #VBadge"

async def generate_assets():
    script = get_viral_content()
    print(f"Final Script: {script}")

    # Voice generation with Fallback
    try:
        communicate = edge_tts.Communicate(script, "hi-IN-MadhurNeural")
        await communicate.save("voice.mp3")
    except:
        communicate = edge_tts.Communicate(script, "hi-IN-SwaraNeural")
        await communicate.save("voice.mp3")

    # Ultra-Stable Image Download Logic
    print("Downloading stable image...")
    seed = datetime.datetime.now().second
    # Direct image link to avoid JSON/HTML errors
    img_url = f"https://image.pollinations.ai/prompt/free_fire_epic_neon_gaming_character_v_badge?width=720&height=1280&seed={seed}&nologo=true"
    
    try:
        r = requests.get(img_url, timeout=30)
        if r.status_code == 200 and len(r.content) > 1000:
            with open("thumbnail.jpg", "wb") as f:
                f.write(r.content)
            print("✅ Image Saved!")
        else:
            raise Exception("Bad Image Data")
    except:
        print("Using Emergency Backup Image...")
        backup = "https://images.pexels.com/photos/3165335/pexels-photo-3165335.jpeg?auto=compress&cs=tinysrgb&w=720&h=1280"
        with open("thumbnail.jpg", "wb") as f:
            f.write(requests.get(backup).content)

    return script

def create_video(is_short=True):
    print("🚀 Video Encoding (Bulletproof Mode)...")
    width, height = (720, 1280) if is_short else (1280, 720)
    
    # Fix for 'No JPEG data found' error: force image decoding and fix frame rate
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", "12", 
        "-i", "thumbnail.jpg",
        "-i", "voice.mp3",
        "-c:v", "libx264", "-preset", "ultrafast",
        "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
        "-vf", f"scale={width}:{height},format=yuv420p",
        "-shortest", "video.mp4"
    ]
    subprocess.run(cmd)
    print("✅ Video Rendered Successfully!")

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
        print("🚀 YOUTUBE UPLOAD DONE!")
    except Exception as e:
        print(f"❌ Upload Error: {e}")

def main():
    today = datetime.datetime.now().strftime('%A')
    print(f"--- Uzumaki Bot starting for {today} ---")
    script = asyncio.run(generate_assets())
    is_short = today not in ['Sunday', 'Monday']
    create_video(is_short=is_short)
    upload_to_youtube("Uzumaki-FF V-Badge Journey", script, is_short=is_short)

if __name__ == "__main__":
    main()
        
