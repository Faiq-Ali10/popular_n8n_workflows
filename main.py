from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import Base, Workflow
from database import engine, get_db

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message":"Hello world, if you want popular n8n workflows data, please go to /popular"}

@app.get("/popular")
async def popular(db: Session = Depends(get_db)):
    """
    Fetch top 50 workflows ordered by score (descending).
    """
    workflows = (
        db.query(Workflow)
        .order_by(Workflow.score.desc())
        .limit(50)
        .all()
    )

    result = []
    for wf in workflows:
        if wf.platform == "YouTube":   # type: ignore
            popularity_metrics = {
                "views": wf.views,
                "likes": wf.likes,
                "comments": wf.comments,
                "like_to_view_ratio": wf.like_to_view_ratio,
                "comment_to_view_ratio": wf.comment_to_view_ratio,
            }
        elif wf.platform == "Forum":  # type: ignore
            popularity_metrics = {
                "replies": wf.replies,
                "forum_likes": wf.forum_likes,
                "contributors": wf.contributors,
                "thread_views": wf.thread_views,
            }
        elif wf.platform == "Google":  # type: ignore
            popularity_metrics = {
                "relative_search_interest": wf.relative_search_interest,
                "search_volume": wf.search_volume,
                "trend_change": wf.trend_change,
            }
        else:
            popularity_metrics = {}

        result.append({
            "workflow": wf.title,
            "platform": wf.platform,
            "popularity_metrics": popularity_metrics,
            "country": wf.country,
            "score": wf.score,
            "updated_at": wf.updated_at,
        })

    return result
