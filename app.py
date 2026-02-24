import streamlit as st
import time
import json
import random
from datetime import datetime, date
import pandas as pd

# ─────────────────────────────────────────────
# CONFIG & THEME
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FinanceIQ · Insurance Report Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# PLACEHOLDERS – Replace before production
# ─────────────────────────────────────────────
OPENAI_API_KEY = "sk-PLACEHOLDER-YOUR-OPENAI-KEY-HERE"
ORACLE_API_BASE_URL = "https://your-oracle-instance.example.com/api/v1"
ORACLE_API_TOKEN = "PLACEHOLDER-ORACLE-API-TOKEN"
ORACLE_DB_SCHEMA = "FIN_INSURANCE"

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,300&family=DM+Mono:wght@400;500&display=swap');

/* ── Root variables ── */
:root {
    --red:       #ED1C2E;
    --red-dark:  #C0141F;
    --red-light: #FF4D5A;
    --white:     #FFFFFF;
    --black:     #212121;
    --gray-1:    #666666;
    --gray-2:    #999999;
    --gray-3:    #CCCCCC;
    --gray-4:    #F5F5F5;
    --gray-5:    #EBEBEB;
    --shadow:    0 2px 12px rgba(0,0,0,0.08);
    --shadow-lg: 0 8px 32px rgba(0,0,0,0.12);
}

/* ── Base ── */
html, body, [data-testid="stApp"], .main {
    background: #F7F7F8 !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--black) !important;
}
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--gray-5) !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Buttons ── */
.stButton > button {
    background: var(--red) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1.2rem !important;
    transition: background 0.2s, transform 0.1s, box-shadow 0.2s !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: var(--red-dark) !important;
    box-shadow: 0 4px 16px rgba(237,28,46,0.3) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    font-family: 'DM Sans', sans-serif !important;
    border: 1.5px solid var(--gray-3) !important;
    border-radius: 6px !important;
    background: white !important;
    color: var(--black) !important;
    font-size: 0.875rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--red) !important;
    box-shadow: 0 0 0 3px rgba(237,28,46,0.12) !important;
}
.stSelectbox > div > div { border: 1.5px solid var(--gray-3) !important; border-radius: 6px !important; }

/* ── Labels ── */
label, .stSelectbox label, .stTextInput label, .stTextArea label {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    color: var(--gray-1) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    margin-bottom: 4px !important;
}

/* ── Tabs ── */
[data-baseweb="tab-list"] {
    background: var(--gray-4) !important;
    border-radius: 8px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: none !important;
}
[data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    color: var(--gray-1) !important;
    border: none !important;
    padding: 8px 18px !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: white !important;
    color: var(--red) !important;
    font-weight: 700 !important;
    box-shadow: var(--shadow) !important;
}
[data-baseweb="tab-highlight"] { display: none !important; }
[data-baseweb="tab-border"] { display: none !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--red) !important; }

/* ── Divider ── */
hr { border-color: var(--gray-5) !important; margin: 1rem 0 !important; }

