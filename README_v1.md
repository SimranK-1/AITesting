# FinanceIQ · Demo Setup

## Requirements
- Python 3.9+
- No API keys needed for demo

## Install & Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app will open at http://localhost:8501

## Demo walkthrough

1. **Quick Report (sidebar)**
   - Select "Bill to Accounting" → Send To: Reinsurer → FY2025 Q3
   - Click "Generate Report"
   - Watch the animated 3-agent pipeline run in real time
   - Switch to "Report Viewer" tab to see the full formatted output
   - Download as JSON or CSV

2. **Chat interface**
   - Type: `Generate a Bill to Accounting to Reinsurer using FY2025Q3 data`
   - Or try: `Claims recovery statement for Q3 2025`
   - Or try: `Premium listing for FY2024 Q4 to Broker`

3. **Architecture tab**
   - Shows the LangGraph pipeline diagram
   - Shows integration placeholder status

## Enabling live integrations (post-demo)

Open `app.py` and update the 4 constants at the top:

```python
OPENAI_API_KEY      = "sk-YOUR-KEY"
ORACLE_API_BASE_URL = "https://your-oracle.example.com/api/v1"
ORACLE_API_TOKEN    = "YOUR-ORACLE-TOKEN"
ORACLE_DB_SCHEMA    = "FIN_INSURANCE"
```

Then replace the 3 functions marked `← REPLACE WITH LIVE INTEGRATION`:
- `parse_query()` → LangChain + OpenAI call
- `fetch_reinsurance_data()` → Oracle REST API
- `fetch_premium_data()` → Oracle REST API
- `fetch_claims_data()` → Oracle REST API
