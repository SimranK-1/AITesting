# FinanceIQ · Insurance Finance Report Agent

A prototype Streamlit application for insurance finance teams to generate structured reports via a 3-agent AI pipeline.

---

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Architecture

```
User Input (Chat or Quick Panel)
        │
        ▼
  Orchestrator  ←── LLM Intent Parser (OpenAI GPT-4o)
        │
        ├── Agent 1: Oracle Connector  → Fetches raw data from Oracle Financials Cloud
        ├── Agent 2: Finance Reasoning → Applies accounting/actuarial logic
        └── Agent 3: Report Formatter  → Structures output to standard templates
```

---

## Integration Placeholders

Open `app.py` and update the following constants at the top:

```python
# OpenAI LLM
OPENAI_API_KEY = "sk-PLACEHOLDER-YOUR-OPENAI-KEY-HERE"

# Oracle Financials Cloud
ORACLE_API_BASE_URL = "https://your-oracle-instance.example.com/api/v1"
ORACLE_API_TOKEN    = "PLACEHOLDER-ORACLE-API-TOKEN"
ORACLE_DB_SCHEMA    = "FIN_INSURANCE"
```

Then replace the stub functions:
- `oracle_fetch_reinsurance_data()` — Agent 1, hits Oracle REST API
- `oracle_fetch_premium_listing()` — Agent 1, premium policy data
- `oracle_fetch_claims_data()` — Agent 1, claims ledger data
- `parse_query_with_llm()` — Orchestrator, replace with LangChain/OpenAI call

---

## Supported Report Types

| Report | Description |
|---|---|
| Bill to Accounting | Reinsurance billing statement with settlement balance |
| Premium Listing | Detailed premiums written and ceded by policy |
| Claims Recovery Statement | Claims incurred vs. reinsurance recoveries |
| Loss Run Report | Period loss run by line of business |
| Bordereaux Report | Risk & premium bordereaux for treaty submission |

---

## Color Theme

| Role | Hex |
|---|---|
| Primary accent | `#ED1C2E` |
| Background | `#FFFFFF` |
| Primary text | `#212121` |
| Secondary text | `#666666` / `#999999` |
