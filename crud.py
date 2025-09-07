from sqlalchemy.orm import Session
from typing import List, Union, Sequence
import models
from schemas.platforms import YouTubeData, ForumData, GoogleData

# Union type alias for readability
PlatformSchema = Union[YouTubeData, ForumData, GoogleData]

def create_workflows(
    db: Session,
    records: Sequence[PlatformSchema]   # <-- Sequence instead of List
) -> List[models.Workflow]:
    db_objects: List[models.Workflow] = []

    for record in records:
        workflow = models.Workflow(
            # Common fields
            title=record.workflow,
            platform=record.platform,
            country=record.country,
            score = record.score,

            # YouTube metrics
            views=getattr(record, "views", None),
            likes=getattr(record, "likes", None),
            comments=getattr(record, "comments", None),
            like_to_view_ratio=getattr(record, "like_to_view_ratio", None),
            comment_to_view_ratio=getattr(record, "comment_to_view_ratio", None),

            # Forum metrics
            replies=getattr(record, "replies", None),
            forum_likes=getattr(record, "forum_likes", None),
            contributors=getattr(record, "contributors", None),
            thread_views=getattr(record, "thread_views", None),

            # Google metrics
            relative_search_interest=getattr(record, "relative_search_interest", None),
            search_volume=getattr(record, "search_volume", None),
            trend_change=getattr(record, "trend_change", None),
        )

        db.add(workflow)
        db_objects.append(workflow)

    db.commit()

    # Refresh so auto-generated fields (id, updated_at) are available
    for obj in db_objects:
        db.refresh(obj)

    return db_objects
