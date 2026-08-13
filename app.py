import pandas as pd
from pathlib import Path

DATA = Path('data')


def load_inputs():
    kw = pd.read_csv(DATA / 'keyword_performance.csv')
    placement = pd.read_csv(DATA / 'placement_performance.csv')
    planner = pd.read_csv(DATA / 'keyword_planner.csv')
    trends = pd.read_csv(DATA / 'search_trends.csv')
    return kw, placement, planner, trends


def keyword_recommendations(kw, planner, trends):
    df = kw.merge(planner, on='keyword', how='left').merge(trends, on='keyword', how='left')
    df['cvr'] = (df['orders'] / df['clicks']).fillna(0)
    df['roas'] = (df['sales'] / df['spend']).replace([float('inf')], 0).fillna(0)
    df['sales_change_pct'] = ((df['sales'] - df['prev_sales']) / df['prev_sales'].replace(0, pd.NA)).fillna(0)

    actions = []
    reasons = []
    scores = []
    for _, r in df.iterrows():
        score = 0
        action = 'Maintain'
        reason = []
        if r['search_trend_pct'] >= 15 and r['cvr'] >= 0.08 and r['roas'] >= 3:
            action = 'Increase bid 10-15%'; score += 40
            reason.append('rising demand + strong CVR/ROAS')
        if r['roas'] < 1.8 and r['clicks'] >= 40:
            action = 'Decrease bid 15-20%'; score += 45
            reason.append('meaningful traffic but weak ROAS')
        if r['cvr'] < 0.04 and r['clicks'] >= 50:
            action = 'Reduce bid / inspect targeting'; score += 25
            reason.append('low conversion')
        if r['planner_volume'] >= 5000 and r['impressions'] < 3000:
            score += 20
            reason.append('high planner demand with limited paid coverage')
        if r['sales_change_pct'] <= -0.15 and r['search_trend_pct'] >= 0:
            score += 25
            reason.append('sales down despite stable/rising search demand')
        actions.append(action)
        reasons.append('; '.join(reason) or 'performance within normal range')
        scores.append(score)
    df['recommended_action'] = actions
    df['diagnosis'] = reasons
    df['priority_score'] = scores
    return df.sort_values('priority_score', ascending=False)


def placement_recommendations(df):
    out = df.copy()
    out['cvr'] = (out['orders'] / out['clicks']).fillna(0)
    out['roas'] = (out['sales'] / out['spend']).fillna(0)
    best = out.sort_values(['cvr','roas'], ascending=False).iloc[0]
    return out, f"Best placement: {best['placement']} (CVR {best['cvr']:.1%}, ROAS {best['roas']:.2f}x)"


def build_report(keyword_df, placement_note):
    lines = ['# Weekly Ads Optimization Report', '', '## Executive summary', placement_note, '', '## Priority keyword actions']
    for _, r in keyword_df.head(8).iterrows():
        lines.append(f"- **{r['keyword']}** — {r['recommended_action']} | {r['diagnosis']} | ROAS {r['roas']:.2f}x | CVR {r['cvr']:.1%}")
    lines += ['', '## Next-step framework', '- Scale high-converting keywords with rising demand.', '- Cut or restructure spend where traffic is not converting.', '- Reallocate toward placements with superior conversion efficiency.', '- Add emerging search terms that have demand but weak campaign coverage.']
    Path('optimization_report.md').write_text('\n'.join(lines), encoding='utf-8')


def main():
    kw, placement, planner, trends = load_inputs()
    recs = keyword_recommendations(kw, planner, trends)
    placement_table, placement_note = placement_recommendations(placement)
    print(recs[['keyword','cvr','roas','sales_change_pct','search_trend_pct','recommended_action','diagnosis','priority_score']].to_string(index=False))
    print('\n' + placement_note)
    build_report(recs, placement_note)

if __name__ == '__main__':
    main()
