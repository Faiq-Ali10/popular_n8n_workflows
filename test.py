import requests, os
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
resp = requests.get(
    "https://www.googleapis.com/youtube/v3/search",
    params={
        "part": "snippet",
        "q": "WhatsApp Automation n8n",
        "type": "video",
        "maxResults": 5,
        "key": YOUTUBE_API_KEY
    }
).json()
print(resp)
