"""
FinanceIQ · Insurance Finance Report Agent — DEMO MODE
======================================================
Fully self-contained prototype. No API keys required.
All agent interactions, data, and responses are scripted
to realistically simulate the production pipeline.

To enable live integrations, replace the stub functions
marked  ← REPLACE WITH LIVE INTEGRATION
"""

import streamlit as st
import time
import json
import random
from datetime import datetime
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinanceIQ · Insurance Report Agent",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# LIVE INTEGRATION PLACEHOLDERS  (replace before production)
# ─────────────────────────────────────────────────────────────────────────────
OPENAI_API_KEY      = "sk-PLACEHOLDER"                       # ← REPLACE WITH LIVE INTEGRATION
ORACLE_API_BASE_URL = "https://oracle.example.com/api/v1"   # ← REPLACE WITH LIVE INTEGRATION
ORACLE_API_TOKEN    = "ORACLE-TOKEN-PLACEHOLDER"             # ← REPLACE WITH LIVE INTEGRATION
ORACLE_DB_SCHEMA    = "FIN_INSURANCE"

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Mono:wght@400;500&display=swap');

:root {
    --red:      #ED1C2E;
    --red-dk:   #C0141F;
    --white:    #FFFFFF;
    --black:    #212121;
    --g1:       #666666;
    --g2:       #999999;
    --g3:       #CCCCCC;
    --g4:       #F5F5F5;
    --g5:       #EBEBEB;
    --green:    #1A9E5C;
    --amber:    #D97706;
    --blue:     #1D6FA4;
    --shadow:   0 2px 12px rgba(0,0,0,0.07);
    --shadow-lg:0 8px 32px rgba(0,0,0,0.11);
}

html, body, [data-testid="stApp"], .main {
    background: #F4F4F6 !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--black) !important;
}
.block-container { padding: 0 !important; max-width: 100% !important; }

[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--g5) !important;
    box-shadow: 2px 0 16px rgba(0,0,0,0.04) !important;
    min-width: 310px !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

.stButton > button {
    background: var(--red) !important;
    color: white !important;
    border: none !important;
    border-radius: 7px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.52rem 1.2rem !important;
    transition: background 0.18s, transform 0.1s, box-shadow 0.18s !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    background: var(--red-dk) !important;
    box-shadow: 0 4px 18px rgba(237,28,46,0.28) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* suggestion pill buttons */
.suggest-btn > button {
    background: white !important;
    color: var(--black) !important;
    border: 1.5px solid var(--g5) !important;
    border-radius: 6px !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    padding: 0.4rem 0.9rem !important;
    letter-spacing: 0 !important;
    text-align: left !important;
    white-space: normal !important;
    height: auto !important;
    line-height: 1.4 !important;
}
.suggest-btn > button:hover {
    background: #FFF5F5 !important;
    border-color: var(--red) !important;
    color: var(--red) !important;
    box-shadow: none !important;
    transform: none !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    font-family: 'DM Sans', sans-serif !important;
    border: 1.5px solid var(--g3) !important;
    border-radius: 7px !important;
    background: white !important;
    color: var(--black) !important;
    font-size: 0.875rem !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--red) !important;
    box-shadow: 0 0 0 3px rgba(237,28,46,0.11) !important;
    outline: none !important;
}
.stSelectbox > div > div {
    border: 1.5px solid var(--g3) !important;
    border-radius: 7px !important;
    background: white !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.875rem !important;
}

label, .stSelectbox label, .stTextInput label {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.73rem !important;
    color: var(--g1) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
}

[data-baseweb="tab-list"] {
    background: var(--g4) !important;
    border-radius: 9px !important;
    padding: 4px !important;
    gap: 3px !important;
    border: none !important;
}
[data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 7px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.84rem !important;
    color: var(--g1) !important;
    border: none !important;
    padding: 8px 18px !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: white !important;
    color: var(--red) !important;
    font-weight: 700 !important;
    box-shadow: var(--shadow) !important;
}
[data-baseweb="tab-highlight"],
[data-baseweb="tab-border"] { display: none !important; }

