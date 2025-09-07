import requests
from typing import List
from schemas.platforms import YouTubeData
from popularity_score import PopularityScorer
from dotenv import load_dotenv
import os

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def fetch_youtube_workflows(query: str, country: str = "US") -> List[YouTubeData]:
    """
    Fetch YouTube videos for a given query and country,
    return a list of YouTubeData schemas with scores.
    """
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 50,
        "regionCode": country,        # ensures results are localized by country
        "relevanceLanguage": "en",    # optional: restrict to English
        "key": YOUTUBE_API_KEY,
    }

    try:
        response = requests.get(url, params=params).json()
        #print("YOUTUBE RAW RESPONSE:", response)
    except Exception as e:
        raise e

    workflows: List[YouTubeData] = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]

            # Fetch statistics for this video
        stats_url = "https://www.googleapis.com/youtube/v3/videos"
        stats_params = {
            "part": "statistics",
            "id": video_id,
            "key": YOUTUBE_API_KEY,
        }
        stats_response = requests.get(stats_url, params=stats_params).json()
        stats = stats_response.get("items", [{}])[0].get("statistics", {})

        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0))
        comments = int(stats.get("commentCount", 0))

        workflows.append(
            YouTubeData(
                workflow=item["snippet"]["title"],
                platform="YouTube",
                country=country,
                views=views,
                likes=likes,
                comments=comments,
                like_to_view_ratio=likes / views if views else 0.0,
                comment_to_view_ratio=comments / views if views else 0.0,
                score=0.0,  # temporary, will be updated below
            )
        )

    # Compute scores using all workflows as reference
    scorer = PopularityScorer()
    for wf in workflows:
        wf.score = scorer.calculate_youtube_score(wf, workflows)

    return workflows
