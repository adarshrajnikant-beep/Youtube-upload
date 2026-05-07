import os
import datetime
import requests
import asyncio
import edge_tts

# Configuration from Secrets
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

def get_viral_content():
    # OpenRouter se viral Free Fire script mangna
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
        json={
            "model": "meta-llama/llama-3-8b-instruct:free",
            "messages": [{"role": "user", "content": "Write a 30-second viral Free Fire Hindi script for YouTube Shorts about V-Badge journey."}]
        }
    )
    return response.json()['choices'][0]['message']['content']

async def make_voice(text):
    communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural")
    await communicate.save("voice.mp3")

def main():
    today = datetime.datetime.now().strftime('%A')
    content = get_viral_content()
    
    # Image Generation for Community Post/Video Background
    img_url = f"https://pollinations.ai/p/free_fire_v_badge_ultra_realistic_gaming_setup?width=1080&height=1920&seed={datetime.datetime.now().second}"
    img_data = requests.get(img_url).content
    with open('post.jpg', 'wb') as f:
        f.write(img_data)

    if today in ['Sunday', 'Monday']:
        print("Creating Video for Sunday/Monday...")
        asyncio.run(make_voice(content))
        # Yahan video mixing aur upload ka code aayega
    else:
        print("Uploading Community Post...")
        # Yahan YouTube Community Post upload ka code aayega

if __name__ == "__main__":
    main()
      
