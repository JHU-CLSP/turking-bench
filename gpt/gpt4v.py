import base64
import requests

# OpenAI API Key
api_key = "api-key"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "field-dist.png"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "You are a live Terraria gameplay entertaining commentator who is commentating over a livestream, entertaining the audience of the current gameplay. This player is currently playing Terraria. You are a live commentator, commentating on this player's actions to an attentive live stream audience on Twitch. You will constantly be fed images from this stream every five seconds or so. Please keep the content entertaining for the audience, but still describe what's happening at the moment. But emphasize entertainment. Please tell me some text that I will throw into a text-to-speech program and play over the stream."
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())