/* ── Alert / info boxes ── */
.stAlert { border-radius: 8px !important; font-family: 'DM Sans', sans-serif !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border-radius: 8px !important; overflow: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "reports" not in st.session_state:
    st.session_state.reports = []
if "agent_log" not in st.session_state:
    st.session_state.agent_log = []

# ─────────────────────────────────────────────
# DUMMY DATA LAYER  (Oracle API stub)
# ─────────────────────────────────────────────
def oracle_fetch_reinsurance_data(fy: str, quarter: str) -> dict:
    """
    PLACEHOLDER — Oracle API Integration
    Replace this function with actual Oracle REST/DB calls using:
        ORACLE_API_BASE_URL, ORACLE_API_TOKEN, ORACLE_DB_SCHEMA
    """
    base = 1_000_000 + random.randint(0, 500_000)
    return {
        "source": "Oracle Financials Cloud",
        "schema": ORACLE_DB_SCHEMA,
        "fy": fy,
        "quarter": quarter,
        "extracted_at": datetime.now().isoformat(),
        "premiums_written": round(base * 1.2, 2),
        "premiums_ceded": round(base * 0.4, 2),
        "losses_incurred": round(base * 0.65, 2),
        "losses_ceded": round(base * 0.22, 2),
        "commissions_paid": round(base * 0.08, 2),
        "commissions_received": round(base * 0.03, 2),
        "admin_expenses": round(base * 0.045, 2),
        "interest_income": round(base * 0.012, 2),
        "reinsurer": "Swiss Re Ltd.",
        "treaty_id": "TRY-2025-007",
        "currency": "USD",
        "lines_of_business": ["Property", "Casualty", "Marine"],
    }

def oracle_fetch_premium_listing(fy: str, quarter: str) -> list:
    """PLACEHOLDER — Oracle premium listing query."""
    policies = ["POL-10291", "POL-10388", "POL-10455", "POL-10512", "POL-10687"]
    lobs = ["Property", "Casualty", "Marine", "Casualty", "Property"]
    return [
        {
            "policy_id": p,
            "lob": lobs[i],
            "gross_premium": round(random.uniform(50000, 500000), 2),
            "ceded_pct": round(random.uniform(0.30, 0.60), 4),
            "effective_date": f"2025-{random.randint(1,3):02d}-{random.randint(1,28):02d}",
        }
        for i, p in enumerate(policies)
    ]

def oracle_fetch_claims_data(fy: str, quarter: str) -> list:
    """PLACEHOLDER — Oracle claims query."""
    claim_ids = ["CLM-8821", "CLM-8934", "CLM-9011", "CLM-9203"]
    return [
        {
            "claim_id": c,
            "lob": random.choice(["Property", "Casualty", "Marine"]),
            "incurred": round(random.uniform(20000, 900000), 2),
            "recovered": round(random.uniform(5000, 300000), 2),
            "status": random.choice(["Open", "Closed", "Pending"]),
            "reported_date": f"2025-{random.randint(7,9):02d}-{random.randint(1,28):02d}",
        }
        for c in claim_ids
    ]

# ─────────────────────────────────────────────
# AGENT SIMULATION
# ─────────────────────────────────────────────

REPORT_REGISTRY = {
    "bill_to_accounting": {
        "label": "Bill to Accounting",
        "description": "Reinsurance billing statement for accounting reconciliation.",
        "data_fn": oracle_fetch_reinsurance_data,
    },
    "premium_listing": {
        "label": "Premium Listing",
        "description": "Detailed listing of premiums written and ceded by policy.",
        "data_fn": oracle_fetch_premium_listing,
    },
    "claims_recovery": {
        "label": "Claims Recovery Statement",
        "description": "Summary of claims incurred and reinsurance recoveries.",
        "data_fn": oracle_fetch_claims_data,
    },
    "loss_run": {
        "label": "Loss Run Report",
        "description": "Period loss run by line of business.",
        "data_fn": oracle_fetch_claims_data,
    },
    "bordereaux": {
        "label": "Bordereaux Report",
        "description": "Detailed risk and premium bordereaux for treaty submission.",
        "data_fn": oracle_fetch_premium_listing,
    },
}

COUNTERPARTIES = ["Reinsurer", "Broker", "Internal Accounting", "Cedant", "Regulator"]


def parse_query_with_llm(query: str) -> dict:
    """
    PLACEHOLDER — LLM Intent Parsing (Agent 2)
    Replace with OpenAI / LangChain LLM call using OPENAI_API_KEY.
    The LLM should extract: report_type, counterparty, fy, quarter from free-text.
    """
    q = query.lower()
    report_type = "bill_to_accounting"
    for key, val in REPORT_REGISTRY.items():
        if key.replace("_", " ") in q or val["label"].lower() in q:
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
        if qn.lower() in q:
            quarter = qn
            break

    return {
        "report_type": report_type,
        "counterparty": counterparty,
        "fy": fy,
        "quarter": quarter,
    }


def agent_1_oracle_source(fy: str, quarter: str, report_type: str) -> dict:
    """Agent 1: Data Sourcing from Oracle."""
    fn = REPORT_REGISTRY[report_type]["data_fn"]
    raw = fn(fy, quarter)
    return {"status": "success", "rows_fetched": random.randint(12, 340), "payload": raw}


def agent_2_finance_reasoning(parsed: dict, raw_data: dict) -> dict:
    """Agent 2: Finance Agent — decides calculations and transformations."""
    rt = parsed["report_type"]
    p = raw_data["payload"]

    if rt == "bill_to_accounting":
        net_premium = round(p.get("premiums_ceded", 0) - p.get("commissions_received", 0), 2)
        net_loss = round(p.get("losses_ceded", 0), 2)
        balance_due = round(net_premium - net_loss - p.get("commissions_paid", 0), 2)
        return {
            "net_premium_ceded": net_premium,
            "net_loss_recovery": net_loss,
            "commission_adjustment": p.get("commissions_paid", 0),
            "balance_due": balance_due,
            "currency": p.get("currency", "USD"),
            "reinsurer": p.get("reinsurer", "N/A"),
            "treaty_id": p.get("treaty_id", "N/A"),
            "lines_of_business": p.get("lines_of_business", []),
        }
    elif rt == "premium_listing":
        rows = p if isinstance(p, list) else []
        total = sum(r.get("gross_premium", 0) for r in rows)
        total_ceded = sum(r.get("gross_premium", 0) * r.get("ceded_pct", 0) for r in rows)
        return {"rows": rows, "total_gross": round(total, 2), "total_ceded": round(total_ceded, 2)}
    else:
        rows = p if isinstance(p, list) else []
        total_inc = sum(r.get("incurred", 0) for r in rows)
        total_rec = sum(r.get("recovered", 0) for r in rows)
        return {"rows": rows, "total_incurred": round(total_inc, 2), "total_recovered": round(total_rec, 2)}


def agent_3_format_output(parsed: dict, finance_data: dict, raw_meta: dict) -> dict:
    """Agent 3: Formats output to standard report structure."""
    rt = parsed["report_type"]
    label = REPORT_REGISTRY[rt]["label"]
    report_id = f"RPT-{random.randint(10000,99999)}"
    now = datetime.now()

    return {
        "report_id": report_id,
        "report_type": rt,
        "report_label": label,
        "counterparty": parsed["counterparty"],
        "fy": parsed["fy"],
        "quarter": parsed["quarter"],
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "generated_by": "FinanceIQ Agent",
        "status": "FINAL",
        "data_source": "Oracle Financials Cloud",
        "rows_fetched": raw_meta.get("rows_fetched", 0),
        "finance_summary": finance_data,
    }


def run_agent_pipeline(query: str = None, params: dict = None) -> dict:
    """Orchestrates the 3-agent pipeline."""
    log = []

    # Intent parsing
    log.append({"agent": "Orchestrator", "step": "Parsing user intent…", "status": "running"})
    time.sleep(0.3)
    if query:
        parsed = parse_query_with_llm(query)
    else:
        parsed = params
    log.append({"agent": "Orchestrator", "step": f"Intent resolved → {parsed['report_label'] if 'report_label' in parsed else REPORT_REGISTRY[parsed['report_type']]['label']}", "status": "done"})

    # Agent 1
    log.append({"agent": "Agent 1 · Oracle Connector", "step": f"Connecting to Oracle ({ORACLE_DB_SCHEMA})…", "status": "running"})
    time.sleep(0.6)
    raw = agent_1_oracle_source(parsed["fy"], parsed["quarter"], parsed["report_type"])
    log.append({"agent": "Agent 1 · Oracle Connector", "step": f"Fetched {raw['rows_fetched']} records from {parsed['fy']} {parsed['quarter']}", "status": "done"})

    # Agent 2
    log.append({"agent": "Agent 2 · Finance Reasoning", "step": "Applying actuarial & accounting logic…", "status": "running"})
    time.sleep(0.5)
    finance_data = agent_2_finance_reasoning(parsed, raw)
    log.append({"agent": "Agent 2 · Finance Reasoning", "step": "Calculations complete. Validating against treaty rules…", "status": "done"})

    # Agent 3
    log.append({"agent": "Agent 3 · Report Formatter", "step": "Structuring output to standard template…", "status": "running"})
    time.sleep(0.3)
    report = agent_3_format_output(parsed, finance_data, raw)
    log.append({"agent": "Agent 3 · Report Formatter", "step": f"Report {report['report_id']} ready.", "status": "done"})

    st.session_state.agent_log = log
    st.session_state.reports.insert(0, report)
    return report


# ─────────────────────────────────────────────
# RENDER HELPERS
# ─────────────────────────────────────────────

def badge(text: str, color: str = "#ED1C2E") -> str:
    return f'<span style="background:{color};color:white;padding:2px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;letter-spacing:0.05em;">{text}</span>'


def kpi_card(label: str, value: str, sub: str = "") -> str:
    return f"""
    <div style="background:white;border:1px solid #EBEBEB;border-radius:10px;padding:1.1rem 1.3rem;
                box-shadow:0 2px 10px rgba(0,0,0,0.05);min-width:160px;">
        <div style="font-size:0.72rem;font-weight:600;color:#666;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">{label}</div>
        <div style="font-size:1.55rem;font-weight:700;color:#212121;font-family:'DM Mono',monospace;">{value}</div>
        {f'<div style="font-size:0.78rem;color:#999;margin-top:4px;">{sub}</div>' if sub else ''}
    </div>"""


def agent_step_html(agent: str, step: str, status: str) -> str:
    dot_color = "#ED1C2E" if status == "running" else "#28a745"
    anim = "animation:pulse 1s infinite;" if status == "running" else ""
    label = "PROCESSING" if status == "running" else "✓ DONE"
    label_color = "#ED1C2E" if status == "running" else "#28a745"
    return f"""
    <div style="display:flex;align-items:flex-start;gap:12px;padding:10px 0;border-bottom:1px solid #F5F5F5;">
        <div style="width:10px;height:10px;border-radius:50%;background:{dot_color};margin-top:5px;flex-shrink:0;{anim}"></div>
        <div style="flex:1;">
            <div style="font-size:0.72rem;font-weight:700;color:{dot_color};text-transform:uppercase;letter-spacing:0.08em;">{agent}</div>
            <div style="font-size:0.85rem;color:#212121;margin-top:2px;">{step}</div>
        </div>
        <div style="font-size:0.68rem;font-weight:700;color:{label_color};letter-spacing:0.05em;white-space:nowrap;">{label}</div>
    </div>"""


def render_bill_to_accounting(report: dict):
    fs = report["finance_summary"]
    st.markdown(f"""
    <div style="background:white;border:1px solid #EBEBEB;border-radius:12px;padding:2rem;box-shadow:0 4px 20px rgba(0,0,0,0.06);">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1.5rem;">
            <div>
                <div style="font-size:1.3rem;font-weight:700;color:#212121;">Bill to Accounting</div>
                <div style="font-size:0.85rem;color:#666;margin-top:4px;">Reinsurance Settlement Statement</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:0.75rem;color:#999;">Report ID</div>
                <div style="font-family:'DM Mono',monospace;font-weight:600;color:#ED1C2E;">{report['report_id']}</div>
                <div style="margin-top:6px;">{badge(report['status'])}</div>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.5rem;padding:1rem;background:#F7F7F8;border-radius:8px;">
            <div>
                <div style="font-size:0.72rem;color:#666;text-transform:uppercase;font-weight:600;">Reinsurer</div>
                <div style="font-weight:600;margin-top:2px;">{fs.get('reinsurer','N/A')}</div>
            </div>
            <div>
                <div style="font-size:0.72rem;color:#666;text-transform:uppercase;font-weight:600;">Treaty</div>
                <div style="font-weight:600;margin-top:2px;">{fs.get('treaty_id','N/A')}</div>
            </div>
            <div>
                <div style="font-size:0.72rem;color:#666;text-transform:uppercase;font-weight:600;">Period</div>
                <div style="font-weight:600;margin-top:2px;">{report['fy']} · {report['quarter']}</div>
            </div>
            <div>
                <div style="font-size:0.72rem;color:#666;text-transform:uppercase;font-weight:600;">Lines of Business</div>
                <div style="font-weight:600;margin-top:2px;">{', '.join(fs.get('lines_of_business',[]))}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(kpi_card("Net Premium Ceded", f"${fs.get('net_premium_ceded',0):,.0f}", fs.get('currency','USD')), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card("Net Loss Recovery", f"${fs.get('net_loss_recovery',0):,.0f}", fs.get('currency','USD')), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card("Commission Adj.", f"${fs.get('commission_adjustment',0):,.0f}", fs.get('currency','USD')), unsafe_allow_html=True)
    with col4:
        bal = fs.get('balance_due', 0)
        bal_color = "#ED1C2E" if bal > 0 else "#28a745"
        st.markdown(f"""
        <div style="background:white;border:2px solid {bal_color};border-radius:10px;padding:1.1rem 1.3rem;box-shadow:0 2px 10px rgba(0,0,0,0.05);">
            <div style="font-size:0.72rem;font-weight:600;color:{bal_color};text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Balance Due</div>
            <div style="font-size:1.55rem;font-weight:700;color:{bal_color};font-family:'DM Mono',monospace;">${bal:,.0f}</div>
            <div style="font-size:0.78rem;color:#999;margin-top:4px;">{"Payable to Reinsurer" if bal > 0 else "Receivable"}</div>
        </div>""", unsafe_allow_html=True)


def render_tabular_report(report: dict):
    fs = report["finance_summary"]
    rows = fs.get("rows", [])
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, height=280)

    cols = st.columns(3)
    for i, (key, val) in enumerate([(k, v) for k, v in fs.items() if k != "rows"]):
        with cols[i % 3]:
            st.markdown(kpi_card(key.replace("_", " ").title(), f"${val:,.0f}" if isinstance(val, (int, float)) else str(val)), unsafe_allow_html=True)


def render_report(report: dict):
    rt = report["report_type"]
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:1rem;">
        <div style="width:4px;height:32px;background:#ED1C2E;border-radius:2px;"></div>
        <div>
            <div style="font-size:1.05rem;font-weight:700;color:#212121;">{report['report_label']}</div>
            <div style="font-size:0.8rem;color:#666;">Generated {report['generated_at']} · Source: {report['data_source']} · {report['rows_fetched']} records</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if rt == "bill_to_accounting":
        render_bill_to_accounting(report)
    else:
        render_tabular_report(report)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    # Logo area
    st.markdown("""
    <div style="padding:1.5rem 1.2rem 1rem;border-bottom:1px solid #EBEBEB;">
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:36px;height:36px;background:#ED1C2E;border-radius:8px;display:flex;align-items:center;justify-content:center;">
                <span style="color:white;font-size:1.1rem;">⬡</span>
            </div>
            <div>
                <div style="font-weight:700;font-size:1rem;color:#212121;line-height:1.1;">FinanceIQ</div>
                <div style="font-size:0.7rem;color:#999;text-transform:uppercase;letter-spacing:0.08em;">Insurance · Finance Agent</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:1rem 1.2rem 0.4rem;">
        <div style="font-size:0.72rem;font-weight:700;color:#ED1C2E;text-transform:uppercase;letter-spacing:0.1em;">Generate a Quick Report</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="padding:0 0.4rem;">', unsafe_allow_html=True)

        report_options = {v["label"]: k for k, v in REPORT_REGISTRY.items()}
        selected_report_label = st.selectbox(
            "Report Type",
            list(report_options.keys()),
            key="sb_report_type",
        )
        selected_report_key = report_options[selected_report_label]

        counterparty = st.selectbox(
            "Send To",
            COUNTERPARTIES,
            key="sb_counterparty",
        )

        col_y, col_q = st.columns(2)
        with col_y:
            fy = st.selectbox("Fiscal Year", ["FY2025", "FY2024", "FY2023"], key="sb_fy")
        with col_q:
            quarter = st.selectbox("Quarter", ["Q1", "Q2", "Q3", "Q4"], index=2, key="sb_quarter")

        if st.button("🚀  Generate Report", key="sidebar_gen", use_container_width=True):
            params = {
                "report_type": selected_report_key,
                "report_label": selected_report_label,
                "counterparty": counterparty,
                "fy": fy,
                "quarter": quarter,
            }
            with st.spinner("Agent pipeline running…"):
                report = run_agent_pipeline(params=params)
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"✅ **{report['report_label']}** for **{counterparty}** ({fy} {quarter}) generated. Report ID: `{report['report_id']}`",
                "report_id": report["report_id"],
            })
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr style="margin:1rem 0;">', unsafe_allow_html=True)

    # Report History
    st.markdown("""
    <div style="padding:0 0.4rem 0.4rem;">
        <div style="font-size:0.72rem;font-weight:700;color:#666;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem;">Recent Reports</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.reports:
        for r in st.session_state.reports[:5]:
            st.markdown(f"""
            <div style="padding:0.6rem 0.4rem;border-bottom:1px solid #F5F5F5;cursor:pointer;">
                <div style="font-size:0.8rem;font-weight:600;color:#212121;">{r['report_label']}</div>
                <div style="display:flex;justify-content:space-between;margin-top:2px;">
                    <span style="font-size:0.72rem;color:#999;">{r['fy']} {r['quarter']} · {r['counterparty']}</span>
                    <span style="font-size:0.68rem;font-family:'DM Mono',monospace;color:#ED1C2E;">{r['report_id']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="padding:0.4rem;font-size:0.82rem;color:#999;">No reports yet.</div>', unsafe_allow_html=True)

    # Agent status
    if st.session_state.agent_log:
        st.markdown('<hr style="margin:1rem 0;">', unsafe_allow_html=True)
        st.markdown("""
        <div style="padding:0 0.4rem 0.4rem;">
            <div style="font-size:0.72rem;font-weight:700;color:#666;text-transform:uppercase;letter-spacing:0.1em;">Agent Activity Log</div>
        </div>
        """, unsafe_allow_html=True)
        log_html = ""
        for entry in st.session_state.agent_log:
            log_html += agent_step_html(entry["agent"], entry["step"], entry["status"])
        st.markdown(f'<div style="padding:0 0.4rem;">{log_html}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN PANEL
# ─────────────────────────────────────────────

# Top header bar
st.markdown("""
<div style="background:white;border-bottom:1px solid #EBEBEB;padding:1rem 2rem;display:flex;
            justify-content:space-between;align-items:center;box-shadow:0 1px 6px rgba(0,0,0,0.04);">
    <div>
        <span style="font-size:0.72rem;font-weight:700;color:#999;text-transform:uppercase;letter-spacing:0.08em;">Finance Intelligence Platform</span>
        <div style="font-size:1.15rem;font-weight:700;color:#212121;margin-top:2px;">Report Generation Agent</div>
    </div>
    <div style="display:flex;align-items:center;gap:16px;">
        <div style="font-size:0.8rem;color:#999;">Finance Team · Q3 2025</div>
        <div style="width:8px;height:8px;border-radius:50%;background:#28a745;"></div>
        <div style="font-size:0.8rem;color:#28a745;font-weight:600;">System Online</div>
    </div>
</div>
""", unsafe_allow_html=True)

main_pad = "padding:1.5rem 2rem;"

# Tabs
tab1, tab2, tab3 = st.tabs(["💬  Agent Chat", "📄  Report Viewer", "ℹ️  Architecture"])

# ─────────────── TAB 1: CHAT ───────────────
with tab1:
    st.markdown(f'<div style="{main_pad}">', unsafe_allow_html=True)

    # Welcome banner
    if not st.session_state.messages:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#ED1C2E 0%,#C0141F 100%);
                    border-radius:12px;padding:2rem;color:white;margin-bottom:1.5rem;">
            <div style="font-size:1.4rem;font-weight:700;margin-bottom:0.5rem;">Welcome to FinanceIQ Agent</div>
            <div style="font-size:0.9rem;opacity:0.9;line-height:1.6;">
                Describe the report you need in plain language, or use the Quick Report panel on the left.
            </div>
            <div style="margin-top:1.2rem;display:flex;gap:0.8rem;flex-wrap:wrap;">
                <div style="background:rgba(255,255,255,0.15);border-radius:20px;padding:6px 16px;font-size:0.8rem;font-weight:500;">
                    💡 "Generate a Bill to Accounting to Reinsurer using FY2025Q3 data"
                </div>
                <div style="background:rgba(255,255,255,0.15);border-radius:20px;padding:6px 16px;font-size:0.8rem;font-weight:500;">
                    💡 "Create a Claims Recovery Statement for Q2 2025"
                </div>
                <div style="background:rgba(255,255,255,0.15);border-radius:20px;padding:6px 16px;font-size:0.8rem;font-weight:500;">
                    💡 "Premium listing for FY2025Q1 to Broker"
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state.messages:
        is_user = msg["role"] == "user"
        bg = "#ED1C2E" if is_user else "white"
        txt_color = "white" if is_user else "#212121"
        align = "flex-end" if is_user else "flex-start"
        border = "" if is_user else "border:1px solid #EBEBEB;"
        st.markdown(f"""
        <div style="display:flex;justify-content:{align};margin-bottom:1rem;">
            <div style="max-width:72%;background:{bg};color:{txt_color};
                        border-radius:12px;padding:0.85rem 1.1rem;
                        {border}box-shadow:0 2px 8px rgba(0,0,0,0.06);
                        font-size:0.9rem;line-height:1.5;">
                {msg['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Input
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    with st.container():
        col_input, col_send = st.columns([6, 1])
        with col_input:
            user_query = st.text_input(
                "query_input",
                placeholder="e.g. Generate a Bill to Accounting to Reinsurer using FY2025Q3 data…",
                label_visibility="collapsed",
                key="chat_input",
            )
        with col_send:
            send = st.button("Send →", key="chat_send", use_container_width=True)

    if send and user_query.strip():
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.spinner("Agents working…"):
            report = run_agent_pipeline(query=user_query)
        resp = f"""✅ Report generated successfully!<br><br>
        <b>{report['report_label']}</b> for <b>{report['counterparty']}</b><br>
        Period: {report['fy']} · {report['quarter']}<br>
        Report ID: <code>{report['report_id']}</code> · {report['rows_fetched']} records fetched from Oracle<br><br>
        Switch to the <b>Report Viewer</b> tab to view the full report."""
        st.session_state.messages.append({"role": "assistant", "content": resp, "report_id": report["report_id"]})
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────── TAB 2: REPORT VIEWER ───────────────
with tab2:
    st.markdown(f'<div style="{main_pad}">', unsafe_allow_html=True)

    if not st.session_state.reports:
        st.markdown("""
        <div style="text-align:center;padding:4rem 2rem;color:#999;">
            <div style="font-size:3rem;margin-bottom:1rem;">📋</div>
            <div style="font-size:1rem;font-weight:600;color:#666;">No reports generated yet</div>
            <div style="font-size:0.85rem;margin-top:0.5rem;">Use the chat or Quick Report panel to generate your first report.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Selector if multiple reports
        if len(st.session_state.reports) > 1:
            options = {f"{r['report_id']} · {r['report_label']} ({r['fy']} {r['quarter']})": i
                       for i, r in enumerate(st.session_state.reports)}
            selected_label = st.selectbox("Select Report", list(options.keys()), key="report_selector")
            selected_idx = options[selected_label]
        else:
            selected_idx = 0

        report = st.session_state.reports[selected_idx]

        # Report actions row
        col_a, col_b, col_c, _ = st.columns([1, 1, 1, 3])
        with col_a:
            st.download_button(
                "⬇ Export JSON",
                data=json.dumps(report, indent=2),
                file_name=f"{report['report_id']}.json",
                mime="application/json",
                use_container_width=True,
            )
        with col_b:
            csv_data = pd.DataFrame([report]).to_csv(index=False)
            st.download_button(
                "⬇ Export CSV",
                data=csv_data,
                file_name=f"{report['report_id']}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        render_report(report)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────── TAB 3: ARCHITECTURE ───────────────
with tab3:
    st.markdown(f'<div style="{main_pad}">', unsafe_allow_html=True)
    st.markdown("""
    <div style="max-width:820px;">

    <div style="font-size:1.2rem;font-weight:700;color:#212121;margin-bottom:0.4rem;">Agent Architecture</div>
    <div style="font-size:0.88rem;color:#666;margin-bottom:2rem;">
        FinanceIQ uses a three-agent LangGraph pipeline orchestrated by a central router.
        Each agent has a discrete responsibility, enabling modular upgrades and independent scaling.
    </div>

    <!-- Pipeline diagram -->
    <div style="display:flex;align-items:center;gap:0;margin-bottom:2rem;overflow-x:auto;">

        <div style="background:white;border:1.5px solid #EBEBEB;border-radius:10px;padding:1rem 1.2rem;min-width:160px;box-shadow:0 2px 10px rgba(0,0,0,0.05);">
            <div style="width:32px;height:32px;background:#F5F5F5;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1rem;margin-bottom:8px;">👤</div>
            <div style="font-weight:700;font-size:0.85rem;">User</div>
            <div style="font-size:0.72rem;color:#999;margin-top:3px;">Chat or Quick Panel</div>
        </div>

        <div style="flex:1;height:2px;background:linear-gradient(90deg,#CCCCCC,#ED1C2E);min-width:30px;"></div>

        <div style="background:white;border:2px solid #ED1C2E;border-radius:10px;padding:1rem 1.2rem;min-width:160px;box-shadow:0 4px 16px rgba(237,28,46,0.15);">
            <div style="width:32px;height:32px;background:#ED1C2E;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1rem;margin-bottom:8px;">⬡</div>
            <div style="font-weight:700;font-size:0.85rem;color:#ED1C2E;">Orchestrator</div>
            <div style="font-size:0.72rem;color:#666;margin-top:3px;">LLM Intent Parser<br>LangGraph Router</div>
        </div>

        <div style="flex:1;height:2px;background:linear-gradient(90deg,#ED1C2E,#CCCCCC);min-width:30px;"></div>

        <div style="display:flex;flex-direction:column;gap:10px;">

            <div style="background:white;border:1.5px solid #EBEBEB;border-radius:10px;padding:0.8rem 1rem;min-width:160px;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
                <div style="font-size:0.68rem;font-weight:700;color:#ED1C2E;text-transform:uppercase;letter-spacing:0.08em;">Agent 1</div>
                <div style="font-weight:700;font-size:0.85rem;margin-top:3px;">Oracle Connector</div>
                <div style="font-size:0.72rem;color:#666;margin-top:2px;">Fetches raw financial data<br>via Oracle REST API</div>
            </div>

            <div style="background:white;border:1.5px solid #EBEBEB;border-radius:10px;padding:0.8rem 1rem;min-width:160px;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
                <div style="font-size:0.68rem;font-weight:700;color:#ED1C2E;text-transform:uppercase;letter-spacing:0.08em;">Agent 2</div>
                <div style="font-weight:700;font-size:0.85rem;margin-top:3px;">Finance Reasoning</div>
                <div style="font-size:0.72rem;color:#666;margin-top:2px;">Applies accounting &<br>actuarial business logic</div>
            </div>

            <div style="background:white;border:1.5px solid #EBEBEB;border-radius:10px;padding:0.8rem 1rem;min-width:160px;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
                <div style="font-size:0.68rem;font-weight:700;color:#ED1C2E;text-transform:uppercase;letter-spacing:0.08em;">Agent 3</div>
                <div style="font-weight:700;font-size:0.85rem;margin-top:3px;">Report Formatter</div>
                <div style="font-size:0.72rem;color:#666;margin-top:2px;">Structures output to<br>standard report templates</div>
            </div>

        </div>

        <div style="flex:1;height:2px;background:linear-gradient(90deg,#CCCCCC,#212121);min-width:30px;"></div>

        <div style="background:#212121;border-radius:10px;padding:1rem 1.2rem;min-width:140px;box-shadow:0 4px 16px rgba(0,0,0,0.15);">
            <div style="width:32px;height:32px;background:rgba(237,28,46,0.2);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1rem;margin-bottom:8px;">📄</div>
            <div style="font-weight:700;font-size:0.85rem;color:white;">Report Output</div>
            <div style="font-size:0.72rem;color:#999;margin-top:3px;">JSON / PDF / CSV</div>
        </div>

    </div>

    <!-- Integration placeholders -->
    <div style="font-size:1rem;font-weight:700;color:#212121;margin-bottom:1rem;">Integration Placeholders</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:2rem;">

        <div style="background:#FFF5F5;border:1.5px solid #FFCDD2;border-radius:10px;padding:1.1rem;">
            <div style="font-size:0.72rem;font-weight:700;color:#ED1C2E;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">🔑 OpenAI API</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.78rem;color:#666;word-break:break-all;">OPENAI_API_KEY = "sk-PLACEHOLDER…"</div>
            <div style="font-size:0.75rem;color:#999;margin-top:6px;">Used by Orchestrator for intent parsing & Agent 2 for finance reasoning</div>
        </div>

        <div style="background:#FFF5F5;border:1.5px solid #FFCDD2;border-radius:10px;padding:1.1rem;">
            <div style="font-size:0.72rem;font-weight:700;color:#ED1C2E;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">🗄️ Oracle Financials API</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.78rem;color:#666;word-break:break-all;">ORACLE_API_BASE_URL = "https://…"</div>
            <div style="font-size:0.75rem;color:#999;margin-top:6px;">Agent 1 connects to Oracle Cloud Financials for live ledger & claims data</div>
        </div>

    </div>

    <!-- Tech stack -->
    <div style="font-size:1rem;font-weight:700;color:#212121;margin-bottom:1rem;">Technology Stack</div>
    <div style="display:flex;flex-wrap:wrap;gap:0.6rem;">
        """ + "".join([
        f'<div style="background:white;border:1px solid #EBEBEB;border-radius:20px;padding:6px 14px;font-size:0.8rem;font-weight:500;color:#212121;">{t}</div>'
        for t in ["Streamlit · UI", "LangGraph · Agent Orchestration", "LangChain · LLM Integration",
                  "OpenAI GPT-4o · Reasoning LLM", "Oracle REST API · Data Source",
                  "Pandas · Data Processing", "Python 3.11+"]
    ]) + """
    </div>

    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
