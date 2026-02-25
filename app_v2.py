"""
FinanceIQ · Oracle Finance Platform — DEMO MODE
================================================
One-stop platform for Oracle Financials interaction:
  · Finance Report Generation (3-agent pipeline)
  · Report Viewer with export
  · Oracle Data Entry (GL, AP, AR, Policy, Claims)
  · Architecture reference

No API keys required for demo.
Replace stubs marked ← REPLACE WITH LIVE INTEGRATION before production.
"""

import streamlit as st
import time
import json
import random
from datetime import datetime, date
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinanceIQ · Oracle Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# LIVE INTEGRATION PLACEHOLDERS
# ─────────────────────────────────────────────────────────────────────────────
OPENAI_API_KEY      = "sk-PLACEHOLDER"                      # ← REPLACE WITH LIVE INTEGRATION
ORACLE_API_BASE_URL = "https://oracle.example.com/api/v1"  # ← REPLACE WITH LIVE INTEGRATION
ORACLE_API_TOKEN    = "ORACLE-TOKEN-PLACEHOLDER"            # ← REPLACE WITH LIVE INTEGRATION
ORACLE_DB_SCHEMA    = "FIN_INSURANCE"

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Mono:wght@400;500&display=swap');

:root {
    --red:    #ED1C2E;  --red-dk: #C0141F;
    --white:  #FFFFFF;  --black:  #212121;
    --g1:     #666666;  --g2:     #999999;
    --g3:     #CCCCCC;  --g4:     #F5F5F5;
    --g5:     #EBEBEB;  --green:  #1A9E5C;
    --amber:  #D97706;  --blue:   #1D6FA4;
    --shadow: 0 2px 12px rgba(0,0,0,0.07);
}

html, body, [data-testid="stApp"], .main {
    background: #F4F4F6 !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--black) !important;
}
.block-container { padding:0 !important; max-width:100% !important; }

[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--g5) !important;
    box-shadow: 2px 0 16px rgba(0,0,0,0.04) !important;
    min-width: 310px !important;
}
[data-testid="stSidebar"] > div:first-child { padding:0 !important; }

#MainMenu, footer, header { visibility:hidden; }
[data-testid="stToolbar"] { display:none; }

/* Primary button */
.stButton > button {
    background: var(--red) !important; color: white !important;
    border: none !important; border-radius: 7px !important;
    font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important;
    font-size: 0.85rem !important; padding: 0.52rem 1.2rem !important;
    transition: background 0.18s, transform 0.1s, box-shadow 0.18s !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    background: var(--red-dk) !important;
    box-shadow: 0 4px 18px rgba(237,28,46,0.28) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Suggestion pills */
.suggest-btn > button {
    background: white !important; color: var(--black) !important;
    border: 1.5px solid var(--g5) !important; border-radius: 6px !important;
    font-size: 0.8rem !important; font-weight: 500 !important;
    padding: 0.4rem 0.9rem !important; letter-spacing: 0 !important;
    text-align: left !important; white-space: normal !important;
    height: auto !important; line-height: 1.4 !important;
}
.suggest-btn > button:hover {
    background: #FFF5F5 !important; border-color: var(--red) !important;
    color: var(--red) !important; box-shadow: none !important; transform: none !important;
}

/* GL entry type selector pills */
.entry-pill > button {
    background: white !important; color: var(--g1) !important;
    border: 1.5px solid var(--g5) !important; border-radius: 6px !important;
    font-size: 0.78rem !important; font-weight: 600 !important;
    padding: 0.45rem 0.8rem !important; letter-spacing: 0.01em !important;
    text-align: center !important;
}
.entry-pill > button:hover {
    border-color: var(--red) !important; color: var(--red) !important;
    background: #FFF5F5 !important; box-shadow: none !important; transform: none !important;
}
.entry-pill-active > button {
    background: var(--red) !important; color: white !important;
    border-color: var(--red) !important; box-shadow: none !important; transform: none !important;
}
.entry-pill-active > button:hover {
    background: var(--red-dk) !important; color: white !important;
    box-shadow: 0 2px 8px rgba(237,28,46,0.3) !important;
}

/* Confirm/approve button - green */
.confirm-btn > button {
    background: #1A9E5C !important; color: white !important;
    border: none !important;
}
.confirm-btn > button:hover {
    background: #158A4E !important;
    box-shadow: 0 4px 14px rgba(26,158,92,0.3) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    font-family: 'DM Sans', sans-serif !important;
    border: 1.5px solid var(--g3) !important; border-radius: 7px !important;
    background: white !important; color: var(--black) !important;
    font-size: 0.875rem !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--red) !important;
    box-shadow: 0 0 0 3px rgba(237,28,46,0.11) !important; outline: none !important;
}
.stSelectbox > div > div, .stDateInput > div > div {
    border: 1.5px solid var(--g3) !important; border-radius: 7px !important;
    background: white !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 0.875rem !important;
}
.stNumberInput > div > div { border-radius: 7px !important; }

label, .stSelectbox label, .stTextInput label,
.stTextArea label, .stNumberInput label, .stDateInput label {
    font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important;
    font-size: 0.73rem !important; color: var(--g1) !important;
    text-transform: uppercase !important; letter-spacing: 0.07em !important;
}

/* Tabs */
[data-baseweb="tab-list"] {
    background: var(--g4) !important; border-radius: 9px !important;
    padding: 4px !important; gap: 3px !important; border: none !important;
}
[data-baseweb="tab"] {
    background: transparent !important; border-radius: 7px !important;
    font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important;
    font-size: 0.84rem !important; color: var(--g1) !important;
    border: none !important; padding: 8px 18px !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: white !important; color: var(--red) !important;
    font-weight: 700 !important; box-shadow: var(--shadow) !important;
}
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] { display:none !important; }

