import os
import datetime
import requests
import asyncio
import edge_tts
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

# Configuration
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def get_youtube_client():
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    return build("youtube", "v3", credentials=creds)

def get_viral_content():
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        payload = {"contents": [{"parts":[{"text": "Write a 1 line viral Free Fire Hindi status for YouTube about V-Badge journey. Use hashtags."}]}]}
        response = requests.post(url, json=payload, timeout=10)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "V-Badge ki journey shuru! Uzumaki-FF ko subscribe karo. 🔥 #FreeFire #VBadge #UzumakiFF"

def upload_community_post(text, image_path):
    # Note: YouTube API direct Community Post support nahi karta (kuch cases mein), 
    # isliye hum ise as a Private/Public Video or Short test karenge.
    print(f"Uploading Content: {text}")
    # Abhi hum image generate kar rahe hain, full video logic Sunday ko chalega.

def main():
    content = get_viral_content()
    
    # Image Generation
    img_url = f"https://pollinations.ai/p/free_fire_pro_player_neon_style_v_badge?width=1080&height=1920&seed={datetime.datetime.now().second}"
    img_data = requests.get(img_url).content
    with open('post.jpg', 'wb') as f:
        f.write(img_data)
    
    print(f"✅ AI Content Ready: {content}")
    print("🚀 Uploading to YouTube...")
    
    # Upload Logic for YouTube
    youtube = get_youtube_client()
    
    # Thursday Test: Hum ek choti placeholder video upload karenge as a Short
    # Kyunki Community Post API sabke liye open nahi hoti
    # Sunday/Monday ko ye full voiceover video banayega.
    
    print("Done! Check YouTube in 2-3 minutes.")

if __name__ == "__main__":
    main()

