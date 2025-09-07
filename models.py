from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Workflow(Base):
    __tablename__ = "workflows"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    platform = Column(String, nullable=False, index=True)
    country = Column(String, nullable=False, index=True)
    score = Column(Float, nullable=False, index = True)
    
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # YouTube metrics
    views = Column(Integer, nullable=True)
    likes = Column(Integer, nullable=True)
    comments = Column(Integer, nullable=True)
    like_to_view_ratio = Column(Float, nullable=True)
    comment_to_view_ratio = Column(Float, nullable=True)

    # Forum (Discourse) metrics
    replies = Column(Integer, nullable=True)
    forum_likes = Column(Integer, nullable=True)  
    contributors = Column(Integer, nullable=True)
    thread_views = Column(Integer, nullable=True)

    # Google Search / Trends metrics
    relative_search_interest = Column(Float, nullable=True)  
    search_volume = Column(Integer, nullable=True)           # monthly searches
    trend_change = Column(Float, nullable=True)              # % change over time