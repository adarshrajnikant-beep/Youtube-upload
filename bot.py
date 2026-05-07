import os
import datetime
import requests
import asyncio
import edge_tts

# Configuration
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def get_viral_content():
    # 1. Pehle Gemini Try Karte Hain (As Primary/Backup)
    if GEMINI_KEY:
        try:
            print("Trying Gemini AI...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
            payload = {"contents": [{"parts":[{"text": "Write a 1 line viral Free Fire Hindi status for YouTube Shorts about V-Badge journey."}]}]}
            response = requests.post(url, json=payload, timeout=10)
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            print(f"Gemini failed: {e}")

    # 2. Agar Gemini fail ho toh OpenRouter
    if OPENROUTER_KEY:
        try:
            print("Trying OpenRouter...")
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
                json={
                    "model": "meta-llama/llama-3-8b-instruct:free",
                    "messages": [{"role": "user", "content": "Write 1 line Free Fire Hindi status."}]
                },
                timeout=10
            )
            return response.json()['choices'][0]['message']['content']
        except:
            pass

    # 3. Last Option: Hardcoded Backup
    return "V-Badge ki journey shuru! Uzumaki-FF ko subscribe karo. 🔥 #FreeFire #VBadge"

# ... (Baki ka code wahi rahega jo pehle tha)

def main():
    content = get_viral_content()
    print(f"Final Content: {content}")
    
    # Image Generation
    img_url = f"https://pollinations.ai/p/free_fire_pro_player_with_v_badge_neon_gaming_style?width=1080&height=1920&seed={datetime.datetime.now().second}"
    img_data = requests.get(img_url).content
    with open('post.jpg', 'wb') as f:
        f.write(img_data)
    print("✅ Image generated!")

if __name__ == "__main__":
    main()
    
