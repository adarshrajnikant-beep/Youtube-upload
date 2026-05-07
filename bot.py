import os
import datetime
import requests
import asyncio
import edge_tts

# Configuration
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

def get_viral_content():
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
            json={
                "model": "meta-llama/llama-3-8b-instruct:free",
                "messages": [{"role": "user", "content": "Write 1 line viral Free Fire Hindi status for YouTube about V-Badge journey."}]
            },
            timeout=15
        )
        data = response.json()
        if 'choices' in data:
            return data['choices'][0]['message']['content']
        else:
            print("AI Error, using backup script...")
            return "V-Badge ki journey shuru! Uzumaki-FF ko subscribe karo. 🔥 #FreeFire #VBadge"
    except:
        return "Aaj ka goal: 100 Likes! Free Fire viral gameplay coming soon. 🎮 #UzumakiFF"

async def make_voice(text):
    communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural")
    await communicate.save("voice.mp3")

def main():
    today = datetime.datetime.now().strftime('%A')
    content = get_viral_content()
    print(f"Content: {content}")
    
    # Image Generation
    img_url = f"https://pollinations.ai/p/free_fire_v_badge_gaming_character_ultra_realistic?width=1080&height=1920&seed={datetime.datetime.now().second}"
    img_data = requests.get(img_url).content
    with open('post.jpg', 'wb') as f:
        f.write(img_data)
    print("✅ Image generated!")

    # Abhi ke liye hum sirf check kar rahe hain
    print(f"Ready to upload on {today}")

if __name__ == "__main__":
    main()
    
