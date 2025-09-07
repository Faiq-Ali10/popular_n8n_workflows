import math
from typing import List
from schemas.platforms import YouTubeData, ForumData, GoogleData

class PopularityScorer:
    def __init__(self):
        # Weights for different aspects (should sum to 1.0 for each platform)
        self.youtube_weights = {
            'reach_score': 0.3,      # Based on views
            'engagement_score': 0.4,  # Based on likes/comments ratios
            'absolute_engagement': 0.3 # Raw engagement numbers
        }
        
        self.forum_weights = {
            'reach_score': 0.25,     # Based on thread views
            'engagement_score': 0.4,  # Based on replies and likes
            'community_score': 0.35   # Based on contributors
        }
        
        self.google_weights = {
            'interest_score': 0.4,    # Relative search interest
            'volume_score': 0.35,     # Search volume
            'trend_score': 0.25       # Trend change
        }
    
    def normalize_log(self, value: float) -> float:
        """Log normalization to handle large number ranges"""
        return math.log1p(value)
    
    def normalize_linear(self, value: float, max_val: float) -> float:
        """Linear normalization between 0-1"""
        return min(value / max_val, 1.0) if max_val > 0 else 0.0
    
    def calculate_youtube_score(self, data: YouTubeData, reference_data: List[YouTubeData]) -> float:
        """Calculate YouTube popularity score"""
        # Get reference values for normalization
        max_views = max((d.views for d in reference_data), default=0)
        max_likes = max((d.likes for d in reference_data), default=0)
        max_comments = max((d.comments for d in reference_data), default=0)
        max_like_ratio = max((d.like_to_view_ratio for d in reference_data), default=0)
        max_comment_ratio = max((d.comment_to_view_ratio for d in reference_data), default=0)

        # Reach score (log-normalized views)
        reach_score = self.normalize_log(data.views) / self.normalize_log(max_views) if max_views > 0 else 0

        # Engagement quality score (normalized ratios)
        like_ratio_norm = self.normalize_linear(data.like_to_view_ratio, max_like_ratio) if max_like_ratio > 0 else 0
        comment_ratio_norm = self.normalize_linear(data.comment_to_view_ratio, max_comment_ratio) if max_comment_ratio > 0 else 0
        engagement_score = (like_ratio_norm + comment_ratio_norm) / 2

        # Absolute engagement score
        like_norm = self.normalize_log(data.likes) / self.normalize_log(max_likes) if max_likes > 0 else 0
        comment_norm = self.normalize_log(data.comments) / self.normalize_log(max_comments) if max_comments > 0 else 0
        absolute_engagement = (like_norm + comment_norm) / 2

        # Weighted final score
        final_score = (
            reach_score * self.youtube_weights['reach_score'] +
            engagement_score * self.youtube_weights['engagement_score'] +
            absolute_engagement * self.youtube_weights['absolute_engagement']
        )

        return final_score


    def calculate_forum_score(self, data: ForumData, reference_data: List[ForumData]) -> float:
        """Calculate forum popularity score"""
        # Get reference values
        max_views = max((d.thread_views for d in reference_data), default=0)
        max_replies = max((d.replies for d in reference_data), default=0)
        max_likes = max((d.forum_likes for d in reference_data), default=0)
        max_contributors = max((d.contributors for d in reference_data), default=0)

        # Reach score
        reach_score = self.normalize_log(data.thread_views) / self.normalize_log(max_views) if max_views > 0 else 0

        # Engagement score (replies and likes)
        reply_norm = self.normalize_log(data.replies) / self.normalize_log(max_replies) if max_replies > 0 else 0
        like_norm = self.normalize_log(data.forum_likes) / self.normalize_log(max_likes) if max_likes > 0 else 0
        engagement_score = (reply_norm + like_norm) / 2

        # Community diversity score
        community_score = self.normalize_log(data.contributors) / self.normalize_log(max_contributors) if max_contributors > 0 else 0

        # Weighted final score
        final_score = (
            reach_score * self.forum_weights['reach_score'] +
            engagement_score * self.forum_weights['engagement_score'] +
            community_score * self.forum_weights['community_score']
        )

        return final_score


    def calculate_google_score(self, data: GoogleData, reference_data: List[GoogleData]) -> float:
        """Calculate Google search popularity score"""
        # Get reference values
        max_volume = max((d.search_volume for d in reference_data), default=0)
        max_trend_change = max((abs(d.trend_change) for d in reference_data), default=0)

        # Interest score (0-100 scale)
        interest_score = data.relative_search_interest / 100.0

        # Volume score (log-normalized)
        volume_score = self.normalize_log(data.search_volume) / self.normalize_log(max_volume) if max_volume > 0 else 0

        # Trend score (normalize trend change, positive trends get higher scores)
        if max_trend_change > 0:
            trend_normalized = (data.trend_change + max_trend_change) / (2 * max_trend_change)
            trend_score = max(0, min(1, trend_normalized))
        else:
            trend_score = 0.5  # Neutral if no trend data

        # Weighted final score
        final_score = (
            interest_score * self.google_weights['interest_score'] +
            volume_score * self.google_weights['volume_score'] +
            trend_score * self.google_weights['trend_score']
        )

        return final_score
