from pydantic import BaseModel

# Base schema for all platforms
class BaseData(BaseModel):
    workflow: str
    platform: str
    country: str 
    score : float

# YouTube schema 
class YouTubeData(BaseData):
    views: int
    likes: int
    comments: int
    like_to_view_ratio: float
    comment_to_view_ratio: float

# Forum schema
class ForumData(BaseData):
    replies: int
    forum_likes: int
    contributors: int
    thread_views: int

# Google schema
class GoogleData(BaseData):
    relative_search_interest: float
    search_volume: int
    trend_change: float