[data-testid="stDataFrame"] { border-radius: 9px !important; overflow: hidden !important; }
[data-testid="stDataFrame"] table { font-family: 'DM Mono', monospace !important; font-size: 0.8rem !important; }
[data-testid="stDataFrame"] th { background: #F5F5F5 !important; font-weight: 700 !important; color: #212121 !important; }

.stSpinner > div { border-top-color: var(--red) !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-thumb { background: #CCCCCC; border-radius: 3px; }

.stProgress > div > div > div { background: var(--red) !important; }

@keyframes pulse-dot {
    0%,100% { opacity:1; } 50% { opacity:0.45; }
}
.pulse-dot { animation: pulse-dot 1.8s infinite; }

@keyframes slide-in {
    from { opacity:0; transform:translateX(-8px); }
    to   { opacity:1; transform:translateX(0); }
}
.agent-step { animation: slide-in 0.3s ease; }

@keyframes bubble-in {
    from { opacity:0; transform:translateY(6px); }
    to   { opacity:1; transform:translateY(0); }
}
.chat-bubble { animation: bubble-in 0.25s ease; }

@keyframes count-up {
    from { opacity:0; transform:translateY(4px); }
    to   { opacity:1; transform:translateY(0); }
}
.kpi-num { animation: count-up 0.4s ease 0.1s both; }

@keyframes fade-in {
    from { opacity:0; } to { opacity:1; }
}
.suggestions-block { animation: fade-in 0.4s ease 0.2s both; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
defaults = {
    "messages": [],
    "reports": [],
    "agent_steps": [],
    "pending_query": None,   # set by suggestion button click
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# STATIC DEMO DATA
# ─────────────────────────────────────────────────────────────────────────────
DEMO_REINSURANCE = {
    ("FY2025", "Q3"): {
        "premiums_written": 14_820_450.00, "premiums_ceded": 5_928_180.00,
        "losses_incurred": 9_633_292.50,   "losses_ceded":   3_267_499.00,
        "commissions_paid": 1_185_636.00,  "commissions_received": 474_254.40,
        "admin_expenses": 667_320.00,      "interest_income": 177_845.40,
        "reinsurer": "Swiss Re Ltd.", "treaty_id": "TRY-2025-007",
        "currency": "USD", "lines_of_business": ["Property", "Casualty", "Marine"],
        "cedant_share": "60%", "reinsurer_share": "40%",
    },
    ("FY2025", "Q2"): {
        "premiums_written": 13_210_000.00, "premiums_ceded": 5_284_000.00,
        "losses_incurred": 8_586_500.00,   "losses_ceded":   2_999_100.00,
        "commissions_paid": 1_056_800.00,  "commissions_received": 422_720.00,
        "admin_expenses": 594_450.00,      "interest_income": 158_520.00,
        "reinsurer": "Munich Re", "treaty_id": "TRY-2025-007",
        "currency": "USD", "lines_of_business": ["Property", "Casualty"],
        "cedant_share": "60%", "reinsurer_share": "40%",
    },
    ("FY2024", "Q4"): {
        "premiums_written": 12_950_000.00, "premiums_ceded": 5_180_000.00,
        "losses_incurred": 8_250_000.00,   "losses_ceded":   2_880_000.00,
        "commissions_paid": 1_036_000.00,  "commissions_received": 414_400.00,
        "admin_expenses": 583_000.00,      "interest_income": 155_400.00,
        "reinsurer": "Hannover Re", "treaty_id": "TRY-2024-004",
        "currency": "USD", "lines_of_business": ["Property", "Casualty", "Marine", "Aviation"],
        "cedant_share": "60%", "reinsurer_share": "40%",
    },
}

DEMO_PREMIUMS = {
    ("FY2025", "Q3"): [
        {"Policy ID":"POL-10291","Insured":"Meridian Logistics Inc.", "LOB":"Marine",   "Gross Premium":487_250.00,"Ceded %":"40.0%","Ceded Premium":194_900.00,"Net Retained":292_350.00,"Effective Date":"2025-07-01","Expiry":"2026-07-01","Status":"Active"},
        {"Policy ID":"POL-10388","Insured":"Baxter Steel Corp.",      "LOB":"Property", "Gross Premium":372_800.00,"Ceded %":"40.0%","Ceded Premium":149_120.00,"Net Retained":223_680.00,"Effective Date":"2025-07-15","Expiry":"2026-07-15","Status":"Active"},
        {"Policy ID":"POL-10455","Insured":"Coastal RE Holdings",     "LOB":"Casualty", "Gross Premium":298_600.00,"Ceded %":"40.0%","Ceded Premium":119_440.00,"Net Retained":179_160.00,"Effective Date":"2025-08-01","Expiry":"2026-08-01","Status":"Active"},
        {"Policy ID":"POL-10512","Insured":"Pacific Cargo Group",     "LOB":"Marine",   "Gross Premium":521_400.00,"Ceded %":"40.0%","Ceded Premium":208_560.00,"Net Retained":312_840.00,"Effective Date":"2025-08-15","Expiry":"2026-08-15","Status":"Active"},
        {"Policy ID":"POL-10687","Insured":"Allied Construction LLC", "LOB":"Property", "Gross Premium":443_100.00,"Ceded %":"40.0%","Ceded Premium":177_240.00,"Net Retained":265_860.00,"Effective Date":"2025-09-01","Expiry":"2026-09-01","Status":"Active"},
        {"Policy ID":"POL-10734","Insured":"Northern Energy Co.",     "LOB":"Casualty", "Gross Premium":315_200.00,"Ceded %":"40.0%","Ceded Premium":126_080.00,"Net Retained":189_120.00,"Effective Date":"2025-09-15","Expiry":"2026-09-15","Status":"Active"},
    ],
}

DEMO_CLAIMS = {
    ("FY2025", "Q3"): [
        {"Claim ID":"CLM-8821","Insured":"Meridian Logistics Inc.", "LOB":"Marine",  "Cause":"Storm Damage",    "Incurred":892_400.00, "Recovered":356_960.00,"Net Loss":535_440.00,"Reported":"2025-07-14","Status":"Open",   "Reserve":450_000.00},
        {"Claim ID":"CLM-8934","Insured":"Baxter Steel Corp.",      "LOB":"Property","Cause":"Fire",            "Incurred":1_240_000.00,"Recovered":496_000.00,"Net Loss":744_000.00,"Reported":"2025-07-28","Status":"Open",   "Reserve":900_000.00},
        {"Claim ID":"CLM-9011","Insured":"Allied Construction LLC", "LOB":"Property","Cause":"Water Damage",    "Incurred":367_800.00, "Recovered":147_120.00,"Net Loss":220_680.00,"Reported":"2025-08-05","Status":"Closed", "Reserve":0},
        {"Claim ID":"CLM-9203","Insured":"Coastal RE Holdings",     "LOB":"Casualty","Cause":"Liability",       "Incurred":543_200.00, "Recovered":217_280.00,"Net Loss":325_920.00,"Reported":"2025-08-22","Status":"Pending","Reserve":300_000.00},
        {"Claim ID":"CLM-9417","Insured":"Pacific Cargo Group",     "LOB":"Marine",  "Cause":"Cargo Theft",     "Incurred":224_292.50, "Recovered":89_717.00, "Net Loss":134_575.50,"Reported":"2025-09-03","Status":"Closed", "Reserve":0},
    ],
}

def _get_pool(pool, fy, quarter):
    key = (fy, quarter)
    return pool.get(key, list(pool.values())[0])

# ─────────────────────────────────────────────────────────────────────────────
# REPORT REGISTRY
# ─────────────────────────────────────────────────────────────────────────────
REPORT_REGISTRY = {
    "bill_to_accounting": {
        "label": "Bill to Accounting",
        "desc":  "Reinsurance billing statement for accounting reconciliation.",
        "keywords": ["bill", "accounting", "billing", "statement", "settlement"],
    },
    "premium_listing": {
        "label": "Premium Listing",
        "desc":  "Detailed listing of premiums written and ceded by policy.",
        "keywords": ["premium", "policy", "listing", "written", "ceded"],
    },
    "claims_recovery": {
        "label": "Claims Recovery Statement",
        "desc":  "Summary of claims incurred and reinsurance recoveries.",
        "keywords": ["claim", "recovery", "loss", "incurred", "recover"],
    },
    "loss_run": {
        "label": "Loss Run Report",
        "desc":  "Period loss run by line of business.",
        "keywords": ["loss run", "lob", "run report"],
    },
    "bordereaux": {
        "label": "Bordereaux Report",
        "desc":  "Detailed risk and premium bordereaux for treaty submission.",
        "keywords": ["bordereaux", "treaty", "risk", "submission"],
    },
}

COUNTERPARTIES = ["Reinsurer", "Broker", "Internal Accounting", "Cedant", "Regulator"]

# ─────────────────────────────────────────────────────────────────────────────
# QUERY SUGGESTIONS  (context-aware, triggered after each report)
# ─────────────────────────────────────────────────────────────────────────────
SUGGESTIONS_MAP = {
    "bill_to_accounting": [
        "Generate a Claims Recovery Statement for FY2025Q3 to Reinsurer",
        "Run a Premium Listing for FY2025Q3 to Internal Accounting",
        "Generate a Bill to Accounting to Reinsurer using FY2025Q2 data",
        "Produce a Bordereaux Report for FY2025Q3 to Reinsurer",
    ],
    "premium_listing": [
        "Generate a Bill to Accounting to Reinsurer using FY2025Q3 data",
        "Run a Claims Recovery Statement for FY2025Q3 to Broker",
        "Produce a Premium Listing for FY2024Q4 to Internal Accounting",
        "Generate a Loss Run Report for FY2025Q3 to Reinsurer",
    ],
    "claims_recovery": [
        "Generate a Bill to Accounting to Reinsurer using FY2025Q3 data",
        "Run a Loss Run Report for FY2025Q3 to Reinsurer",
        "Produce a Claims Recovery Statement for FY2025Q2 to Broker",
        "Generate a Bordereaux Report for FY2025Q3 to Reinsurer",
    ],
    "loss_run": [
        "Generate a Claims Recovery Statement for FY2025Q3 to Reinsurer",
        "Run a Bill to Accounting to Reinsurer for FY2025Q3",
        "Produce a Loss Run Report for FY2024Q4 to Internal Accounting",
        "Generate a Premium Listing for FY2025Q3 to Broker",
    ],
    "bordereaux": [
        "Generate a Bill to Accounting to Reinsurer using FY2025Q3 data",
        "Run a Premium Listing for FY2025Q3 to Reinsurer",
        "Produce a Bordereaux Report for FY2025Q2 to Broker",
        "Generate a Claims Recovery Statement for FY2025Q3 to Cedant",
    ],
}

def get_suggestions(report_type: str) -> list:
    return SUGGESTIONS_MAP.get(report_type, SUGGESTIONS_MAP["bill_to_accounting"])

# ─────────────────────────────────────────────────────────────────────────────
# AGENT STEP SCRIPTS
# ─────────────────────────────────────────────────────────────────────────────
def get_agent_script(report_type, fy, quarter, counterparty, rows):
    label = REPORT_REGISTRY[report_type]["label"]
    return [
        ("Orchestrator",              f'Intent parsed — "{label}" for {counterparty}, {fy} {quarter}', 0.35),
        ("Orchestrator",              "Routing to Agent 1 · Oracle Connector", 0.25),
        ("Agent 1 · Oracle Connector",f"Authenticating with Oracle Financials Cloud ({ORACLE_DB_SCHEMA})", 0.55),
        ("Agent 1 · Oracle Connector",f"Executing GL query: SELECT * FROM {ORACLE_DB_SCHEMA}.REINS_LEDGER WHERE PERIOD = '{fy}{quarter}'", 0.65),
        ("Agent 1 · Oracle Connector",f"Fetch complete — {rows} records retrieved, validation passed", 0.35),
        ("Agent 2 · Finance Reasoning","Loading treaty parameters from treaty register (TRY-2025-007)", 0.45),
        ("Agent 2 · Finance Reasoning","Applying proportional reinsurance cession rules (40% quota share)", 0.45),
        ("Agent 2 · Finance Reasoning","Computing net premiums, loss recoveries, commission adjustments", 0.55),
        ("Agent 2 · Finance Reasoning","Calculations complete — treaty compliance check passed", 0.35),
        ("Agent 3 · Report Formatter", f"Mapping data to {label} standard template", 0.35),
        ("Agent 3 · Report Formatter", "Applying number formatting, currency conversion, rounding rules", 0.35),
        ("Agent 3 · Report Formatter", "Report structured and validated — ready for delivery", 0.25),
    ]

# ─────────────────────────────────────────────────────────────────────────────
# INTENT PARSER  (← REPLACE WITH LIVE INTEGRATION: LangChain + OpenAI)
# ─────────────────────────────────────────────────────────────────────────────
def parse_query(query: str) -> dict:
    q = query.lower()
    report_type = "bill_to_accounting"
    for key, meta in REPORT_REGISTRY.items():
        if any(kw in q for kw in meta["keywords"]):
            report_type = key
            break
    counterparty = "Reinsurer"
    for cp in COUNTERPARTIES:
        if cp.lower() in q:
            counterparty = cp
            break
    fy = "FY2025"
    for token in query.upper().split():
        if token.startswith("FY") and len(token) >= 6:
            fy = token[:6]
            break
    quarter = "Q3"
    for qn in ["Q1", "Q2", "Q3", "Q4"]:
        if qn in query.upper():
            quarter = qn
            break
    return {"report_type": report_type, "counterparty": counterparty, "fy": fy, "quarter": quarter}

# ─────────────────────────────────────────────────────────────────────────────
# DATA FETCH STUBS  (← REPLACE WITH LIVE INTEGRATION: Oracle REST API)
# ─────────────────────────────────────────────────────────────────────────────
def fetch_reinsurance_data(fy, quarter):
    return _get_pool(DEMO_REINSURANCE, fy, quarter)

def fetch_premium_data(fy, quarter):
    return _get_pool(DEMO_PREMIUMS, fy, quarter)

def fetch_claims_data(fy, quarter):
    return _get_pool(DEMO_CLAIMS, fy, quarter)

# ─────────────────────────────────────────────────────────────────────────────
# FINANCE CALCULATIONS  (Agent 2)
# ─────────────────────────────────────────────────────────────────────────────
def compute_bill_to_accounting(raw):
    net_prem = raw["premiums_ceded"] - raw["commissions_received"]
    net_loss = raw["losses_ceded"]
    comm_adj = raw["commissions_paid"]
    balance  = net_prem - net_loss - comm_adj
    return {
        "net_premium_ceded":     round(net_prem, 2),
        "net_loss_recovery":     round(net_loss, 2),
        "commission_adjustment": round(comm_adj, 2),
        "balance_due":           round(balance, 2),
        "raw": raw,
    }

def compute_premium_listing(rows):
    df = pd.DataFrame(rows)
    return {
        "rows":        rows,
        "total_gross": df["Gross Premium"].sum(),
        "total_ceded": df["Ceded Premium"].sum(),
        "total_net":   df["Net Retained"].sum(),
    }

def compute_claims(rows):
    df = pd.DataFrame(rows)
    return {
        "rows":            rows,
        "total_incurred":  df["Incurred"].sum(),
        "total_recovered": df["Recovered"].sum(),
        "total_net_loss":  df["Net Loss"].sum(),
        "open_claims":     int((df["Status"] == "Open").sum()),
    }

# ─────────────────────────────────────────────────────────────────────────────
# REPORT ASSEMBLY  (Agent 3)
# ─────────────────────────────────────────────────────────────────────────────
def assemble_report(parsed, finance_data, row_count):
    rt    = parsed["report_type"]
    rid   = f"RPT-{random.randint(10000,99999)}"
    return {
        "report_id":    rid,
        "report_type":  rt,
        "report_label": REPORT_REGISTRY[rt]["label"],
        "counterparty": parsed["counterparty"],
        "fy":           parsed["fy"],
        "quarter":      parsed["quarter"],
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data_source":  "Oracle Financials Cloud",
        "rows_fetched": row_count,
        "status":       "FINAL",
        "finance":      finance_data,
    }

# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE WITH ANIMATED STEPS
# ─────────────────────────────────────────────────────────────────────────────
def render_agent_log(steps, running_agent=None):
    agent_colors = {
        "Orchestrator":               "#8B5CF6",
        "Agent 1 · Oracle Connector": "#1D6FA4",
        "Agent 2 · Finance Reasoning":"#D97706",
        "Agent 3 · Report Formatter": "#1A9E5C",
    }
    rows_html = ""
    for i, (agent, step) in enumerate(steps):
        is_last  = (i == len(steps) - 1)
        is_run   = is_last and running_agent == agent
        color    = agent_colors.get(agent, "#666")
        dot_bg   = color if is_run else "#1A9E5C"
        dot_anim = "animation:pulse-dot 1s infinite;" if is_run else ""
        tag_text = "PROCESSING" if is_run else "DONE"
        rows_html += f"""
        <div class="agent-step" style="display:flex;align-items:flex-start;gap:10px;
                    padding:9px 0;border-bottom:1px solid #F0F0F0;">
            <div style="width:8px;height:8px;border-radius:50%;background:{dot_bg};
                        margin-top:5px;flex-shrink:0;{dot_anim}"></div>
            <div style="flex:1;min-width:0;">
                <div style="font-size:0.67rem;font-weight:700;color:{color};
                            text-transform:uppercase;letter-spacing:0.09em;">{agent}</div>
                <div style="font-size:0.82rem;color:#212121;margin-top:1px;">{step}</div>
            </div>
            <div style="font-size:0.62rem;font-weight:700;color:{dot_bg};
                        letter-spacing:0.06em;white-space:nowrap;margin-left:4px;">{tag_text}</div>
        </div>"""
    return f"""
    <div style="background:white;border:1px solid #EBEBEB;border-radius:10px;
                padding:0.85rem 1rem;box-shadow:0 2px 10px rgba(0,0,0,0.05);">
        <div style="font-size:0.67rem;font-weight:700;color:#ED1C2E;
                    text-transform:uppercase;letter-spacing:0.11em;margin-bottom:6px;">
            Agent Pipeline · Live
        </div>
        {rows_html}
    </div>"""


def run_pipeline_with_animation(parsed, step_container):
    rt = parsed["report_type"]
    fy = parsed["fy"]
    q  = parsed["quarter"]

    if rt == "bill_to_accounting":
        raw   = fetch_reinsurance_data(fy, q)
        rows  = 47
        fdata = compute_bill_to_accounting(raw)
    elif rt == "premium_listing":
        raw   = fetch_premium_data(fy, q)
        rows  = len(raw)
        fdata = compute_premium_listing(raw)
    elif rt in ("claims_recovery", "loss_run"):
        raw   = fetch_claims_data(fy, q)
        rows  = len(raw)
        fdata = compute_claims(raw)
    else:  # bordereaux
        raw   = fetch_premium_data(fy, q)
        rows  = len(raw)
        fdata = compute_premium_listing(raw)

    script    = get_agent_script(rt, fy, q, parsed["counterparty"], rows)
    completed = []
    for agent, step, delay in script:
        time.sleep(delay)
        completed.append((agent, step))
        step_container.markdown(render_agent_log(completed, running_agent=agent), unsafe_allow_html=True)

    time.sleep(0.2)
    return assemble_report(parsed, fdata, rows)

# ─────────────────────────────────────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def fmt_usd(v):
    return f"${v:,.2f}"

def badge(text, bg="#ED1C2E", fg="white"):
    return (f'<span style="background:{bg};color:{fg};padding:2px 10px;border-radius:20px;'
            f'font-size:0.68rem;font-weight:700;letter-spacing:0.05em;">{text}</span>')

def kpi(label, value, sub="", accent=False):
    border    = "2px solid #ED1C2E" if accent else "1px solid #EBEBEB"
    val_color = "#ED1C2E" if accent else "#212121"
    return f"""
    <div style="background:white;border:{border};border-radius:10px;
                padding:1.1rem 1.3rem;box-shadow:0 2px 10px rgba(0,0,0,0.05);">
        <div style="font-size:0.68rem;font-weight:600;color:#666;text-transform:uppercase;
                    letter-spacing:0.08em;margin-bottom:5px;">{label}</div>
        <div class="kpi-num" style="font-size:1.5rem;font-weight:700;color:{val_color};
                                    font-family:'DM Mono',monospace;">{value}</div>
        {f'<div style="font-size:0.74rem;color:#999;margin-top:3px;">{sub}</div>' if sub else ''}
    </div>"""

def section_header(title, subtitle=""):
    return f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:1.2rem;">
        <div style="width:4px;height:28px;background:#ED1C2E;border-radius:2px;flex-shrink:0;"></div>
        <div>
            <div style="font-size:1rem;font-weight:700;color:#212121;">{title}</div>
            {f'<div style="font-size:0.8rem;color:#666;margin-top:1px;">{subtitle}</div>' if subtitle else ''}
        </div>
    </div>"""

# ─────────────────────────────────────────────────────────────────────────────
# REPORT RENDERERS
# ─────────────────────────────────────────────────────────────────────────────
def render_bill_to_accounting(report):
    f = report["finance"]
    r = f["raw"]

    st.markdown(section_header(
        "Bill to Accounting — Reinsurance Settlement Statement",
        f"Period: {report['fy']} · {report['quarter']}  |  Treaty: {r['treaty_id']}  |  Counterparty: {report['counterparty']}"
    ), unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:white;border:1px solid #EBEBEB;border-radius:12px;
                padding:1.5rem 1.8rem;margin-bottom:1.2rem;
                box-shadow:0 3px 14px rgba(0,0,0,0.06);">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
            <div>
                <div style="font-size:0.68rem;font-weight:600;color:#666;text-transform:uppercase;
                            letter-spacing:0.09em;margin-bottom:4px;">Reinsurer</div>
                <div style="font-size:1.15rem;font-weight:700;color:#212121;">{r["reinsurer"]}</div>
                <div style="font-size:0.8rem;color:#666;margin-top:3px;">
                    Treaty {r["treaty_id"]}  ·  {", ".join(r["lines_of_business"])}  ·  {r["reinsurer_share"]} Quota Share
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:0.68rem;color:#999;text-transform:uppercase;letter-spacing:0.08em;">Report ID</div>
                <div style="font-family:'DM Mono',monospace;font-weight:600;color:#ED1C2E;font-size:1rem;">
                    {report["report_id"]}
                </div>
                <div style="margin-top:6px;">{badge("FINAL")}&nbsp;&nbsp;{badge("DEMO MODE","#666")}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi("Premiums Written",  fmt_usd(r["premiums_written"]), "Gross (100%)"),             unsafe_allow_html=True)
    with c2: st.markdown(kpi("Premiums Ceded",    fmt_usd(r["premiums_ceded"]),   f'{r["reinsurer_share"]} ceded'), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Losses Incurred",   fmt_usd(r["losses_incurred"]),  "Gross (100%)"),             unsafe_allow_html=True)
    with c4: st.markdown(kpi("Losses Ceded",      fmt_usd(r["losses_ceded"]),     "Reinsurer share"),          unsafe_allow_html=True)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    bal       = f["balance_due"]
    bal_label = "Payable to Reinsurer" if bal > 0 else "Receivable from Reinsurer"
    with c1: st.markdown(kpi("Net Premium Ceded",  fmt_usd(f["net_premium_ceded"]),    "After commission adj."),  unsafe_allow_html=True)
    with c2: st.markdown(kpi("Net Loss Recovery",  fmt_usd(f["net_loss_recovery"]),    "Ceded losses"),           unsafe_allow_html=True)
    with c3: st.markdown(kpi("Commission Adj.",    fmt_usd(f["commission_adjustment"]),"Ceding commissions"),     unsafe_allow_html=True)
    with c4: st.markdown(kpi("Balance Due",        fmt_usd(abs(bal)), bal_label, accent=True),                   unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.76rem;font-weight:700;color:#212121;text-transform:uppercase;letter-spacing:0.09em;margin-bottom:0.7rem;">Settlement Reconciliation</div>', unsafe_allow_html=True)

    recon = {
        "Line Item": [
            "Premiums Written (Gross)", "Reinsurer Share of Premiums (40%)",
            "Less: Ceding Commissions Payable", "Net Premium Due to Reinsurer", "",
            "Gross Losses Incurred", "Reinsurer Share of Losses (40%)",
            "Less: Loss Adjustment Expenses", "Net Loss Recovery Due to Cedant", "",
            "Interest on Funds Withheld", "Administration Expenses", "Settlement Balance Due",
        ],
        "Amount (USD)": [
            fmt_usd(r["premiums_written"]),   fmt_usd(r["premiums_ceded"]),
            f'({fmt_usd(r["commissions_paid"])})', fmt_usd(f["net_premium_ceded"]), "—",
            fmt_usd(r["losses_incurred"]),    fmt_usd(r["losses_ceded"]),
            f'({fmt_usd(r["admin_expenses"]*0.3)})', fmt_usd(f["net_loss_recovery"]), "—",
            fmt_usd(r["interest_income"]),    f'({fmt_usd(r["admin_expenses"])})', fmt_usd(abs(bal)),
        ],
        "Notes": [
            "All lines of business", "Quota share — 40%", "Per treaty schedule",
            "Net of commissions", "",
            "All lines of business", "Proportional share", "LAE @ 30% of admin",
            "Ceded proportionally", "",
            "Funds withheld rate 4.2%", "Pro-rated Q allocation",
            "DUE TO REINSURER" if bal > 0 else "DUE FROM REINSURER",
        ],
    }
    st.dataframe(pd.DataFrame(recon), use_container_width=True, hide_index=True, height=490)


def render_premium_listing(report):
    f = report["finance"]
    st.markdown(section_header(
        "Premium Listing",
        f"{report['fy']} · {report['quarter']}  |  {report['counterparty']}"
    ), unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(kpi("Total Gross Premium", fmt_usd(f["total_gross"]), f'{len(f["rows"])} policies'), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Total Ceded Premium", fmt_usd(f["total_ceded"]), "40% quota share"),            unsafe_allow_html=True)
    with c3: st.markdown(kpi("Total Net Retained",  fmt_usd(f["total_net"]),  "60% retention", accent=True), unsafe_allow_html=True)
    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    df = pd.DataFrame(f["rows"])
    for col in ["Gross Premium", "Ceded Premium", "Net Retained"]:
        df[col] = df[col].apply(fmt_usd)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_claims(report):
    f = report["finance"]
    st.markdown(section_header(
        report["report_label"],
        f"{report['fy']} · {report['quarter']}  |  {report['counterparty']}"
    ), unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi("Total Incurred",      fmt_usd(f["total_incurred"]),  "Gross losses"),           unsafe_allow_html=True)
    with c2: st.markdown(kpi("Total Recovered",     fmt_usd(f["total_recovered"]), "Reinsurer share"),        unsafe_allow_html=True)
    with c3: st.markdown(kpi("Net Loss (Retained)", fmt_usd(f["total_net_loss"]),  "Cedant share", accent=True), unsafe_allow_html=True)
    with c4: st.markdown(kpi("Open Claims",         str(f["open_claims"]),         "Pending settlement"),     unsafe_allow_html=True)
    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    df = pd.DataFrame(f["rows"])
    for col in ["Incurred", "Recovered", "Net Loss", "Reserve"]:
        if col in df.columns:
            df[col] = df[col].apply(fmt_usd)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_report(report):
    rt = report["report_type"]
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;
                flex-wrap:wrap;gap:0.8rem;margin-bottom:1.2rem;">
        <div>
            <div style="font-size:0.66rem;color:#999;text-transform:uppercase;font-weight:700;letter-spacing:0.09em;">
                Report ID: {report["report_id"]}
            </div>
            <div style="font-size:0.8rem;color:#666;margin-top:2px;">
                Generated {report["generated_at"]}  ·  Source: {report["data_source"]}  ·  {report["rows_fetched"]} records
            </div>
        </div>
        <div>{badge("FINAL")}&nbsp;{badge("DEMO MODE","#666")}</div>
    </div>
    """, unsafe_allow_html=True)

    if rt == "bill_to_accounting":
        render_bill_to_accounting(report)
    elif rt == "premium_listing":
        render_premium_listing(report)
    else:
        render_claims(report)

# ─────────────────────────────────────────────────────────────────────────────
# CHAT MESSAGE BUILDERS
# ─────────────────────────────────────────────────────────────────────────────
def build_assistant_message(report):
    bal     = report["finance"].get("balance_due", 0)
    bal_str = (f"<b>Settlement balance: ${abs(bal):,.2f} "
               f"{'payable to reinsurer' if bal > 0 else 'receivable from reinsurer'}</b><br><br>") if bal else ""
    return (
        f"Report generated successfully.<br><br>"
        f"<b>{report['report_label']}</b> for <b>{report['counterparty']}</b> — "
        f"<b>{report['fy']} {report['quarter']}</b><br><br>"
        f"{bal_str}"
        f"<span style='font-family:DM Mono,monospace;font-size:0.84em;color:#ED1C2E;'>"
        f"Report ID: {report['report_id']}</span>"
        f"&nbsp; · &nbsp;{report['rows_fetched']} records from Oracle<br><br>"
        f"Open the <b>Report Viewer</b> tab to view the full output."
    )

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:

    # Logo
    st.markdown("""
    <div style="padding:1.4rem 1.4rem 1rem;border-bottom:1px solid #EBEBEB;">
        <div style="display:flex;align-items:center;gap:11px;margin-bottom:10px;">
            <div style="width:38px;height:38px;background:#ED1C2E;border-radius:9px;
                        display:flex;align-items:center;justify-content:center;
                        box-shadow:0 4px 12px rgba(237,28,46,0.28);">
                <span style="color:white;font-size:1rem;font-weight:700;letter-spacing:-0.03em;">Fi</span>
            </div>
            <div>
                <div style="font-weight:700;font-size:1.05rem;color:#212121;
                            line-height:1.1;letter-spacing:-0.02em;">FinanceIQ</div>
                <div style="font-size:0.67rem;color:#999;text-transform:uppercase;letter-spacing:0.1em;">
                    Insurance · Finance Agent
                </div>
            </div>
        </div>
        <div style="display:inline-flex;align-items:center;gap:6px;background:#F0FDF4;
                    border:1px solid #BBF7D0;border-radius:20px;padding:4px 12px;">
            <div class="pulse-dot" style="width:7px;height:7px;border-radius:50%;background:#22C55E;"></div>
            <span style="font-size:0.7rem;font-weight:600;color:#15803D;">Demo Mode · No API Keys Required</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick Report
    st.markdown("""
    <div style="padding:1rem 1.2rem 0.4rem;">
        <div style="font-size:0.68rem;font-weight:700;color:#ED1C2E;
                    text-transform:uppercase;letter-spacing:0.13em;">Generate a Quick Report</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        report_labels = {v["label"]: k for k, v in REPORT_REGISTRY.items()}
        sel_label = st.selectbox("Report Type", list(report_labels.keys()), key="sb_rt")
        sel_key   = report_labels[sel_label]
        cp        = st.selectbox("Send To", COUNTERPARTIES, key="sb_cp")
        cy, cq    = st.columns(2)
        with cy: fy      = st.selectbox("Fiscal Year", ["FY2025","FY2024","FY2023"], key="sb_fy")
        with cq: quarter = st.selectbox("Quarter",     ["Q1","Q2","Q3","Q4"], index=2, key="sb_q")

        gen_btn = st.button("Generate Report", key="sb_gen", use_container_width=True)

    if gen_btn:
        parsed = {"report_type": sel_key, "counterparty": cp, "fy": fy, "quarter": quarter}
        step_ph = st.empty()
        with st.spinner(""):
            report = run_pipeline_with_animation(parsed, step_ph)
        time.sleep(0.4)
        step_ph.empty()
        st.session_state.reports.insert(0, report)
        st.session_state.messages.append({"role": "user",      "content": f"Generate a {sel_label} to {cp} using {fy}{quarter} data"})
        st.session_state.messages.append({"role": "assistant", "content": build_assistant_message(report)})
        st.session_state.messages.append({"role": "suggestions", "report_type": report["report_type"]})
        st.rerun()

    st.markdown('<hr style="margin:0.8rem 0;border-color:#EBEBEB;">', unsafe_allow_html=True)

    # Last generated
    if st.session_state.reports:
        r = st.session_state.reports[0]
        st.markdown(f"""
        <div style="padding:0 0.4rem;">
            <div style="font-size:0.68rem;font-weight:700;color:#666;text-transform:uppercase;
                        letter-spacing:0.1em;margin-bottom:0.5rem;">Last Generated</div>
            <div style="background:#F7F7F8;border-radius:8px;padding:0.7rem 0.9rem;">
                <div style="font-weight:700;font-size:0.85rem;color:#212121;">{r["report_label"]}</div>
                <div style="font-size:0.75rem;color:#666;margin-top:2px;">{r["fy"]} {r["quarter"]} · {r["counterparty"]}</div>
                <div style="font-size:0.7rem;font-family:'DM Mono',monospace;color:#ED1C2E;margin-top:4px;">{r["report_id"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Report history
    if len(st.session_state.reports) > 1:
        st.markdown("""
        <div style="padding:0.8rem 0.4rem 0.3rem;">
            <div style="font-size:0.68rem;font-weight:700;color:#666;text-transform:uppercase;letter-spacing:0.1em;">
                Report History
            </div>
        </div>
        """, unsafe_allow_html=True)
        for r in st.session_state.reports[1:6]:
            st.markdown(f"""
            <div style="padding:0.5rem 0.4rem;border-bottom:1px solid #F5F5F5;">
                <div style="font-size:0.8rem;font-weight:600;color:#212121;">{r["report_label"]}</div>
                <div style="display:flex;justify-content:space-between;margin-top:1px;">
                    <span style="font-size:0.72rem;color:#999;">{r["fy"]} {r["quarter"]} · {r["counterparty"]}</span>
                    <span style="font-size:0.68rem;font-family:'DM Mono',monospace;color:#ED1C2E;">{r["report_id"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN PANEL — TOP BAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:white;border-bottom:1px solid #EBEBEB;padding:0.85rem 2rem;
            display:flex;justify-content:space-between;align-items:center;
            box-shadow:0 1px 6px rgba(0,0,0,0.04);position:sticky;top:0;z-index:100;">
    <div>
        <div style="font-size:0.68rem;font-weight:700;color:#999;text-transform:uppercase;letter-spacing:0.1em;">
            Finance Intelligence Platform
        </div>
        <div style="font-size:1.05rem;font-weight:700;color:#212121;margin-top:1px;">
            Report Generation Agent
        </div>
    </div>
    <div style="display:flex;align-items:center;gap:1.2rem;">
        <div style="font-size:0.77rem;color:#999;">Finance Team · FY2025</div>
        <div style="display:flex;align-items:center;gap:6px;">
            <div style="width:7px;height:7px;border-radius:50%;background:#22C55E;"></div>
            <span style="font-size:0.77rem;color:#22C55E;font-weight:600;">System Online</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

P   = "padding:1.5rem 2rem;"
tab1, tab2, tab3 = st.tabs(["Agent Chat", "Report Viewer", "Architecture"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — CHAT
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)

    # Welcome banner (only shown before first message)
    if not st.session_state.messages:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#ED1C2E 0%,#B01020 100%);
                    border-radius:14px;padding:2rem;color:white;margin-bottom:1.5rem;
                    box-shadow:0 8px 32px rgba(237,28,46,0.22);">
            <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:0.13em;opacity:0.75;margin-bottom:8px;">
                Demo Mode · No API Keys Required
            </div>
            <div style="font-size:1.35rem;font-weight:700;margin-bottom:0.5rem;letter-spacing:-0.02em;">
                Welcome to FinanceIQ Agent
            </div>
            <div style="font-size:0.87rem;opacity:0.88;line-height:1.65;">
                Describe the finance report you need in plain language, or use the
                <b>Quick Report</b> panel on the left. The agent pipeline will simulate
                fetching data from Oracle, applying finance logic, and formatting the output.
            </div>
            <div style="margin-top:1.3rem;display:flex;flex-wrap:wrap;gap:0.7rem;">
                <div style="background:rgba(255,255,255,0.14);border-radius:6px;padding:7px 14px;
                            font-size:0.78rem;font-weight:500;border:1px solid rgba(255,255,255,0.2);">
                    "Generate a Bill to Accounting to Reinsurer using FY2025Q3 data"
                </div>
                <div style="background:rgba(255,255,255,0.14);border-radius:6px;padding:7px 14px;
                            font-size:0.78rem;font-weight:500;border:1px solid rgba(255,255,255,0.2);">
                    "Create a Claims Recovery Statement for Q2 2025"
                </div>
                <div style="background:rgba(255,255,255,0.14);border-radius:6px;padding:7px 14px;
                            font-size:0.78rem;font-weight:500;border:1px solid rgba(255,255,255,0.2);">
                    "Premium listing for FY2025Q1 to Broker"
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Render chat history ──────────────────────────────────────────────────
    for i, msg in enumerate(st.session_state.messages):

        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-bubble" style="display:flex;justify-content:flex-end;margin-bottom:0.8rem;">
                <div style="max-width:68%;background:#ED1C2E;color:white;
                            border-radius:14px 14px 3px 14px;padding:0.8rem 1.1rem;
                            font-size:0.88rem;line-height:1.55;
                            box-shadow:0 3px 12px rgba(237,28,46,0.18);">
                    {msg["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif msg["role"] == "assistant":
            st.markdown(f"""
            <div class="chat-bubble" style="display:flex;justify-content:flex-start;margin-bottom:0.5rem;">
                <div style="display:flex;gap:10px;align-items:flex-start;max-width:75%;">
                    <div style="width:30px;height:30px;background:#212121;border-radius:50%;
                                display:flex;align-items:center;justify-content:center;
                                flex-shrink:0;margin-top:2px;">
                        <span style="color:white;font-size:0.68rem;font-weight:700;letter-spacing:-0.03em;">Fi</span>
                    </div>
                    <div style="background:white;color:#212121;border:1px solid #EBEBEB;
                                border-radius:14px 14px 14px 3px;padding:0.85rem 1.1rem;
                                font-size:0.88rem;line-height:1.6;
                                box-shadow:0 2px 10px rgba(0,0,0,0.05);">
                        {msg["content"]}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif msg["role"] == "suggestions":
            # Render suggested follow-up queries as clickable pills
            report_type  = msg.get("report_type", "bill_to_accounting")
            suggestions  = get_suggestions(report_type)
            st.markdown("""
            <div class="suggestions-block" style="padding-left:40px;margin-bottom:1rem;">
                <div style="font-size:0.7rem;font-weight:700;color:#999;
                            text-transform:uppercase;letter-spacing:0.09em;margin-bottom:0.5rem;">
                    Suggested follow-up queries
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Two-column pill layout
            col_a, col_b = st.columns(2)
            pairs = [(suggestions[j], suggestions[j+1] if j+1 < len(suggestions) else None)
                     for j in range(0, len(suggestions), 2)]
            for left_q, right_q in pairs:
                with col_a:
                    with st.container():
                        st.markdown('<div class="suggest-btn">', unsafe_allow_html=True)
                        if st.button(left_q, key=f"sug_{i}_{left_q[:20]}"):
                            st.session_state.pending_query = left_q
                        st.markdown('</div>', unsafe_allow_html=True)
                if right_q:
                    with col_b:
                        with st.container():
                            st.markdown('<div class="suggest-btn">', unsafe_allow_html=True)
                            if st.button(right_q, key=f"sug_{i}_{right_q[:20]}"):
                                st.session_state.pending_query = right_q
                            st.markdown('</div>', unsafe_allow_html=True)

    # ── Agent log placeholder (shown during generation) ──────────────────────
    agent_log_ph = st.empty()

    # ── Input bar ────────────────────────────────────────────────────────────
    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    col_in, col_send = st.columns([6, 1])
    with col_in:
        user_query = st.text_input(
            "chat_q",
            value=st.session_state.pending_query or "",
            placeholder='e.g. "Generate a Bill to Accounting to Reinsurer using FY2025Q3 data"',
            label_visibility="collapsed",
            key="chat_input",
        )
    with col_send:
        send_btn = st.button("Send", key="chat_send", use_container_width=True)

    # Handle suggestion click (prefills the input and auto-submits next rerun)
    if st.session_state.pending_query and not send_btn:
        st.session_state.pending_query = None
        st.rerun()

    # Handle send
    submit_query = user_query.strip() if send_btn and user_query.strip() else None

    if submit_query:
        st.session_state.messages.append({"role": "user", "content": submit_query})
        parsed = parse_query(submit_query)
        with st.spinner(""):
            report = run_pipeline_with_animation(parsed, agent_log_ph)
        time.sleep(0.4)
        agent_log_ph.empty()
        st.session_state.reports.insert(0, report)
        st.session_state.messages.append({"role": "assistant", "content": build_assistant_message(report)})
        st.session_state.messages.append({"role": "suggestions", "report_type": report["report_type"]})
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — REPORT VIEWER
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)

    if not st.session_state.reports:
        st.markdown("""
        <div style="text-align:center;padding:5rem 2rem;">
            <div style="width:48px;height:48px;border:2px solid #EBEBEB;border-radius:10px;
                        display:flex;align-items:center;justify-content:center;
                        margin:0 auto 1rem;background:white;">
                <div style="font-size:1.2rem;color:#CCC;">&#9783;</div>
            </div>
            <div style="font-size:1rem;font-weight:600;color:#666;">No reports generated yet</div>
            <div style="font-size:0.85rem;color:#999;margin-top:0.4rem;">
                Use the Agent Chat or the Quick Report panel to generate your first report.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        if len(st.session_state.reports) > 1:
            opts   = {f"{r['report_id']} · {r['report_label']} ({r['fy']} {r['quarter']})": i
                      for i, r in enumerate(st.session_state.reports)}
            chosen = st.selectbox("Select Report", list(opts.keys()), key="rv_sel")
            idx    = opts[chosen]
        else:
            idx = 0

        report = st.session_state.reports[idx]

        ca, cb, _ = st.columns([1, 1, 5])
        with ca:
            st.download_button(
                "Export JSON",
                data=json.dumps(report, indent=2, default=str),
                file_name=f"{report['report_id']}.json",
                mime="application/json",
                use_container_width=True,
            )
        with cb:
            flat = {k: v for k, v in report.items() if k != "finance"}
            flat.update({f"finance_{k}": v for k, v in report["finance"].items()
                         if not isinstance(v, (list, dict))})
            st.download_button(
                "Export CSV",
                data=pd.DataFrame([flat]).to_csv(index=False),
                file_name=f"{report['report_id']}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        render_report(report)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — ARCHITECTURE
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)
    st.markdown("""
    <div style="max-width:860px;">

    <div style="font-size:1.12rem;font-weight:700;color:#212121;margin-bottom:0.3rem;">
        Agent Architecture
    </div>
    <div style="font-size:0.87rem;color:#666;margin-bottom:2rem;line-height:1.65;">
        FinanceIQ uses a three-agent LangGraph pipeline. Each agent has a discrete
        responsibility — enabling independent scaling, testing, and replacement
        without affecting the rest of the system.
    </div>

    <!-- pipeline diagram -->
    <div style="display:flex;align-items:center;overflow-x:auto;margin-bottom:2rem;padding-bottom:0.5rem;">

        <div style="background:white;border:1.5px solid #EBEBEB;border-radius:10px;
                    padding:1rem 1.2rem;min-width:130px;box-shadow:0 2px 10px rgba(0,0,0,0.05);">
            <div style="font-size:0.65rem;font-weight:700;color:#999;text-transform:uppercase;
                        letter-spacing:0.09em;margin-bottom:6px;">Input</div>
            <div style="font-weight:700;font-size:0.85rem;">User</div>
            <div style="font-size:0.7rem;color:#999;margin-top:2px;">Chat or Quick Panel</div>
        </div>

        <div style="height:2px;background:linear-gradient(90deg,#CCC,#8B5CF6);min-width:28px;flex:1;"></div>

        <div style="background:white;border:2px solid #8B5CF6;border-radius:10px;
                    padding:1rem 1.2rem;min-width:155px;box-shadow:0 4px 16px rgba(139,92,246,0.12);">
            <div style="font-size:0.65rem;font-weight:700;color:#8B5CF6;text-transform:uppercase;
                        letter-spacing:0.09em;margin-bottom:6px;">Orchestrator</div>
            <div style="font-weight:700;font-size:0.85rem;">LangGraph Router</div>
            <div style="font-size:0.7rem;color:#666;margin-top:2px;">LLM Intent Parser<br>Node dispatcher</div>
        </div>

        <div style="height:2px;background:linear-gradient(90deg,#8B5CF6,#CCC);min-width:28px;flex:1;"></div>

        <div style="display:flex;flex-direction:column;gap:10px;">

            <div style="background:white;border:1.5px solid #BFDBFE;border-radius:10px;
                        padding:0.75rem 1rem;min-width:175px;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
                <div style="font-size:0.63rem;font-weight:700;color:#1D6FA4;
                            text-transform:uppercase;letter-spacing:0.09em;">Agent 1 · Oracle</div>
                <div style="font-weight:700;font-size:0.82rem;margin-top:2px;">Data Connector</div>
                <div style="font-size:0.7rem;color:#666;margin-top:2px;">
                    Queries Oracle Financials GL,<br>claims and policy ledgers
                </div>
            </div>

            <div style="background:white;border:1.5px solid #FDE68A;border-radius:10px;
                        padding:0.75rem 1rem;min-width:175px;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
                <div style="font-size:0.63rem;font-weight:700;color:#D97706;
                            text-transform:uppercase;letter-spacing:0.09em;">Agent 2 · Finance</div>
                <div style="font-weight:700;font-size:0.82rem;margin-top:2px;">Reasoning Engine</div>
                <div style="font-size:0.7rem;color:#666;margin-top:2px;">
                    Applies accounting rules,<br>treaty logic and calculations
                </div>
            </div>

            <div style="background:white;border:1.5px solid #BBF7D0;border-radius:10px;
                        padding:0.75rem 1rem;min-width:175px;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
                <div style="font-size:0.63rem;font-weight:700;color:#1A9E5C;
                            text-transform:uppercase;letter-spacing:0.09em;">Agent 3 · Format</div>
                <div style="font-weight:700;font-size:0.82rem;margin-top:2px;">Report Formatter</div>
                <div style="font-size:0.7rem;color:#666;margin-top:2px;">
                    Structures output to standard<br>report templates
                </div>
            </div>

        </div>

        <div style="height:2px;background:linear-gradient(90deg,#CCC,#212121);min-width:28px;flex:1;"></div>

        <div style="background:#212121;border-radius:10px;padding:1rem 1.2rem;
                    min-width:130px;box-shadow:0 4px 16px rgba(0,0,0,0.14);">
            <div style="font-size:0.65rem;font-weight:700;color:#999;text-transform:uppercase;
                        letter-spacing:0.09em;margin-bottom:6px;">Output</div>
            <div style="font-weight:700;font-size:0.85rem;color:white;">Report</div>
            <div style="font-size:0.7rem;color:#999;margin-top:2px;">JSON · CSV · PDF</div>
        </div>

    </div>

    <!-- Integration status -->
    <div style="font-size:0.9rem;font-weight:700;color:#212121;margin-bottom:0.8rem;">Integration Status</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;margin-bottom:2rem;">

        <div style="background:#FFFBEB;border:1.5px solid #FDE68A;border-radius:10px;padding:1rem 1.2rem;">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
                <div style="width:8px;height:8px;border-radius:50%;background:#D97706;"></div>
                <div style="font-size:0.68rem;font-weight:700;color:#D97706;
                            text-transform:uppercase;letter-spacing:0.09em;">OpenAI API · Pending</div>
            </div>
            <div style="font-family:'DM Mono',monospace;font-size:0.74rem;color:#666;
                        word-break:break-all;margin-bottom:5px;">OPENAI_API_KEY = "sk-PLACEHOLDER"</div>
            <div style="font-size:0.72rem;color:#999;line-height:1.5;">
                Powers Orchestrator intent parsing and Agent 2 finance reasoning via LangChain
            </div>
        </div>

        <div style="background:#FFFBEB;border:1.5px solid #FDE68A;border-radius:10px;padding:1rem 1.2rem;">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
                <div style="width:8px;height:8px;border-radius:50%;background:#D97706;"></div>
                <div style="font-size:0.68rem;font-weight:700;color:#D97706;
                            text-transform:uppercase;letter-spacing:0.09em;">Oracle Financials · Pending</div>
            </div>
            <div style="font-family:'DM Mono',monospace;font-size:0.74rem;color:#666;
                        word-break:break-all;margin-bottom:5px;">ORACLE_API_BASE_URL = "https://..."</div>
            <div style="font-size:0.72rem;color:#999;line-height:1.5;">
                Agent 1 queries Oracle Cloud GL, reinsurance ledger, claims and policy tables
            </div>
        </div>

    </div>

    <!-- Demo note -->
    <div style="background:#F0FDF4;border:1.5px solid #BBF7D0;border-radius:10px;
                padding:1rem 1.3rem;margin-bottom:2rem;">
        <div style="font-size:0.68rem;font-weight:700;color:#15803D;text-transform:uppercase;
                    letter-spacing:0.09em;margin-bottom:5px;">Demo Mode Active</div>
        <div style="font-size:0.82rem;color:#166534;line-height:1.55;">
            All data shown is scripted, deterministic dummy data designed to realistically
            represent Oracle Financials output. Agent interactions are simulated with realistic
            timing and step-by-step logging. Supply API credentials above to enable live data.
        </div>
    </div>

    <!-- Tech stack -->
    <div style="font-size:0.9rem;font-weight:700;color:#212121;margin-bottom:0.8rem;">Technology Stack</div>
    <div style="display:flex;flex-wrap:wrap;gap:0.5rem;">
    """ + "".join([
        f'<div style="background:white;border:1px solid #EBEBEB;border-radius:20px;'
        f'padding:5px 14px;font-size:0.78rem;font-weight:500;color:#212121;">{t}</div>'
        for t in ["Streamlit · UI", "LangGraph · Orchestration", "LangChain · LLM Tooling",
                  "OpenAI GPT-4o · Reasoning", "Oracle REST API · Data Source",
                  "Pandas · Data Processing", "Python 3.11+"]
    ]) + """
    </div></div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
