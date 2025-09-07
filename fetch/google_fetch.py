from typing import List
from pytrends.request import TrendReq
from schemas.platforms import GoogleData
from popularity_score import PopularityScorer

def fetch_google_trends_workflows(keyword_list: List[str], country: str = "US") -> List[GoogleData]:
    """
    Fetch Google Trends data for a list of keywords.
    Returns a list of GoogleData schemas.
    """
    pytrends = TrendReq(hl="en-US", tz=360)

    geo = "US" if country.upper() == "US" else "IN"
    try:
        pytrends.build_payload(keyword_list, timeframe="today 3-m", geo=geo)
        interest_over_time = pytrends.interest_over_time()
    except Exception as e:
        print(f"⚠️ Error fetching Google Trends data: {e}")
        return []

    workflows: List[GoogleData] = []

    for keyword in keyword_list:
        try:
            # Current interest (last available value)
            if not interest_over_time.empty and keyword in interest_over_time.columns:
                current_interest = float(interest_over_time[keyword].iloc[-1])
            else:
                current_interest = 0.0

                # Change in interest (last value vs ~30 days ago)
            trend_change = 0.0
            if not interest_over_time.empty and len(interest_over_time) > 30:
                prev = float(interest_over_time[keyword].iloc[-30])
                if prev > 0:
                    trend_change = (current_interest - prev) / prev

            workflows.append(
                GoogleData(
                    workflow=keyword,
                    platform="Google",
                    country=country,
                    score = 0.0,
                    relative_search_interest=current_interest,
                    search_volume=int(current_interest * 100),  # dummy scaling; real volume needs Ads API
                    trend_change=trend_change,
                )
            )
        except Exception as e:
            print(f"⚠️ Error parsing Google Trends for keyword '{keyword}': {e}")
            continue
        
    # Compute scores using all workflows as reference
    scorer = PopularityScorer()
    for wf in workflows:
        wf.score = scorer.calculate_google_score(wf, workflows)

    return workflows
