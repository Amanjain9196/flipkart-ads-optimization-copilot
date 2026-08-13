# Flipkart Ads Optimization Copilot

**Repository description:** AI-style ads decision engine that combines keyword performance, placements, planner demand and search trends to recommend bid, budget and targeting actions.

> Portfolio demo using synthetic data only. No real Flipkart account IDs, private report URLs, credentials, campaign IDs, employer metrics or confidential commercial information are included.

## Problem
Ads optimization becomes difficult when decisions are spread across separate reports: keyword performance, placement performance, keyword planner data and organic/search-demand trends. Looking at any one report in isolation can lead to the wrong action.

## Solution
This copilot joins multiple signals at keyword level and generates an optimization report explaining:

- which keywords are gaining or losing sales
- where conversion is strong or weak
- where bids should increase or decrease
- which placements deserve more or less investment
- which rising search terms have low paid coverage
- where spend is inefficient
- what the top actions are for the next optimization cycle

## Inputs
```text
Keyword performance ─┐
Placement performance ├─> Signal join -> Diagnostic rules -> Recommendations -> Executive report
Keyword planner ──────┤
Search trends ────────┘
```

## Decision examples
- Rising search demand + strong CVR + limited impressions -> **increase bid / improve coverage**
- High CPC + low CVR + weak ROAS -> **reduce bid / add negatives / review targeting**
- Strong top-of-search CVR -> **shift placement investment toward top search**
- Planner volume growing but keyword absent from campaigns -> **new keyword opportunity**
- Sales down despite stable demand -> **inspect ad visibility, bid competitiveness or listing conversion**

## Run
```bash
pip install -r requirements.txt
python app.py
```

## Output
The script prints a ranked keyword optimization table and generates an `optimization_report.md` suitable for conversion into a weekly email or business review note.

## Portfolio signal
Demonstrates multi-source analytics, performance marketing logic, recommendation systems, explainability and executive communication — useful for an AI Chief of Staff / AI product portfolio.
