import requests
from typing import List
from schemas.platforms import ForumData
from popularity_score import PopularityScorer 

def fetch_forum_workflows(category: str = "workflow-examples", country: str = "US") -> List[ForumData]:
    """
    Fetch workflows from n8n Forum (Discourse) for a given category.
    Returns a list of ForumData schemas.
    """
    
    workflows: List[ForumData] = []
    for n in range(1, 20):
        url = url = f"https://community.n8n.io/c/{category}.json?page={n}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"⚠️ Error fetching forum data: {e}")
            return workflows  # return empty list if error occurs

        for topic in data.get("topic_list", {}).get("topics", []):
            try:
                workflows.append(
                    ForumData(
                        workflow=topic.get("title", "Untitled"),
                        platform="Forum",
                        country=country,
                        score = 0.0,
                        replies=topic.get("reply_count", 0),
                        forum_likes=topic.get("like_count", 0),
                        contributors=topic.get("participant_count", 0),
                        thread_views=topic.get("views", 0),
                    )
                )
            except Exception as e:
                print(f"⚠️ Error parsing topic {topic.get('id')}: {e}")
                continue
        
        scorer = PopularityScorer() 
        for wf in workflows:
            wf.score = scorer.calculate_forum_score(wf, workflows)

    return workflows

if __name__ == "__main__":
    fetch_forum_workflows()