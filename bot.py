import os
import requests
import time

# OpenRouter Configuration
def get_ai_content():
    api_key = os.getenv("OPENROUTER_API_KEY")
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "meta-llama/llama-3-8b-instruct:free",
            "messages": [{"role": "user", "content": "Generate a short viral Free Fire MAX caption with hashtags for a V-Badge journey."}]
        }
    )
    return response.json()['choices'][0]['message']['content']

# Image Generation (Pollinations - 100% Free)
def generate_image(prompt):
    seed = int(time.time())
    image_url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1080&height=1920&seed={seed}&model=flux"
    img_data = requests.get(image_url).content
    with open('uzumaki_post.jpg', 'wb') as handler:
        handler.write(img_data)
    print("Image Generated: uzumaki_post.jpg")

# Main Execution
if __name__ == "__main__":
    caption = get_ai_content()
    print(f"Caption: {caption}")
    generate_image("Free Fire MAX character with V-Badge glowing aura cinematic")
    # YouTube Upload logic yahan add hoga (v3 API credentials ke saath)
  