[data-testid="stDataFrame"] { border-radius: 9px !important; overflow: hidden !important; }
[data-testid="stDataFrame"] table { font-family: 'DM Mono', monospace !important; font-size: 0.8rem !important; }
[data-testid="stDataFrame"] th { background: #F5F5F5 !important; font-weight: 700 !important; color: #212121 !important; }

.stSpinner > div { border-top-color: var(--red) !important; }
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-thumb { background:#CCCCCC; border-radius:3px; }

@keyframes pulse-dot  { 0%,100%{opacity:1}  50%{opacity:0.45} }
@keyframes slide-in   { from{opacity:0;transform:translateX(-8px)} to{opacity:1;transform:translateX(0)} }
@keyframes bubble-in  { from{opacity:0;transform:translateY(6px)}  to{opacity:1;transform:translateY(0)} }
@keyframes count-up   { from{opacity:0;transform:translateY(4px)}  to{opacity:1;transform:translateY(0)} }
@keyframes fade-in    { from{opacity:0} to{opacity:1} }
@keyframes pop-in     { from{opacity:0;transform:scale(0.96)} to{opacity:1;transform:scale(1)} }

.pulse-dot        { animation: pulse-dot 1.8s infinite; }
.agent-step       { animation: slide-in 0.3s ease; }
.chat-bubble      { animation: bubble-in 0.25s ease; }
.kpi-num          { animation: count-up 0.4s ease 0.1s both; }
.suggestions-block{ animation: fade-in 0.4s ease 0.2s both; }
.entry-card       { animation: pop-in 0.2s ease; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
defaults = {
    "messages":           [],
    "reports":            [],
    "pending_query":      None,
    "gl_messages":        [],     # GL chatbot history
    "gl_entries":         [],     # submitted GL journal entries
    "gl_pending":         None,   # parsed entry awaiting confirm
    "gl_active_type":     "Journal Entry",
    "oracle_log":         [],     # audit log of all oracle write operations
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# REPORT STATIC DATA
# ─────────────────────────────────────────────────────────────────────────────
DEMO_REINSURANCE = {
    ("FY2025","Q3"): {"premiums_written":14_820_450.00,"premiums_ceded":5_928_180.00,"losses_incurred":9_633_292.50,"losses_ceded":3_267_499.00,"commissions_paid":1_185_636.00,"commissions_received":474_254.40,"admin_expenses":667_320.00,"interest_income":177_845.40,"reinsurer":"Swiss Re Ltd.","treaty_id":"TRY-2025-007","currency":"USD","lines_of_business":["Property","Casualty","Marine"],"cedant_share":"60%","reinsurer_share":"40%"},
    ("FY2025","Q2"): {"premiums_written":13_210_000.00,"premiums_ceded":5_284_000.00,"losses_incurred":8_586_500.00,"losses_ceded":2_999_100.00,"commissions_paid":1_056_800.00,"commissions_received":422_720.00,"admin_expenses":594_450.00,"interest_income":158_520.00,"reinsurer":"Munich Re","treaty_id":"TRY-2025-007","currency":"USD","lines_of_business":["Property","Casualty"],"cedant_share":"60%","reinsurer_share":"40%"},
    ("FY2024","Q4"): {"premiums_written":12_950_000.00,"premiums_ceded":5_180_000.00,"losses_incurred":8_250_000.00,"losses_ceded":2_880_000.00,"commissions_paid":1_036_000.00,"commissions_received":414_400.00,"admin_expenses":583_000.00,"interest_income":155_400.00,"reinsurer":"Hannover Re","treaty_id":"TRY-2024-004","currency":"USD","lines_of_business":["Property","Casualty","Marine","Aviation"],"cedant_share":"60%","reinsurer_share":"40%"},
}
DEMO_PREMIUMS = {
    ("FY2025","Q3"): [
        {"Policy ID":"POL-10291","Insured":"Meridian Logistics Inc.","LOB":"Marine","Gross Premium":487_250.00,"Ceded %":"40.0%","Ceded Premium":194_900.00,"Net Retained":292_350.00,"Effective Date":"2025-07-01","Expiry":"2026-07-01","Status":"Active"},
        {"Policy ID":"POL-10388","Insured":"Baxter Steel Corp.","LOB":"Property","Gross Premium":372_800.00,"Ceded %":"40.0%","Ceded Premium":149_120.00,"Net Retained":223_680.00,"Effective Date":"2025-07-15","Expiry":"2026-07-15","Status":"Active"},
        {"Policy ID":"POL-10455","Insured":"Coastal RE Holdings","LOB":"Casualty","Gross Premium":298_600.00,"Ceded %":"40.0%","Ceded Premium":119_440.00,"Net Retained":179_160.00,"Effective Date":"2025-08-01","Expiry":"2026-08-01","Status":"Active"},
        {"Policy ID":"POL-10512","Insured":"Pacific Cargo Group","LOB":"Marine","Gross Premium":521_400.00,"Ceded %":"40.0%","Ceded Premium":208_560.00,"Net Retained":312_840.00,"Effective Date":"2025-08-15","Expiry":"2026-08-15","Status":"Active"},
        {"Policy ID":"POL-10687","Insured":"Allied Construction LLC","LOB":"Property","Gross Premium":443_100.00,"Ceded %":"40.0%","Ceded Premium":177_240.00,"Net Retained":265_860.00,"Effective Date":"2025-09-01","Expiry":"2026-09-01","Status":"Active"},
        {"Policy ID":"POL-10734","Insured":"Northern Energy Co.","LOB":"Casualty","Gross Premium":315_200.00,"Ceded %":"40.0%","Ceded Premium":126_080.00,"Net Retained":189_120.00,"Effective Date":"2025-09-15","Expiry":"2026-09-15","Status":"Active"},
    ],
}
DEMO_CLAIMS = {
    ("FY2025","Q3"): [
        {"Claim ID":"CLM-8821","Insured":"Meridian Logistics Inc.","LOB":"Marine","Cause":"Storm Damage","Incurred":892_400.00,"Recovered":356_960.00,"Net Loss":535_440.00,"Reported":"2025-07-14","Status":"Open","Reserve":450_000.00},
        {"Claim ID":"CLM-8934","Insured":"Baxter Steel Corp.","LOB":"Property","Cause":"Fire","Incurred":1_240_000.00,"Recovered":496_000.00,"Net Loss":744_000.00,"Reported":"2025-07-28","Status":"Open","Reserve":900_000.00},
        {"Claim ID":"CLM-9011","Insured":"Allied Construction LLC","LOB":"Property","Cause":"Water Damage","Incurred":367_800.00,"Recovered":147_120.00,"Net Loss":220_680.00,"Reported":"2025-08-05","Status":"Closed","Reserve":0},
        {"Claim ID":"CLM-9203","Insured":"Coastal RE Holdings","LOB":"Casualty","Cause":"Liability","Incurred":543_200.00,"Recovered":217_280.00,"Net Loss":325_920.00,"Reported":"2025-08-22","Status":"Pending","Reserve":300_000.00},
        {"Claim ID":"CLM-9417","Insured":"Pacific Cargo Group","LOB":"Marine","Cause":"Cargo Theft","Incurred":224_292.50,"Recovered":89_717.00,"Net Loss":134_575.50,"Reported":"2025-09-03","Status":"Closed","Reserve":0},
    ],
}

def _get_pool(pool, fy, quarter):
    return pool.get((fy, quarter), list(pool.values())[0])

# ─────────────────────────────────────────────────────────────────────────────
# ORACLE ENTRY TYPE DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────
ENTRY_TYPES = {
    "Journal Entry": {
        "table":   "GL_JE_HEADERS / GL_JE_LINES",
        "desc":    "Post debit/credit journal entries to the general ledger",
        "color":   "#1D6FA4",
        "keywords":["journal","je","debit","credit","post","gl entry","general ledger"],
        "fields":  ["ledger","period","category","currency","description","debit_account","credit_account","amount","reference"],
    },
    "AP Invoice": {
        "table":   "AP_INVOICES_ALL",
        "desc":    "Record accounts payable invoices from vendors and reinsurers",
        "color":   "#8B5CF6",
        "keywords":["ap ","invoice","payable","vendor","bill","accounts payable"],
        "fields":  ["vendor","invoice_number","invoice_date","due_date","amount","currency","description","cost_centre"],
    },
    "AR Transaction": {
        "table":   "AR_PAYMENT_SCHEDULES_ALL",
        "desc":    "Create accounts receivable transactions and premium receipts",
        "color":   "#D97706",
        "keywords":["ar ","receivable","receipt","premium receipt","collection","accounts receivable"],
        "fields":  ["customer","transaction_number","transaction_date","due_date","amount","currency","description","policy_ref"],
    },
    "Policy Entry": {
        "table":   "INS_POLICY_MASTER",
        "desc":    "Create or update insurance policy records in the policy master",
        "color":   "#1A9E5C",
        "keywords":["policy","insured","coverage","inception","renewal","lob","line of business"],
        "fields":  ["policy_number","insured_name","lob","inception_date","expiry_date","sum_insured","premium","currency","broker","status"],
    },
    "Claim Entry": {
        "table":   "INS_CLAIMS_HEADER",
        "desc":    "Register new claims or update existing claim reserves",
        "color":   "#ED1C2E",
        "keywords":["claim","loss","reserve","adjuster","peril","incident","claimant"],
        "fields":  ["claim_number","policy_ref","insured","date_of_loss","peril","incurred_amount","reserve","currency","status","adjuster"],
    },
    "Reinsurance Entry": {
        "table":   "RE_TRANSACTION_HEADER",
        "desc":    "Post reinsurance cessions, recoveries, and treaty adjustments",
        "color":   "#C0141F",
        "keywords":["reinsurance","cession","recovery","treaty","retrocession","proportional","xol"],
        "fields":  ["treaty_id","reinsurer","transaction_type","period","ceded_premium","ceded_loss","commission","currency","reference"],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# GL CHATBOT — NLP PARSER & RESPONSE BUILDER
# ─────────────────────────────────────────────────────────────────────────────
ACCOUNTS = {
    "premium income":    ("4001 - Premium Income",           "1101 - Cash & Bank"),
    "claims expense":    ("5001 - Claims Expense",           "2201 - Claims Payable"),
    "commission":        ("5101 - Commission Expense",       "2101 - Commissions Payable"),
    "reinsurance":       ("5201 - Reinsurance Premium Ceded","1201 - Reinsurance Recoverable"),
    "admin":             ("5301 - Admin & Overhead",         "2301 - Accrued Expenses"),
    "investment":        ("4101 - Investment Income",        "1301 - Investment Portfolio"),
    "reserve":           ("5401 - Loss Reserve Movement",    "2401 - Outstanding Claims Reserve"),
    "unearned premium":  ("2501 - Unearned Premium Reserve", "4001 - Premium Income"),
}
GL_CATEGORIES  = ["Reinsurance","Premium","Claims","Commission","Admin","Investment","Adjustment","Reserve"]
GL_LEDGERS     = ["Primary Ledger - USD","Secondary Ledger - GBP","Management Ledger","Consolidation Ledger"]
GL_COST_CENTRES= ["Property UW","Casualty UW","Marine UW","Finance","Actuarial","Claims","Investments"]
GL_PERIODS     = ["Jul-25","Aug-25","Sep-25","Oct-25","Nov-25","Dec-25","Jan-26","Feb-26"]

def detect_entry_type(query: str) -> str:
    q = query.lower()
    for etype, meta in ENTRY_TYPES.items():
        if any(kw in q for kw in meta["keywords"]):
            return etype
    return "Journal Entry"

def parse_gl_amount(query: str) -> float:
    import re
    # strip commas and currency symbols, find numbers
    text = query.replace(",","").replace("$","").replace("USD","").replace("GBP","")
    matches = re.findall(r'\d+(?:\.\d+)?', text)
    nums = [float(m) for m in matches if float(m) > 100]
    return nums[0] if nums else 0.0

def parse_gl_intent(query: str) -> dict:
    """
    DEMO: keyword-based GL intent parser.
    ← REPLACE WITH LIVE INTEGRATION: LangChain + OpenAI structured output call
    """
    q     = query.lower()
    etype = detect_entry_type(query)
    amt   = parse_gl_amount(query)
    now   = datetime.now()

    # Pick accounts based on keywords
    debit_acc, credit_acc = "5001 - Claims Expense", "2201 - Claims Payable"
    category = "Adjustment"
    for keyword, (dr, cr) in ACCOUNTS.items():
        if keyword in q:
            debit_acc, credit_acc = dr, cr
            category = keyword.replace(" ","_").title().split("_")[0]
            break

    # Detect period
    period = "Sep-25"
    for p in GL_PERIODS:
        month = p[:3].lower()
        if month in q:
            period = p
            break

    # Reference extraction (look for policy/claim/treaty IDs)
    import re
    refs = re.findall(r'[A-Z]{2,4}-\d{3,6}', query.upper())
    reference = refs[0] if refs else f"REF-{now.strftime('%Y%m%d')}-{random.randint(100,999)}"

    # Description
    desc_map = {
        "premium income":   "Premium income recognition",
        "claims expense":   "Claims expense posting",
        "commission":       "Commission expense accrual",
        "reinsurance":      "Reinsurance premium cession",
        "admin":            "Administrative overhead allocation",
        "investment":       "Investment income recognition",
        "reserve":          "Loss reserve movement",
        "unearned premium": "Unearned premium adjustment",
    }
    description = "Manual journal entry"
    for kw, desc in desc_map.items():
        if kw in q:
            description = desc
            break

    return {
        "entry_type":    etype,
        "ledger":        GL_LEDGERS[0],
        "period":        period,
        "category":      category,
        "currency":      "GBP" if "gbp" in q or "pounds" in q else "USD",
        "amount":        amt,
        "debit_account": debit_acc,
        "credit_account":credit_acc,
        "description":   description,
        "reference":     reference,
        "cost_centre":   "Finance",
        "posted_by":     "Finance Team",
        "status":        "Pending Approval",
        "parsed_from":   query,
    }

def simulate_oracle_write(entry: dict) -> dict:
    """
    DEMO: simulates Oracle API write with fake transaction ID.
    ← REPLACE WITH LIVE INTEGRATION: Oracle REST API POST call
    """
    time.sleep(0.4)
    return {
        "oracle_txn_id":  f"JE{random.randint(1000000,9999999)}",
        "batch_id":       f"BAT-{random.randint(10000,99999)}",
        "posted_at":      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status":         "POSTED",
        "warnings":       [],
    }

# GL chatbot response scripts per entry type
def build_gl_parse_response(parsed: dict) -> str:
    et  = parsed["entry_type"]
    amt = f"${parsed['amount']:,.2f}" if parsed["amount"] else "amount not detected — please specify"
    return (
        f"I have parsed your request as a <b>{et}</b>.<br><br>"
        f"<b>Entry Summary:</b><br>"
        f"&nbsp;&nbsp;Ledger: {parsed['ledger']}<br>"
        f"&nbsp;&nbsp;Period: {parsed['period']}<br>"
        f"&nbsp;&nbsp;Category: {parsed['category']}<br>"
        f"&nbsp;&nbsp;Currency: {parsed['currency']}<br>"
        f"&nbsp;&nbsp;Amount: {amt}<br>"
        f"&nbsp;&nbsp;Debit: {parsed['debit_account']}<br>"
        f"&nbsp;&nbsp;Credit: {parsed['credit_account']}<br>"
        f"&nbsp;&nbsp;Description: {parsed['description']}<br>"
        f"&nbsp;&nbsp;Reference: {parsed['reference']}<br><br>"
        f"Please review the entry details in the <b>Review &amp; Confirm</b> panel below. "
        f"If correct, click <b>Post to Oracle</b> to commit this transaction. "
        f"You may also edit the fields before posting."
    )

def build_gl_confirm_response(entry: dict, result: dict) -> str:
    return (
        f"Entry posted successfully to Oracle Financials.<br><br>"
        f"<b>Oracle Transaction ID:</b> <span style='font-family:DM Mono,monospace;color:#ED1C2E;'>"
        f"{result['oracle_txn_id']}</span><br>"
        f"<b>Batch ID:</b> {result['batch_id']}<br>"
        f"<b>Posted At:</b> {result['posted_at']}<br>"
        f"<b>Table:</b> {ENTRY_TYPES[entry['entry_type']]['table']}<br>"
        f"<b>Status:</b> {result['status']}<br><br>"
        f"The entry is now visible in the Oracle GL and the audit log has been updated. "
        f"You may post another entry or use the structured form for batch submissions."
    )

# ─────────────────────────────────────────────────────────────────────────────
# REPORT REGISTRY (for finance reporting tab)
# ─────────────────────────────────────────────────────────────────────────────
REPORT_REGISTRY = {
    "bill_to_accounting": {"label":"Bill to Accounting","desc":"Reinsurance billing statement for accounting reconciliation.","keywords":["bill","accounting","billing","statement","settlement"]},
    "premium_listing":    {"label":"Premium Listing","desc":"Detailed listing of premiums written and ceded by policy.","keywords":["premium","policy","listing","written","ceded"]},
    "claims_recovery":    {"label":"Claims Recovery Statement","desc":"Summary of claims incurred and reinsurance recoveries.","keywords":["claim","recovery","loss","incurred","recover"]},
    "loss_run":           {"label":"Loss Run Report","desc":"Period loss run by line of business.","keywords":["loss run","lob","run report"]},
    "bordereaux":         {"label":"Bordereaux Report","desc":"Detailed risk and premium bordereaux for treaty submission.","keywords":["bordereaux","treaty","risk","submission"]},
}
COUNTERPARTIES = ["Reinsurer","Broker","Internal Accounting","Cedant","Regulator"]

SUGGESTIONS_MAP = {
    "bill_to_accounting": ["Generate a Claims Recovery Statement for FY2025Q3 to Reinsurer","Run a Premium Listing for FY2025Q3 to Internal Accounting","Generate a Bill to Accounting to Reinsurer using FY2025Q2 data","Produce a Bordereaux Report for FY2025Q3 to Reinsurer"],
    "premium_listing":    ["Generate a Bill to Accounting to Reinsurer using FY2025Q3 data","Run a Claims Recovery Statement for FY2025Q3 to Broker","Produce a Premium Listing for FY2024Q4 to Internal Accounting","Generate a Loss Run Report for FY2025Q3 to Reinsurer"],
    "claims_recovery":    ["Generate a Bill to Accounting to Reinsurer using FY2025Q3 data","Run a Loss Run Report for FY2025Q3 to Reinsurer","Produce a Claims Recovery Statement for FY2025Q2 to Broker","Generate a Bordereaux Report for FY2025Q3 to Reinsurer"],
    "loss_run":           ["Generate a Claims Recovery Statement for FY2025Q3 to Reinsurer","Run a Bill to Accounting to Reinsurer for FY2025Q3","Produce a Loss Run Report for FY2024Q4 to Internal Accounting","Generate a Premium Listing for FY2025Q3 to Broker"],
    "bordereaux":         ["Generate a Bill to Accounting to Reinsurer using FY2025Q3 data","Run a Premium Listing for FY2025Q3 to Reinsurer","Produce a Bordereaux Report for FY2025Q2 to Broker","Generate a Claims Recovery Statement for FY2025Q3 to Cedant"],
}

def get_suggestions(rt): return SUGGESTIONS_MAP.get(rt, SUGGESTIONS_MAP["bill_to_accounting"])

# ─────────────────────────────────────────────────────────────────────────────
# REPORT PIPELINE
# ─────────────────────────────────────────────────────────────────────────────
def get_agent_script(rt, fy, q, cp, rows):
    label = REPORT_REGISTRY[rt]["label"]
    return [
        ("Orchestrator",               f'Intent parsed — "{label}" for {cp}, {fy} {q}', 0.30),
        ("Orchestrator",               "Routing to Agent 1 · Oracle Connector", 0.20),
        ("Agent 1 · Oracle Connector", f"Authenticating with Oracle Financials Cloud ({ORACLE_DB_SCHEMA})", 0.50),
        ("Agent 1 · Oracle Connector", f"Executing GL query: SELECT * FROM {ORACLE_DB_SCHEMA}.REINS_LEDGER WHERE PERIOD='{fy}{q}'", 0.60),
        ("Agent 1 · Oracle Connector", f"Fetch complete — {rows} records retrieved, validation passed", 0.30),
        ("Agent 2 · Finance Reasoning","Loading treaty parameters from treaty register (TRY-2025-007)", 0.40),
        ("Agent 2 · Finance Reasoning","Applying proportional reinsurance cession rules (40% quota share)", 0.40),
        ("Agent 2 · Finance Reasoning","Computing net premiums, loss recoveries, commission adjustments", 0.50),
        ("Agent 2 · Finance Reasoning","Calculations complete — treaty compliance check passed", 0.30),
        ("Agent 3 · Report Formatter", f"Mapping data to {label} standard template", 0.30),
        ("Agent 3 · Report Formatter", "Applying number formatting, currency conversion, rounding rules", 0.30),
        ("Agent 3 · Report Formatter", "Report structured and validated — ready for delivery", 0.20),
    ]

def render_agent_log(steps, running_agent=None):
    colors = {"Orchestrator":"#8B5CF6","Agent 1 · Oracle Connector":"#1D6FA4","Agent 2 · Finance Reasoning":"#D97706","Agent 3 · Report Formatter":"#1A9E5C"}
    rows = ""
    for i,(agent,step) in enumerate(steps):
        is_last = i==len(steps)-1
        is_run  = is_last and running_agent==agent
        c = colors.get(agent,"#666")
        dot_bg = c if is_run else "#1A9E5C"
        anim   = "animation:pulse-dot 1s infinite;" if is_run else ""
        tag    = "PROCESSING" if is_run else "DONE"
        rows += f"""<div class="agent-step" style="display:flex;align-items:flex-start;gap:10px;padding:9px 0;border-bottom:1px solid #F0F0F0;">
            <div style="width:8px;height:8px;border-radius:50%;background:{dot_bg};margin-top:5px;flex-shrink:0;{anim}"></div>
            <div style="flex:1;"><div style="font-size:0.67rem;font-weight:700;color:{c};text-transform:uppercase;letter-spacing:0.09em;">{agent}</div>
            <div style="font-size:0.82rem;color:#212121;margin-top:1px;">{step}</div></div>
            <div style="font-size:0.62rem;font-weight:700;color:{dot_bg};letter-spacing:0.06em;white-space:nowrap;margin-left:4px;">{tag}</div>
        </div>"""
    return f"""<div style="background:white;border:1px solid #EBEBEB;border-radius:10px;padding:0.85rem 1rem;box-shadow:0 2px 10px rgba(0,0,0,0.05);">
        <div style="font-size:0.67rem;font-weight:700;color:#ED1C2E;text-transform:uppercase;letter-spacing:0.11em;margin-bottom:6px;">Agent Pipeline · Live</div>{rows}</div>"""

def parse_report_query(query):
    q = query.lower()
    rt = "bill_to_accounting"
    for key, meta in REPORT_REGISTRY.items():
        if any(kw in q for kw in meta["keywords"]): rt = key; break
    cp = "Reinsurer"
    for c in COUNTERPARTIES:
        if c.lower() in q: cp = c; break
    fy = "FY2025"
    for token in query.upper().split():
        if token.startswith("FY") and len(token)>=6: fy=token[:6]; break
    quarter = "Q3"
    for qn in ["Q1","Q2","Q3","Q4"]:
        if qn in query.upper(): quarter=qn; break
    return {"report_type":rt,"counterparty":cp,"fy":fy,"quarter":quarter}

def run_report_pipeline(parsed, step_ph):
    rt,fy,q,cp = parsed["report_type"],parsed["fy"],parsed["quarter"],parsed["counterparty"]
    if rt=="bill_to_accounting":
        raw=_get_pool(DEMO_REINSURANCE,fy,q); rows=47
        net_prem=raw["premiums_ceded"]-raw["commissions_received"]
        fdata={"net_premium_ceded":round(net_prem,2),"net_loss_recovery":round(raw["losses_ceded"],2),"commission_adjustment":round(raw["commissions_paid"],2),"balance_due":round(net_prem-raw["losses_ceded"]-raw["commissions_paid"],2),"raw":raw}
    elif rt=="premium_listing":
        raw=_get_pool(DEMO_PREMIUMS,fy,q); rows=len(raw)
        df=pd.DataFrame(raw)
        fdata={"rows":raw,"total_gross":df["Gross Premium"].sum(),"total_ceded":df["Ceded Premium"].sum(),"total_net":df["Net Retained"].sum()}
    else:
        raw=_get_pool(DEMO_CLAIMS,fy,q); rows=len(raw)
        df=pd.DataFrame(raw)
        fdata={"rows":raw,"total_incurred":df["Incurred"].sum(),"total_recovered":df["Recovered"].sum(),"total_net_loss":df["Net Loss"].sum(),"open_claims":int((df["Status"]=="Open").sum())}
    script=get_agent_script(rt,fy,q,cp,rows)
    done=[]
    for agent,step,delay in script:
        time.sleep(delay); done.append((agent,step))
        step_ph.markdown(render_agent_log(done,running_agent=agent),unsafe_allow_html=True)
    time.sleep(0.15)
    report={"report_id":f"RPT-{random.randint(10000,99999)}","report_type":rt,"report_label":REPORT_REGISTRY[rt]["label"],"counterparty":cp,"fy":fy,"quarter":q,"generated_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"data_source":"Oracle Financials Cloud","rows_fetched":rows,"status":"FINAL","finance":fdata}
    return report

# ─────────────────────────────────────────────────────────────────────────────
# UI COMPONENTS
# ─────────────────────────────────────────────────────────────────────────────
def fmt(v): return f"${v:,.2f}"

def badge(text, bg="#ED1C2E", fg="white"):
    return f'<span style="background:{bg};color:{fg};padding:2px 10px;border-radius:20px;font-size:0.68rem;font-weight:700;letter-spacing:0.05em;">{text}</span>'

def kpi(label, value, sub="", accent=False):
    border=f"2px solid #ED1C2E" if accent else "1px solid #EBEBEB"
    vc="#ED1C2E" if accent else "#212121"
    return f"""<div style="background:white;border:{border};border-radius:10px;padding:1.1rem 1.3rem;box-shadow:0 2px 10px rgba(0,0,0,0.05);">
        <div style="font-size:0.68rem;font-weight:600;color:#666;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:5px;">{label}</div>
        <div class="kpi-num" style="font-size:1.5rem;font-weight:700;color:{vc};font-family:'DM Mono',monospace;">{value}</div>
        {f'<div style="font-size:0.74rem;color:#999;margin-top:3px;">{sub}</div>' if sub else ''}
    </div>"""

def section_hdr(title, sub=""):
    return f"""<div style="display:flex;align-items:center;gap:10px;margin-bottom:1.2rem;">
        <div style="width:4px;height:28px;background:#ED1C2E;border-radius:2px;flex-shrink:0;"></div>
        <div><div style="font-size:1rem;font-weight:700;color:#212121;">{title}</div>
        {f'<div style="font-size:0.8rem;color:#666;margin-top:1px;">{sub}</div>' if sub else ''}</div>
    </div>"""

def chat_user(text):
    return f"""<div class="chat-bubble" style="display:flex;justify-content:flex-end;margin-bottom:0.8rem;">
        <div style="max-width:68%;background:#ED1C2E;color:white;border-radius:14px 14px 3px 14px;padding:0.8rem 1.1rem;font-size:0.88rem;line-height:1.55;box-shadow:0 3px 12px rgba(237,28,46,0.18);">{text}</div>
    </div>"""

def chat_assistant(text, avatar_color="#212121"):
    return f"""<div class="chat-bubble" style="display:flex;justify-content:flex-start;margin-bottom:0.5rem;">
        <div style="display:flex;gap:10px;align-items:flex-start;max-width:78%;">
            <div style="width:30px;height:30px;background:{avatar_color};border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;">
                <span style="color:white;font-size:0.68rem;font-weight:700;letter-spacing:-0.03em;">Fi</span>
            </div>
            <div style="background:white;color:#212121;border:1px solid #EBEBEB;border-radius:14px 14px 14px 3px;padding:0.85rem 1.1rem;font-size:0.88rem;line-height:1.6;box-shadow:0 2px 10px rgba(0,0,0,0.05);">{text}</div>
        </div>
    </div>"""

# ─────────────────────────────────────────────────────────────────────────────
# REPORT RENDERERS
# ─────────────────────────────────────────────────────────────────────────────
def render_bill(report):
    f=report["finance"]; r=f["raw"]
    st.markdown(section_hdr("Bill to Accounting — Reinsurance Settlement Statement",f"Period: {report['fy']} · {report['quarter']}  |  Treaty: {r['treaty_id']}  |  {report['counterparty']}"),unsafe_allow_html=True)
    st.markdown(f"""<div style="background:white;border:1px solid #EBEBEB;border-radius:12px;padding:1.5rem 1.8rem;margin-bottom:1.2rem;box-shadow:0 3px 14px rgba(0,0,0,0.06);">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
            <div><div style="font-size:0.68rem;font-weight:600;color:#666;text-transform:uppercase;letter-spacing:0.09em;margin-bottom:4px;">Reinsurer</div>
            <div style="font-size:1.15rem;font-weight:700;color:#212121;">{r["reinsurer"]}</div>
            <div style="font-size:0.8rem;color:#666;margin-top:3px;">Treaty {r["treaty_id"]}  ·  {", ".join(r["lines_of_business"])}  ·  {r["reinsurer_share"]} Quota Share</div></div>
            <div style="text-align:right;"><div style="font-size:0.68rem;color:#999;text-transform:uppercase;letter-spacing:0.08em;">Report ID</div>
            <div style="font-family:'DM Mono',monospace;font-weight:600;color:#ED1C2E;font-size:1rem;">{report["report_id"]}</div>
            <div style="margin-top:6px;">{badge("FINAL")}&nbsp;&nbsp;{badge("DEMO MODE","#666")}</div></div>
        </div></div>""",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown(kpi("Premiums Written",fmt(r["premiums_written"]),"Gross (100%)"),unsafe_allow_html=True)
    with c2: st.markdown(kpi("Premiums Ceded",fmt(r["premiums_ceded"]),f'{r["reinsurer_share"]} ceded'),unsafe_allow_html=True)
    with c3: st.markdown(kpi("Losses Incurred",fmt(r["losses_incurred"]),"Gross (100%)"),unsafe_allow_html=True)
    with c4: st.markdown(kpi("Losses Ceded",fmt(r["losses_ceded"]),"Reinsurer share"),unsafe_allow_html=True)
    st.markdown("<div style='height:0.8rem'></div>",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    bal=f["balance_due"]
    with c1: st.markdown(kpi("Net Premium Ceded",fmt(f["net_premium_ceded"]),"After commission adj."),unsafe_allow_html=True)
    with c2: st.markdown(kpi("Net Loss Recovery",fmt(f["net_loss_recovery"]),"Ceded losses"),unsafe_allow_html=True)
    with c3: st.markdown(kpi("Commission Adj.",fmt(f["commission_adjustment"]),"Ceding commissions"),unsafe_allow_html=True)
    with c4: st.markdown(kpi("Balance Due",fmt(abs(bal)),"Payable to Reinsurer" if bal>0 else "Receivable",accent=True),unsafe_allow_html=True)
    st.markdown("<div style='height:1rem'></div>",unsafe_allow_html=True)
    recon={"Line Item":["Premiums Written (Gross)","Reinsurer Share of Premiums (40%)","Less: Ceding Commissions Payable","Net Premium Due to Reinsurer","","Gross Losses Incurred","Reinsurer Share of Losses (40%)","Less: Loss Adjustment Expenses","Net Loss Recovery Due to Cedant","","Interest on Funds Withheld","Administration Expenses","Settlement Balance Due"],
           "Amount (USD)":[fmt(r["premiums_written"]),fmt(r["premiums_ceded"]),f'({fmt(r["commissions_paid"])})',fmt(f["net_premium_ceded"]),"—",fmt(r["losses_incurred"]),fmt(r["losses_ceded"]),f'({fmt(r["admin_expenses"]*0.3)})',fmt(f["net_loss_recovery"]),"—",fmt(r["interest_income"]),f'({fmt(r["admin_expenses"])})',fmt(abs(bal))],
           "Notes":["All lines of business","Quota share — 40%","Per treaty schedule","Net of commissions","","All lines of business","Proportional share","LAE @ 30% of admin","Ceded proportionally","","Funds withheld rate 4.2%","Pro-rated Q allocation","DUE TO REINSURER" if bal>0 else "DUE FROM REINSURER"]}
    st.dataframe(pd.DataFrame(recon),use_container_width=True,hide_index=True,height=490)

def render_premium(report):
    f=report["finance"]
    st.markdown(section_hdr("Premium Listing",f"{report['fy']} · {report['quarter']}  |  {report['counterparty']}"),unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1: st.markdown(kpi("Total Gross Premium",fmt(f["total_gross"]),f'{len(f["rows"])} policies'),unsafe_allow_html=True)
    with c2: st.markdown(kpi("Total Ceded Premium",fmt(f["total_ceded"]),"40% quota share"),unsafe_allow_html=True)
    with c3: st.markdown(kpi("Total Net Retained",fmt(f["total_net"]),"60% retention",accent=True),unsafe_allow_html=True)
    st.markdown("<div style='height:0.8rem'></div>",unsafe_allow_html=True)
    df=pd.DataFrame(f["rows"])
    for col in ["Gross Premium","Ceded Premium","Net Retained"]: df[col]=df[col].apply(fmt)
    st.dataframe(df,use_container_width=True,hide_index=True)

def render_claims_rpt(report):
    f=report["finance"]
    st.markdown(section_hdr(report["report_label"],f"{report['fy']} · {report['quarter']}  |  {report['counterparty']}"),unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown(kpi("Total Incurred",fmt(f["total_incurred"]),"Gross losses"),unsafe_allow_html=True)
    with c2: st.markdown(kpi("Total Recovered",fmt(f["total_recovered"]),"Reinsurer share"),unsafe_allow_html=True)
    with c3: st.markdown(kpi("Net Loss (Retained)",fmt(f["total_net_loss"]),"Cedant share",accent=True),unsafe_allow_html=True)
    with c4: st.markdown(kpi("Open Claims",str(f["open_claims"]),"Pending settlement"),unsafe_allow_html=True)
    st.markdown("<div style='height:0.8rem'></div>",unsafe_allow_html=True)
    df=pd.DataFrame(f["rows"])
    for col in ["Incurred","Recovered","Net Loss","Reserve"]:
        if col in df.columns: df[col]=df[col].apply(fmt)
    st.dataframe(df,use_container_width=True,hide_index=True)

def render_report(report):
    rt=report["report_type"]
    st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.8rem;margin-bottom:1.2rem;">
        <div><div style="font-size:0.66rem;color:#999;text-transform:uppercase;font-weight:700;letter-spacing:0.09em;">Report ID: {report["report_id"]}</div>
        <div style="font-size:0.8rem;color:#666;margin-top:2px;">Generated {report["generated_at"]}  ·  Source: {report["data_source"]}  ·  {report["rows_fetched"]} records</div></div>
        <div>{badge("FINAL")}&nbsp;{badge("DEMO MODE","#666")}</div></div>""",unsafe_allow_html=True)
    if rt=="bill_to_accounting": render_bill(report)
    elif rt=="premium_listing": render_premium(report)
    else: render_claims_rpt(report)

# ─────────────────────────────────────────────────────────────────────────────
# ORACLE DATA ENTRY — STRUCTURED FORMS
# ─────────────────────────────────────────────────────────────────────────────
def render_entry_form(entry_type: str):
    """Renders the appropriate structured form for each Oracle entry type."""
    et_meta = ENTRY_TYPES[entry_type]
    color   = et_meta["color"]

    st.markdown(f"""<div style="background:white;border:1px solid #EBEBEB;border-radius:12px;
        padding:1.5rem 1.8rem;box-shadow:0 3px 14px rgba(0,0,0,0.05);margin-bottom:1rem;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:1rem;">
            <div style="width:4px;height:28px;background:{color};border-radius:2px;"></div>
            <div><div style="font-size:0.95rem;font-weight:700;color:#212121;">{entry_type}</div>
            <div style="font-size:0.76rem;color:#666;margin-top:1px;">
                Oracle Table: <span style="font-family:'DM Mono',monospace;color:{color};">{et_meta["table"]}</span>
            </div></div>
        </div>""", unsafe_allow_html=True)

    result = None

    if entry_type == "Journal Entry":
        c1, c2, c3 = st.columns(3)
        with c1: ledger  = st.selectbox("Ledger",     GL_LEDGERS,     key="f_ledger")
        with c2: period  = st.selectbox("Period",     GL_PERIODS,     key="f_period")
        with c3: cat     = st.selectbox("Category",   GL_CATEGORIES,  key="f_cat")
        c1, c2 = st.columns(2)
        with c1: debit_a = st.text_input("Debit Account", value="5001 - Claims Expense", key="f_dr")
        with c2: cred_a  = st.text_input("Credit Account",value="2201 - Claims Payable", key="f_cr")
        c1, c2, c3 = st.columns(3)
        with c1: amt     = st.number_input("Amount",  min_value=0.0, step=1000.0, key="f_amt")
        with c2: curr    = st.selectbox("Currency",   ["USD","GBP","EUR","SGD"], key="f_curr")
        with c3: ref     = st.text_input("Reference", placeholder="e.g. TRY-2025-007", key="f_ref")
        desc   = st.text_input("Description", placeholder="Enter journal entry description", key="f_desc")
        result = {"entry_type":entry_type,"ledger":ledger,"period":period,"category":cat,"debit_account":debit_a,"credit_account":cred_a,"amount":amt,"currency":curr,"reference":ref,"description":desc}

    elif entry_type == "AP Invoice":
        c1, c2, c3 = st.columns(3)
        with c1: vendor  = st.text_input("Vendor Name",       key="f_vendor")
        with c2: inv_no  = st.text_input("Invoice Number",    key="f_invno")
        with c3: inv_dt  = st.date_input("Invoice Date",      value=date.today(), key="f_invdt")
        c1, c2, c3 = st.columns(3)
        with c1: due_dt  = st.date_input("Due Date",          value=date.today(), key="f_duedt")
        with c2: amt     = st.number_input("Invoice Amount",  min_value=0.0, step=1000.0, key="f_ap_amt")
        with c3: curr    = st.selectbox("Currency",           ["USD","GBP","EUR"], key="f_ap_curr")
        c1, c2 = st.columns(2)
        with c1: cc      = st.selectbox("Cost Centre",        GL_COST_CENTRES, key="f_ap_cc")
        with c2: desc    = st.text_input("Description",       key="f_ap_desc")
        result = {"entry_type":entry_type,"vendor":vendor,"invoice_number":inv_no,"invoice_date":str(inv_dt),"due_date":str(due_dt),"amount":amt,"currency":curr,"cost_centre":cc,"description":desc}

    elif entry_type == "AR Transaction":
        c1, c2, c3 = st.columns(3)
        with c1: cust    = st.text_input("Customer / Insured", key="f_cust")
        with c2: txn_no  = st.text_input("Transaction Number", key="f_txnno")
        with c3: txn_dt  = st.date_input("Transaction Date",   value=date.today(), key="f_txndt")
        c1, c2, c3 = st.columns(3)
        with c1: due_dt  = st.date_input("Due Date",           value=date.today(), key="f_ar_due")
        with c2: amt     = st.number_input("Amount",           min_value=0.0, step=1000.0, key="f_ar_amt")
        with c3: curr    = st.selectbox("Currency",            ["USD","GBP","EUR"], key="f_ar_curr")
        c1, c2 = st.columns(2)
        with c1: pol_ref = st.text_input("Policy Reference",   key="f_ar_pol")
        with c2: desc    = st.text_input("Description",        key="f_ar_desc")
        result = {"entry_type":entry_type,"customer":cust,"transaction_number":txn_no,"transaction_date":str(txn_dt),"due_date":str(due_dt),"amount":amt,"currency":curr,"policy_ref":pol_ref,"description":desc}

    elif entry_type == "Policy Entry":
        c1, c2, c3 = st.columns(3)
        with c1: pol_no  = st.text_input("Policy Number",     placeholder="POL-XXXXX", key="f_pol_no")
        with c2: insured = st.text_input("Insured Name",      key="f_insured")
        with c3: lob     = st.selectbox("Line of Business",   ["Property","Casualty","Marine","Aviation","Cyber","Life"], key="f_lob")
        c1, c2, c3 = st.columns(3)
        with c1: inc_dt  = st.date_input("Inception Date",    value=date.today(), key="f_inc")
        with c2: exp_dt  = st.date_input("Expiry Date",       value=date.today(), key="f_exp")
        with c3: status  = st.selectbox("Status",             ["Active","Pending","Renewed","Lapsed","Cancelled"], key="f_pol_st")
        c1, c2, c3, c4 = st.columns(4)
        with c1: si      = st.number_input("Sum Insured",     min_value=0.0, step=100_000.0, key="f_si")
        with c2: prem    = st.number_input("Premium",         min_value=0.0, step=1000.0, key="f_prem")
        with c3: curr    = st.selectbox("Currency",           ["USD","GBP","EUR"], key="f_pol_curr")
        with c4: broker  = st.text_input("Broker",            key="f_broker")
        result = {"entry_type":entry_type,"policy_number":pol_no,"insured_name":insured,"lob":lob,"inception_date":str(inc_dt),"expiry_date":str(exp_dt),"status":status,"sum_insured":si,"premium":prem,"currency":curr,"broker":broker}

    elif entry_type == "Claim Entry":
        c1, c2, c3 = st.columns(3)
        with c1: clm_no  = st.text_input("Claim Number",      placeholder="CLM-XXXXX", key="f_clm_no")
        with c2: pol_ref = st.text_input("Policy Reference",  placeholder="POL-XXXXX", key="f_clm_pol")
        with c3: insured = st.text_input("Insured Name",      key="f_clm_ins")
        c1, c2, c3 = st.columns(3)
        with c1: dol     = st.date_input("Date of Loss",      value=date.today(), key="f_dol")
        with c2: peril   = st.selectbox("Peril",              ["Fire","Flood","Storm","Theft","Liability","Marine Peril","Business Interruption","Other"], key="f_peril")
        with c3: clm_st  = st.selectbox("Status",             ["Open","Pending","Closed","Reopened","Disputed"], key="f_clm_st")
        c1, c2, c3, c4 = st.columns(4)
        with c1: inc_amt = st.number_input("Incurred Amount", min_value=0.0, step=10_000.0, key="f_inc_amt")
        with c2: reserve = st.number_input("Reserve",         min_value=0.0, step=10_000.0, key="f_reserve")
        with c3: curr    = st.selectbox("Currency",           ["USD","GBP","EUR"], key="f_clm_curr")
        with c4: adj     = st.text_input("Adjuster",          key="f_adj")
        result = {"entry_type":entry_type,"claim_number":clm_no,"policy_ref":pol_ref,"insured":insured,"date_of_loss":str(dol),"peril":peril,"status":clm_st,"incurred_amount":inc_amt,"reserve":reserve,"currency":curr,"adjuster":adj}

    elif entry_type == "Reinsurance Entry":
        c1, c2, c3 = st.columns(3)
        with c1: treaty  = st.text_input("Treaty ID",         placeholder="TRY-XXXX-XXX", key="f_treaty")
        with c2: reinsur = st.text_input("Reinsurer",         key="f_reinsur")
        with c3: txn_type= st.selectbox("Transaction Type",   ["Premium Cession","Loss Recovery","Commission Receipt","Adjustment","Reinstatement Premium"], key="f_re_type")
        c1, c2, c3 = st.columns(3)
        with c1: period  = st.selectbox("Period",             GL_PERIODS, key="f_re_period")
        with c2: curr    = st.selectbox("Currency",           ["USD","GBP","EUR"], key="f_re_curr")
        with c3: ref     = st.text_input("Reference",         key="f_re_ref")
        c1, c2, c3 = st.columns(3)
        with c1: ced_prem= st.number_input("Ceded Premium",   min_value=0.0, step=10_000.0, key="f_cedprem")
        with c2: ced_loss= st.number_input("Ceded Loss",      min_value=0.0, step=10_000.0, key="f_cedloss")
        with c3: comm    = st.number_input("Commission",      min_value=0.0, step=1_000.0, key="f_re_comm")
        result = {"entry_type":entry_type,"treaty_id":treaty,"reinsurer":reinsur,"transaction_type":txn_type,"period":period,"currency":curr,"reference":ref,"ceded_premium":ced_prem,"ceded_loss":ced_loss,"commission":comm}

    st.markdown("</div>", unsafe_allow_html=True)
    return result

# ─────────────────────────────────────────────────────────────────────────────
# ORACLE WRITE SIMULATION (animated)
# ─────────────────────────────────────────────────────────────────────────────
def run_oracle_write(entry: dict, log_ph) -> dict:
    """
    DEMO: simulates Oracle write with animated log.
    ← REPLACE WITH LIVE INTEGRATION: Oracle REST API POST to relevant endpoint.
    """
    et    = entry["entry_type"]
    table = ENTRY_TYPES[et]["table"]
    color = ENTRY_TYPES[et]["color"]

    steps = [
        ("Oracle API Gateway",   f"Connecting to {ORACLE_API_BASE_URL}",                         0.35),
        ("Oracle API Gateway",   f"Authenticated — token validated ({ORACLE_DB_SCHEMA})",        0.30),
        ("Validation Layer",     "Running pre-submission field validation checks",               0.40),
        ("Validation Layer",     "Checking account code validity and period status",             0.35),
        ("Validation Layer",     "Validating currency and business rules",                       0.30),
        ("Validation Layer",     "Validation passed — no errors or warnings detected",           0.30),
        ("Oracle Write Engine",  f"Preparing INSERT/UPDATE to {table}",                          0.40),
        ("Oracle Write Engine",  "Executing database transaction with COMMIT",                   0.50),
        ("Oracle Write Engine",  "Transaction committed — row locks released",                   0.30),
        ("Audit & Compliance",   "Writing audit trail to FIN_AUDIT_LOG",                         0.35),
        ("Audit & Compliance",   "Notifying downstream GL posting engine",                       0.30),
        ("Audit & Compliance",   "Entry posted and confirmed",                                   0.20),
    ]

    agent_colors = {
        "Oracle API Gateway":  "#1D6FA4",
        "Validation Layer":    "#D97706",
        "Oracle Write Engine": color,
        "Audit & Compliance":  "#1A9E5C",
    }

    def render_write_log(done, running=None):
        rows = ""
        for i,(a,s) in enumerate(done):
            is_last = i==len(done)-1
            is_run  = is_last and running==a
            c       = agent_colors.get(a,"#666")
            dot     = c if is_run else "#1A9E5C"
            anim    = "animation:pulse-dot 1s infinite;" if is_run else ""
            tag     = "PROCESSING" if is_run else "DONE"
            rows += f"""<div class="agent-step" style="display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid #F0F0F0;">
                <div style="width:8px;height:8px;border-radius:50%;background:{dot};margin-top:5px;flex-shrink:0;{anim}"></div>
                <div style="flex:1;"><div style="font-size:0.67rem;font-weight:700;color:{c};text-transform:uppercase;letter-spacing:0.09em;">{a}</div>
                <div style="font-size:0.82rem;color:#212121;margin-top:1px;">{s}</div></div>
                <div style="font-size:0.62rem;font-weight:700;color:{dot};letter-spacing:0.06em;white-space:nowrap;">{tag}</div>
            </div>"""
        return f"""<div style="background:white;border:1px solid #EBEBEB;border-radius:10px;padding:0.85rem 1rem;box-shadow:0 2px 10px rgba(0,0,0,0.05);">
            <div style="font-size:0.67rem;font-weight:700;color:{color};text-transform:uppercase;letter-spacing:0.11em;margin-bottom:6px;">Oracle Write Pipeline · Live</div>{rows}</div>"""

    done = []
    for agent, step, delay in steps:
        time.sleep(delay)
        done.append((agent, step))
        log_ph.markdown(render_write_log(done, running=agent), unsafe_allow_html=True)

    result = simulate_oracle_write(entry)
    time.sleep(0.2)
    return result

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.4rem 1.4rem 1rem;border-bottom:1px solid #EBEBEB;">
        <div style="display:flex;align-items:center;gap:11px;margin-bottom:10px;">
            <div style="width:38px;height:38px;background:#ED1C2E;border-radius:9px;display:flex;
                        align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(237,28,46,0.28);">
                <span style="color:white;font-size:1rem;font-weight:700;letter-spacing:-0.03em;">Fi</span>
            </div>
            <div>
                <div style="font-weight:700;font-size:1.05rem;color:#212121;line-height:1.1;letter-spacing:-0.02em;">FinanceIQ</div>
                <div style="font-size:0.67rem;color:#999;text-transform:uppercase;letter-spacing:0.1em;">Oracle Finance Platform</div>
            </div>
        </div>
        <div style="display:inline-flex;align-items:center;gap:6px;background:#F0FDF4;border:1px solid #BBF7D0;border-radius:20px;padding:4px 12px;">
            <div class="pulse-dot" style="width:7px;height:7px;border-radius:50%;background:#22C55E;"></div>
            <span style="font-size:0.7rem;font-weight:600;color:#15803D;">Demo Mode · No API Keys Required</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick Report panel
    st.markdown('<div style="padding:1rem 1.2rem 0.4rem;"><div style="font-size:0.68rem;font-weight:700;color:#ED1C2E;text-transform:uppercase;letter-spacing:0.13em;">Generate a Quick Report</div></div>', unsafe_allow_html=True)
    report_labels = {v["label"]:k for k,v in REPORT_REGISTRY.items()}
    sel_label = st.selectbox("Report Type",  list(report_labels.keys()), key="sb_rt")
    sel_key   = report_labels[sel_label]
    cp        = st.selectbox("Send To",      COUNTERPARTIES,             key="sb_cp")
    cy,cq     = st.columns(2)
    with cy: fy      = st.selectbox("Fiscal Year", ["FY2025","FY2024","FY2023"], key="sb_fy")
    with cq: quarter = st.selectbox("Quarter",     ["Q1","Q2","Q3","Q4"], index=2, key="sb_q")
    gen_btn = st.button("Generate Report", key="sb_gen", use_container_width=True)

    if gen_btn:
        parsed  = {"report_type":sel_key,"counterparty":cp,"fy":fy,"quarter":quarter}
        step_ph = st.empty()
        with st.spinner(""):
            report = run_report_pipeline(parsed, step_ph)
        time.sleep(0.3); step_ph.empty()
        st.session_state.reports.insert(0, report)
        st.session_state.messages.append({"role":"user","content":f"Generate a {sel_label} to {cp} using {fy}{quarter} data"})
        st.session_state.messages.append({"role":"assistant","content":f"Report generated — <b>{report['report_label']}</b> for <b>{cp}</b>, {fy} {quarter}. Report ID: <span style='font-family:DM Mono,monospace;color:#ED1C2E;'>{report['report_id']}</span>. Open the Report Viewer tab to view the output."})
        st.session_state.messages.append({"role":"suggestions","report_type":report["report_type"]})
        st.rerun()

    st.markdown('<hr style="margin:0.8rem 0;border-color:#EBEBEB;">', unsafe_allow_html=True)

    # Oracle Audit Log summary in sidebar
    if st.session_state.oracle_log:
        st.markdown('<div style="padding:0 0.4rem 0.3rem;"><div style="font-size:0.68rem;font-weight:700;color:#1A9E5C;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;">Oracle Write Log</div></div>', unsafe_allow_html=True)
        for entry in st.session_state.oracle_log[-5:][::-1]:
            color = ENTRY_TYPES[entry["entry_type"]]["color"]
            st.markdown(f"""<div style="padding:0.5rem 0.4rem;border-bottom:1px solid #F5F5F5;">
                <div style="display:flex;align-items:center;gap:6px;margin-bottom:2px;">
                    <div style="width:6px;height:6px;border-radius:50%;background:{color};flex-shrink:0;"></div>
                    <div style="font-size:0.8rem;font-weight:600;color:#212121;">{entry["entry_type"]}</div>
                </div>
                <div style="font-size:0.72rem;font-family:'DM Mono',monospace;color:{color};">{entry["oracle_txn_id"]}</div>
                <div style="font-size:0.7rem;color:#999;margin-top:1px;">{entry["posted_at"][:16]}  ·  {entry["status"]}</div>
            </div>""", unsafe_allow_html=True)

    # Last report
    elif st.session_state.reports:
        r = st.session_state.reports[0]
        st.markdown(f"""<div style="padding:0 0.4rem;">
            <div style="font-size:0.68rem;font-weight:700;color:#666;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;">Last Report</div>
            <div style="background:#F7F7F8;border-radius:8px;padding:0.7rem 0.9rem;">
                <div style="font-weight:700;font-size:0.85rem;color:#212121;">{r["report_label"]}</div>
                <div style="font-size:0.75rem;color:#666;margin-top:2px;">{r["fy"]} {r["quarter"]} · {r["counterparty"]}</div>
                <div style="font-size:0.7rem;font-family:'DM Mono',monospace;color:#ED1C2E;margin-top:4px;">{r["report_id"]}</div>
            </div></div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN PANEL — TOP BAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:white;border-bottom:1px solid #EBEBEB;padding:0.85rem 2rem;
            display:flex;justify-content:space-between;align-items:center;
            box-shadow:0 1px 6px rgba(0,0,0,0.04);position:sticky;top:0;z-index:100;">
    <div>
        <div style="font-size:0.68rem;font-weight:700;color:#999;text-transform:uppercase;letter-spacing:0.1em;">Oracle Finance Platform</div>
        <div style="font-size:1.05rem;font-weight:700;color:#212121;margin-top:1px;">FinanceIQ · Intelligent Oracle Interface</div>
    </div>
    <div style="display:flex;align-items:center;gap:1.4rem;">
        <div style="font-size:0.77rem;color:#999;">Finance Team · FY2025</div>
        <div style="display:flex;align-items:center;gap:6px;">
            <div style="width:7px;height:7px;border-radius:50%;background:#22C55E;"></div>
            <span style="font-size:0.77rem;color:#22C55E;font-weight:600;">Oracle Connected</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

P = "padding:1.5rem 2rem;"
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Report Agent",
    "Report Viewer",
    "Oracle Data Entry",
    "Audit Log",
    "Architecture",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — REPORT AGENT CHAT
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#ED1C2E 0%,#B01020 100%);
                    border-radius:14px;padding:2rem;color:white;margin-bottom:1.5rem;
                    box-shadow:0 8px 32px rgba(237,28,46,0.22);">
            <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.13em;opacity:0.75;margin-bottom:8px;">Finance Report Agent</div>
            <div style="font-size:1.35rem;font-weight:700;margin-bottom:0.5rem;letter-spacing:-0.02em;">Generate Finance Reports via Natural Language</div>
            <div style="font-size:0.87rem;opacity:0.88;line-height:1.65;">
                Describe the report you need. The agent pipeline will fetch data from Oracle, apply finance logic, and format the output.
            </div>
            <div style="margin-top:1.3rem;display:flex;flex-wrap:wrap;gap:0.7rem;">
                <div style="background:rgba(255,255,255,0.14);border-radius:6px;padding:7px 14px;font-size:0.78rem;font-weight:500;border:1px solid rgba(255,255,255,0.2);">"Generate a Bill to Accounting to Reinsurer using FY2025Q3 data"</div>
                <div style="background:rgba(255,255,255,0.14);border-radius:6px;padding:7px 14px;font-size:0.78rem;font-weight:500;border:1px solid rgba(255,255,255,0.2);">"Claims Recovery Statement for Q3 2025 to Broker"</div>
                <div style="background:rgba(255,255,255,0.14);border-radius:6px;padding:7px 14px;font-size:0.78rem;font-weight:500;border:1px solid rgba(255,255,255,0.2);">"Premium listing for FY2025Q1 to Internal Accounting"</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    for i, msg in enumerate(st.session_state.messages):
        if msg["role"]=="user":
            st.markdown(chat_user(msg["content"]), unsafe_allow_html=True)
        elif msg["role"]=="assistant":
            st.markdown(chat_assistant(msg["content"]), unsafe_allow_html=True)
        elif msg["role"]=="suggestions":
            suggs = get_suggestions(msg.get("report_type","bill_to_accounting"))
            st.markdown('<div class="suggestions-block" style="padding-left:40px;margin-bottom:1rem;"><div style="font-size:0.7rem;font-weight:700;color:#999;text-transform:uppercase;letter-spacing:0.09em;margin-bottom:0.5rem;">Suggested follow-up queries</div></div>', unsafe_allow_html=True)
            ca, cb = st.columns(2)
            pairs  = [(suggs[j], suggs[j+1] if j+1<len(suggs) else None) for j in range(0,len(suggs),2)]
            for lq, rq in pairs:
                with ca:
                    st.markdown('<div class="suggest-btn">', unsafe_allow_html=True)
                    if st.button(lq, key=f"s_{i}_{lq[:18]}"): st.session_state.pending_query = lq
                    st.markdown('</div>', unsafe_allow_html=True)
                if rq:
                    with cb:
                        st.markdown('<div class="suggest-btn">', unsafe_allow_html=True)
                        if st.button(rq, key=f"s_{i}_{rq[:18]}"): st.session_state.pending_query = rq
                        st.markdown('</div>', unsafe_allow_html=True)

    alog_ph = st.empty()
    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    ci, cs = st.columns([6,1])
    with ci:
        user_query = st.text_input("rq", value=st.session_state.pending_query or "",
            placeholder='e.g. "Generate a Bill to Accounting to Reinsurer using FY2025Q3 data"',
            label_visibility="collapsed", key="chat_input")
    with cs:
        send_btn = st.button("Send", key="chat_send", use_container_width=True)

    if st.session_state.pending_query and not send_btn:
        st.session_state.pending_query = None
        st.rerun()

    if send_btn and user_query.strip():
        st.session_state.messages.append({"role":"user","content":user_query})
        parsed = parse_report_query(user_query)
        with st.spinner(""):
            report = run_report_pipeline(parsed, alog_ph)
        time.sleep(0.3); alog_ph.empty()
        st.session_state.reports.insert(0, report)
        bal = report["finance"].get("balance_due", 0)
        bal_str = f"<b>Settlement balance: ${abs(bal):,.2f} {'payable to reinsurer' if bal>0 else 'receivable'}</b><br><br>" if bal else ""
        resp = (f"Report generated successfully.<br><br><b>{report['report_label']}</b> for <b>{report['counterparty']}</b> — <b>{report['fy']} {report['quarter']}</b><br><br>"
                f"{bal_str}<span style='font-family:DM Mono,monospace;font-size:0.84em;color:#ED1C2E;'>Report ID: {report['report_id']}</span>&nbsp; · &nbsp;{report['rows_fetched']} records from Oracle<br><br>Open the <b>Report Viewer</b> tab to view the full output.")
        st.session_state.messages.append({"role":"assistant","content":resp})
        st.session_state.messages.append({"role":"suggestions","report_type":report["report_type"]})
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — REPORT VIEWER
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)
    if not st.session_state.reports:
        st.markdown("""<div style="text-align:center;padding:5rem 2rem;">
            <div style="font-size:1rem;font-weight:600;color:#666;">No reports generated yet</div>
            <div style="font-size:0.85rem;color:#999;margin-top:0.4rem;">Use the Report Agent tab or Quick Report panel to generate a report.</div>
        </div>""", unsafe_allow_html=True)
    else:
        if len(st.session_state.reports)>1:
            opts   = {f"{r['report_id']} · {r['report_label']} ({r['fy']} {r['quarter']})":i for i,r in enumerate(st.session_state.reports)}
            chosen = st.selectbox("Select Report", list(opts.keys()), key="rv_sel")
            idx    = opts[chosen]
        else: idx=0
        report = st.session_state.reports[idx]
        ca,cb,_ = st.columns([1,1,5])
        with ca:
            st.download_button("Export JSON", data=json.dumps(report,indent=2,default=str), file_name=f"{report['report_id']}.json", mime="application/json", use_container_width=True)
        with cb:
            flat = {k:v for k,v in report.items() if k!="finance"}
            flat.update({f"finance_{k}":v for k,v in report["finance"].items() if not isinstance(v,(list,dict))})
            st.download_button("Export CSV", data=pd.DataFrame([flat]).to_csv(index=False), file_name=f"{report['report_id']}.csv", mime="text/csv", use_container_width=True)
        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        render_report(report)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — ORACLE DATA ENTRY
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;margin-bottom:1.5rem;">
        <div>
            <div style="font-size:1.1rem;font-weight:700;color:#212121;">Oracle Data Entry</div>
            <div style="font-size:0.85rem;color:#666;margin-top:3px;max-width:600px;">
                Post entries directly to Oracle Financials via natural language chat or the structured form below.
                All entry types are supported — journal entries, AP/AR, policies, claims, and reinsurance transactions.
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:8px;background:#F0FDF4;border:1px solid #BBF7D0;border-radius:8px;padding:8px 14px;">
            <div style="width:7px;height:7px;border-radius:50%;background:#22C55E;"></div>
            <span style="font-size:0.78rem;font-weight:600;color:#15803D;">Oracle Financials Connected  ·  Schema: FIN_INSURANCE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Entry type capability cards
    st.markdown('<div style="font-size:0.74rem;font-weight:700;color:#666;text-transform:uppercase;letter-spacing:0.09em;margin-bottom:0.7rem;">Supported Entry Types</div>', unsafe_allow_html=True)
    cap_cols = st.columns(len(ENTRY_TYPES))
    for i,(etype, meta) in enumerate(ENTRY_TYPES.items()):
        with cap_cols[i]:
            is_active = st.session_state.gl_active_type == etype
            cls = "entry-pill-active" if is_active else "entry-pill"
            st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
            if st.button(etype, key=f"pill_{etype}"):
                st.session_state.gl_active_type = etype
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:0.2rem'></div>", unsafe_allow_html=True)

    # Show selected type description
    active_meta = ENTRY_TYPES[st.session_state.gl_active_type]
    st.markdown(f"""
    <div style="background:#F7F7F8;border-left:3px solid {active_meta['color']};border-radius:0 8px 8px 0;
                padding:0.6rem 1rem;margin-bottom:1.2rem;font-size:0.82rem;color:#444;">
        <b>{st.session_state.gl_active_type}</b> — {active_meta['desc']}
        &nbsp;&nbsp;|&nbsp;&nbsp;Oracle Table: <span style="font-family:'DM Mono',monospace;color:{active_meta['color']};">{active_meta['table']}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Two-column layout: Chatbot | Form ────────────────────────────────────
    col_chat, col_form = st.columns([1, 1], gap="large")

    # ── LEFT: GL Chatbot ─────────────────────────────────────────────────────
    with col_chat:
        st.markdown(f"""
        <div style="background:white;border:1px solid #EBEBEB;border-radius:12px;
                    padding:1.2rem 1.4rem 0.8rem;box-shadow:0 2px 10px rgba(0,0,0,0.05);">
            <div style="font-size:0.74rem;font-weight:700;color:#ED1C2E;text-transform:uppercase;
                        letter-spacing:0.1em;margin-bottom:0.8rem;">Oracle Entry Assistant</div>
        """, unsafe_allow_html=True)

        # Welcome state
        if not st.session_state.gl_messages:
            st.markdown(f"""
            <div style="background:#F7F7F8;border-radius:10px;padding:1rem 1.2rem;margin-bottom:0.8rem;border-left:3px solid {active_meta['color']};">
                <div style="font-size:0.83rem;font-weight:600;color:#212121;margin-bottom:6px;">
                    Describe your Oracle entry in plain language.
                </div>
                <div style="font-size:0.79rem;color:#666;line-height:1.6;">
                    Examples:<br>
                    &nbsp;"Post a journal entry — debit claims expense $250,000 credit claims payable for Sep-25"<br>
                    &nbsp;"Create an AP invoice for Swiss Re for $180,000 USD due 30 days"<br>
                    &nbsp;"Register a new property policy for Baxter Steel, sum insured $5M, inception 2025-10-01"<br>
                    &nbsp;"Open a claim for Meridian Logistics — storm damage, incurred $350,000 reserve $400,000"<br>
                    &nbsp;"Post reinsurance cession — treaty TRY-2025-007, ceded premium $500,000 for Sep-25"
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Chat messages
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.gl_messages:
                if msg["role"]=="user":
                    st.markdown(chat_user(msg["content"]), unsafe_allow_html=True)
                elif msg["role"]=="assistant":
                    st.markdown(chat_assistant(msg["content"], avatar_color="#1D6FA4"), unsafe_allow_html=True)
                elif msg["role"]=="system_success":
                    st.markdown(f"""<div class="chat-bubble" style="display:flex;justify-content:flex-start;margin-bottom:0.8rem;">
                        <div style="display:flex;gap:10px;align-items:flex-start;max-width:90%;">
                            <div style="width:30px;height:30px;background:#1A9E5C;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;">
                                <span style="color:white;font-size:0.68rem;font-weight:700;">Ok</span>
                            </div>
                            <div style="background:#F0FDF4;color:#166534;border:1px solid #BBF7D0;border-radius:14px 14px 14px 3px;padding:0.85rem 1.1rem;font-size:0.88rem;line-height:1.6;">
                                {msg["content"]}
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

        # Live agent log placeholder
        gl_log_ph = st.empty()

        # Pending entry confirmation panel
        if st.session_state.gl_pending:
            p = st.session_state.gl_pending
            color = ENTRY_TYPES.get(p.get("entry_type","Journal Entry"),{}).get("color","#ED1C2E")
            st.markdown(f"""
            <div class="entry-card" style="background:#FFFBEB;border:1.5px solid #FDE68A;border-radius:10px;
                        padding:1rem 1.2rem;margin:0.8rem 0;">
                <div style="font-size:0.7rem;font-weight:700;color:#D97706;text-transform:uppercase;letter-spacing:0.09em;margin-bottom:0.5rem;">
                    Pending — Review Before Posting
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 12px;font-size:0.8rem;margin-bottom:0.8rem;">
                    {"".join(f'<div><span style="color:#999;">{k.replace("_"," ").title()}:</span> <b>{v}</b></div>' for k,v in p.items() if k not in ["parsed_from","posted_by","status"] and str(v).strip())}
                </div>
            </div>
            """, unsafe_allow_html=True)
            cc1, cc2 = st.columns(2)
            with cc1:
                st.markdown('<div class="confirm-btn">', unsafe_allow_html=True)
                post_btn = st.button("Post to Oracle", key="gl_post", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with cc2:
                if st.button("Discard Entry", key="gl_discard", use_container_width=True):
                    st.session_state.gl_pending = None
                    st.session_state.gl_messages.append({"role":"assistant","content":"Entry discarded. You may describe a new entry below."})
                    st.rerun()

            if post_btn:
                result = run_oracle_write(st.session_state.gl_pending, gl_log_ph)
                time.sleep(0.3); gl_log_ph.empty()
                final_entry = {**st.session_state.gl_pending, **result}
                st.session_state.gl_entries.insert(0, final_entry)
                st.session_state.oracle_log.insert(0, final_entry)
                confirm_msg = build_gl_confirm_response(st.session_state.gl_pending, result)
                st.session_state.gl_messages.append({"role":"system_success","content":confirm_msg})
                st.session_state.gl_pending = None
                st.rerun()

        # Input
        gi, gs = st.columns([5, 1])
        with gi:
            gl_query = st.text_input("gl_q", placeholder='Describe the Oracle entry in plain language...', label_visibility="collapsed", key="gl_input")
        with gs:
            gl_send = st.button("Send", key="gl_send", use_container_width=True)

        if gl_send and gl_query.strip():
            st.session_state.gl_messages.append({"role":"user","content":gl_query})
            # Auto-switch entry type based on query
            detected = detect_entry_type(gl_query)
            if detected != st.session_state.gl_active_type:
                st.session_state.gl_active_type = detected
            parsed_entry = parse_gl_intent(gl_query)
            response_msg = build_gl_parse_response(parsed_entry)
            st.session_state.gl_messages.append({"role":"assistant","content":response_msg})
            st.session_state.gl_pending = parsed_entry
            st.rerun()

    # ── RIGHT: Structured Form ────────────────────────────────────────────────
    with col_form:
        st.markdown(f"""
        <div style="background:white;border:1px solid #EBEBEB;border-radius:12px;
                    padding:1.2rem 1.4rem 0.4rem;box-shadow:0 2px 10px rgba(0,0,0,0.05);margin-bottom:0.8rem;">
            <div style="font-size:0.74rem;font-weight:700;color:{active_meta['color']};text-transform:uppercase;
                        letter-spacing:0.1em;margin-bottom:0.8rem;">Structured Entry Form</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        form_result = render_entry_form(st.session_state.gl_active_type)

        form_log_ph = st.empty()
        st.markdown('<div class="confirm-btn">', unsafe_allow_html=True)
        submit_form = st.button(f"Post {st.session_state.gl_active_type} to Oracle", key="form_submit", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if submit_form and form_result:
            # Basic validation
            amt_key = next((k for k in form_result if "amount" in k or "premium" in k or "incurred" in k), None)
            if amt_key and form_result.get(amt_key,0) == 0:
                st.warning("Please enter an amount greater than zero before posting.")
            else:
                result = run_oracle_write(form_result, form_log_ph)
                time.sleep(0.3); form_log_ph.empty()
                final_entry = {**form_result, **result}
                st.session_state.gl_entries.insert(0, final_entry)
                st.session_state.oracle_log.insert(0, final_entry)
                st.success(f"Posted to Oracle — Transaction ID: **{result['oracle_txn_id']}**  |  Batch: {result['batch_id']}  |  Status: {result['status']}")
                st.session_state.gl_messages.append({"role":"system_success","content":build_gl_confirm_response(form_result, result)})

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — AUDIT LOG
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)
    st.markdown(section_hdr("Oracle Write Audit Log","Complete record of all entries posted to Oracle Financials in this session"), unsafe_allow_html=True)

    if not st.session_state.oracle_log:
        st.markdown("""<div style="text-align:center;padding:4rem 2rem;">
            <div style="font-size:1rem;font-weight:600;color:#666;">No entries posted yet</div>
            <div style="font-size:0.85rem;color:#999;margin-top:0.4rem;">Use the Oracle Data Entry tab to post entries. All transactions will appear here.</div>
        </div>""", unsafe_allow_html=True)
    else:
        # Summary KPIs
        total_entries = len(st.session_state.oracle_log)
        type_counts   = {}
        for e in st.session_state.oracle_log:
            type_counts[e["entry_type"]] = type_counts.get(e["entry_type"],0) + 1

        ck1, ck2, ck3 = st.columns(3)
        with ck1: st.markdown(kpi("Total Entries Posted", str(total_entries), "This session"), unsafe_allow_html=True)
        with ck2: st.markdown(kpi("Entry Types Used", str(len(type_counts)), "Distinct Oracle modules"), unsafe_allow_html=True)
        with ck3: st.markdown(kpi("All Status", "POSTED", "Oracle confirmed", accent=True), unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # Per-entry cards
        for entry in st.session_state.oracle_log:
            et    = entry.get("entry_type","—")
            color = ENTRY_TYPES.get(et,{}).get("color","#666")
            table = ENTRY_TYPES.get(et,{}).get("table","—")

            # Build detail rows — exclude internal/meta keys
            skip = {"entry_type","oracle_txn_id","batch_id","posted_at","status","warnings","parsed_from","posted_by"}
            detail_items = [(k.replace("_"," ").title(), v) for k,v in entry.items() if k not in skip and str(v).strip() and v!=0]
            detail_html  = "".join(f'<div style="display:flex;gap:6px;padding:4px 0;border-bottom:1px solid #F5F5F5;"><span style="font-size:0.75rem;color:#999;min-width:130px;">{k}</span><span style="font-size:0.75rem;font-weight:500;color:#212121;">{v}</span></div>' for k,v in detail_items)

            with st.expander(f"{et}  ·  {entry.get('oracle_txn_id','—')}  ·  {entry.get('posted_at','')[:16]}", expanded=False):
                st.markdown(f"""
                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.8rem;margin-bottom:1rem;">
                    <div style="background:#F7F7F8;border-radius:8px;padding:0.7rem 0.9rem;">
                        <div style="font-size:0.65rem;color:#999;text-transform:uppercase;font-weight:700;">Oracle Txn ID</div>
                        <div style="font-family:'DM Mono',monospace;font-weight:700;color:{color};font-size:0.9rem;">{entry.get("oracle_txn_id","—")}</div>
                    </div>
                    <div style="background:#F7F7F8;border-radius:8px;padding:0.7rem 0.9rem;">
                        <div style="font-size:0.65rem;color:#999;text-transform:uppercase;font-weight:700;">Batch ID</div>
                        <div style="font-family:'DM Mono',monospace;font-weight:600;color:#212121;">{entry.get("batch_id","—")}</div>
                    </div>
                    <div style="background:#F7F7F8;border-radius:8px;padding:0.7rem 0.9rem;">
                        <div style="font-size:0.65rem;color:#999;text-transform:uppercase;font-weight:700;">Oracle Table</div>
                        <div style="font-size:0.78rem;font-weight:600;color:#212121;">{table}</div>
                    </div>
                    <div style="background:#F0FDF4;border-radius:8px;padding:0.7rem 0.9rem;">
                        <div style="font-size:0.65rem;color:#15803D;text-transform:uppercase;font-weight:700;">Status</div>
                        <div style="font-weight:700;color:#1A9E5C;">{entry.get("status","—")}</div>
                    </div>
                </div>
                <div style="font-size:0.7rem;font-weight:700;color:#666;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem;">Entry Details</div>
                {detail_html}
                """, unsafe_allow_html=True)

                # Export single entry
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        log_export = json.dumps(st.session_state.oracle_log, indent=2, default=str)
        st.download_button("Export Full Audit Log (JSON)", data=log_export, file_name=f"oracle_audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", mime="application/json")

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — ARCHITECTURE
# ─────────────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)
    st.markdown("""
    <div style="max-width:900px;">
    <div style="font-size:1.12rem;font-weight:700;color:#212121;margin-bottom:0.3rem;">Platform Architecture</div>
    <div style="font-size:0.87rem;color:#666;margin-bottom:2rem;line-height:1.65;">
        FinanceIQ is a unified Oracle Financials interface — combining a 3-agent report generation pipeline
        with a conversational data entry layer that posts directly to Oracle via REST API.
    </div>

    <!-- Module overview -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:2rem;">
        <div style="background:white;border:1.5px solid #EBEBEB;border-radius:12px;padding:1.2rem 1.4rem;box-shadow:0 2px 10px rgba(0,0,0,0.05);">
            <div style="font-size:0.7rem;font-weight:700;color:#ED1C2E;text-transform:uppercase;letter-spacing:0.09em;margin-bottom:8px;">Module 1 — Finance Report Agent</div>
            <div style="font-size:0.82rem;color:#666;line-height:1.6;">
                3-agent LangGraph pipeline. Agent 1 fetches Oracle data, Agent 2 applies finance and actuarial logic,
                Agent 3 formats output to standard report templates. Outputs: Bill to Accounting, Premium Listings,
                Claims Recovery, Loss Run, and Bordereaux reports.
            </div>
        </div>
        <div style="background:white;border:1.5px solid #EBEBEB;border-radius:12px;padding:1.2rem 1.4rem;box-shadow:0 2px 10px rgba(0,0,0,0.05);">
            <div style="font-size:0.7rem;font-weight:700;color:#1D6FA4;text-transform:uppercase;letter-spacing:0.09em;margin-bottom:8px;">Module 2 — Oracle Data Entry Agent</div>
            <div style="font-size:0.82rem;color:#666;line-height:1.6;">
                Conversational chatbot and structured forms for posting directly to Oracle Financials.
                Supports Journal Entries, AP Invoices, AR Transactions, Policy Master, Claims, and Reinsurance entries.
                Full audit log with Oracle transaction IDs.
            </div>
        </div>
    </div>

    <!-- Oracle entry types table -->
    <div style="font-size:0.9rem;font-weight:700;color:#212121;margin-bottom:0.8rem;">Supported Oracle Entry Types</div>
    <div style="background:white;border:1px solid #EBEBEB;border-radius:12px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.05);margin-bottom:2rem;">
    """ + "".join([
        f"""<div style="display:grid;grid-template-columns:180px 1fr 200px;gap:1rem;
                        padding:0.85rem 1.2rem;border-bottom:1px solid #F5F5F5;align-items:start;">
            <div style="font-size:0.82rem;font-weight:700;color:{meta['color']};">{etype}</div>
            <div style="font-size:0.8rem;color:#666;">{meta['desc']}</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.72rem;color:#999;">{meta['table']}</div>
        </div>"""
        for etype, meta in ENTRY_TYPES.items()
    ]) + """
    </div>

    <!-- Integration placeholders -->
    <div style="font-size:0.9rem;font-weight:700;color:#212121;margin-bottom:0.8rem;">Integration Placeholders</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;margin-bottom:2rem;">
        <div style="background:#FFFBEB;border:1.5px solid #FDE68A;border-radius:10px;padding:1rem 1.2rem;">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
                <div style="width:8px;height:8px;border-radius:50%;background:#D97706;"></div>
                <div style="font-size:0.68rem;font-weight:700;color:#D97706;text-transform:uppercase;letter-spacing:0.09em;">OpenAI API · Pending</div>
            </div>
            <div style="font-family:'DM Mono',monospace;font-size:0.74rem;color:#666;word-break:break-all;margin-bottom:5px;">OPENAI_API_KEY = "sk-PLACEHOLDER"</div>
            <div style="font-size:0.72rem;color:#999;line-height:1.5;">LangChain + GPT-4o for report intent parsing, GL entry NLP, and finance reasoning.</div>
        </div>
        <div style="background:#FFFBEB;border:1.5px solid #FDE68A;border-radius:10px;padding:1rem 1.2rem;">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
                <div style="width:8px;height:8px;border-radius:50%;background:#D97706;"></div>
                <div style="font-size:0.68rem;font-weight:700;color:#D97706;text-transform:uppercase;letter-spacing:0.09em;">Oracle Financials API · Pending</div>
            </div>
            <div style="font-family:'DM Mono',monospace;font-size:0.74rem;color:#666;word-break:break-all;margin-bottom:5px;">ORACLE_API_BASE_URL = "https://..."</div>
            <div style="font-size:0.72rem;color:#999;line-height:1.5;">REST API for GL reads (reports) and GL/AP/AR/Policy/Claims writes (data entry).</div>
        </div>
    </div>

    <!-- Tech stack -->
    <div style="font-size:0.9rem;font-weight:700;color:#212121;margin-bottom:0.8rem;">Technology Stack</div>
    <div style="display:flex;flex-wrap:wrap;gap:0.5rem;">
    """ + "".join([
        f'<div style="background:white;border:1px solid #EBEBEB;border-radius:20px;padding:5px 14px;font-size:0.78rem;font-weight:500;color:#212121;">{t}</div>'
        for t in ["Streamlit · UI","LangGraph · Orchestration","LangChain · LLM Tooling","OpenAI GPT-4o · Reasoning","Oracle REST API · Read + Write","Pandas · Data Processing","Python 3.11+"]
    ]) + """</div></div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
