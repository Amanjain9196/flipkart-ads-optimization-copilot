import pandas as pd
from app import keyword_recommendations


def test_scales_strong_rising_keyword():
    kw = pd.DataFrame([{'keyword':'term','impressions':1000,'clicks':100,'spend':1000,'orders':12,'sales':5000,'prev_sales':4000}])
    planner = pd.DataFrame([{'keyword':'term','planner_volume':6000,'competition_index':0.7,'suggested_bid':15}])
    trends = pd.DataFrame([{'keyword':'term','search_trend_pct':20}])
    out = keyword_recommendations(kw, planner, trends)
    assert out.iloc[0]['recommended_action'] == 'Increase bid 10-15%'
    assert out.iloc[0]['priority_score'] > 0
