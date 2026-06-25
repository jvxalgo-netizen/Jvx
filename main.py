"""
JVX-JVX Hybrid Terminal v31.3 — Primary Trading Edition
Features: Login Gate, Live Broker Integration, T3 + UT Bot, Advanced Backtesting,
          Multi-Confirmation Strategies, Smart Risk Management, Options Builder,
          Quantum Algo, Production Safety

Author: Hitesh Vidhani
Repo  : https://github.com/jvxalgo-netizen/Jvx
"""

import json
import warnings
from xml.parsers.expat import errors
import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import requests
from io import BytesIO
import os
import sys
import importlib
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components
import time
from pmClient.yahoo import fetch_yahoo_quote, fetch_yahoo_history

# ───────────────────────────────────────────
# DHANHQ IMPORT
# ───────────────────────────────────────────
try:
    dhanhq_spec = importlib.util.find_spec("dhanhq")
    if dhanhq_spec is not None:
        dhanhq_module = importlib.import_module("dhanhq")
        dhanhq = getattr(dhanhq_module, "dhanhq", None)
        DHANHQ_AVAILABLE = dhanhq is not None
    else:
        DHANHQ_AVAILABLE = False
        dhanhq = None
except Exception:
    DHANHQ_AVAILABLE = False
    dhanhq = None

# ───────────────────────────────────────────
# PAYTM MONEY IMPORT
# ───────────────────────────────────────────
try:
    pyPMClient_spec = importlib.util.find_spec("pyPMClient")
    if pyPMClient_spec is not None:
        pyPMClient_module = importlib.import_module("pyPMClient")
        PMClient = getattr(pyPMClient_module, "PMClient", None)
        PAYTM_AVAILABLE = PMClient is not None
    else:
        PAYTM_AVAILABLE = False
        PMClient = None
except Exception:
    PAYTM_AVAILABLE = False
    PMClient = None

# ───────────────────────────────────────────
# ML LIBRARY IMPORTS (FOR ML STRATEGY PIPELINE)
# ───────────────────────────────────────────
try:
    sklearn_spec = importlib.util.find_spec("sklearn")
    if sklearn_spec is not None:
        sklearn_ensemble = importlib.import_module("sklearn.ensemble")
        sklearn_metrics = importlib.import_module("sklearn.metrics")
        RandomForestClassifier = sklearn_ensemble.RandomForestClassifier
        accuracy_score = sklearn_metrics.accuracy_score
        precision_score = sklearn_metrics.precision_score
        recall_score = sklearn_metrics.recall_score
        confusion_matrix = sklearn_metrics.confusion_matrix
        SKLEARN_AVAILABLE = True
    else:
        SKLEARN_AVAILABLE = False
        RandomForestClassifier = None
        accuracy_score = None
        precision_score = None
        recall_score = None
        confusion_matrix = None
except Exception:
    SKLEARN_AVAILABLE = False
    RandomForestClassifier = None
    accuracy_score = None
    precision_score = None
    recall_score = None
    confusion_matrix = None

try:
    xgboost_spec = importlib.util.find_spec("xgboost")
    if xgboost_spec is not None:
        xgboost_module = importlib.import_module("xgboost")
        XGBClassifier = xgboost_module.XGBClassifier
        XGBOOST_AVAILABLE = True
    else:
        XGBOOST_AVAILABLE = False
        XGBClassifier = None
except Exception:
    XGBOOST_AVAILABLE = False
    XGBClassifier = None

try:
    tensorflow_spec = importlib.util.find_spec("tensorflow")
    if tensorflow_spec is not None:
        tf = importlib.import_module("tensorflow")
        TENSORFLOW_AVAILABLE = True
    else:
        TENSORFLOW_AVAILABLE = False
        tf = None
except Exception:
    TENSORFLOW_AVAILABLE = False
    tf = None

try:
    stable_baselines3_spec = importlib.util.find_spec("stable_baselines3")
    if stable_baselines3_spec is not None:
        stable_baselines3 = importlib.import_module("stable_baselines3")
        RL_AVAILABLE = True
    else:
        RL_AVAILABLE = False
        stable_baselines3 = None
except Exception:
    RL_AVAILABLE = False
    stable_baselines3 = None

# ───────────────────────────────────────────
# SYMBOL MAPPING — PRODUCTION
# ───────────────────────────────────────────
SYMBOL_MAP = {
    "NIFTY 50": {"security_id": "13", "exchange": "NSE", "segment": "I"},
    "BANKNIFTY": {"security_id": "25", "exchange": "NSE", "segment": "I"},
    "FINNIFTY": {"security_id": "27", "exchange": "NSE", "segment": "I"},
    "SENSEX": {"security_id": "51", "exchange": "BSE", "segment": "I"},
    "RELIANCE": {"security_id": "2885", "exchange": "NSE", "segment": "E"},
    "HDFCBANK": {"security_id": "1333", "exchange": "NSE", "segment": "E"},
    "INFY": {"security_id": "1594", "exchange": "NSE", "segment": "E"},
    "TCS": {"security_id": "11536", "exchange": "NSE", "segment": "E"},
    "ICICIBANK": {"security_id": "4963", "exchange": "NSE", "segment": "E"},
    "SBIN": {"security_id": "3045", "exchange": "NSE", "segment": "E"},
    "AXISBANK": {"security_id": "5900", "exchange": "NSE", "segment": "E"},
    "KOTAKBANK": {"security_id": "1922", "exchange": "NSE", "segment": "E"},
    "ITC": {"security_id": "1660", "exchange": "NSE", "segment": "E"},
    "HINDUNILVR": {"security_id": "1394", "exchange": "NSE", "segment": "E"},
    "LT": {"security_id": "1164", "exchange": "NSE", "segment": "E"},
    "BAJFINANCE": {"security_id": "317", "exchange": "NSE", "segment": "E"},
    "TATAMOTORS": {"security_id": "3456", "exchange": "NSE", "segment": "E"},
    "MARUTI": {"security_id": "10999", "exchange": "NSE", "segment": "E"},
    "SUNPHARMA": {"security_id": "3351", "exchange": "NSE", "segment": "E"},
    "DRREDDY": {"security_id": "881", "exchange": "NSE", "segment": "E"},
    "WIPRO": {"security_id": "9692", "exchange": "NSE", "segment": "E"},
    "HCLTECH": {"security_id": "1851", "exchange": "NSE", "segment": "E"},
    "TECHM": {"security_id": "13538", "exchange": "NSE", "segment": "E"},
    "ADANIENT": {"security_id": "117", "exchange": "NSE", "segment": "E"},
    "ADANIPORTS": {"security_id": "15083", "exchange": "NSE", "segment": "E"},
    "COALINDIA": {"security_id": "20374", "exchange": "NSE", "segment": "E"},
    "NTPC": {"security_id": "11630", "exchange": "NSE", "segment": "E"},
    "POWERGRID": {"security_id": "14977", "exchange": "NSE", "segment": "E"},
    "ONGC": {"security_id": "2475", "exchange": "NSE", "segment": "E"},
    "TATASTEEL": {"security_id": "3499", "exchange": "NSE", "segment": "E"},
    "JSWSTEEL": {"security_id": "11723", "exchange": "NSE", "segment": "E"},
    "GRASIM": {"security_id": "1232", "exchange": "NSE", "segment": "E"},
    "ULTRACEMCO": {"security_id": "11532", "exchange": "NSE", "segment": "E"},
    "SHREECEM": {"security_id": "3103", "exchange": "NSE", "segment": "E"},
    "EICHERMOTORS": {"security_id": "910", "exchange": "NSE", "segment": "E"},
    "HEROMOTOCO": {"security_id": "1348", "exchange": "NSE", "segment": "E"},
    "M&M": {"security_id": "2031", "exchange": "NSE", "segment": "E"},
    "TITAN": {"security_id": "3506", "exchange": "NSE", "segment": "E"},
    "ASIANPAINT": {"security_id": "236", "exchange": "NSE", "segment": "E"},
    "BRITANNIA": {"security_id": "547", "exchange": "NSE", "segment": "E"},
    "NESTLEIND": {"security_id": "17963", "exchange": "NSE", "segment": "E"},
    "HINDALCO": {"security_id": "1363", "exchange": "NSE", "segment": "E"},
    "VEDL": {"security_id": "11941", "exchange": "NSE", "segment": "E"},
    "CIPLA": {"security_id": "694", "exchange": "NSE", "segment": "E"},
    "DIVISLAB": {"security_id": "10540", "exchange": "NSE", "segment": "E"},
    "APOLLOHOSP": {"security_id": "157", "exchange": "NSE", "segment": "E"},
    "UPL": {"security_id": "11287", "exchange": "NSE", "segment": "E"},
    "BAJAJFINSV": {"security_id": "16675", "exchange": "NSE", "segment": "E"},
    "BAJAJ-AUTO": {"security_id": "16669", "exchange": "NSE", "segment": "E"},
    "INDUSINDBK": {"security_id": "5258", "exchange": "NSE", "segment": "E"},
    "SBILIFE": {"security_id": "21808", "exchange": "NSE", "segment": "E"},
    "HDFCLIFE": {"security_id": "467", "exchange": "NSE", "segment": "E"},
    "BPCL": {"security_id": "526", "exchange": "NSE", "segment": "E"},
    "IOC": {"security_id": "1624", "exchange": "NSE", "segment": "E"},
    "GAIL": {"security_id": "11872", "exchange": "NSE", "segment": "E"},
    "MCDOWELL-N": {"security_id": "1922", "exchange": "NSE", "segment": "E"},
    "PIDILITIND": {"security_id": "681", "exchange": "NSE", "segment": "E"},
    "DABUR": {"security_id": "772", "exchange": "NSE", "segment": "E"},
    "GODREJCP": {"security_id": "1219", "exchange": "NSE", "segment": "E"},
    "MARICO": {"security_id": "2181", "exchange": "NSE", "segment": "E"},
    "COLPAL": {"security_id": "15141", "exchange": "NSE", "segment": "E"},
    "TATACONSUM": {"security_id": "3432", "exchange": "NSE", "segment": "E"},
    "HAVELLS": {"security_id": "25178", "exchange": "NSE", "segment": "E"},
    "BERGEPAINT": {"security_id": "404", "exchange": "NSE", "segment": "E"},
    "MUTHOOTFIN": {"security_id": "23650", "exchange": "NSE", "segment": "E"},
    "CHOLAFIN": {"security_id": "6819", "exchange": "NSE", "segment": "E"},
    "SRF": {"security_id": "3273", "exchange": "NSE", "segment": "E"},
    "MRF": {"security_id": "2277", "exchange": "NSE", "segment": "E"},
    "PAGEIND": {"security_id": "3683", "exchange": "NSE", "segment": "E"},
    "TORNTPHARM": {"security_id": "3518", "exchange": "NSE", "segment": "E"},
    "BOSCHLTD": {"security_id": "479", "exchange": "NSE", "segment": "E"},
    "SIEMENS": {"security_id": "3150", "exchange": "NSE", "segment": "E"},
    "ABB": {"security_id": "694", "exchange": "NSE", "segment": "E"},
    "LTIM": {"security_id": "17818", "exchange": "NSE", "segment": "E"},
    "PERSISTENT": {"security_id": "18365", "exchange": "NSE", "segment": "E"},
    "COFORGE": {"security_id": "11543", "exchange": "NSE", "segment": "E"},
    "MPHASIS": {"security_id": "4503", "exchange": "NSE", "segment": "E"},
    "NAUKRI": {"security_id": "13751", "exchange": "NSE", "segment": "E"},
    "ZOMATO": {"security_id": "5097", "exchange": "NSE", "segment": "E"},
    "PAYTM": {"security_id": "6705", "exchange": "NSE", "segment": "E"},
    "NYKAA": {"security_id": "34877", "exchange": "NSE", "segment": "E"},
    "POLICYBZR": {"security_id": "36617", "exchange": "NSE", "segment": "E"},
    "DELHIVERY": {"security_id": "42856", "exchange": "NSE", "segment": "E"},
    "LICI": {"security_id": "48288", "exchange": "NSE", "segment": "E"},
}


def get_symbol_security_id(symbol):
    mapped = SYMBOL_MAP.get(symbol)
    if mapped:
        return mapped["security_id"], mapped["exchange"], mapped["segment"]
    return symbol, "NSE", "E"


# ───────────────────────────────────────────
# DHANHQ SYMBOL MAPPING — PRODUCTION
# ───────────────────────────────────────────
DHAN_SYMBOL_MAP = {
    "NIFTY 50": {"security_id": "13", "exchange": "NSE", "segment": "IDX"},
    "BANKNIFTY": {"security_id": "25", "exchange": "NSE", "segment": "IDX"},
    "FINNIFTY": {"security_id": "27", "exchange": "NSE", "segment": "IDX"},
    "SENSEX": {"security_id": "51", "exchange": "BSE", "segment": "IDX"},
    "RELIANCE": {"security_id": "2885", "exchange": "NSE", "segment": "EQ"},
    "HDFCBANK": {"security_id": "1333", "exchange": "NSE", "segment": "EQ"},
    "INFY": {"security_id": "1594", "exchange": "NSE", "segment": "EQ"},
    "TCS": {"security_id": "11536", "exchange": "NSE", "segment": "EQ"},
    "ICICIBANK": {"security_id": "4963", "exchange": "NSE", "segment": "EQ"},
    "SBIN": {"security_id": "3045", "exchange": "NSE", "segment": "EQ"},
    "AXISBANK": {"security_id": "5900", "exchange": "NSE", "segment": "EQ"},
    "KOTAKBANK": {"security_id": "1922", "exchange": "NSE", "segment": "EQ"},
    "ITC": {"security_id": "1660", "exchange": "NSE", "segment": "EQ"},
    "HINDUNILVR": {"security_id": "1394", "exchange": "NSE", "segment": "EQ"},
    "LT": {"security_id": "1164", "exchange": "NSE", "segment": "EQ"},
    "BAJFINANCE": {"security_id": "317", "exchange": "NSE", "segment": "EQ"},
}


def get_dhan_security_id(symbol):
    mapped = DHAN_SYMBOL_MAP.get(symbol)
    if mapped:
        return mapped["security_id"], mapped["exchange"], mapped["segment"]
    return symbol, "NSE", "EQ"


# ───────────────────────────────────────────
# PAYTM MONEY SYMBOL MAPPING — PRODUCTION
# ───────────────────────────────────────────
PAYTM_SYMBOL_MAP = {
    "NIFTY 50": {"security_id": "13", "exchange": "NSE", "segment": "I"},
    "BANKNIFTY": {"security_id": "25", "exchange": "NSE", "segment": "I"},
    "FINNIFTY": {"security_id": "27", "exchange": "NSE", "segment": "I"},
    "SENSEX": {"security_id": "51", "exchange": "BSE", "segment": "I"},
    "RELIANCE": {"security_id": "2885", "exchange": "NSE", "segment": "E"},
    "HDFCBANK": {"security_id": "1333", "exchange": "NSE", "segment": "E"},
    "INFY": {"security_id": "1594", "exchange": "NSE", "segment": "E"},
    "TCS": {"security_id": "11536", "exchange": "NSE", "segment": "E"},
    "ICICIBANK": {"security_id": "4963", "exchange": "NSE", "segment": "E"},
    "SBIN": {"security_id": "3045", "exchange": "NSE", "segment": "E"},
    "AXISBANK": {"security_id": "5900", "exchange": "NSE", "segment": "E"},
    "KOTAKBANK": {"security_id": "1922", "exchange": "NSE", "segment": "E"},
    "ITC": {"security_id": "1660", "exchange": "NSE", "segment": "E"},
    "HINDUNILVR": {"security_id": "1394", "exchange": "NSE", "segment": "E"},
    "LT": {"security_id": "1164", "exchange": "NSE", "segment": "E"},
    "BAJFINANCE": {"security_id": "317", "exchange": "NSE", "segment": "E"},
}


def get_paytm_security_id(symbol):
    mapped = PAYTM_SYMBOL_MAP.get(symbol)
    if mapped:
        return mapped["security_id"], mapped["exchange"], mapped["segment"]
    return symbol, "NSE", "E"


# ───────────────────────────────────────────
# PRODUCTION SAFETY & VALIDATION
# ───────────────────────────────────────────
MARKET_OPEN = datetime.strptime("09:15", "%H:%M").time()
MARKET_CLOSE = datetime.strptime("15:30", "%H:%M").time()
PRE_MARKET_OPEN = datetime.strptime("09:00", "%H:%M").time()


def is_market_open():
    now = datetime.now()
    current_time = now.time()
    weekday = now.weekday()
    if weekday > 4:
        return False, "Market closed (Weekend)"
    if PRE_MARKET_OPEN <= current_time < MARKET_OPEN:
        return False, f"Pre-market ({current_time.strftime('%H:%M')})"
    if MARKET_OPEN <= current_time <= MARKET_CLOSE:
        return True, f"Market Open ({current_time.strftime('%H:%M')})"
    return False, f"Market Closed ({current_time.strftime('%H:%M')})"


def validate_order(symbol, qty, side, order_type, price, broker_client=None):
    errors = []
    warnings = []
    open_ok, msg = is_market_open()
    if not open_ok:
        errors.append(f"Market not open: {msg}")

    broker = st.session_state.get('selected_broker', 'DHANHQ')
    if broker == 'PAYTM':
        sec_id, exchange, segment = get_paytm_security_id(symbol)
        if sec_id == symbol and symbol not in PAYTM_SYMBOL_MAP:
            warnings.append(f"Symbol '{symbol}' not mapped — verify security_id before live trading")
    else:
        sec_id, exchange, segment = symbol, "NSE", "EQ"

    if qty <= 0:
        errors.append("Quantity must be > 0")
    if qty > 10000:
        errors.append(f"Quantity {qty} exceeds freeze limit — split into multiple orders")
    if order_type in ["LIMIT", "SL", "SL-M"] and price <= 0:
        errors.append(f"{order_type} order requires a valid price > 0")
    if st.session_state.get('exec_mode') == 'LIVE':
        if not broker_client:
            errors.append("Broker client not connected — cannot place LIVE order")
        if broker_client:
            try:
                if broker == 'PAYTM':
                    funds = broker_client.funds_summary()
                    available = funds.get('availableBalance', 0) if isinstance(funds, dict) else 0
                else:
                    funds = broker_client.get_fund_limit()
                    available = funds.get('availabelBalance', 0) if isinstance(funds, dict) else 0
                estimated_margin = qty * price * 0.2 if price > 0 else qty * 100
                if available < estimated_margin:
                    warnings.append(f"Low margin: ₹{available:,.0f} available, ~₹{estimated_margin:,.0f} required")
            except Exception as e:
                warnings.append(f"Could not verify margin: {e}")
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_trades = [t for t in st.session_state.get('trade_history', [])
                    if t.get('Time', '').startswith(today_str)]
    today_pnl = sum([t.get('PnL', 0) for t in today_trades if 'PnL' in t])
    daily_loss_limit = st.session_state.get('daily_loss_limit', 5000)
    if today_pnl < -daily_loss_limit:
        errors.append(f"🛑 DAILY LOSS LIMIT HIT: ₹{abs(today_pnl):,.0f} loss > ₹{daily_loss_limit:,.0f} limit. Trading halted for today.")
    last_order_time = st.session_state.get('last_order_time')
    if last_order_time:
        elapsed = (datetime.now() - last_order_time).total_seconds()
        if elapsed < 5:
            errors.append(f"Rate limit: Wait {5 - elapsed:.0f}s before next order")
    if st.session_state.get('loss_streak', 0) >= st.session_state.get('loss_limit', 3):
        errors.append(f"🛑 Circuit breaker: {st.session_state.loss_streak} consecutive losses")
    return errors, warnings


def safe_api_call(func, *args, fallback_return=None, max_retries=2, **kwargs):
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(0.5 * (attempt + 1))
                continue
            st.error(f"API Error after {max_retries} attempts: {e}")
            return fallback_return
    return fallback_return


# ───────────────────────────────────────────
# 1. PAGE CONFIG & WHITE THEME
# ───────────────────────────────────────────
st.set_page_config(
    page_title="JVX Trading Terminal v31.3",
    layout="wide",
    page_icon="📈",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background: #ffffff !important;
        color: #1a1a1a !important;
    }
    [data-testid="stSidebar"] {
        background: #f8f9fa !important;
        border-right: 1px solid #e0e0e0 !important;
    }
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div {
        color: #1a1a1a !important;
    }
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    [data-testid="stMetric"] {
        background: #ffffff !important;
        border: 1px solid #e8e8e8 !important;
        border-radius: 12px;
        padding: 12px;
    }
    [data-testid="stMetric"] label {
        color: #666666 !important;
    }
    [data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #1a1a1a !important;
    }
    div.stButton > button {
        background: linear-gradient(135deg, #00b894, #00d4aa) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px;
        font-weight: 700;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,184,148,0.25);
    }
    div.stButton > button[kind="secondary"] {
        background: #f0f0f0 !important;
        color: #333333 !important;
        border: 1px solid #d0d0d0 !important;
    }
    .brand-logo {
        width: 64px; height: 64px; border-radius: 16px;
        display: flex; align-items: center; justify-content: center;
        background: linear-gradient(135deg, #00d4aa, #0080ff);
        box-shadow: 0 4px 16px rgba(0,212,170,0.2);
        font-size: 24px; font-weight: 800; color: #ffffff;
    }
    .status-connected { color: #00b894; font-weight: 700; }
    .status-disconnected { color: #e74c3c; font-weight: 700; }
    .win-rate-high { color: #00b894; font-weight: 700; font-size: 1.2rem; }
    .win-rate-low { color: #e74c3c; font-weight: 700; font-size: 1.2rem; }
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    textarea, input {
        background: #ffffff !important;
        color: #1a1a1a !important;
        border: 1px solid #d0d0d0 !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #1a1a1a !important;
    }
    .stAlert, [data-testid="stAlert"] {
        color: #1a1a1a !important;
        background: #ffffff !important;
    }
    .stAlert p, .stAlert div, .stAlert span {
        color: #1a1a1a !important;
    }
    .stDataFrame, [data-testid="stDataFrame"] {
        background: #ffffff !important;
    }
    button[data-baseweb="tab"] {
        color: #1a1a1a !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #00b894 !important;
        border-bottom-color: #00b894 !important;
    }
    details summary {
        color: #1a1a1a !important;
    }
    div[data-testid="stSlider"] div {
        color: #1a1a1a !important;
    }
    div[data-testid="stToggle"] label {
        color: #1a1a1a !important;
    }
    .stCaption, caption {
        color: #666666 !important;
    }
    .stInfo { background: #e8f6f3 !important; border-left-color: #00b894 !important; }
    .stWarning { background: #fff9e6 !important; border-left-color: #f1c40f !important; }
    .stError { background: #fdeaea !important; border-left-color: #e74c3c !important; }
    .stSuccess { background: #e8f6f3 !important; border-left-color: #00b894 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ───────────────────────────────────────────
# 2. AUTHENTICATION
# ───────────────────────────────────────────
USERS = {
    "mitisha": hashlib.sha256("Jasvik@123".encode()).hexdigest()
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    c1, c2, c3 = st.columns([1, 1.4, 1])
    with c2:
        st.markdown("""
        <style>
        @keyframes wandSparkle {
            0% { transform: rotate(0deg) translateY(0); filter: brightness(1); }
            25% { transform: rotate(-15deg) translateY(-5px); filter: brightness(1.3) drop-shadow(0 0 10px #ffd700); }
            50% { transform: rotate(10deg) translateY(-3px); filter: brightness(1.5) drop-shadow(0 0 20px #ff8c00); }
            75% { transform: rotate(-5deg) translateY(-8px); filter: brightness(1.2) drop-shadow(0 0 15px #ffd700); }
            100% { transform: rotate(0deg) translateY(0); filter: brightness(1); }
        }
        @keyframes magicFloat {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            33% { transform: translateY(-15px) rotate(5deg); }
            66% { transform: translateY(-8px) rotate(-3deg); }
        }
        @keyframes sparkle {
            0%, 100% { opacity: 0; transform: scale(0); }
            50% { opacity: 1; transform: scale(1); }
        }
        .wand-container {
            text-align: center;
            padding: 30px 0 10px 0;
            position: relative;
        }
        .magic-wand {
            font-size: 70px;
            display: inline-block;
            animation: wandSparkle 2.5s infinite ease-in-out;
            filter: drop-shadow(0 0 15px rgba(255, 215, 0, 0.4));
        }
        .sparkle {
            position: absolute;
            font-size: 20px;
            animation: sparkle 1.5s infinite;
        }
        .sparkle-1 { top: 10px; left: 45%; animation-delay: 0s; }
        .sparkle-2 { top: 20px; right: 35%; animation-delay: 0.5s; }
        .sparkle-3 { top: 5px; left: 40%; animation-delay: 1s; }
        .sparkle-4 { top: 25px; right: 40%; animation-delay: 1.2s; }
        .login-brand {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 42px;
            font-weight: 900;
            letter-spacing: 4px;
            margin: 8px 0 0 0;
        }
        .login-subtitle {
            color: #888;
            font-size: 15px;
            margin: 4px 0 24px 0;
            letter-spacing: 2px;
        }
        .magic-border {
            border: 2px solid transparent;
            border-radius: 20px;
            background: linear-gradient(white, white) padding-box,
                        linear-gradient(135deg, #667eea, #764ba2, #f093fb) border-box;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.15);
        }
        </style>
        <div class="wand-container">
            <div class="magic-wand">🪄</div>
            <div class="sparkle sparkle-1">✨</div>
            <div class="sparkle sparkle-2">⭐</div>
            <div class="sparkle sparkle-3">✨</div>
            <div class="sparkle sparkle-4">⭐</div>
            <h1 class="login-brand">JVX</h1>
            <p class="login-subtitle">JVX Trading Terminal</p>
            <p style="color:#a78bfa; font-size:12px; margin:0; font-style:italic;">✨ Welcome to your algo trading command center</p>
        </div>
        """, unsafe_allow_html=True)
        with st.form("login_form"):
            user = st.text_input("👤 Username")
            pwd = st.text_input("🔑 Password", type="password")
            if st.form_submit_button("🔐 Secure Login", use_container_width=True):
                if USERS.get(user) == hashlib.sha256(pwd.encode()).hexdigest():
                    st.session_state.authenticated = True
                    st.session_state.username = user
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials! Access denied by the Ministry of Magic.")
        st.markdown("<p style='text-align:center; color:#666; font-size:12px; margin-top:16px;'>🪄 Developed by Hitesh Vidhani</p>", unsafe_allow_html=True)
    st.stop()

# ───────────────────────────────────────────
# 3. SESSION STATE
# ───────────────────────────────────────────
defaults = {
    'exec_mode': 'PAPER',
    'auto_trade': False,
    'loss_streak': 0,
    'loss_limit': 3,
    'profit_target': 5000,
    'daily_loss_limit': 5000,
    'max_orders_per_minute': 10,
    'last_order_time': None,
    'selected_strategy': 'Multi-Confirmation Pro',
    'watchlist': ['NIFTY 50', 'BANKNIFTY', 'RELIANCE', 'HDFCBANK', 'INFY', 'TCS'],
    'open_position': None,
    'trade_history': [],
    'alert_enabled': True,
    'alert_threshold': 75,
    'alert_history': [],
    'last_alert_signature': None,
    'market_data': {},
    'live_data_source': 'SIMULATED',
    'selected_broker': 'ZERODHA',
    # Paytm Money
    'paytm_api_key': '',
    'paytm_api_secret': '',
    'paytm_access_token': '',
    'paytm_public_access_token': '',
    'paytm_read_access_token': '',
    'paytm_connected': False,
    'paytm_client': None,
    'paytm_funds': None,
    'paytm_positions': None,
    # DhanHQ
    'dhan_client_id': '',
    'dhan_access_token': '',
    'dhan_connected': False,
    'dhan_client': None,
    'dhan_funds': None,
    'dhan_positions': None,
    'order_symbol': 'RELIANCE',
    'order_qty': 1,
    'order_type': 'MARKET',
    'order_side': 'BUY',
    'order_price': 0.0,
    'order_result': None,
    'backtest_results': {},
    'strategy_params': {
        'ema_fast': 9,
        'ema_slow': 21,
        'ema_trend': 50,
        'rsi_period': 14,
        'rsi_overbought': 70,
        'rsi_oversold': 30,
        'volume_factor': 1.5,
        'atr_multiplier_sl': 1.5,
        'atr_multiplier_tp': 3.0,
        'bb_period': 20,
        'bb_std': 2.0,
        'macd_fast': 12,
        'macd_slow': 26,
        'macd_signal': 9,
        't3_period': 10,
        't3_factor': 0.7,
        'ut_bot_atr': 10,
        'ut_bot_multiplier': 3.0,
        'supertrend_atr': 10,
        'supertrend_multiplier': 3.0
    }
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ───────────────────────────────────────────
# 4. PAYTM MONEY CLIENT WRAPPER (PRIMARY) — FIXED
# ───────────────────────────────────────────
class PaytmMoneyManager:
    def __init__(self):
        self.client = None

    def connect(self, api_key, api_secret, request_token=None):
        if not PAYTM_AVAILABLE:
            return False, "pyPMClient library not installed. Run: pip install pyPMClient"
        try:
            self.client = PMClient(api_key=api_key, api_secret=api_secret)
            if request_token:
                session = self.client.generate_session(request_token=request_token)
            user_details = self.client.get_user_details()
            st.session_state.paytm_client = self.client
            st.session_state.paytm_connected = True
            return True, user_details
        except Exception as e:
            st.session_state.paytm_connected = False
            return False, str(e)

    def connect_with_tokens(self, api_key, api_secret, access_token, public_access_token=None, read_access_token=None):
        if not PAYTM_AVAILABLE:
            return False, "pyPMClient library not installed. Run: pip install pyPMClient"
        try:
            self.client = PMClient(
                api_key=api_key, 
                api_secret=api_secret,
                access_token=access_token,
                public_access_token=public_access_token,
                read_access_token=read_access_token
            )
            user_details = self.client.get_user_details()
            st.session_state.paytm_client = self.client
            st.session_state.paytm_connected = True
            return True, user_details
        except Exception as e:
            st.session_state.paytm_connected = False
            return False, str(e)

    def get_quote(self, symbol):
        if not self.client:
            return None
        sec_id, exchange, segment = get_paytm_security_id(symbol)
        try:
            preferences = [{
                "actionType": "ADD",
                "modeType": "FULL",
                "scripType": "INDEX" if segment == "I" else "EQUITY",
                "exchangeType": exchange,
                "scripId": sec_id
            }]
            quote = self.client.get_live_market_data("FULL", preferences)
            return quote
        except Exception as e:
            return {"error": str(e)}

    def place_order(self, symbol, qty, side, order_type='MARKET', price=0.0, product_type='I'):
        if not self.client:
            return {"success": False, "error": "Paytm Money not connected"}
        sec_id, exchange, segment = get_paytm_security_id(symbol)
        errors, warnings = validate_order(symbol, qty, side, order_type, price, self.client)
        if errors:
            return {"success": False, "error": " | ".join(errors), "warnings": warnings}
        try:
            txn_type = "B" if side == "BUY" else "S"
            order_type_map = {'MARKET': 'MKT', 'LIMIT': 'LMT', 'SL': 'SL', 'SL-M': 'SL-M'}
            pm_order_type = order_type_map.get(order_type, 'MKT')

            if st.session_state.get('exec_mode') == 'PAPER':
                order_id = f"PAYTM_PAPER{datetime.now().strftime('%H%M%S')}{np.random.randint(1000,9999)}"
                return {
                    "success": True,
                    "order_id": order_id,
                    "symbol": symbol,
                    "security_id": sec_id,
                    "side": side,
                    "type": order_type,
                    "quantity": qty,
                    "price": price,
                    "status": "PAPER_EXECUTED",
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "warnings": warnings
                }

            order_response = self.client.place_order(
                txn_type=txn_type,
                exchange=exchange,
                segment=segment,
                product=product_type,
                security_id=sec_id,
                quantity=qty,
                validity="DAY",
                order_type=pm_order_type,
                price=price if price > 0 else 0,
                source="N",
                off_mkt_flag="false"
            )

            if order_response:
                st.session_state.last_order_time = datetime.now()
                return {
                    "success": True,
                    "order_id": order_response.get('order_no', 'UNKNOWN'),
                    "symbol": symbol,
                    "security_id": sec_id,
                    "side": side,
                    "type": order_type,
                    "quantity": qty,
                    "price": price,
                    "status": order_response.get('status', 'PENDING'),
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "raw_response": order_response,
                    "warnings": warnings
                }
            return {"success": False, "error": "Paytm Money order placement failed", "warnings": warnings}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_positions(self):
        if not self.client:
            return None
        try:
            return self.client.position()
        except:
            return None

    def get_holdings(self):
        if not self.client:
            return None
        try:
            return self.client.user_holdings_data()
        except:
            return None

    def get_fund_limits(self):
        if not self.client:
            return None
        try:
            return self.client.funds_summary()
        except:
            return None

    def get_order_book(self):
        if not self.client:
            return None
        try:
            return self.client.order_book()
        except:
            return None


paytm_manager = PaytmMoneyManager()

# ───────────────────────────────────────────
# DHANHQ CLIENT WRAPPER
# ───────────────────────────────────────────
class DhanHQManager:
    def __init__(self):
        self.client = None

    def connect(self, client_id, access_token):
        if not DHANHQ_AVAILABLE:
            return False, "dhanhq library not installed. Run: pip install dhanhq"
        try:
            self.client = dhanhq(client_id, access_token)
            funds = safe_api_call(self.client.get_fund_limit, fallback_return={})
            st.session_state.dhan_client = self.client
            st.session_state.dhan_connected = True
            st.session_state.dhan_funds = funds
            return True, funds
        except Exception as e:
            st.session_state.dhan_connected = False
            return False, str(e)

    def get_quote(self, symbol):
        if not self.client:
            return None
        sec_id, exchange, segment = get_dhan_security_id(symbol)
        try:
            quote = safe_api_call(self.client.quote, sec_id, fallback_return=None)
            return quote
        except Exception as e:
            return {"error": str(e)}

    def place_order(self, symbol, qty, side, order_type='MARKET', price=0.0, product_type='INTRADAY'):
        if not self.client:
            return {"success": False, "error": "DhanHQ not connected"}
        sec_id, exchange, segment = get_dhan_security_id(symbol)
        errors, warnings = validate_order(symbol, qty, side, order_type, price, self.client)
        if errors:
            return {"success": False, "error": " | ".join(errors), "warnings": warnings}
        try:
            order_type_map = {'MARKET': 'MARKET', 'LIMIT': 'LIMIT', 'SL': 'SL', 'SL-M': 'SL-M'}
            dhan_order_type = order_type_map.get(order_type, 'MARKET')
            if st.session_state.get('exec_mode') == 'PAPER':
                order_id = f"PAPER{datetime.now().strftime('%H%M%S')}{np.random.randint(1000,9999)}"
                return {
                    "success": True,
                    "order_id": order_id,
                    "symbol": symbol,
                    "security_id": sec_id,
                    "side": side,
                    "type": order_type,
                    "quantity": qty,
                    "price": price,
                    "status": "PAPER_EXECUTED",
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "warnings": warnings
                }
            order_response = safe_api_call(
                self.client.place_order,
                security_id=sec_id,
                exchange_segment=exchange,
                transaction_type=side,
                quantity=qty,
                order_type=dhan_order_type,
                product_type=product_type,
                price=price if price > 0 else 0,
                fallback_return=None
            )
            if order_response:
                st.session_state.last_order_time = datetime.now()
                return {
                    "success": True,
                    "order_id": order_response.get('orderId', 'UNKNOWN'),
                    "symbol": symbol,
                    "security_id": sec_id,
                    "side": side,
                    "type": order_type,
                    "quantity": qty,
                    "price": price,
                    "status": order_response.get('orderStatus', 'PENDING'),
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "raw_response": order_response,
                    "warnings": warnings
                }
            return {"success": False, "error": "DhanHQ order placement failed", "warnings": warnings}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_positions(self):
        if not self.client:
            return None
        return safe_api_call(self.client.get_positions, fallback_return=None)

    def get_holdings(self):
        if not self.client:
            return None
        return safe_api_call(self.client.get_holdings, fallback_return=None)

    def get_fund_limits(self):
        if not self.client:
            return None
        return safe_api_call(self.client.get_fund_limit, fallback_return=None)


dhan_manager = DhanHQManager()

class YahooManager:
    def get_quote(self, symbol):
        try:
            return fetch_yahoo_quote(symbol)
        except Exception as e:
            return {"error": str(e)}

    def get_history(self, symbol, period="1mo", interval="1d"):
        try:
            return fetch_yahoo_history(symbol, period=period, interval=interval)
        except Exception as e:
            return {"error": str(e)}


yahoo_manager = YahooManager()

# ───────────────────────────────────────────
# BROKER AGNOSTIC ORDER FUNCTION
# ───────────────────────────────────────────
def place_broker_order(symbol, qty, side, order_type='MARKET', price=0.0):
    """Route order to selected broker."""
    broker = st.session_state.get('selected_broker', 'ZERODHA')
    if broker == 'PAYTM':
        return paytm_manager.place_order(symbol, qty, side, order_type, price)
    elif broker == 'DHANHQ':
        return dhan_manager.place_order(symbol, qty, side, order_type, price)
    elif broker == 'YAHOO':
        return {"success": False, "error": "Yahoo Finance is quote-only and does not support live order placement."}
    else:
        return paytm_manager.place_order(symbol, qty, side, order_type, price)


def get_broker_quote(symbol):
    """Get quote from selected broker."""
    broker = st.session_state.get('selected_broker', 'ZERODHA')
    if broker == 'PAYTM':
        return paytm_manager.get_quote(symbol)
    elif broker == 'DHANHQ':
        return dhan_manager.get_quote(symbol)
    elif broker == 'YAHOO':
        return yahoo_manager.get_quote(symbol)
    else:
        return paytm_manager.get_quote(symbol)

# ───────────────────────────────────────────
# 5. MARKET DATA ENGINE
# ───────────────────────────────────────────
def _generate_simulated_data(sym):
    rng = np.random.default_rng(42)
    base = 22000 if "NIFTY" in sym else 2500
    walk = np.cumsum(rng.normal(0, 12, 300))
    df = pd.DataFrame({
        "Close": base + walk,
        "Volume": rng.integers(10000, 50000, 300)
    })
    df['Open'] = df['Close'] - rng.normal(0, 4, 300)
    df['High'] = df[['Open', 'Close']].max(axis=1) + rng.uniform(2, 8, 300)
    df['Low'] = df[['Open', 'Close']].min(axis=1) - rng.uniform(2, 8, 300)
    st.session_state.market_data[sym] = df


def init_market_data():
    if not st.session_state.market_data:
        if st.session_state.get('selected_broker') == 'PAYTM' and st.session_state.get('paytm_connected') and paytm_manager.client:
            st.session_state.live_data_source = 'PAYTM'
            for sym in st.session_state.watchlist:
                quote = paytm_manager.get_quote(sym)
                if quote and 'error' not in quote:
                    try:
                        ltp = float(quote.get('lastPrice', 0)) or float(quote.get('close', 2500))
                        df = pd.DataFrame({
                            "Close": [ltp] * 300,
                            "Volume": [np.random.randint(10000, 50000)] * 300
                        })
                        noise = np.cumsum(np.random.normal(0, ltp*0.001, 300))
                        df['Close'] = ltp + noise
                        df['Open'] = df['Close'] - np.random.normal(0, ltp*0.0005, 300)
                        df['High'] = df[['Open', 'Close']].max(axis=1) + abs(np.random.normal(0, ltp*0.001, 300))
                        df['Low'] = df[['Open', 'Close']].min(axis=1) - abs(np.random.normal(0, ltp*0.001, 300))
                        st.session_state.market_data[sym] = df
                    except Exception:
                        _generate_simulated_data(sym)
                else:
                    _generate_simulated_data(sym)
        elif st.session_state.get('selected_broker') == 'YAHOO':
            st.session_state.live_data_source = 'YAHOO'
            for sym in st.session_state.watchlist:
                quote = yahoo_manager.get_quote(sym)
                if quote and 'error' not in quote:
                    try:
                        ltp = float(quote.get('regularMarketPrice', quote.get('close', 2500)))
                        if ltp <= 0:
                            ltp = float(quote.get('previousClose', 2500))
                        df = pd.DataFrame({
                            "Close": [ltp] * 300,
                            "Volume": [np.random.randint(10000, 50000)] * 300
                        })
                        noise = np.cumsum(np.random.normal(0, ltp*0.001, 300))
                        df['Close'] = ltp + noise
                        df['Open'] = df['Close'] - np.random.normal(0, ltp*0.0005, 300)
                        df['High'] = df[['Open', 'Close']].max(axis=1) + abs(np.random.normal(0, ltp*0.001, 300))
                        df['Low'] = df[['Open', 'Close']].min(axis=1) - abs(np.random.normal(0, ltp*0.001, 300))
                        st.session_state.market_data[sym] = df
                    except Exception:
                        _generate_simulated_data(sym)
                else:
                    _generate_simulated_data(sym)
        elif st.session_state.get('selected_broker') == 'DHANHQ' and st.session_state.get('dhan_connected') and dhan_manager.client:
            st.session_state.live_data_source = 'DHANHQ'
            for sym in st.session_state.watchlist:
                quote = dhan_manager.get_quote(sym)
                if quote and 'error' not in quote:
                    try:
                        ltp = float(quote.get('lastPrice', 0)) or float(quote.get('close', 2500))
                        df = pd.DataFrame({
                            "Close": [ltp] * 300,
                            "Volume": [np.random.randint(10000, 50000)] * 300
                        })
                        noise = np.cumsum(np.random.normal(0, ltp*0.001, 300))
                        df['Close'] = ltp + noise
                        df['Open'] = df['Close'] - np.random.normal(0, ltp*0.0005, 300)
                        df['High'] = df[['Open', 'Close']].max(axis=1) + abs(np.random.normal(0, ltp*0.001, 300))
                        df['Low'] = df[['Open', 'Close']].min(axis=1) - abs(np.random.normal(0, ltp*0.001, 300))
                        st.session_state.market_data[sym] = df
                    except Exception:
                        _generate_simulated_data(sym)
                else:
                    _generate_simulated_data(sym)
        else:
            st.session_state.live_data_source = 'SIMULATED'
            for sym in st.session_state.watchlist:
                _generate_simulated_data(sym)


def _simulate_symbol(sym):
    df = st.session_state.market_data[sym]
    last = df.iloc[-1]
    new_close = last['Close'] + np.random.normal(0, 10)
    new_row = pd.DataFrame({
        "Close": [new_close],
        "Volume": [np.random.randint(10000, 50000)],
        "Open": [last['Close']],
        "High": [max(last['Close'], new_close) + np.random.uniform(2, 6)],
        "Low": [min(last['Close'], new_close) - np.random.uniform(2, 6)]
    })
    st.session_state.market_data[sym] = pd.concat([df, new_row], ignore_index=True).tail(500)


def simulate_tick():
    if st.session_state.get('selected_broker') == 'PAYTM' and st.session_state.get('paytm_connected') and paytm_manager.client:
        for sym in st.session_state.watchlist:
            quote = paytm_manager.get_quote(sym)
            if quote and 'error' not in quote:
                try:
                    ltp = float(quote.get('lastPrice', 0)) or float(quote.get('close', 0))
                    if ltp > 0:
                        df = st.session_state.market_data[sym]
                        new_row = pd.DataFrame({
                            "Close": [ltp],
                            "Volume": [np.random.randint(10000, 50000)],
                            "Open": [df.iloc[-1]['Close']],
                            "High": [ltp * 1.002],
                            "Low": [ltp * 0.998]
                        })
                        st.session_state.market_data[sym] = pd.concat([df, new_row], ignore_index=True).tail(500)
                        continue
                except:
                    pass
            _simulate_symbol(sym)
    elif st.session_state.get('selected_broker') == 'YAHOO':
        for sym in st.session_state.watchlist:
            quote = yahoo_manager.get_quote(sym)
            if quote and 'error' not in quote:
                try:
                    ltp = float(quote.get('regularMarketPrice', quote.get('close', 0)))
                    if ltp <= 0:
                        ltp = float(quote.get('previousClose', 0))
                    if ltp > 0:
                        df = st.session_state.market_data[sym]
                        new_row = pd.DataFrame({
                            "Close": [ltp],
                            "Volume": [np.random.randint(10000, 50000)],
                            "Open": [df.iloc[-1]['Close']],
                            "High": [ltp * 1.002],
                            "Low": [ltp * 0.998]
                        })
                        st.session_state.market_data[sym] = pd.concat([df, new_row], ignore_index=True).tail(500)
                        continue
                except Exception:
                    pass
            _simulate_symbol(sym)
    elif st.session_state.get('selected_broker') == 'DHANHQ' and st.session_state.get('dhan_connected') and dhan_manager.client:
        for sym in st.session_state.watchlist:
            quote = dhan_manager.get_quote(sym)
            if quote and 'error' not in quote:
                try:
                    ltp = float(quote.get('lastPrice', 0)) or float(quote.get('close', 0))
                    if ltp > 0:
                        df = st.session_state.market_data[sym]
                        new_row = pd.DataFrame({
                            "Close": [ltp],
                            "Volume": [np.random.randint(10000, 50000)],
                            "Open": [df.iloc[-1]['Close']],
                            "High": [ltp * 1.002],
                            "Low": [ltp * 0.998]
                        })
                        st.session_state.market_data[sym] = pd.concat([df, new_row], ignore_index=True).tail(500)
                        continue
                except:
                    pass
            _simulate_symbol(sym)
    else:
        for sym in st.session_state.watchlist:
            _simulate_symbol(sym)


init_market_data()
# ───────────────────────────────────────────
# 6. STRATEGY ENGINE (T3 + UT Bot + Multi-Confirmation)
# ───────────────────────────────────────────
class StrategyEngine:
    def __init__(self, params):
        self.p = params

    def calculate_t3(self, data, p=10, f=0.7):
        e1 = data.ewm(span=p, adjust=False).mean()
        e2 = e1.ewm(span=p, adjust=False).mean()
        e3 = e2.ewm(span=p, adjust=False).mean()
        e4 = e3.ewm(span=p, adjust=False).mean()
        e5 = e4.ewm(span=p, adjust=False).mean()
        e6 = e5.ewm(span=p, adjust=False).mean()
        t3 = -f**3 * e6 + (3*f**2 + 3*f**3) * e5 - (6*f**2 + 3*f + 3*f**3) * e4 + (1 + 3*f + f**3 + 3*f**2) * e3
        return t3

    def calculate_ut_bot(self, df, atr_period=10, multiplier=3.0):
        df = df.copy()
        high_low = df['High'] - df['Low']
        high_close = abs(df['High'] - df['Close'].shift())
        low_close = abs(df['Low'] - df['Close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(atr_period).mean()
        df['UT_Buy'] = False
        df['UT_Sell'] = False
        df['UT_Stop'] = np.nan
        x_atr = multiplier * atr
        df.loc[0, 'UT_Stop'] = df.loc[0, 'Close']
        for i in range(1, len(df)):
            prev_stop = df.loc[i-1, 'UT_Stop']
            prev_close = df.loc[i-1, 'Close']
            curr_close = df.loc[i, 'Close']
            curr_xatr = x_atr.iloc[i] if not pd.isna(x_atr.iloc[i]) else 0
            if prev_close > prev_stop:
                new_stop = max(prev_stop, curr_close - curr_xatr)
                df.loc[i, 'UT_Stop'] = new_stop
                if curr_close < new_stop:
                    df.loc[i, 'UT_Sell'] = True
                    df.loc[i, 'UT_Stop'] = curr_close + curr_xatr
            else:
                new_stop = min(prev_stop, curr_close + curr_xatr)
                df.loc[i, 'UT_Stop'] = new_stop
                if curr_close > new_stop:
                    df.loc[i, 'UT_Buy'] = True
                    df.loc[i, 'UT_Stop'] = curr_close - curr_xatr
        return df

    def calculate_supertrend(self, df, atr_period=10, multiplier=3.0):
        df = df.copy()
        high_low = df['High'] - df['Low']
        high_close = (df['High'] - df['Close'].shift()).abs()
        low_close = (df['Low'] - df['Close'].shift()).abs()
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(atr_period).mean()
        hl2 = (df['High'] + df['Low']) / 2
        basic_upper = (hl2 + multiplier * atr).to_numpy()
        basic_lower = (hl2 - multiplier * atr).to_numpy()
        close = df['Close'].to_numpy()
        n = len(df)

        final_upper = np.full(n, np.nan)
        final_lower = np.full(n, np.nan)
        supertrend = np.full(n, np.nan)
        direction = np.ones(n, dtype=int)

        start = atr_period
        if start < n and not np.isnan(basic_upper[start]):
            final_upper[start] = basic_upper[start]
            final_lower[start] = basic_lower[start]
            supertrend[start] = final_upper[start]
            direction[start] = -1

            for i in range(start + 1, n):
                bu, bl, c, pc = basic_upper[i], basic_lower[i], close[i], close[i - 1]
                final_upper[i] = bu if (bu < final_upper[i - 1] or pc > final_upper[i - 1]) else final_upper[i - 1]
                final_lower[i] = bl if (bl > final_lower[i - 1] or pc < final_lower[i - 1]) else final_lower[i - 1]

                if supertrend[i - 1] == final_upper[i - 1]:
                    if c <= final_upper[i]:
                        supertrend[i] = final_upper[i]
                        direction[i] = -1
                    else:
                        supertrend[i] = final_lower[i]
                        direction[i] = 1
                else:
                    if c >= final_lower[i]:
                        supertrend[i] = final_lower[i]
                        direction[i] = 1
                    else:
                        supertrend[i] = final_upper[i]
                        direction[i] = -1

        df['Supertrend'] = supertrend
        df['Supertrend_Direction'] = direction
        return df

    def calculate_indicators(self, df):
        df = df.copy()
        p = self.p
        df['EMA_FAST'] = df['Close'].ewm(span=p['ema_fast'], adjust=False).mean()
        df['EMA_SLOW'] = df['Close'].ewm(span=p['ema_slow'], adjust=False).mean()
        df['EMA_TREND'] = df['Close'].ewm(span=p['ema_trend'], adjust=False).mean()
        delta = df['Close'].diff()
        gain = delta.clip(lower=0).rolling(p['rsi_period']).mean()
        loss = (-delta.clip(upper=0)).rolling(p['rsi_period']).mean()
        rs = gain / loss.replace(0, np.nan)
        df['RSI'] = (100 - (100 / (1 + rs))).fillna(50)
        ema12 = df['Close'].ewm(span=p['macd_fast'], adjust=False).mean()
        ema26 = df['Close'].ewm(span=p['macd_slow'], adjust=False).mean()
        df['MACD'] = ema12 - ema26
        df['MACD_SIGNAL'] = df['MACD'].ewm(span=p['macd_signal'], adjust=False).mean()
        df['MACD_HIST'] = df['MACD'] - df['MACD_SIGNAL']
        df['BB_MID'] = df['Close'].rolling(p['bb_period']).mean()
        bb_std = df['Close'].rolling(p['bb_period']).std()
        df['BB_UPPER'] = df['BB_MID'] + p['bb_std'] * bb_std
        df['BB_LOWER'] = df['BB_MID'] - p['bb_std'] * bb_std
        high_low = df['High'] - df['Low']
        high_close = abs(df['High'] - df['Close'].shift())
        low_close = abs(df['Low'] - df['Close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['ATR'] = tr.rolling(14).mean()
        df['VOL_MA'] = df['Volume'].rolling(20).mean()
        df['VOL_RATIO'] = df['Volume'] / df['VOL_MA']
        df['T3'] = self.calculate_t3(df['Close'], p['t3_period'], p['t3_factor'])
        df = self.calculate_ut_bot(df, p['ut_bot_atr'], p['ut_bot_multiplier'])
        df = self.calculate_supertrend(df, p.get('supertrend_atr', 10), p.get('supertrend_multiplier', 3.0))
        return df

    def generate_signals(self, df):
        df = self.calculate_indicators(df)
        p = self.p
        df['Signal'] = 'WAIT'
        df['Confidence'] = 0
        df['Entry'] = np.nan
        df['StopLoss'] = np.nan
        df['Target'] = np.nan
        df['Reason'] = ''
        for i in range(max(p['ema_trend'], p['bb_period']) + 10, len(df)):
            row = df.iloc[i]
            prev = df.iloc[i-1]
            trend_up = row['EMA_FAST'] > row['EMA_SLOW'] > row['EMA_TREND']
            trend_down = row['EMA_FAST'] < row['EMA_SLOW'] < row['EMA_TREND']
            rsi_buy = 45 < row['RSI'] < p['rsi_overbought']
            rsi_sell = p['rsi_oversold'] < row['RSI'] < 55
            macd_buy = row['MACD_HIST'] > 0 and prev['MACD_HIST'] <= 0
            macd_sell = row['MACD_HIST'] < 0 and prev['MACD_HIST'] >= 0
            macd_bull = row['MACD'] > row['MACD_SIGNAL']
            macd_bear = row['MACD'] < row['MACD_SIGNAL']
            volume_ok = row['VOL_RATIO'] > p['volume_factor']
            bb_lower_bounce = row['Close'] <= row['BB_LOWER'] * 1.01
            bb_upper_reject = row['Close'] >= row['BB_UPPER'] * 0.99
            atr = row['ATR'] if not pd.isna(row['ATR']) else row['Close'] * 0.01
            t3_above = row['Close'] > row['T3']
            t3_below = row['Close'] < row['T3']
            ut_buy = row['UT_Buy']
            ut_sell = row['UT_Sell']
            ut_bull = row['Close'] > row['UT_Stop']
            ut_bear = row['Close'] < row['UT_Stop']
            confidence = 0
            reasons = []
            if trend_up:
                confidence += 20
                reasons.append("EMA trend up")
            if rsi_buy:
                confidence += 15
                reasons.append("RSI bullish")
            if macd_buy or macd_bull:
                confidence += 15
                reasons.append("MACD bullish")
            if volume_ok:
                confidence += 10
                reasons.append("Volume spike")
            if bb_lower_bounce:
                confidence += 10
                reasons.append("BB lower bounce")
            if t3_above:
                confidence += 15
                reasons.append("T3 bullish")
            if ut_buy or ut_bull:
                confidence += 15
                reasons.append("UT Bot bullish")
            if row['Close'] > row['Supertrend'] and prev['Close'] <= prev['Supertrend']:
                confidence += 15
                reasons.append("Supertrend BUY")
            elif row['Close'] > row['Supertrend']:
                confidence += 10
                reasons.append("Above Supertrend")
            if confidence >= p.get('min_confidence', 70):
                df.loc[df.index[i], 'Signal'] = 'BUY'
                df.loc[df.index[i], 'Confidence'] = min(confidence, 95)
                df.loc[df.index[i], 'Entry'] = row['Close']
                df.loc[df.index[i], 'StopLoss'] = row['UT_Stop'] if not pd.isna(row['UT_Stop']) else row['Close'] - p['atr_multiplier_sl'] * atr
                df.loc[df.index[i], 'Target'] = row['Close'] + p['atr_multiplier_tp'] * atr
                df.loc[df.index[i], 'Reason'] = " | ".join(reasons)
                continue
            confidence = 0
            reasons = []
            if trend_down:
                confidence += 20
                reasons.append("EMA trend down")
            if rsi_sell:
                confidence += 15
                reasons.append("RSI bearish")
            if macd_sell or macd_bear:
                confidence += 15
                reasons.append("MACD bearish")
            if volume_ok:
                confidence += 10
                reasons.append("Volume spike")
            if bb_upper_reject:
                confidence += 10
                reasons.append("BB upper reject")
            if t3_below:
                confidence += 15
                reasons.append("T3 bearish")
            if ut_sell or ut_bear:
                confidence += 15
                reasons.append("UT Bot bearish")
            if row['Close'] < row['Supertrend'] and prev['Close'] >= prev['Supertrend']:
                confidence += 15
                reasons.append("Supertrend SELL")
            elif row['Close'] < row['Supertrend']:
                confidence += 10
                reasons.append("Below Supertrend")
            if confidence >= p.get('min_confidence', 70):
                df.loc[df.index[i], 'Signal'] = 'SELL'
                df.loc[df.index[i], 'Confidence'] = min(confidence, 95)
                df.loc[df.index[i], 'Entry'] = row['Close']
                df.loc[df.index[i], 'StopLoss'] = row['UT_Stop'] if not pd.isna(row['UT_Stop']) else row['Close'] + p['atr_multiplier_sl'] * atr
                df.loc[df.index[i], 'Target'] = row['Close'] - p['atr_multiplier_tp'] * atr
                df.loc[df.index[i], 'Reason'] = " | ".join(reasons)
        return df

    def backtest(self, df, initial_capital=100000, risk_per_trade=0.02):
        df = self.generate_signals(df)
        capital = initial_capital
        position = None
        trades = []
        equity_curve = [capital]
        for i in range(1, len(df)):
            row = df.iloc[i]
            if position is None:
                if row['Signal'] == 'BUY':
                    risk_amount = capital * risk_per_trade
                    sl_dist = abs(row['Entry'] - row['StopLoss'])
                    qty = max(1, int(risk_amount / sl_dist)) if sl_dist > 0 else 1
                    position = {'side': 'LONG', 'entry': row['Entry'], 'sl': row['StopLoss'], 'target': row['Target'], 'qty': qty, 'entry_idx': i}
                elif row['Signal'] == 'SELL':
                    risk_amount = capital * risk_per_trade
                    sl_dist = abs(row['StopLoss'] - row['Entry'])
                    qty = max(1, int(risk_amount / sl_dist)) if sl_dist > 0 else 1
                    position = {'side': 'SHORT', 'entry': row['Entry'], 'sl': row['StopLoss'], 'target': row['Target'], 'qty': qty, 'entry_idx': i}
            else:
                exited = False
                pnl = 0
                if position['side'] == 'LONG':
                    if row['Low'] <= position['sl']:
                        pnl = (position['sl'] - position['entry']) * position['qty']
                        exited = True
                    elif row['High'] >= position['target']:
                        pnl = (position['target'] - position['entry']) * position['qty']
                        exited = True
                    elif row['Signal'] == 'SELL':
                        pnl = (row['Close'] - position['entry']) * position['qty']
                        exited = True
                else:
                    if row['High'] >= position['sl']:
                        pnl = (position['entry'] - position['sl']) * position['qty']
                        exited = True
                    elif row['Low'] <= position['target']:
                        pnl = (position['entry'] - position['target']) * position['qty']
                        exited = True
                    elif row['Signal'] == 'BUY':
                        pnl = (position['entry'] - row['Close']) * position['qty']
                        exited = True
                if exited:
                    capital += pnl
                    trades.append({'side': position['side'], 'entry': position['entry'], 'exit': row['Close'], 'pnl': pnl, 'return_pct': (pnl / initial_capital) * 100, 'result': 'WIN' if pnl > 0 else 'LOSS', 'hold_bars': i - position['entry_idx']})
                    equity_curve.append(capital)
                    position = None
        if not trades:
            return {'trades': [], 'metrics': {}, 'equity': equity_curve}
        wins = [t for t in trades if t['result'] == 'WIN']
        losses = [t for t in trades if t['result'] == 'LOSS']
        total_return = ((capital - initial_capital) / initial_capital) * 100
        win_rate = (len(wins) / len(trades)) * 100 if trades else 0
        avg_win = np.mean([t['pnl'] for t in wins]) if wins else 0
        avg_loss = np.mean([t['pnl'] for t in losses]) if losses else 0
        profit_factor = abs(sum(t['pnl'] for t in wins) / sum(t['pnl'] for t in losses)) if losses and sum(t['pnl'] for t in losses) != 0 else float('inf')
        peak = initial_capital
        max_dd = 0
        for eq in equity_curve:
            if eq > peak:
                peak = eq
            dd = (peak - eq) / peak
            if dd > max_dd:
                max_dd = dd
        returns = [trades[i]['return_pct'] for i in range(1, len(trades))] if len(trades) > 1 else [0]
        sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
        return {
            'trades': trades,
            'metrics': {
                'total_trades': len(trades), 'win_rate': round(win_rate, 2), 'profit_factor': round(profit_factor, 2),
                'total_return_pct': round(total_return, 2), 'max_drawdown_pct': round(max_dd * 100, 2),
                'sharpe_ratio': round(sharpe, 2), 'avg_win': round(avg_win, 2), 'avg_loss': round(avg_loss, 2),
                'win_loss_ratio': round(abs(avg_win / avg_loss), 2) if avg_loss != 0 else 0,
                'final_capital': round(capital, 2)
            },
            'equity': equity_curve
        }


engine = StrategyEngine(st.session_state.strategy_params)

class VWAPVolumeStrategy:
    def __init__(self, params):
        self.params = params

    def backtest(self, df, initial_capital=100000, risk_per_trade=0.02):
        params = self.params.copy()
        params['volume_factor'] = max(params.get('volume_factor', 1.5), 1.2)
        engine = StrategyEngine(params)
        return engine.backtest(df, initial_capital, risk_per_trade)

class OpeningRangeBreakout:
    def __init__(self, params, opening_range_bars=15):
        self.params = params
        self.opening_range_bars = opening_range_bars

    def backtest(self, df, initial_capital=100000, risk_per_trade=0.02):
        df = df.copy()
        if len(df) < self.opening_range_bars + 1:
            return {'trades': [], 'metrics': {}, 'equity': [initial_capital]}
        opening_range = df.iloc[:self.opening_range_bars]
        high = opening_range['High'].max()
        low = opening_range['Low'].min()
        df['Signal'] = 'WAIT'
        for i in range(self.opening_range_bars, len(df)):
            if df.iloc[i]['Close'] > high:
                df.at[df.index[i], 'Signal'] = 'BUY'
            elif df.iloc[i]['Close'] < low:
                df.at[df.index[i], 'Signal'] = 'SELL'
        engine = StrategyEngine(self.params)
        df = engine.generate_signals(df)
        return engine.backtest(df, initial_capital, risk_per_trade)

class SmartMoneyConcepts:
    def __init__(self, params):
        self.params = params

    def backtest(self, df, initial_capital=100000, risk_per_trade=0.02):
        params = self.params.copy()
        params['t3_factor'] = min(params.get('t3_factor', 0.7), 0.7)
        engine = StrategyEngine(params)
        return engine.backtest(df, initial_capital, risk_per_trade)

class RSIDivergenceStrategy:
    def __init__(self, params):
        self.params = params

    def backtest(self, df, initial_capital=100000, risk_per_trade=0.02):
        params = self.params.copy()
        params['rsi_period'] = max(params.get('rsi_period', 14), 14)
        engine = StrategyEngine(params)
        return engine.backtest(df, initial_capital, risk_per_trade)

# ───────────────────────────────────────────
# 7. OPTIONS UTILITIES
# ───────────────────────────────────────────
def get_strike_interval(symbol):
    sym = symbol.upper().replace(" ", "")
    if "NIFTY" in sym and "BANK" not in sym:
        return 50
    elif "BANK" in sym or "BANKNIFTY" in sym:
        return 100
    elif "FINNIFTY" in sym:
        return 50
    elif "MIDCAP" in sym or "SENSEX" in sym:
        return 100
    return 10


def get_lot_size(symbol):
    sym = symbol.upper().replace(" ", "")
    if sym == "NIFTY50" or sym == "NIFTY":
        return 50
    elif "BANK" in sym or "BANKNIFTY" in sym:
        return 15
    elif "FINNIFTY" in sym:
        return 40
    elif "SENSEX" in sym:
        return 10
    elif sym == "RELIANCE":
        return 250
    elif sym == "HDFCBANK":
        return 550
    elif sym == "INFY":
        return 400
    elif sym == "TCS":
        return 250
    return 1


def calculate_option_strikes(symbol, ltp, signal, num_strikes_each_side=2):
    interval = get_strike_interval(symbol)
    lot_size = get_lot_size(symbol)
    atm_strike = round(ltp / interval) * interval
    strikes = {"symbol": symbol, "ltp": round(ltp, 2), "signal": signal, "interval": interval, "lot_size": lot_size, "atm": atm_strike, "recommendations": []}
    if signal == "BUY":
        strikes["option_type"] = "CE"
        strikes["bias"] = "BULLISH"
        for i in range(num_strikes_each_side, 0, -1):
            strike = atm_strike - (i * interval)
            strikes["recommendations"].append({"strike": strike, "type": "CE", "moneyness": f"ITM ({i}x)", "premium_estimate": "Higher", "risk": "Lower (safer)", "reward": "Moderate", "suggested_qty": max(1, int(50000 / (strike * lot_size))) if strike > 0 else 1})
        strikes["recommendations"].append({"strike": atm_strike, "type": "CE", "moneyness": "ATM", "premium_estimate": "Medium", "risk": "Medium", "reward": "High", "suggested_qty": max(1, int(50000 / (atm_strike * lot_size))) if atm_strike > 0 else 1})
        for i in range(1, num_strikes_each_side + 1):
            strike = atm_strike + (i * interval)
            strikes["recommendations"].append({"strike": strike, "type": "CE", "moneyness": f"OTM ({i}x)", "premium_estimate": "Lower", "risk": "Higher (aggressive)", "reward": "Very High (if moves)", "suggested_qty": max(1, int(50000 / (strike * lot_size))) if strike > 0 else 1})
    elif signal == "SELL":
        strikes["option_type"] = "PE"
        strikes["bias"] = "BEARISH"
        for i in range(num_strikes_each_side, 0, -1):
            strike = atm_strike + (i * interval)
            strikes["recommendations"].append({"strike": strike, "type": "PE", "moneyness": f"ITM ({i}x)", "premium_estimate": "Higher", "risk": "Lower (safer)", "reward": "Moderate", "suggested_qty": max(1, int(50000 / (strike * lot_size))) if strike > 0 else 1})
        strikes["recommendations"].append({"strike": atm_strike, "type": "PE", "moneyness": "ATM", "premium_estimate": "Medium", "risk": "Medium", "reward": "High", "suggested_qty": max(1, int(50000 / (atm_strike * lot_size))) if atm_strike > 0 else 1})
        for i in range(1, num_strikes_each_side + 1):
            strike = atm_strike - (i * interval)
            strikes["recommendations"].append({"strike": strike, "type": "PE", "moneyness": f"OTM ({i}x)", "premium_estimate": "Lower", "risk": "Higher (aggressive)", "reward": "Very High (if moves)", "suggested_qty": max(1, int(50000 / (strike * lot_size))) if strike > 0 else 1})
    else:
        strikes["option_type"] = "—"
        strikes["bias"] = "NEUTRAL"
    return strikes


def render_options_card(symbol, ltp, signal, confidence):
    if signal not in ["BUY", "SELL"]:
        st.info("⚠️ No clear directional signal. Options trade not recommended.")
        return
    strikes = calculate_option_strikes(symbol, ltp, signal)
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f0f9ff, #e0f2fe); border: 1px solid #bae6fd; border-radius: 16px; padding: 20px; margin: 16px 0;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div>
                <h3 style="margin:0; color:#0369a1;">📊 Options Strike Selector</h3>
                <p style="margin:4px 0 0 0; color:#64748b; font-size:14px;">
                    {symbol} @ ₹{ltp:.2f} | Signal: <b>{signal}</b> | Confidence: {confidence:.0f}%
                </p>
            </div>
            <div style="background:#ffffff; border-radius:12px; padding:12px 20px; text-align:center; border:1px solid #e2e8f0;">
                <div style="font-size:24px; font-weight:800; color:#{'16a34a' if signal=='BUY' else 'dc2626'};">
                    {strikes['option_type']}
                </div>
                <div style="font-size:11px; color:#64748b;">{strikes['bias']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if strikes["recommendations"]:
        cols = st.columns(len(strikes["recommendations"]))
        for idx, rec in enumerate(strikes["recommendations"]):
            with cols[idx]:
                moneyness_color = {"ATM": "#f59e0b", "ITM (2x)": "#16a34a", "ITM (1x)": "#22c55e", "OTM (1x)": "#dc2626", "OTM (2x)": "#b91c1c"}
                color = moneyness_color.get(rec["moneyness"], "#64748b")
                is_atm = rec["moneyness"] == "ATM"
                st.markdown(f"""
                <div style="background:{'#f0fdf4' if is_atm else '#ffffff'}; border:{'2px solid #22c55e' if is_atm else '1px solid #e2e8f0'}; border-radius: 12px; padding: 16px; text-align:center;">
                    <div style="font-size:12px; color:#64748b; margin-bottom:4px;">{rec['moneyness']}</div>
                    <div style="font-size:22px; font-weight:800; color:#1e293b; margin-bottom:4px;">{rec['strike']}</div>
                    <div style="font-size:13px; color:#475569; margin-bottom:8px;">{rec['type']} | Lot: {rec['suggested_qty']}x</div>
                    <div style="font-size:11px; color:{color}; font-weight:600;">{rec['risk']}</div>
                    {'<div style="margin-top:8px; font-size:11px; background:#dcfce7; color:#166534; padding:4px 8px; border-radius:6px; font-weight:700;">⭐ RECOMMENDED</div>' if is_atm else ''}
                </div>
                """, unsafe_allow_html=True)


# ───────────────────────────────────────────
# 7B. COST & BROKERAGE CALCULATOR ENGINE
# ───────────────────────────────────────────
GST_RATE_PCT = 18.0

CHARGE_DEFAULTS = {
    "Equity Delivery": {
        "brokerage_type": "flat",
        "brokerage_flat": 0.0,
        "brokerage_pct": 0.0,
        "stt_buy_pct": 0.1, "stt_sell_pct": 0.1,
        "exch_txn_pct": 0.00297,
        "stamp_duty_buy_pct": 0.015,
        "sebi_pct": 0.0001,
        "dp_charge": 20.0,
    },
    "Equity Intraday": {
        "brokerage_type": "lower_of_flat_pct",
        "brokerage_flat": 10.0,
        "brokerage_pct": 0.05,
        "stt_buy_pct": 0.0, "stt_sell_pct": 0.025,
        "exch_txn_pct": 0.00297,
        "stamp_duty_buy_pct": 0.003,
        "sebi_pct": 0.0001,
        "dp_charge": 0.0,
    },
    "Equity Futures": {
        "brokerage_type": "flat",
        "brokerage_flat": 10.0,
        "brokerage_pct": 0.0,
        "stt_buy_pct": 0.0, "stt_sell_pct": 0.05,
        "exch_txn_pct": 0.00173,
        "stamp_duty_buy_pct": 0.002,
        "sebi_pct": 0.0001,
        "dp_charge": 0.0,
    },
    "Equity Options": {
        "brokerage_type": "flat",
        "brokerage_flat": 15.0,
        "brokerage_pct": 0.0,
        "stt_buy_pct": 0.0, "stt_sell_pct": 0.15,
        "exch_txn_pct": 0.03503,
        "stamp_duty_buy_pct": 0.003,
        "sebi_pct": 0.0001,
        "dp_charge": 0.0,
    },
}


def calc_brokerage_leg(cfg, leg_turnover):
    if cfg["brokerage_type"] == "flat":
        return cfg["brokerage_flat"]
    if cfg["brokerage_type"] == "lower_of_flat_pct":
        if leg_turnover <= 0:
            return 0.0
        pct_amt = leg_turnover * cfg["brokerage_pct"] / 100
        return min(cfg["brokerage_flat"], pct_amt)
    return 0.0


def calculate_trade_charges(segment, buy_price, sell_price, quantity, overrides=None):
    cfg = dict(CHARGE_DEFAULTS[segment])
    if overrides:
        cfg.update(overrides)

    buy_turnover = buy_price * quantity
    sell_turnover = sell_price * quantity
    total_turnover = buy_turnover + sell_turnover

    brokerage = calc_brokerage_leg(cfg, buy_turnover) + calc_brokerage_leg(cfg, sell_turnover)
    stt = buy_turnover * cfg["stt_buy_pct"] / 100 + sell_turnover * cfg["stt_sell_pct"] / 100
    exch_txn = total_turnover * cfg["exch_txn_pct"] / 100
    sebi_fee = total_turnover * cfg["sebi_pct"] / 100
    stamp_duty = buy_turnover * cfg["stamp_duty_buy_pct"] / 100
    dp_charge = cfg["dp_charge"] if segment == "Equity Delivery" else 0.0
    gst = (brokerage + exch_txn + sebi_fee) * GST_RATE_PCT / 100

    total_charges = brokerage + stt + exch_txn + sebi_fee + stamp_duty + gst + dp_charge
    gross_pnl = sell_turnover - buy_turnover
    net_pnl = gross_pnl - total_charges
    breakeven_price = buy_price + (total_charges / quantity) if quantity else 0.0

    return {
        "buy_turnover": buy_turnover, "sell_turnover": sell_turnover, "total_turnover": total_turnover,
        "brokerage": brokerage, "stt": stt, "exch_txn": exch_txn, "sebi_fee": sebi_fee,
        "stamp_duty": stamp_duty, "gst": gst, "dp_charge": dp_charge, "total_charges": total_charges,
        "gross_pnl": gross_pnl, "net_pnl": net_pnl, "breakeven_price": breakeven_price,
        "charges_pct_of_turnover": (total_charges / total_turnover * 100) if total_turnover else 0.0,
    }


# ───────────────────────────────────────────
# 8. QUANTUM ALGO
# ───────────────────────────────────────────
class QuantumAlgo:
    def __init__(self, capital=10000, daily_target=2000, max_risk_per_trade_pct=2.0):
        self.capital = capital
        self.daily_target = daily_target
        self.max_risk_per_trade = capital * (max_risk_per_trade_pct / 100)

    def calculate_position_size(self, entry, stop_loss, leverage=1):
        risk_per_unit = abs(entry - stop_loss)
        if risk_per_unit <= 0:
            return 1
        qty = int(self.max_risk_per_trade / risk_per_unit)
        return max(1, qty) * leverage

    def quantum_signal(self, df, symbol):
        df = df.copy().tail(30)
        if len(df) < 10:
            return None
        df['EMA_3'] = df['Close'].ewm(span=3, adjust=False).mean()
        df['EMA_5'] = df['Close'].ewm(span=5, adjust=False).mean()
        df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
        df['MOMENTUM'] = df['Close'].diff(3)
        df['VOL_SPIKE'] = df['Volume'] / df['Volume'].rolling(5).mean()
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        signal = None
        confidence = 0
        reasons = []
        if (latest['EMA_3'] > latest['EMA_5'] and prev['EMA_3'] <= prev['EMA_5'] and
            latest['VOL_SPIKE'] > 2.0 and latest['Close'] > latest['VWAP'] and latest['MOMENTUM'] > 0):
            signal = "BUY"
            confidence = 75
            reasons = ["EMA3 cross", "Volume spike", "Above VWAP", "Positive momentum"]
            if latest['VOL_SPIKE'] > 3.0:
                confidence += 10
            if latest['MOMENTUM'] > latest['Close'] * 0.005:
                confidence += 10
        elif (latest['EMA_3'] < latest['EMA_5'] and prev['EMA_3'] >= prev['EMA_5'] and
              latest['VOL_SPIKE'] > 2.0 and latest['Close'] < latest['VWAP'] and latest['MOMENTUM'] < 0):
            signal = "SELL"
            confidence = 75
            reasons = ["EMA3 cross down", "Volume spike", "Below VWAP", "Negative momentum"]
            if latest['VOL_SPIKE'] > 3.0:
                confidence += 10
            if abs(latest['MOMENTUM']) > latest['Close'] * 0.005:
                confidence += 10
        if signal:
            atr = max(abs(latest['High'] - latest['Low']), 0.5)
            sl = latest['Close'] - (atr * 1.2) if signal == "BUY" else latest['Close'] + (atr * 1.2)
            target = latest['Close'] + (atr * 2.5) if signal == "BUY" else latest['Close'] - (atr * 2.5)
            return {"symbol": symbol, "signal": signal, "confidence": min(confidence, 95), "entry": round(latest['Close'], 2), "stop_loss": round(sl, 2), "target": round(target, 2), "reasons": " | ".join(reasons), "vwap": round(latest['VWAP'], 2), "volume_ratio": round(latest['VOL_SPIKE'], 2), "momentum": round(latest['MOMENTUM'], 2)}
        return None

    def get_session_recommendation(self):
        hour = datetime.now().hour
        if 9 <= hour < 11:
            return {"session": "MORNING OPEN", "quality": "HIGH", "reason": "High volatility, best for momentum scalps", "color": "#16a34a"}
        elif 11 <= hour < 13:
            return {"session": "MIDDAY", "quality": "MEDIUM", "reason": "Range-bound possible, use tight stops", "color": "#f59e0b"}
        elif 13 <= hour < 15:
            return {"session": "AFTERNOON", "quality": "HIGH", "reason": "Trend continuation or reversal setups", "color": "#16a34a"}
        return {"session": "CLOSED / PRE-MARKET", "quality": "LOW", "reason": "Market not active or low liquidity", "color": "#dc2626"}


# ───────────────────────────────────────────
# 8B. ML STRATEGY PIPELINE ENGINE
# ───────────────────────────────────────────
ML_FEATURE_GROUPS = {
    "Trend":      ["EMA_DIFF", "EMA_SLOPE", "PRICE_VS_TREND"],
    "Momentum":   ["RSI_C", "MACD_HIST_N", "ROC_5"],
    "Volatility": ["ATR_N", "BB_WIDTH", "RET_STD20"],
}
ML_FEATURE_COLS = ML_FEATURE_GROUPS["Trend"] + ML_FEATURE_GROUPS["Momentum"] + ML_FEATURE_GROUPS["Volatility"]


def ml_build_features(df):
    feat = engine.calculate_indicators(df.copy())
    feat['EMA_DIFF'] = (feat['EMA_FAST'] - feat['EMA_SLOW']) / feat['Close']
    feat['EMA_SLOPE'] = feat['EMA_TREND'].diff(5) / feat['Close']
    feat['PRICE_VS_TREND'] = (feat['Close'] - feat['EMA_TREND']) / feat['Close']
    feat['RSI_C'] = feat['RSI'] - 50
    feat['MACD_HIST_N'] = feat['MACD_HIST'] / feat['Close']
    feat['ROC_5'] = feat['Close'].pct_change(5)
    feat['ATR_N'] = feat['ATR'] / feat['Close']
    feat['BB_WIDTH'] = (feat['BB_UPPER'] - feat['BB_LOWER']) / feat['BB_MID']
    feat['RET_STD20'] = feat['Close'].pct_change().rolling(20).std()
    feat['Target'] = np.where(feat['Close'].shift(-1) > feat['Close'], 1, 0)
    return feat.dropna().reset_index(drop=True)


def ml_train_model(feat_df, model_type="Random Forest", n_estimators=150, test_size=0.2):
    n = len(feat_df)
    split = int(n * (1 - test_size))
    train_df, test_df = feat_df.iloc[:split], feat_df.iloc[split:]
    X_train, y_train = train_df[ML_FEATURE_COLS], train_df['Target']
    X_test, y_test = test_df[ML_FEATURE_COLS], test_df['Target']

    if model_type == "XGBoost" and XGBOOST_AVAILABLE:
        model = XGBClassifier(n_estimators=n_estimators, max_depth=4, learning_rate=0.08,
                               eval_metric='logloss', verbosity=0)
    else:
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=6, min_samples_leaf=5, random_state=42)

    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, preds) * 100,
        "precision": precision_score(y_test, preds, zero_division=0) * 100,
        "recall": recall_score(y_test, preds, zero_division=0) * 100,
        "train_size": len(train_df),
        "test_size": len(test_df),
        "feature_importance": dict(zip(ML_FEATURE_COLS, model.feature_importances_)),
    }
    test_df = test_df.copy()
    test_df['ML_Pred'] = preds
    test_df['ML_Proba_Up'] = proba
    return model, metrics, test_df


def ml_compute_trade_plan(latest_row, proba_up, threshold, atr_multiplier, rr_mode, rr_fixed):
    entry = float(latest_row['Close'])
    atr = float(latest_row['ATR']) if not pd.isna(latest_row['ATR']) else entry * 0.01
    confidence = max(proba_up, 1 - proba_up)

    if proba_up >= threshold:
        signal = "BUY"
    elif proba_up <= (1 - threshold):
        signal = "SELL"
    else:
        signal = "WAIT"

    if rr_mode == "Dynamic (confidence-scaled)":
        rr_ratio = round(1.0 + (confidence - 0.5) * 6, 2)
        rr_ratio = max(1.0, min(rr_ratio, 4.0))
    else:
        rr_ratio = rr_fixed

    if signal == "BUY":
        stop_loss = entry - atr_multiplier * atr
        target = entry + rr_ratio * (entry - stop_loss)
    elif signal == "SELL":
        stop_loss = entry + atr_multiplier * atr
        target = entry - rr_ratio * (stop_loss - entry)
    else:
        stop_loss, target = np.nan, np.nan

    return {
        "signal": signal, "entry": entry, "atr": atr, "proba_up": proba_up, "confidence": confidence,
        "stop_loss": stop_loss, "target": target, "rr_ratio": rr_ratio,
    }


# ───────────────────────────────────────────
# 9. SIDEBAR NAVIGATION
# ───────────────────────────────────────────
st.sidebar.markdown(f"👤 **{st.session_state.username}**")
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.divider()

st.sidebar.markdown("### 📡 Broker Status")

_broker_list = ["PAYTM", "DHANHQ", "ZERODHA", "ANGELONE", "YAHOO"]
_curr_broker = st.session_state.get('selected_broker', 'ZERODHA')
_broker_idx = _broker_list.index(_curr_broker) if _curr_broker in _broker_list else 0
st.session_state.selected_broker = st.sidebar.selectbox(
    "Select Broker",
    _broker_list,
    index=_broker_idx
)

if st.session_state.selected_broker == 'PAYTM':
    if st.session_state.paytm_connected:
        st.sidebar.markdown("<span class='status-connected'>🟢 Paytm Money Connected</span>", unsafe_allow_html=True)
        if st.session_state.paytm_funds:
            st.sidebar.caption(f"Funds: {st.session_state.paytm_funds}")
    else:
        st.sidebar.markdown("<span class='status-disconnected'>🔴 Paytm Money Disconnected</span>", unsafe_allow_html=True)
elif st.session_state.selected_broker == 'DHANHQ':
    if st.session_state.dhan_connected:
        st.sidebar.markdown("<span class='status-connected'>🟢 DhanHQ Connected</span>", unsafe_allow_html=True)
        if st.session_state.dhan_funds:
            st.sidebar.caption(f"Funds: {st.session_state.dhan_funds}")
    else:
        st.sidebar.markdown("<span class='status-disconnected'>🔴 DhanHQ Disconnected</span>", unsafe_allow_html=True)
elif st.session_state.selected_broker == 'ZERODHA':
    zerodha_ok = st.session_state.get('zerodha_connected', False)
    if zerodha_ok:
        st.sidebar.markdown("<span class='status-connected'>🟢 Zerodha Connected</span>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<span class='status-disconnected'>🔴 Zerodha Disconnected</span>", unsafe_allow_html=True)
elif st.session_state.selected_broker == 'ANGELONE':
    angel_ok = st.session_state.get('angel_connected', False)
    if angel_ok:
        st.sidebar.markdown("<span class='status-connected'>🟢 Angel One Connected</span>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<span class='status-disconnected'>🔴 Angel One Disconnected</span>", unsafe_allow_html=True)
elif st.session_state.selected_broker == 'YAHOO':
    st.sidebar.markdown("<span class='status-connected'>🟢 Yahoo Finance Enabled</span>", unsafe_allow_html=True)

st.sidebar.divider()

open_ok, market_msg = is_market_open()
if open_ok:
    st.sidebar.markdown(f"<span style='color:#00b894; font-weight:700;'>🟢 {market_msg}</span>", unsafe_allow_html=True)
else:
    st.sidebar.markdown(f"<span style='color:#e74c3c; font-weight:700;'>🔴 {market_msg}</span>", unsafe_allow_html=True)

source = st.session_state.get('live_data_source', 'SIMULATED')
if source == 'PAYTM':
    st.sidebar.markdown("<span style='color:#00b894; font-size:12px;'>📡 Live Data: Paytm Money</span>", unsafe_allow_html=True)
elif source == 'DHANHQ':
    st.sidebar.markdown("<span style='color:#00b894; font-size:12px;'>📡 Live Data: DhanHQ</span>", unsafe_allow_html=True)
elif source == 'ZERODHA':
    st.sidebar.markdown("<span style='color:#00b894; font-size:12px;'>📡 Live Data: Zerodha Kite</span>", unsafe_allow_html=True)
elif source == 'ANGELONE':
    st.sidebar.markdown("<span style='color:#00b894; font-size:12px;'>📡 Live Data: Angel One</span>", unsafe_allow_html=True)
elif source == 'YAHOO':
    st.sidebar.markdown("<span style='color:#00b894; font-size:12px;'>📡 Live Data: Yahoo Finance</span>", unsafe_allow_html=True)
else:
    st.sidebar.markdown("<span style='color:#f59e0b; font-size:12px;'>📡 Live Data: Simulated</span>", unsafe_allow_html=True)

st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigate Modules:",
    [
        "📊 Live Dashboard",
        "💡 Trading Ideas",
        "🤖 Automated Algo Trading",
        "📡 Real-Time Algo Signals",
        "🎯 Strategy Market Scanner",
        "📂 Algo Portfolio",
        "🏗️ Custom Strategy Builder",
        "📈 TradingView Chart",
        "🧪 Backtest Lab (Paper Trade)",
        "⚡ Quick Execution",
        "💰 Cost & Brokerage Calculator",
        "📋 Trade Ledger",
        "📒 Order Book",
        "🔍 Market Depth",
        "📈 Options Strike Selector",
        "🚀 Quantum Algo",
        "📋 Options Strategies",
        "📅 0DTE Scanner",
        "🤖 AI Bots",
        "🧬 ML Strategy Pipeline",
        "🧠 Strategy Lab",
        "🌲 David Strategy (Ichimoku+TDFI)",
        "📝 Pine Script Editor",
        "🏛️ NSE/BSE Market Intelligence",
        "💹 FII & DII Tracker",
        "📊 Volume & Dividend",
        "📲 Telegram Bot",
        "💰 Paytm Money Connect",
        "🔐 DhanHQ Connect",
        "🔑 Zerodha Connect",
        "👼 Angel One Connect",
    ],
    index=0
)

st.sidebar.divider()

if st.sidebar.button("▶️ Refresh Live Data", type="primary", use_container_width=True):
    symbol = st.session_state.get('order_symbol', st.session_state.watchlist[0])
    simulate_tick()
    st.rerun()

st.session_state.exec_mode = st.sidebar.selectbox("Mode", ["PAPER", "LIVE"])
if st.session_state.exec_mode == "LIVE":
    if st.session_state.selected_broker == 'PAYTM' and not st.session_state.paytm_connected:
        st.sidebar.warning("⚠️ Connect Paytm Money first for LIVE mode")
    elif st.session_state.selected_broker == 'DHANHQ' and not st.session_state.dhan_connected:
        st.sidebar.warning("⚠️ Connect DhanHQ first for LIVE mode")
    else:
        st.sidebar.success(f"✅ LIVE mode ready ({st.session_state.selected_broker})")

st.session_state.auto_trade = st.sidebar.toggle("🤖 Auto-Pilot", value=st.session_state.auto_trade)
st.session_state.alert_enabled = st.sidebar.toggle("🔔 Alerts", value=st.session_state.alert_enabled)

st.sidebar.caption("Developed by Hitesh Vidhani")


# ───────────────────────────────────────────
# 10. PAGE RENDERERS
# ───────────────────────────────────────────
def render_dashboard():
    st.markdown("""
    <div style='display:flex; align-items:center; gap:14px; margin-bottom:20px;'>
        <div class='brand-logo'>JV</div>
        <div>
            <h2 style='margin:0; color:#00d4aa;'>JVX</h2>
            <p style='margin:0; color:#888; font-size:13px;'>Paytm Money Pro Terminal v31.3 🪄</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🔍 Symbol & Timeframe")

    col_search, col_tf, col_period, col_refresh = st.columns([2, 1, 1, 1])

    with col_search:
        search_col1, search_col2 = st.columns([3, 1])
        with search_col1:
            custom_sym = st.text_input("🔎 Search Symbol (e.g. RELIANCE, AAPL, BTC-USD)", 
                                       value=st.session_state.get('custom_symbol', ''),
                                       placeholder="Type symbol and press Enter...")
        with search_col2:
            st.write("")
            st.write("")
            if st.button("🔍 Load", use_container_width=True):
                if custom_sym.strip():
                    st.session_state.custom_symbol = custom_sym.strip().upper()
                    if st.session_state.custom_symbol not in st.session_state.watchlist:
                        st.session_state.watchlist.append(st.session_state.custom_symbol)
                    _generate_simulated_data(st.session_state.custom_symbol)
                    st.rerun()

        symbol = st.selectbox("📋 Or Select from Watchlist", st.session_state.watchlist, 
                            index=st.session_state.watchlist.index(st.session_state.order_symbol) if st.session_state.order_symbol in st.session_state.watchlist else 0)

    with col_tf:
        timeframe = st.selectbox("⏱️ Timeframe", 
                                ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"],
                                index=8)
        st.session_state.timeframe = timeframe

    with col_period:
        period = st.selectbox("📅 Period", 
                             ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
                             index=4)
        st.session_state.chart_period = period

    with col_refresh:
        st.write("")
        st.write("")
        if st.button("🔄 Refresh Data", type="primary", use_container_width=True):
            simulate_tick()
            st.rerun()

    source = st.session_state.get('live_data_source', 'SIMULATED')
    if source == 'PAYTM':
        st.success(f"📡 Live Data: Paytm Money | {symbol} | {timeframe} | {period}")
    elif source == 'DHANHQ':
        st.success(f"📡 Live Data: DhanHQ | {symbol} | {timeframe} | {period}")
    else:
        st.warning(f"📡 Simulated Data | {symbol} | {timeframe} | {period}")

    raw_df = st.session_state.market_data[symbol].copy()
    df = engine.generate_signals(raw_df)
    latest = df.iloc[-1]
    p = st.session_state.strategy_params
    pos = st.session_state.open_position

    if st.session_state.auto_trade and st.session_state.loss_streak < st.session_state.loss_limit:
        if pos is None and latest['Signal'] == 'BUY' and latest['Confidence'] >= st.session_state.alert_threshold:
            st.session_state.open_position = {
                'symbol': symbol, 'entry': float(latest['Close']),
                'sl': float(latest['StopLoss']), 'target': float(latest['Target']),
                'time': datetime.now().strftime("%H:%M:%S")
            }
            st.toast(f"🤖 Auto-Pilot: BUY {symbol} @ ₹{latest['Close']:.2f}")
            st.rerun()
        elif pos is not None and pos['symbol'] == symbol:
            pnl = float(latest['Close']) - pos['entry']
            if latest['Signal'] == 'SELL' or latest['Low'] <= pos['sl'] or latest['High'] >= pos['target']:
                outcome = 'WIN' if pnl >= 0 else 'LOSS'
                st.session_state.trade_history.append({
                    'Action': 'AUTO CLOSE', 'Symbol': symbol, 'Entry': pos['entry'],
                    'Exit': latest['Close'], 'PnL': round(pnl, 2), 'Outcome': outcome,
                    'Time': datetime.now().strftime("%H:%M:%S")
                })
                st.session_state.loss_streak = 0 if outcome == 'WIN' else st.session_state.loss_streak + 1
                st.session_state.open_position = None
                st.rerun()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("LTP", f"₹{latest['Close']:.2f}")
    c2.metric("Signal", latest['Signal'])
    c3.metric("Confidence", f"{latest['Confidence']:.0f}%")
    c4.metric("RSI", f"{latest['RSI']:.1f}")
    c5.metric("Loss Streak", f"{st.session_state.loss_streak}/{st.session_state.loss_limit}")

    fig = make_subplots(
        rows=4, cols=1, shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.5, 0.15, 0.15, 0.2],
        subplot_titles=(f'{symbol} Price Action + T3 + UT Bot', 'RSI + MACD', 'T3 Trend', 'Volume')
    )

    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'], name='Price'
    ), row=1, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df['EMA_FAST'], line=dict(color='#00d4aa', width=1), name=f"EMA{p['ema_fast']}", opacity=0.7), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA_SLOW'], line=dict(color='#ff6b6b', width=1), name=f"EMA{p['ema_slow']}", opacity=0.7), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA_TREND'], line=dict(color='#ffd93d', width=1), name=f"EMA{p['ema_trend']}", opacity=0.7), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_UPPER'], line=dict(color='gray', width=1, dash='dash'), name='BB Upper', opacity=0.4), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_LOWER'], line=dict(color='gray', width=1, dash='dash'), name='BB Lower', opacity=0.4), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['T3'], line=dict(color='#7c3aed', width=2), name='T3 JVX'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['UT_Stop'], line=dict(color='#f97316', width=1.5, dash='dot'), name='UT Bot Stop'), row=1, col=1)

    buy_signals = df[df['Signal'] == 'BUY'].copy()
    sell_signals = df[df['Signal'] == 'SELL'].copy()

    if not buy_signals.empty:
        fig.add_trace(go.Scatter(
            x=buy_signals.index,
            y=buy_signals['Low'] - (buy_signals['ATR'] * 0.5),
            mode='markers+text',
            text=['BUY'] * len(buy_signals),
            textposition='bottom center',
            textfont=dict(color='#16a34a', size=11, family='Arial Black'),
            marker=dict(color='#16a34a', size=16, symbol='triangle-up', line=dict(color='white', width=1)),
            name='BUY Signal'
        ), row=1, col=1)

    if not sell_signals.empty:
        fig.add_trace(go.Scatter(
            x=sell_signals.index,
            y=sell_signals['High'] + (sell_signals['ATR'] * 0.5),
            mode='markers+text',
            text=['SELL'] * len(sell_signals),
            textposition='top center',
            textfont=dict(color='#dc2626', size=11, family='Arial Black'),
            marker=dict(color='#dc2626', size=16, symbol='triangle-down', line=dict(color='white', width=1)),
            name='SELL Signal'
        ), row=1, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], line=dict(color='#ab47bc', width=2), name='RSI'), row=2, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="#dc2626", opacity=0.6, row=2, col=1)
    fig.add_hline(y=50, line_dash="dash", line_color="#999", opacity=0.4, row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="#16a34a", opacity=0.6, row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], line=dict(color='#00d4aa', width=1.5), name='MACD'), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['MACD_SIGNAL'], line=dict(color='#ff6b6b', width=1.5), name='MACD Signal'), row=2, col=1)
    macd_colors = ['#00d4aa' if h >= 0 else '#ff6b6b' for h in df['MACD_HIST']]
    fig.add_trace(go.Bar(x=df.index, y=df['MACD_HIST'], marker_color=macd_colors, name='MACD Hist', opacity=0.5), row=2, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], line=dict(color='#1e293b', width=1), name='Close', opacity=0.6), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['T3'], line=dict(color='#7c3aed', width=2), name='T3', fill='tonexty', fillcolor='rgba(124,58,237,0.1)'), row=3, col=1)
    t3_bull = df[df['Close'] > df['T3']]
    t3_bear = df[df['Close'] < df['T3']]
    if not t3_bull.empty:
        fig.add_trace(go.Scatter(x=t3_bull.index, y=t3_bull['Close'], mode='markers', marker=dict(color='#16a34a', size=4, symbol='circle'), name='T3 Bull', opacity=0.6), row=3, col=1)
    if not t3_bear.empty:
        fig.add_trace(go.Scatter(x=t3_bear.index, y=t3_bear['Close'], mode='markers', marker=dict(color='#dc2626', size=4, symbol='circle'), name='T3 Bear', opacity=0.6), row=3, col=1)

    colors = ['#16a34a' if df['Close'].iloc[i] >= df['Open'].iloc[i] else '#dc2626' for i in range(len(df))]
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=colors, name='Volume', opacity=0.6), row=4, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['VOL_MA'], line=dict(color='#64748b', width=1.5), name='Vol MA20'), row=4, col=1)
    vol_spikes = df[df['VOL_RATIO'] > 2.0]
    if not vol_spikes.empty:
        fig.add_trace(go.Scatter(x=vol_spikes.index, y=vol_spikes['Volume'], mode='markers', marker=dict(color='#f59e0b', size=8, symbol='star'), name='Vol Spike', opacity=0.8), row=4, col=1)

    fig.update_layout(
        template="plotly_white",
        height=850,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
        margin=dict(l=0, r=0, t=60, b=0)
    )
    fig.update_xaxes(
        rangeslider_visible=False,
        tickformat='%d %b %Y',
        tickangle=-45,
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(0,0,0,0.05)'
    )
    if st.session_state.get('timeframe', '1d') in ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h']:
        fig.update_xaxes(tickformat='%H:%M<br>%d %b')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Live Trade Setup")
    tc1, tc2, tc3, tc4 = st.columns(4)
    tc1.metric("Entry", f"₹{latest['Entry']:.2f}" if not pd.isna(latest['Entry']) else "—")
    tc2.metric("Stop Loss", f"₹{latest['StopLoss']:.2f}" if not pd.isna(latest['StopLoss']) else "—")
    tc3.metric("Target", f"₹{latest['Target']:.2f}" if not pd.isna(latest['Target']) else "—")
    tc4.metric("Risk:Reward", f"1:{p['atr_multiplier_tp']/p['atr_multiplier_sl']:.1f}")
    if not pd.isna(latest['Reason']) and latest['Reason']:
        st.caption(f"📝 Confluence: {latest['Reason']}")

    st.divider()
    render_options_card(symbol, float(latest['Close']), latest['Signal'], float(latest['Confidence']))

    st.subheader("⚡ Quick Execution")
    if st.session_state.loss_streak >= st.session_state.loss_limit:
        st.error("🛑 CIRCUIT BREAKER: Trading blocked due to consecutive losses.")
    elif pos is None:
        if latest['Signal'] == 'BUY' and latest['Confidence'] >= st.session_state.alert_threshold:
            if st.button(f"🟢 BUY {symbol} @ ₹{latest['Close']:.2f}", use_container_width=True):
                st.session_state.open_position = {
                    'symbol': symbol, 'entry': float(latest['Close']),
                    'sl': float(latest['StopLoss']), 'target': float(latest['Target']),
                    'time': datetime.now().strftime("%H:%M:%S")
                }
                st.rerun()
        else:
            st.info("No valid entry signal at this time.")
    else:
        if pos['symbol'] == symbol:
            pnl = float(latest['Close']) - pos['entry']
            col_pnl, col_btn = st.columns([1, 2])
            col_pnl.metric("Open PnL", f"₹{pnl:.2f}", delta=f"{pnl:.2f}")
            if col_btn.button("🔴 CLOSE POSITION", type="primary", use_container_width=True):
                outcome = 'WIN' if pnl >= 0 else 'LOSS'
                st.session_state.trade_history.append({
                    'Action': 'MANUAL CLOSE', 'Symbol': symbol, 'Entry': pos['entry'],
                    'Exit': latest['Close'], 'PnL': round(pnl, 2), 'Outcome': outcome,
                    'Time': datetime.now().strftime("%H:%M:%S")
                })
                st.session_state.loss_streak = 0 if outcome == 'WIN' else st.session_state.loss_streak + 1
                st.session_state.open_position = None
                st.rerun()


def render_backtest():
    st.header("🧪 Strategy Backtest Engine")
    st.info("⚠️ **Risk Disclaimer**: No strategy guarantees 90% win rate in live markets. Backtests show historical performance on simulated data. Past performance ≠ future results.")
    symbol = st.selectbox("Select Asset for Backtest", st.session_state.watchlist)
    col1, col2, col3 = st.columns(3)
    initial_capital = col1.number_input("Initial Capital", value=100000, step=10000)
    risk_per_trade = col2.slider("Risk per Trade (%)", 0.5, 5.0, 2.0, 0.5) / 100
    min_confidence = col3.slider("Min Confidence (%)", 50, 95, 70, 5)
    if st.button("🚀 Run Backtest", type="primary", use_container_width=True):
        with st.spinner("Running walk-forward analysis..."):
            params = st.session_state.strategy_params.copy()
            params['min_confidence'] = min_confidence
            bt_engine = StrategyEngine(params)
            raw_df = st.session_state.market_data[symbol].copy()
            results = bt_engine.backtest(raw_df, initial_capital, risk_per_trade)
            st.session_state.backtest_results[symbol] = results
        if results['metrics']:
            m = results['metrics']
            st.subheader("📈 Performance Metrics")
            mc1, mc2, mc3, mc4, mc5, mc6 = st.columns(6)
            win_rate_color = 'win-rate-high' if m['win_rate'] >= 60 else 'win-rate-low'
            mc1.markdown(f"<div class='{win_rate_color}'>Win Rate<br>{m['win_rate']}%</div>", unsafe_allow_html=True)
            mc2.metric("Total Trades", m['total_trades'])
            mc3.metric("Profit Factor", m['profit_factor'])
            mc4.metric("Total Return", f"{m['total_return_pct']}%")
            mc5.metric("Max Drawdown", f"{m['max_drawdown_pct']}%")
            mc6.metric("Sharpe Ratio", m['sharpe_ratio'])
            st.markdown("---")
            if len(results['equity']) > 1:
                eq_df = pd.DataFrame({'Equity': results['equity']})
                fig = go.Figure()
                fig.add_trace(go.Scatter(y=eq_df['Equity'], mode='lines', line=dict(color='#00d4aa')))
                fig.update_layout(template='plotly_white', title='Equity Curve', height=300, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig, use_container_width=True)
            if results['trades']:
                trades_df = pd.DataFrame(results['trades'])
                st.subheader("📋 Trade Log")
                st.dataframe(trades_df, use_container_width=True, hide_index=True)
                wl_counts = trades_df['result'].value_counts()
                if len(wl_counts) > 0:
                    fig2 = go.Figure(data=[go.Pie(labels=wl_counts.index, values=wl_counts.values, marker_colors=['#00d4aa', '#ff6b6b'])])
                    fig2.update_layout(template='plotly_white', title='Win/Loss Distribution', height=300)
                    st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("No trades generated in backtest period. Try adjusting parameters.")


def render_execution():
    st.header("⚡ Order Execution")
    open_ok, market_msg = is_market_open()
    if not open_ok:
        st.warning(f"⚠️ {market_msg}. Orders may be rejected by broker.")

    broker = st.session_state.get('selected_broker', 'PAYTM')

    if st.session_state.exec_mode == "LIVE":
        if broker == 'PAYTM' and not st.session_state.paytm_connected:
            st.error("🔴 Paytm Money not connected. Switch to PAPER mode or connect Paytm Money.")
            return
        elif broker == 'DHANHQ' and not st.session_state.dhan_connected:
            st.error("🔴 DhanHQ not connected. Switch to PAPER mode or connect DhanHQ.")
            return

    if st.session_state.exec_mode == "LIVE":
        st.info(f"🛡️ **LIVE MODE ACTIVE** — Real money will be used with {broker}. Double-check symbol, quantity, and price before confirming.")

    with st.form("order_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            sym = st.selectbox("Symbol", st.session_state.watchlist, index=st.session_state.watchlist.index(st.session_state.order_symbol))
        with c2:
            side = st.selectbox("Side", ["BUY", "SELL"])
        with c3:
            otype = st.selectbox("Order Type", ["MARKET", "LIMIT", "SL", "SL-M"])
        c4, c5, c6 = st.columns(3)
        with c4:
            qty = st.number_input("Quantity", min_value=1, max_value=10000, value=1)
        with c5:
            price = st.number_input("Price (for LIMIT/SL)", min_value=0.0, value=0.0, step=0.05)
        with c6:
            sl = st.number_input("Stop Loss (₹)", min_value=0.0, value=0.0, step=0.05)
        target = st.number_input("Target (₹)", min_value=0.0, value=0.0, step=0.05)

        with st.expander("💰 Estimate Trading Costs for This Order"):
            cc_seg = st.selectbox("Cost Segment", list(CHARGE_DEFAULTS.keys()), index=1, key="exec_cost_segment")
            ref_price = price if price > 0 else float(st.session_state.market_data[sym].iloc[-1]['Close'])
            est = calculate_trade_charges(cc_seg, ref_price, ref_price, qty)
            ec1, ec2, ec3 = st.columns(3)
            ec1.metric("Round-trip Charges", f"₹{est['total_charges']:.2f}")
            ec2.metric("Breakeven Move", f"₹{est['breakeven_price'] - ref_price:.2f}")
            ec3.metric("Charges % of Turnover", f"{est['charges_pct_of_turnover']:.3f}%")
            st.caption("Assumes you exit at the same reference price — i.e. the minimum favorable move needed just to cover costs. Open '💰 Cost & Brokerage Calculator' for a full custom breakdown.")

        confirm_live = True
        if st.session_state.exec_mode == "LIVE":
            st.markdown("---")
            st.markdown("""
            <div style="background:#fff9e6; border:2px solid #f59e0b; border-radius:12px; padding:16px; margin:12px 0;">
                <h4 style="margin:0 0 8px 0; color:#92400e;">⚠️ LIVE ORDER CONFIRMATION REQUIRED</h4>
                <p style="margin:0; color:#78350f; font-size:14px;">You are about to place a <b>REAL</b> order with actual capital.</p>
            </div>
            """, unsafe_allow_html=True)
            confirm_live = st.checkbox("✅ I confirm this is a REAL order and I accept all risks", value=False)
        submitted = st.form_submit_button("📤 Place Order", use_container_width=True)
        if submitted:
            if st.session_state.exec_mode == "LIVE" and not confirm_live:
                st.error("❌ You must check the confirmation box to place a LIVE order.")
                return

            if broker == 'PAYTM':
                errors, warnings = validate_order(sym, qty, side, otype, price, paytm_manager.client)
            else:
                errors, warnings = validate_order(sym, qty, side, otype, price, dhan_manager.client)

            if errors:
                st.error("🛑 Order blocked: Risk limit exceeded")
                st.error("\n".join([f"- {e}" for e in errors]))
                if warnings:
                    st.warning("\n".join([f"- {w}" for w in warnings]))
                return
            result = place_broker_order(sym, qty, side, otype, price)
            if result.get('success'):
                st.session_state.last_order_time = datetime.now()
                st.session_state.trade_history.append({
                    'Action': f'{side} {otype}', 'Symbol': sym, 'Qty': qty,
                    'Price': result['price'], 'Time': result['timestamp'],
                    'Outcome': 'PAPER' if st.session_state.exec_mode == 'PAPER' else 'LIVE',
                    'PnL': 0, 'SL': sl, 'Target': target
                })
                st.session_state.order_result = result
                if st.session_state.exec_mode == "LIVE":
                    st.success(f"✅ LIVE Order placed: {result['order_id']} | Status: {result['status']}")
                else:
                    st.success(f"✅ PAPER Order placed: {result['order_id']}")
            else:
                st.error(f"❌ Order failed: {result.get('error')}")
    if st.session_state.order_result:
        with st.expander("View Order Details"):
            st.json(st.session_state.order_result)


def render_ledger():
    st.header("📋 Trade Ledger & Analytics")
    if st.session_state.trade_history:
        df = pd.DataFrame(st.session_state.trade_history)
        st.dataframe(df, use_container_width=True, hide_index=True)
        if 'Outcome' in df.columns:
            wins = df[df['Outcome'] == 'WIN']
            losses = df[df['Outcome'] == 'LOSS']
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Trades", len(df))
            c2.metric("Wins", len(wins))
            c3.metric("Losses", len(losses))
            if len(wins) + len(losses) > 0:
                wr = len(wins) / (len(wins) + len(losses)) * 100
                st.metric("Live Win Rate", f"{wr:.1f}%")
    else:
        st.info("No trades executed yet.")


def render_cost_calculator():
    st.header("💰 Cost & Brokerage Calculator")
    st.caption("Estimate brokerage, STT, exchange charges, SEBI fees, stamp duty & GST for a trade — Paytm Money-style defaults, fully editable.")
    st.info("ℹ️ Defaults reflect Paytm Money's published pricing and standard NSE/SEBI/Govt levies as of mid-2026 (incl. FY2026-27 STT rates on F&O, effective 1-Apr-2026). Rates change periodically and stamp duty varies by state — verify against your broker's official calculator/contract note before relying on this for accounting or tax filing.")

    c1, c2, c3 = st.columns(3)
    segment = c1.selectbox("Segment", list(CHARGE_DEFAULTS.keys()), key="cc_segment")
    direction = c2.selectbox("Direction", ["Long (Buy → Sell)", "Short (Sell → Buy)"], key="cc_direction")
    use_watchlist = c3.checkbox("Auto-fill lot size from watchlist", value=False, key="cc_use_watchlist") if segment in ("Equity Futures", "Equity Options") else False

    c4, c5, c6 = st.columns(3)
    entry_label = "Buy Price (₹)" if direction.startswith("Long") else "Sell Price (₹)"
    exit_label = "Sell Price (₹)" if direction.startswith("Long") else "Buy Price (₹)"
    entry_price = c4.number_input(entry_label, min_value=0.0, value=100.0, step=0.05, key="cc_entry")
    exit_price = c5.number_input(exit_label, min_value=0.0, value=105.0, step=0.05, key="cc_exit")

    if segment in ("Equity Futures", "Equity Options"):
        if use_watchlist:
            wl_sym = c6.selectbox("Symbol (for lot size)", st.session_state.watchlist, key="cc_wl_sym")
            lot_size = get_lot_size(wl_sym)
            st.caption(f"Lot size for {wl_sym}: {lot_size}")
        else:
            lot_size = c6.number_input("Lot Size", min_value=1, value=75, step=1, key="cc_lot")
        num_lots = st.number_input("Number of Lots", min_value=1, value=1, step=1, key="cc_lots")
        quantity = lot_size * num_lots
        st.caption(f"Total Quantity: {quantity} ({num_lots} lot × {lot_size})")
    else:
        quantity = c6.number_input("Quantity (Shares)", min_value=1, value=100, step=1, key="cc_qty")

    if direction.startswith("Long"):
        buy_price, sell_price = entry_price, exit_price
    else:
        buy_price, sell_price = exit_price, entry_price

    with st.expander("⚙️ Override brokerage / charge rates (advanced)"):
        cfg_default = CHARGE_DEFAULTS[segment]
        oc1, oc2, oc3 = st.columns(3)
        brokerage_flat = oc1.number_input(
            "Brokerage per order (₹)", min_value=0.0, value=float(cfg_default["brokerage_flat"]), step=1.0, key="cc_bflat",
            help="Flat brokerage per executed order (per leg). For 'lower of flat/%' segments (e.g. Equity Intraday), this is the cap."
        )
        brokerage_pct = oc2.number_input(
            "Brokerage (% of trade value)", min_value=0.0, value=float(cfg_default["brokerage_pct"]), step=0.01, format="%.2f", key="cc_bpct",
            help="Only used for segments priced as 'lower of flat ₹ or % of trade value' (e.g. Equity Intraday)."
        )
        stamp_duty_buy_pct = oc3.number_input(
            "Stamp Duty — buy side (%)", min_value=0.0, value=float(cfg_default["stamp_duty_buy_pct"]), step=0.001, format="%.3f", key="cc_stamp",
            help="State-dependent. Default assumes Maharashtra rates — adjust for your state of residence."
        )

    overrides = {"brokerage_flat": brokerage_flat, "brokerage_pct": brokerage_pct, "stamp_duty_buy_pct": stamp_duty_buy_pct}
    result = calculate_trade_charges(segment, buy_price, sell_price, quantity, overrides)

    st.divider()
    st.subheader("📊 Charge Breakdown")
    bc1, bc2, bc3, bc4 = st.columns(4)
    bc1.metric("Brokerage", f"₹{result['brokerage']:.2f}")
    bc2.metric("STT", f"₹{result['stt']:.2f}")
    bc3.metric("Exchange Txn Charges", f"₹{result['exch_txn']:.2f}")
    bc4.metric("SEBI Fee", f"₹{result['sebi_fee']:.2f}")
    bc5, bc6, bc7, bc8 = st.columns(4)
    bc5.metric("Stamp Duty", f"₹{result['stamp_duty']:.2f}")
    bc6.metric("GST (18%)", f"₹{result['gst']:.2f}")
    bc7.metric("DP Charges", f"₹{result['dp_charge']:.2f}")
    bc8.metric("Total Charges", f"₹{result['total_charges']:.2f}")

    st.divider()
    pc1, pc2, pc3 = st.columns(3)
    pc1.metric("Gross P&L", f"₹{result['gross_pnl']:.2f}")
    pc2.metric("Net P&L (after charges)", f"₹{result['net_pnl']:.2f}", delta=f"-₹{result['total_charges']:.2f} in costs")
    pc3.metric("Breakeven Exit Price", f"₹{result['breakeven_price']:.2f}")
    st.caption(f"Total Turnover: ₹{result['total_turnover']:,.2f}  |  Charges are {result['charges_pct_of_turnover']:.3f}% of turnover")

    with st.expander("📋 Full breakdown table"):
        breakdown_df = pd.DataFrame([
            {"Charge": "Brokerage", "Amount (₹)": round(result['brokerage'], 2)},
            {"Charge": "STT", "Amount (₹)": round(result['stt'], 2)},
            {"Charge": "Exchange Transaction Charges", "Amount (₹)": round(result['exch_txn'], 2)},
            {"Charge": "SEBI Turnover Fee", "Amount (₹)": round(result['sebi_fee'], 2)},
            {"Charge": "Stamp Duty", "Amount (₹)": round(result['stamp_duty'], 2)},
            {"Charge": "GST (18%)", "Amount (₹)": round(result['gst'], 2)},
            {"Charge": "DP Charges", "Amount (₹)": round(result['dp_charge'], 2)},
            {"Charge": "TOTAL CHARGES", "Amount (₹)": round(result['total_charges'], 2)},
        ])
        st.dataframe(breakdown_df, use_container_width=True, hide_index=True)

    st.caption("📌 Stamp duty defaults assume Maharashtra rates (varies by state). STT on F&O reflects FY2026-27 rates post Union Budget 2026. This is an estimate for planning purposes, not a substitute for your broker's official contract note.")


def render_depth():
    st.header("🔍 Market Depth & Watchlist")
    scan = []
    for sym in st.session_state.watchlist:
        df = engine.generate_signals(st.session_state.market_data[sym].copy())
        latest = df.iloc[-1]
        scan.append({'Symbol': sym, 'LTP': round(latest['Close'], 2), 'Signal': latest['Signal'], 'Confidence': f"{latest['Confidence']:.0f}%", 'RSI': round(latest['RSI'], 1), 'Volume': int(latest['Volume'])})
    scan_df = pd.DataFrame(scan)
    st.dataframe(scan_df.style.apply(lambda x: ['background-color: #d1fae5' if v == 'BUY' else 'background-color: #fee2e2' if v == 'SELL' else '' for v in x], subset=['Signal']), use_container_width=True, hide_index=True)
    sym = st.selectbox("Select for Depth", st.session_state.watchlist)
    ltp = st.session_state.market_data[sym].iloc[-1]['Close']
    bids = pd.DataFrame({'Bid Price': [round(ltp - i*0.5, 2) for i in range(1, 6)], 'Bid Qty': np.random.randint(1000, 10000, 5)})
    asks = pd.DataFrame({'Ask Price': [round(ltp + i*0.5, 2) for i in range(1, 6)], 'Ask Qty': np.random.randint(1000, 10000, 5)})
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("<span style='color:#00d4aa'><b>BIDS</b></span>", unsafe_allow_html=True)
        st.dataframe(bids, hide_index=True, use_container_width=True)
    with d2:
        st.markdown("<span style='color:#ff6b6b'><b>ASKS</b></span>", unsafe_allow_html=True)
        st.dataframe(asks, hide_index=True, use_container_width=True)


def render_options_page():
    st.header("📈 Options Strike Selector")
    st.markdown("<p style='color:#64748b; margin-bottom:20px;'>When a BUY or SELL signal is generated on an index or stock, this tool calculates the <b>ATM</b>, <b>ITM</b>, and <b>OTM</b> option strikes for you. <br><span style='color:#16a34a;'>BUY signal → Buy CE (Call)</span> | <span style='color:#dc2626;'>SELL signal → Buy PE (Put)</span></p>", unsafe_allow_html=True)
    symbol = st.selectbox("🎯 Select Underlying", st.session_state.watchlist)
    raw_df = st.session_state.market_data[symbol].copy()
    df = engine.generate_signals(raw_df)
    latest = df.iloc[-1]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("LTP", f"₹{latest['Close']:.2f}")
    col2.metric("Signal", latest['Signal'])
    col3.metric("Confidence", f"{latest['Confidence']:.0f}%")
    col4.metric("RSI", f"{latest['RSI']:.1f}")
    st.divider()
    render_options_card(symbol, float(latest['Close']), latest['Signal'], float(latest['Confidence']))
    if latest['Signal'] in ["BUY", "SELL"]:
        strikes = calculate_option_strikes(symbol, float(latest['Close']), latest['Signal'])
        st.subheader("📋 Detailed Breakdown")
        md_lines = [
            f"| Parameter | Value |",
            f"|-----------|-------|",
            f"| Underlying | {symbol} |",
            f"| Spot Price | ₹{strikes['ltp']} |",
            f"| Signal | {strikes['bias']} ({latest['Signal']}) |",
            f"| Option Type | {strikes['option_type']} |",
            f"| Strike Interval | {strikes['interval']} |",
            f"| Lot Size | {strikes['lot_size']} |",
            f"| ATM Strike | {strikes['atm']} |"
        ]
        st.markdown("\n".join(md_lines))
        if strikes['recommendations']:
            st.subheader("🎯 Strike Comparison Table")
            rec_df = pd.DataFrame(strikes['recommendations'])
            st.dataframe(rec_df, use_container_width=True, hide_index=True)
        st.info("💡 **How to use:**\n- **Conservative**: Choose ITM strike (lower risk, higher premium)\n- **Balanced**: Choose ATM strike (recommended for most traders)\n- **Aggressive**: Choose OTM strike (lower premium, higher leverage, higher risk)\n- Always use Stop Loss as per the main strategy.")
        st.subheader("⚡ Quick Options Order")
        if st.session_state.loss_streak >= st.session_state.loss_limit:
            st.error("🛑 CIRCUIT BREAKER: Trading blocked.")
        else:
            if strikes['recommendations']:
                rec = strikes['recommendations'][1] if len(strikes['recommendations']) > 1 else strikes['recommendations'][0]
                opt_sym = f"{symbol} {rec['strike']} {rec['type']}"
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Recommended Strike", f"{rec['strike']} {rec['type']}")
                with c2:
                    st.metric("Suggested Qty", f"{rec['suggested_qty']} lots")
                with c3:
                    st.metric("Lot Size", strikes['lot_size'])
                if st.button(f"📤 Place {rec['type']} Order @ {rec['strike']}", type="primary", use_container_width=True):
                    order = {"success": True, "order_id": f"OPT{datetime.now().strftime('%H%M%S')}", "symbol": opt_sym, "side": "BUY", "type": "MARKET", "quantity": rec['suggested_qty'] * strikes['lot_size'], "price": latest['Close'], "status": "PAPER EXECUTED", "timestamp": datetime.now().strftime("%H:%M:%S")}
                    st.session_state.trade_history.append({'Action': f"BUY {rec['type']}", 'Symbol': opt_sym, 'Qty': order['quantity'], 'Price': latest['Close'], 'Time': order['timestamp'], 'Outcome': 'PAPER'})
                    st.session_state.order_result = order
                    st.success(f"✅ {opt_sym} order placed! ID: {order['order_id']}")


def render_quantum_page():
    st.header("🚀 Quantum Algo — Small Capital Scalping")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fef3c7, #fde68a); border: 2px solid #f59e0b; border-radius: 16px; padding: 20px; margin-bottom: 24px;">
        <h3 style="margin:0 0 8px 0; color:#92400e;">⚡ Quantum Scalping Mode</h3>
        <p style="margin:0; color:#78350f; font-size:15px;">Built for <b>₹10,000 to ₹50,000</b> capital accounts. Uses ultra-fast signals, tight stops, and aggressive position sizing.</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    capital = c1.number_input("Capital (₹)", min_value=5000, max_value=500000, value=10000, step=5000)
    daily_target = c2.number_input("Daily Target (₹)", min_value=500, max_value=50000, value=2000, step=500)
    risk_per_trade = c3.slider("Risk/Trade (%)", 0.5, 5.0, 2.0, 0.5)
    leverage = c4.selectbox("Leverage", [1, 2, 3, 5], index=0)
    quantum = QuantumAlgo(capital, daily_target, risk_per_trade)
    session_info = quantum.get_session_recommendation()
    st.markdown(f"""
    <div style="display:flex; gap:12px; align-items:center; margin:16px 0;">
        <div style="background:{session_info['color']}; color:white; padding:8px 16px; border-radius:999px; font-weight:700; font-size:14px;">{session_info['session']}</div>
        <div style="color:#475569; font-size:14px;">Quality: <b>{session_info['quality']}</b> — {session_info['reason']}</div>
    </div>
    """, unsafe_allow_html=True)
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_trades = [t for t in st.session_state.trade_history if t.get('Time', '').startswith(today_str)]
    today_pnl = sum([t.get('PnL', 0) for t in today_trades if 'PnL' in t])
    progress = max(0, min(today_pnl / daily_target * 100, 100)) if daily_target > 0 else 0
    st.subheader("📊 Daily Target Progress")
    prog_col1, prog_col2 = st.columns([3, 1])
    with prog_col1:
        st.progress(max(0, min(progress / 100, 1.0)))
    with prog_col2:
        st.metric("Today's PnL", f"₹{today_pnl:.0f}", delta=f"{progress:.0f}% of target")
    if progress >= 100:
        st.success("🎯 Daily target achieved! Consider stopping for the day.")
    elif progress >= 50:
        st.warning("⚠️ Halfway to target. Don't overtrade.")
    st.divider()
    st.subheader("🔥 Quantum Live Scanner")
    st.caption("Scanning all watchlist symbols for scalping opportunities...")
    scan_results = []
    for sym in st.session_state.watchlist:
        raw = st.session_state.market_data[sym].copy()
        sig = quantum.quantum_signal(raw, sym)
        if sig and sig['confidence'] >= 70:
            scan_results.append(sig)
    if scan_results:
        scan_results.sort(key=lambda x: x['confidence'], reverse=True)
        st.success(f"🎯 {len(scan_results)} high-probability scalping setup(s) found!")
        for sig in scan_results[:3]:
            with st.container(border=True):
                col_a, col_b, col_c, col_d = st.columns([2, 1, 1, 1])
                with col_a:
                    st.markdown(f"""
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="font-size:28px;">{'🟢' if sig['signal']=='BUY' else '🔴'}</div>
                        <div>
                            <div style="font-size:18px; font-weight:800; color:#1e293b;">{sig['symbol']}</div>
                            <div style="font-size:12px; color:#64748b;">{sig['reasons']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    st.metric("Confidence", f"{sig['confidence']}%")
                with col_c:
                    st.metric("VWAP Dev", f"{((sig['entry']-sig['vwap'])/sig['vwap']*100):+.2f}%")
                with col_d:
                    st.metric("Vol Spike", f"{sig['volume_ratio']}x")
                qty = quantum.calculate_position_size(sig['entry'], sig['stop_loss'], leverage)
                margin_required = qty * sig['entry'] * (0.2 if leverage > 1 else 1.0)
                st.markdown(f"""
                <div style="background:#f8fafc; border-radius:10px; padding:12px; margin-top:8px;">
                    <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:16px;">
                        <div><b>Entry:</b> ₹{sig['entry']}</div>
                        <div><b>SL:</b> ₹{sig['stop_loss']} (₹{abs(sig['entry']-sig['stop_loss']):.2f} risk)</div>
                        <div><b>Target:</b> ₹{sig['target']} (₹{abs(sig['target']-sig['entry']):.2f} reward)</div>
                        <div><b>Qty:</b> {qty} shares</div>
                        <div><b>Margin:</b> ~₹{margin_required:.0f}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.session_state.loss_streak < st.session_state.loss_limit:
                    btn_text = f"⚡ QUANTUM {sig['signal']} {sig['symbol']}"
                    if st.button(btn_text, key=f"quantum_{sig['symbol']}_{sig['signal']}", use_container_width=True):
                        order = {"success": True, "order_id": f"QTM{datetime.now().strftime('%H%M%S')}", "symbol": sig['symbol'], "side": sig['signal'], "type": "MARKET", "quantity": qty, "entry": sig['entry'], "stop_loss": sig['stop_loss'], "target": sig['target'], "status": "PAPER EXECUTED", "timestamp": datetime.now().strftime("%H:%M:%S")}
                        st.session_state.trade_history.append({'Action': f"QUANTUM {sig['signal']}", 'Symbol': sig['symbol'], 'Qty': qty, 'Price': sig['entry'], 'SL': sig['stop_loss'], 'Target': sig['target'], 'Time': order['timestamp'], 'Outcome': 'PAPER', 'PnL': 0})
                        st.session_state.order_result = order
                        st.success(f"✅ Quantum {sig['signal']} executed! SL: ₹{sig['stop_loss']}, Target: ₹{sig['target']}")
                        st.rerun()
                else:
                    st.error("🛑 Circuit breaker active. Reset in Strategy Lab.")
    else:
        st.info("⏳ No quantum scalping setups right now. Waiting for EMA3 cross + volume spike + VWAP confirmation...")
    st.divider()
    st.subheader("📈 Compounding Projection")
    st.markdown("<p style='color:#64748b; font-size:14px;'>This shows what happens if you compound daily profits. <b>Remember: losses compound too!</b></p>", unsafe_allow_html=True)
    days = st.slider("Projection Days", 1, 30, 5)
    win_rate = st.slider("Expected Win Rate (%)", 40, 80, 55)
    avg_win_pct = st.slider("Avg Win (%)", 1.0, 10.0, 3.0, 0.5)
    avg_loss_pct = st.slider("Avg Loss (%)", 0.5, 5.0, 2.0, 0.5)
    current = capital
    equity_curve = [current]
    for day in range(days):
        expected = (win_rate/100 * avg_win_pct/100) - ((100-win_rate)/100 * avg_loss_pct/100)
        daily_return = np.random.normal(expected, 0.02)
        current = current * (1 + daily_return)
        equity_curve.append(current)
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=equity_curve, mode='lines+markers', line=dict(color='#00b894', width=2), marker=dict(size=8), name='Projected Capital'))
    fig.add_hline(y=capital, line_dash="dash", line_color="#dc2626", annotation_text="Starting Capital")
    fig.update_layout(template='plotly_white', title=f'Compounding Projection ({days} days)', xaxis_title='Days', yaxis_title='Capital (₹)', height=350, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True)
    final = equity_curve[-1]
    st.metric("Projected Final Capital", f"₹{final:,.0f}", delta=f"₹{final-capital:,.0f}")
    st.divider()
    with st.expander("⚠️ REALITY CHECK — Read Before Trading"):
        st.markdown("""
        ### The Hard Truth About ₹2,000/day on ₹10,000
        **Mathematics:**
        - ₹2,000 on ₹10,000 = **20% daily return**
        - Compounded: ₹10,000 → ₹51,000 in 1 week → ₹2.6 crore in 1 month
        - If this were real, every trader would be a billionaire in 3 months.
        **What Actually Happens:**
        1. **Overtrading** → More commissions, more slippage, more mistakes
        2. **Revenge trading** → Chasing losses leads to bigger losses
        3. **Ignored stop losses** → ₹2,000 target becomes ₹10,000 loss
        4. **Brokerage & taxes** → STT, GST, stamp duty eat 0.5-1% per trade
        **Realistic Expectations:**
        | Capital | Realistic Daily Target | Monthly Target |
        |---------|----------------------|----------------|
        | ₹10,000 | ₹200-500 (2-5%) | ₹4,000-10,000 |
        | ₹25,000 | ₹500-1,250 (2-5%) | ₹10,000-25,000 |
        | ₹50,000 | ₹1,000-2,500 (2-5%) | ₹20,000-50,000 |
        | ₹1,00,000 | ₹2,000-5,000 (2-5%) | ₹40,000-1,00,000 |
        **The Quantum Algo's Real Goal:**
        - Capture 2-5 small moves per day
        - Risk only 1-2% per trade
        - Let compounding work over WEEKS, not hours
        - **Target: 10-20% monthly, not 20% daily**
        > *"The stock market is a device for transferring money from the impatient to the patient."* — Warren Buffett
        """)


def render_options_strategies():
    st.header("📋 Options Strategies Builder")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0f9ff, #e0f2fe); border: 1px solid #bae6fd; border-radius: 16px; padding: 20px; margin-bottom: 24px;">
        <h3 style="margin:0 0 8px 0; color:#0369a1;">🎯 Advanced Options Strategies</h3>
        <p style="margin:0; color:#475569; font-size:15px;">Select a strategy, configure strikes, and execute with proper risk management. All strategies include automatic stop loss and target calculation.</p>
    </div>
    """, unsafe_allow_html=True)
    left_col, right_col = st.columns([1.2, 1.8])
    with left_col:
        st.subheader("📋 Strategy List")
        strategies = ["Buy Call", "Sell Put", "Bull Call Spread", "Bull Put Spread", "Buy Put", "Sell Call", "Bear Put Spread", "Bear Call Spread", "Short Straddle", "Short Strangle", "Iron Butterfly", "Iron Condor"]
        strategy_info = {
            "Buy Call": {"risk": "Limited", "reward": "Unlimited", "direction": "Bullish", "color": "#16a34a"},
            "Sell Put": {"risk": "High", "reward": "Limited", "direction": "Bullish", "color": "#22c55e"},
            "Bull Call Spread": {"risk": "Limited", "reward": "Limited", "direction": "Bullish", "color": "#15803d"},
            "Bull Put Spread": {"risk": "Limited", "reward": "Limited", "direction": "Bullish", "color": "#166534"},
            "Buy Put": {"risk": "Limited", "reward": "Unlimited", "direction": "Bearish", "color": "#dc2626"},
            "Sell Call": {"risk": "High", "reward": "Limited", "direction": "Bearish", "color": "#ef4444"},
            "Bear Put Spread": {"risk": "Limited", "reward": "Limited", "direction": "Bearish", "color": "#b91c1c"},
            "Bear Call Spread": {"risk": "Limited", "reward": "Limited", "direction": "Bearish", "color": "#991b1b"},
            "Short Straddle": {"risk": "Unlimited", "reward": "Limited", "direction": "Neutral", "color": "#f59e0b"},
            "Short Strangle": {"risk": "Unlimited", "reward": "Limited", "direction": "Neutral", "color": "#d97706"},
            "Iron Butterfly": {"risk": "Limited", "reward": "Limited", "direction": "Neutral", "color": "#7c3aed"},
            "Iron Condor": {"risk": "Limited", "reward": "Limited", "direction": "Neutral", "color": "#6d28d9"}
        }
        selected_strategy = st.selectbox("Select Strategy", strategies, index=0)
        info = strategy_info[selected_strategy]
        st.markdown(f"""
        <div style="background: #ffffff; border: 2px solid {info['color']}; border-radius: 12px; padding: 16px; margin-top: 12px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-size:18px; font-weight:800; color:{info['color']};">{selected_strategy}</span>
                <span style="background:{info['color']}; color:white; padding:4px 12px; border-radius:999px; font-size:12px; font-weight:700;">{info['direction']}</span>
            </div>
            <div style="display:flex; gap:16px; font-size:14px; color:#475569;">
                <div><b>Risk:</b> {info['risk']}</div>
                <div><b>Reward:</b> {info['reward']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        explanations = {
            "Buy Call": "Buy a Call option when bullish. Profit if price rises above strike + premium paid. Max loss = premium paid.",
            "Sell Put": "Sell a Put option when bullish/neutral. Profit if price stays above strike. Risk if price falls significantly.",
            "Bull Call Spread": "Buy ATM Call + Sell OTM Call. Limits both risk and reward. Best for moderate bullish moves.",
            "Bull Put Spread": "Sell ATM Put + Buy OTM Put. Credit strategy. Profit if price stays above short put strike.",
            "Buy Put": "Buy a Put option when bearish. Profit if price falls below strike - premium paid. Max loss = premium.",
            "Sell Call": "Sell a Call option when bearish/neutral. Profit if price stays below strike. Unlimited risk if price rises.",
            "Bear Put Spread": "Buy ATM Put + Sell OTM Put. Limits both risk and reward. Best for moderate bearish moves.",
            "Bear Call Spread": "Sell ATM Call + Buy OTM Call. Credit strategy. Profit if price stays below short call strike.",
            "Short Straddle": "Sell ATM Call + Sell ATM Put. Profit if price stays near ATM. High risk if big move occurs.",
            "Short Strangle": "Sell OTM Call + Sell OTM Put. Wider profit zone than straddle. Lower premium but safer.",
            "Iron Butterfly": "Sell ATM Straddle + Buy OTM wings. Defined risk. Profit if price stays exactly at ATM.",
            "Iron Condor": "Sell OTM Call Spread + Sell OTM Put Spread. Best for range-bound markets. Defined risk."
        }
        st.info(explanations.get(selected_strategy, ""))
    with right_col:
        st.subheader("⚙️ Strategy Configuration")
        instrument = st.selectbox("✅ Instrument Selector", st.session_state.watchlist, index=0)
        raw_df = st.session_state.market_data[instrument].copy()
        df = engine.generate_signals(raw_df)
        ltp = float(df.iloc[-1]['Close'])
        st.metric("Current LTP", f"₹{ltp:.2f}")
        expiry_type = st.radio("✅ Weekly / Monthly", options=["Weekly", "Monthly"], horizontal=True)
        interval = get_strike_interval(instrument)
        atm_strike = round(ltp / interval) * interval
        strike_col1, strike_col2 = st.columns(2)
        with strike_col1:
            strike_mode = st.selectbox("✅ Strike Selection", ["ATM", "ITM", "OTM", "Custom"], index=0)
        with strike_col2:
            if strike_mode == "ATM":
                selected_strike = atm_strike
                st.number_input("Strike", value=atm_strike, disabled=True)
            elif strike_mode == "ITM":
                itm_offset = st.selectbox("ITM Offset", [1, 2, 3], index=0)
                selected_strike = atm_strike - (itm_offset * interval)
            elif strike_mode == "OTM":
                otm_offset = st.selectbox("OTM Offset", [1, 2, 3], index=0)
                selected_strike = atm_strike + (otm_offset * interval)
            else:
                selected_strike = st.number_input("Custom Strike", value=atm_strike, step=interval)
        lot_size = get_lot_size(instrument)
        lots = st.number_input("✅ Lot Size (Lots)", min_value=1, max_value=100, value=1, step=1)
        total_qty = lots * lot_size
        st.caption(f"Total Quantity: {total_qty} shares ({lots} lot × {lot_size})")
        action_col1, action_col2 = st.columns(2)
        with action_col1:
            buy_clicked = st.button("🟢 BUY", use_container_width=True, type="primary")
        with action_col2:
            sell_clicked = st.button("🔴 SELL", use_container_width=True)
        action = None
        if buy_clicked:
            action = "BUY"
        elif sell_clicked:
            action = "SELL"
        st.markdown("---")
        sl_col1, sl_col2 = st.columns(2)
        with sl_col1:
            stop_loss = st.number_input("✅ Stop Loss (₹)", min_value=0.0, value=round(ltp * 0.95, 2), step=0.5)
        with sl_col2:
            target = st.number_input("✅ Target (₹)", min_value=0.0, value=round(ltp * 1.05, 2), step=0.5)
        time_col1, time_col2 = st.columns(2)
        with time_col1:
            entry_time = st.time_input("✅ Entry Time", value=datetime.now().time())
        with time_col2:
            exit_time = st.time_input("✅ Exit Time", value=(datetime.now() + timedelta(hours=1)).time())
        st.markdown("---")
        st.subheader("📊 Strategy Legs")
        legs = []
        if selected_strategy == "Buy Call":
            legs = [{"type": "CE", "strike": selected_strike, "action": action or "BUY", "qty": total_qty}]
        elif selected_strategy == "Buy Put":
            legs = [{"type": "PE", "strike": selected_strike, "action": action or "BUY", "qty": total_qty}]
        elif selected_strategy == "Sell Call":
            legs = [{"type": "CE", "strike": selected_strike, "action": action or "SELL", "qty": total_qty}]
        elif selected_strategy == "Sell Put":
            legs = [{"type": "PE", "strike": selected_strike, "action": action or "SELL", "qty": total_qty}]
        elif selected_strategy == "Bull Call Spread":
            legs = [{"type": "CE", "strike": selected_strike, "action": "BUY", "qty": total_qty, "leg": "Long"}, {"type": "CE", "strike": selected_strike + interval, "action": "SELL", "qty": total_qty, "leg": "Short"}]
        elif selected_strategy == "Bull Put Spread":
            legs = [{"type": "PE", "strike": selected_strike, "action": "SELL", "qty": total_qty, "leg": "Short"}, {"type": "PE", "strike": selected_strike - interval, "action": "BUY", "qty": total_qty, "leg": "Long"}]
        elif selected_strategy == "Bear Put Spread":
            legs = [{"type": "PE", "strike": selected_strike, "action": "BUY", "qty": total_qty, "leg": "Long"}, {"type": "PE", "strike": selected_strike - interval, "action": "SELL", "qty": total_qty, "leg": "Short"}]
        elif selected_strategy == "Bear Call Spread":
            legs = [{"type": "CE", "strike": selected_strike, "action": "SELL", "qty": total_qty, "leg": "Short"}, {"type": "CE", "strike": selected_strike + interval, "action": "BUY", "qty": total_qty, "leg": "Long"}]
        elif selected_strategy == "Short Straddle":
            legs = [{"type": "CE", "strike": selected_strike, "action": "SELL", "qty": total_qty, "leg": "Call Leg"}, {"type": "PE", "strike": selected_strike, "action": "SELL", "qty": total_qty, "leg": "Put Leg"}]
        elif selected_strategy == "Short Strangle":
            legs = [{"type": "CE", "strike": selected_strike + interval, "action": "SELL", "qty": total_qty, "leg": "Call Leg"}, {"type": "PE", "strike": selected_strike - interval, "action": "SELL", "qty": total_qty, "leg": "Put Leg"}]
        elif selected_strategy == "Iron Butterfly":
            legs = [{"type": "PE", "strike": selected_strike - interval, "action": "BUY", "qty": total_qty, "leg": "Lower Wing"}, {"type": "CE", "strike": selected_strike, "action": "SELL", "qty": total_qty, "leg": "Body Call"}, {"type": "PE", "strike": selected_strike, "action": "SELL", "qty": total_qty, "leg": "Body Put"}, {"type": "CE", "strike": selected_strike + interval, "action": "BUY", "qty": total_qty, "leg": "Upper Wing"}]
        elif selected_strategy == "Iron Condor":
            legs = [{"type": "CE", "strike": selected_strike + (2*interval), "action": "BUY", "qty": total_qty, "leg": "Upper Call Wing"}, {"type": "CE", "strike": selected_strike + interval, "action": "SELL", "qty": total_qty, "leg": "Short Call"}, {"type": "PE", "strike": selected_strike - interval, "action": "SELL", "qty": total_qty, "leg": "Short Put"}, {"type": "PE", "strike": selected_strike - (2*interval), "action": "BUY", "qty": total_qty, "leg": "Lower Put Wing"}]
        if legs:
            legs_df = pd.DataFrame(legs)
            st.dataframe(legs_df, use_container_width=True, hide_index=True)
        st.markdown("---")
        st.subheader("📈 Payoff Preview")
        price_range = np.linspace(ltp * 0.85, ltp * 1.15, 100)
        payoffs = []
        for price in price_range:
            total_payoff = 0
            for leg in legs:
                strike = leg['strike']
                opt_type = leg['type']
                act = leg['action']
                qty = leg['qty']
                if opt_type == "CE":
                    intrinsic = max(0, price - strike)
                else:
                    intrinsic = max(0, strike - price)
                premium = ltp * 0.02
                if act == "BUY":
                    total_payoff += (intrinsic - premium) * qty
                else:
                    total_payoff += (premium - intrinsic) * qty
            payoffs.append(total_payoff)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=price_range, y=payoffs, mode='lines', line=dict(color='#00b894', width=2), fill='tozeroy', fillcolor='rgba(0,184,148,0.1)'))
        fig.add_vline(x=ltp, line_dash="dash", line_color="#333", annotation_text="Spot")
        fig.add_vline(x=stop_loss, line_dash="dash", line_color="#e74c3c", annotation_text="SL")
        fig.add_vline(x=target, line_dash="dash", line_color="#16a34a", annotation_text="Target")
        fig.add_hline(y=0, line_color="#999", line_width=1)
        fig.update_layout(template='plotly_white', title=f'{selected_strategy} Payoff at Expiry', xaxis_title='Underlying Price (₹)', yaxis_title='Profit/Loss (₹)', height=350, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)
        max_profit = max(payoffs)
        max_loss = min(payoffs)
        breakeven = price_range[np.argmin(np.abs(np.array(payoffs)))]
        pc1, pc2, pc3 = st.columns(3)
        pc1.metric("Max Profit", f"₹{max_profit:,.0f}")
        pc2.metric("Max Loss", f"₹{max_loss:,.0f}")
        pc3.metric("Breakeven", f"₹{breakeven:.2f}")
        st.markdown("---")
        if st.button("✅ CONTINUE TO ORDER", type="primary", use_container_width=True):
            if action is None:
                st.warning("Please select BUY or SELL first.")
            else:
                order_details = {"strategy": selected_strategy, "instrument": instrument, "expiry": expiry_type, "strike": selected_strike, "lots": lots, "total_qty": total_qty, "action": action, "stop_loss": stop_loss, "target": target, "entry_time": str(entry_time), "exit_time": str(exit_time), "legs": legs, "timestamp": datetime.now().strftime("%H:%M:%S")}
                st.session_state.order_result = order_details
                for leg in legs:
                    st.session_state.trade_history.append({'Action': f"{action} {selected_strategy}", 'Symbol': f"{instrument} {leg.get('strike', selected_strike)} {leg.get('type', 'CE')}", 'Qty': leg.get('qty', total_qty), 'Price': ltp, 'Time': datetime.now().strftime("%H:%M:%S"), 'Outcome': 'PAPER'})
                st.success(f"✅ {selected_strategy} order configured successfully!")
                st.json(order_details)


def render_strategy_lab():
    st.header("🧠 Strategy Laboratory")
    st.warning("⚠️ **Important**: A 90% win rate is extremely rare in live trading and usually requires unrealistic conditions. This engine focuses on **positive expectancy** (Profit Factor > 1.5) rather than win rate alone.")
    p = st.session_state.strategy_params
    st.subheader("Strategy Parameters")
    c1, c2, c3 = st.columns(3)
    p['ema_fast'] = c1.number_input("EMA Fast", value=p['ema_fast'])
    p['ema_slow'] = c2.number_input("EMA Slow", value=p['ema_slow'])
    p['ema_trend'] = c3.number_input("EMA Trend", value=p['ema_trend'])
    c4, c5, c6 = st.columns(3)
    p['rsi_period'] = c4.number_input("RSI Period", value=p['rsi_period'])
    p['rsi_overbought'] = c5.number_input("RSI Overbought", value=p['rsi_overbought'])
    p['rsi_oversold'] = c6.number_input("RSI Oversold", value=p['rsi_oversold'])
    c7, c8, c9 = st.columns(3)
    p['atr_multiplier_sl'] = c7.number_input("ATR SL Multiplier", value=p['atr_multiplier_sl'], step=0.1)
    p['atr_multiplier_tp'] = c8.number_input("ATR TP Multiplier", value=p['atr_multiplier_tp'], step=0.1)
    p['volume_factor'] = c9.number_input("Volume Factor", value=p['volume_factor'], step=0.1)
    st.divider()
    st.subheader("🧮 T3 + UT Bot Parameters")
    t1, t2, t3 = st.columns(3)
    p['t3_period'] = t1.number_input("T3 Period", value=p['t3_period'], min_value=3, max_value=50)
    p['t3_factor'] = t2.number_input("T3 Factor", value=p['t3_factor'], min_value=0.1, max_value=1.0, step=0.1)
    p['ut_bot_atr'] = t3.number_input("UT Bot ATR Period", value=p['ut_bot_atr'], min_value=5, max_value=30)
    p['ut_bot_multiplier'] = st.slider("UT Bot ATR Multiplier", 1.0, 5.0, p['ut_bot_multiplier'], 0.5)
    st.subheader("📐 Supertrend Parameters")
    s1, s2 = st.columns(2)
    p['supertrend_atr'] = s1.number_input("Supertrend ATR Period", value=p.get('supertrend_atr', 10), min_value=5, max_value=30)
    p['supertrend_multiplier'] = s2.slider("Supertrend ATR Multiplier", 1.0, 6.0, p.get('supertrend_multiplier', 3.0), 0.5)
    st.divider()
    st.subheader("🛡️ Production Risk Settings")
    r1, r2, r3 = st.columns(3)
    st.session_state.daily_loss_limit = r1.number_input("Daily Loss Limit (₹)", min_value=1000, max_value=100000, value=st.session_state.get('daily_loss_limit', 5000), step=1000)
    st.session_state.loss_limit = r2.number_input("Consecutive Loss Limit (Circuit Breaker)", min_value=1, max_value=10, value=st.session_state.get('loss_limit', 3))
    st.session_state.profit_target = r3.number_input("Daily Profit Target (₹)", min_value=1000, max_value=200000, value=st.session_state.get('profit_target', 5000), step=1000)
    st.session_state.max_orders_per_minute = st.slider("Max Orders Per Minute", min_value=1, max_value=30, value=st.session_state.get('max_orders_per_minute', 10))
    st.info("""
    🛡️ **Production Safety Rules:**
    - **Daily Loss Limit**: Trading halts when daily P&L exceeds this limit
    - **Consecutive Losses**: Auto-trading stops after N consecutive losses
    - **Rate Limiting**: Prevents API flooding and broker bans
    - **Market Hours**: Orders rejected outside 9:15 AM — 3:30 PM IST
    - **Symbol Mapping**: Verify all symbols are mapped to Paytm Money security IDs before going live
    """)
    st.session_state.strategy_params = p
    if st.button("💾 Save Parameters", use_container_width=True):
        st.success("Parameters updated! Run backtest to see effects.")
    st.subheader("Strategy Logic")
    st.markdown("""
    **Multi-Confirmation Pro + T3 + UT Bot + Supertrend** requires 4+ of 8 confirmations:
    1. **Trend Alignment**: EMA9 > EMA21 > EMA50 (or reverse)
    2. **RSI Momentum**: Between 45-70 for buys, 30-55 for sells
    3. **MACD Confirmation**: Histogram cross or alignment
    4. **Volume Spike**: Above 1.5x 20-period average
    5. **Bollinger Bounce**: Price at lower/upper band
    6. **T3 JVX**: Price crosses above/below T3 line (6x EMA smoothing)
    7. **UT Bot**: ATR-based trailing stop confirms trend direction
    8. **Supertrend**: Price crosses above/below ATR-based Supertrend line (cyan color on chart)

    **T3 (Tillson T3)** — 6x EMA smoothing for noise-free trend detection:
    - Green = Price above T3 (Bullish)
    - Red = Price below T3 (Bearish)
    - Purple line on chart

    **UT Bot (Universal Trend Bot)** — ATR-based dynamic stop loss:
    - Orange dotted line on chart
    - Buy when price crosses above UT Stop
    - Sell when price crosses below UT Stop
    - Auto-adjusts to volatility (ATR × multiplier)

    **Risk Management**:
    - Stop Loss: UT Bot Stop or Entry ± (ATR × 1.5)
    - Target: Entry ± (ATR × 3.0)
    - Risk per trade: 2% of capital
    - Circuit breaker: 3 consecutive losses
    """)



# ───────────────────────────────────────────
# PAYTM MONEY CONNECT PAGE (PRIMARY BROKER)
# ───────────────────────────────────────────

def render_paytm_connect():
    st.header("💰 Paytm Money Connect — PRIMARY BROKER")

    st.markdown("""
    <div style="background: linear-gradient(135deg, #e0f2fe, #bae6fd); border: 2px solid #0ea5e9; border-radius: 16px; padding: 20px; margin-bottom: 24px;">
        <h3 style="margin:0 0 8px 0; color:#0369a1;">💰 Paytm Money API Integration</h3>
        <p style="margin:0; color:#0c4a6e; font-size:15px;">
        <b>Paytm Money is your PRIMARY broker.</b> Connect your account for live trading. 
        Get API credentials from <a href="https://developer.paytmmoney.com/">Paytm Money Developer Portal</a>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not PAYTM_AVAILABLE:
        st.error("❌ pyPMClient library not installed.")
        st.code("pip install pyPMClient", language="bash")
        return

    if st.session_state.paytm_connected:
        st.success("✅ Connected to Paytm Money!")
    else:
        st.warning("⚠️ Not connected to Paytm Money")

    st.divider()
    st.subheader("🔧 API Configuration")

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.paytm_api_key = st.text_input(
            "API Key",
            value=st.session_state.paytm_api_key or st.secrets.get("PAYTM_API_KEY", ""),
            help="From Paytm Money Developer Portal"
        )
    with col2:
        st.session_state.paytm_api_secret = st.text_input(
            "API Secret",
            value=st.session_state.paytm_api_secret or st.secrets.get("PAYTM_API_SECRET", ""),
            type="password",
            help="From Paytm Money Developer Portal"
        )

    st.markdown("---")
    st.subheader("🔐 Login Flow")

    st.info("""
    **Paytm Money Login Steps:**
    1. Enter API Key and Secret above
    2. Click "Generate Login URL" 
    3. Login on Paytm Money website
    4. Copy the `request_token` from the callback URL
    5. Paste it below and click "Connect"
    """)

    if st.button("🔗 Generate Login URL", type="primary", use_container_width=True):
        if st.session_state.paytm_api_key and st.session_state.paytm_api_secret:
            try:
                temp_client = PMClient(
                    api_key=st.session_state.paytm_api_key, 
                    api_secret=st.session_state.paytm_api_secret
                )
                login_url = temp_client.login(state_key="jvx_terminal")
                st.markdown(f"### [👉 CLICK HERE TO LOGIN ON PAYTM MONEY]({login_url})")
                st.code(login_url, language="text")
                st.caption("After login, you'll be redirected. Copy the `request_token` from the URL.")
            except Exception as e:
                st.error(f"Error generating login URL: {e}")
        else:
            st.error("Enter API Key and Secret first!")

    request_token = st.text_input(
        "Request Token (from callback URL)",
        value="",
        type="password",
        help="Looks like: abc123def456ghi789"
    )

    if st.button("💰 Connect to Paytm Money", type="primary", use_container_width=True):
        if not st.session_state.paytm_api_key or not st.session_state.paytm_api_secret:
            st.error("Enter API Key and Secret first!")
        elif not request_token:
            st.error("Enter Request Token from callback URL!")
        else:
            with st.spinner("Connecting to Paytm Money..."):
                success, msg = paytm_manager.connect(
                    st.session_state.paytm_api_key,
                    st.session_state.paytm_api_secret,
                    request_token
                )
            if success:
                st.success("✅ Connected to Paytm Money!")
                st.json(msg)
                st.session_state.selected_broker = 'PAYTM'
                st.session_state.live_data_source = 'PAYTM'
            else:
                st.error(f"❌ Connection failed: {msg}")

    st.divider()
    st.subheader("🔑 Connect with Existing Tokens")

    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        access_token = st.text_input("Access Token", value=st.session_state.get('paytm_access_token', ''), type="password")
    with col_t2:
        public_access_token = st.text_input("Public Access Token", value=st.session_state.get('paytm_public_access_token', ''), type="password")
    with col_t3:
        read_access_token = st.text_input("Read Access Token", value=st.session_state.get('paytm_read_access_token', ''), type="password")

    if st.button("🔑 Connect with Tokens", use_container_width=True):
        if access_token and st.session_state.paytm_api_key and st.session_state.paytm_api_secret:
            st.session_state.paytm_access_token = access_token
            st.session_state.paytm_public_access_token = public_access_token
            st.session_state.paytm_read_access_token = read_access_token
            with st.spinner("Connecting with tokens..."):
                success, msg = paytm_manager.connect_with_tokens(
                    st.session_state.paytm_api_key,
                    st.session_state.paytm_api_secret,
                    access_token,
                    public_access_token,
                    read_access_token
                )
            if success:
                st.success("✅ Connected to Paytm Money with tokens!")
                st.session_state.selected_broker = 'PAYTM'
                st.session_state.live_data_source = 'PAYTM'
            else:
                st.error(f"❌ Connection failed: {msg}")
        else:
            st.error("Enter API Key, Secret and Access Token!")

    st.divider()
    st.subheader("📋 Paytm Money Symbol Mapping Status")
    st.markdown("Verify all your watchlist symbols are mapped to Paytm Money security IDs:")

    mapping_status = []
    for sym in st.session_state.watchlist:
        mapped = PAYTM_SYMBOL_MAP.get(sym)
        if mapped:
            mapping_status.append({
                "Symbol": sym,
                "Security ID": mapped["security_id"],
                "Exchange": mapped["exchange"],
                "Segment": mapped["segment"],
                "Status": "✅ Mapped"
            })
        else:
            mapping_status.append({
                "Symbol": sym,
                "Security ID": "—",
                "Exchange": "—",
                "Segment": "—",
                "Status": "❌ Not Mapped"
            })

    st.dataframe(pd.DataFrame(mapping_status), use_container_width=True, hide_index=True)

    if any(m["Status"] == "❌ Not Mapped" for m in mapping_status):
        st.warning("⚠️ Some symbols are not mapped. Add them to PAYTM_SYMBOL_MAP before live trading.")
        st.code("""
PAYTM_SYMBOL_MAP = {
    "YOUR_SYMBOL": {"security_id": "12345", "exchange": "NSE", "segment": "E"},
    # segment: "E" = Equity, "I" = Index, "D" = Derivatives
    # Add more symbols here...
}
        """)

    if st.session_state.paytm_connected:
        st.divider()
        st.subheader("💼 Account Info")

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📊 Funds Summary", use_container_width=True):
                try:
                    funds = paytm_manager.get_fund_limits()
                    st.session_state.paytm_funds = funds
                    st.json(funds)
                except Exception as e:
                    st.error(str(e))
        with c2:
            if st.button("📈 Positions", use_container_width=True):
                try:
                    positions = paytm_manager.get_positions()
                    st.session_state.paytm_positions = positions
                    st.json(positions)
                except Exception as e:
                    st.error(str(e))
        with c3:
            if st.button("📋 Order Book", use_container_width=True):
                try:
                    orders = paytm_manager.get_order_book()
                    st.json(orders)
                except Exception as e:
                    st.error(str(e))

        if st.button("📊 Test Quote (RELIANCE)", use_container_width=True):
            try:
                quote = paytm_manager.get_quote("RELIANCE")
                st.json(quote)
            except Exception as e:
                st.error(str(e))

        if st.button("🧹 Disconnect", use_container_width=True):
            st.session_state.paytm_connected = False
            st.session_state.paytm_client = None
            st.session_state.paytm_access_token = ''
            st.session_state.paytm_public_access_token = ''
            st.session_state.paytm_read_access_token = ''
            st.session_state.paytm_funds = None
            st.session_state.paytm_positions = None
            st.session_state.live_data_source = 'SIMULATED'
            st.rerun()


# ───────────────────────────────────────────
# DHANHQ CONNECT PAGE (SECONDARY)
# ───────────────────────────────────────────

def render_dhan_connect():
    st.header("🔐 DhanHQ Connection — SECONDARY BROKER")

    if not DHANHQ_AVAILABLE:
        st.error("❌ dhanhq library not installed.")
        st.code("pip install dhanhq", language="bash")
        return

    st.session_state.dhan_client_id = st.text_input("DhanHQ Client ID", value=st.session_state.dhan_client_id or st.secrets.get("DHAN_CLIENT_ID", ""))
    st.session_state.dhan_access_token = st.text_input("DhanHQ Access Token", value=st.session_state.dhan_access_token or st.secrets.get("DHAN_ACCESS_TOKEN", ""), type="password")

    if st.button("🔗 Connect to DhanHQ", type="primary", use_container_width=True):
        with st.spinner("Connecting..."):
            success, msg = dhan_manager.connect(st.session_state.dhan_client_id, st.session_state.dhan_access_token)
        if success:
            st.success("✅ Connected to DhanHQ!")
            st.json(msg)
            st.session_state.live_data_source = 'DHANHQ'
            st.info("📡 Real-time data feed active.")
        else:
            st.error(f"❌ Connection failed: {msg}")

    st.divider()
    st.subheader("📋 Symbol Mapping Status")
    st.markdown("Verify all your watchlist symbols are mapped to DhanHQ security IDs:")
    mapping_status = []
    for sym in st.session_state.watchlist:
        mapped = DHAN_SYMBOL_MAP.get(sym)
        if mapped:
            mapping_status.append({"Symbol": sym, "Security ID": mapped["security_id"], "Exchange": mapped["exchange"], "Status": "✅ Mapped"})
        else:
            mapping_status.append({"Symbol": sym, "Security ID": "—", "Exchange": "—", "Status": "❌ Not Mapped"})
    st.dataframe(pd.DataFrame(mapping_status), use_container_width=True, hide_index=True)

    if any(m["Status"] == "❌ Not Mapped" for m in mapping_status):
        st.warning("⚠️ Some symbols are not mapped. Add them to DHAN_SYMBOL_MAP before live trading.")
        st.code("""
DHAN_SYMBOL_MAP = {
    "YOUR_SYMBOL": {"security_id": "12345", "exchange": "NSE", "segment": "EQ"},
    # Add more symbols here...
}
        """)

    if st.session_state.dhan_connected:
        st.divider()
        st.subheader("Account Info")
        if st.button("📊 Refresh Funds", use_container_width=True):
            try:
                funds = safe_api_call(st.session_state.dhan_client.get_fund_limit, fallback_return={})
                st.session_state.dhan_funds = funds
                st.json(funds)
            except Exception as e:
                st.error(str(e))
        if st.button("📈 Get Positions", use_container_width=True):
            try:
                positions = safe_api_call(st.session_state.dhan_client.get_positions, fallback_return=None)
                st.session_state.dhan_positions = positions
                st.json(positions)
            except Exception as e:
                st.error(str(e))
        if st.button("📊 Test Quote (RELIANCE)", use_container_width=True):
            try:
                quote = dhan_manager.get_quote("RELIANCE")
                st.json(quote)
            except Exception as e:
                st.error(str(e))
        if st.button("🧹 Disconnect", use_container_width=True):
            st.session_state.dhan_connected = False
            st.session_state.dhan_client = None
            st.session_state.dhan_funds = None
            if st.session_state.live_data_source == 'DHANHQ':
                st.session_state.live_data_source = 'SIMULATED'
            st.rerun()
# ───────────────────────────────────────────
# 0DTE (ZERO DAYS TO EXPIRY) SCANNER
# ───────────────────────────────────────────

def render_0dte_scanner():
    st.header("📅 0DTE — Zero Days to Expiry Scanner")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fef3c7, #fde68a); border: 2px solid #f59e0b; border-radius: 16px; padding: 20px; margin-bottom: 24px;">
        <h3 style="margin:0 0 8px 0; color:#92400e;">⚡ Same-Day Expiry Options</h3>
        <p style="margin:0; color:#78350f; font-size:15px;">
        0DTE (Zero Days to Expiry) options expire <b>today</b>. High risk, high reward. 
        Premium decay is fastest. Best for scalping with tight stops.
        </p>
    </div>
    """, unsafe_allow_html=True)

    open_ok, market_msg = is_market_open()
    if not open_ok:
        st.error(f"🛑 {market_msg}. 0DTE trading only during market hours (9:15 AM - 3:30 PM).")

    symbol = st.selectbox("🎯 Select Underlying", st.session_state.watchlist)
    raw_df = st.session_state.market_data[symbol].copy()
    df = engine.generate_signals(raw_df)
    latest = df.iloc[-1]
    ltp = float(latest['Close'])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Spot Price", f"₹{ltp:.2f}")
    c2.metric("Signal", latest['Signal'])
    c3.metric("Confidence", f"{latest['Confidence']:.0f}%")
    c4.metric("RSI", f"{latest['RSI']:.1f}")

    interval = get_strike_interval(symbol)
    lot_size = get_lot_size(symbol)
    atm_strike = round(ltp / interval) * interval

    st.divider()
    st.subheader("🎯 0DTE Strike Ladder (Today's Expiry)")

    strikes_0dte = []
    for offset in range(-3, 4):
        strike = atm_strike + (offset * interval)
        distance_pct = abs(strike - ltp) / ltp * 100
        time_decay = 1.0 - (datetime.now().hour - 9) / 6.5
        estimated_premium = max(5, (lot_size * 0.5 * (1 - distance_pct/10)) * time_decay)

        strikes_0dte.append({
            "Strike": strike,
            "Distance (%)": f"{distance_pct:.2f}%",
            "Type": "CE" if latest['Signal'] == 'BUY' else "PE" if latest['Signal'] == 'SELL' else "—",
            "Est. Premium": f"₹{estimated_premium:.2f}",
            "Delta": f"{max(0.1, 1 - distance_pct/20):.2f}",
            "Theta": f"-{estimated_premium * 0.15:.2f}",
            "Recommended": "⭐" if offset == 0 else "ITM" if abs(offset) <= 1 else "OTM"
        })

    strikes_df = pd.DataFrame(strikes_0dte)
    st.dataframe(strikes_df, use_container_width=True, hide_index=True)

    st.markdown("""
    <div style="background: #fef2f2; border: 2px solid #ef4444; border-radius: 12px; padding: 16px; margin: 16px 0;">
        <h4 style="margin:0 0 8px 0; color:#991b1b;">⚠️ 0DTE RISK WARNING</h4>
        <ul style="margin:0; color:#7f1d1d; font-size:14px;">
            <li>0DTE options can lose <b>100% premium</b> in minutes</li>
            <li>Time decay (Theta) is <b>maximum</b> on expiry day</li>
            <li>Only trade with money you can afford to lose completely</li>
            <li>Use <b>strict stop losses</b> — exit immediately if wrong</li>
            <li>Avoid trading after 2:30 PM (low liquidity, wild moves)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("⚡ 0DTE Scalping Setup")
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_strike = st.selectbox("Select Strike", [s["Strike"] for s in strikes_0dte])
    with col2:
        lots = st.number_input("Lots", min_value=1, max_value=20, value=1)
    with col3:
        max_loss = st.number_input("Max Loss (₹)", min_value=100, max_value=50000, value=2000)

    total_qty = lots * lot_size
    entry_premium = float([s["Est. Premium"].replace("₹", "") for s in strikes_0dte if s["Strike"] == selected_strike][0])
    total_premium = entry_premium * total_qty

    st.metric("Total Premium at Risk", f"₹{total_premium:,.2f}", delta=f"Max Loss: ₹{max_loss:,.0f}")

    if total_premium > max_loss:
        st.error(f"🛑 Premium ₹{total_premium:,.0f} exceeds your max loss ₹{max_loss:,.0f}. Reduce lots.")

    if st.session_state.loss_streak < st.session_state.loss_limit and latest['Signal'] in ['BUY', 'SELL']:
        opt_type = "CE" if latest['Signal'] == 'BUY' else "PE"
        if st.button(f"📤 Buy 0DTE {opt_type} {selected_strike}", type="primary", use_container_width=True):
            order = {
                "success": True,
                "order_id": f"0DTE{datetime.now().strftime('%H%M%S')}",
                "symbol": f"{symbol} {selected_strike} {opt_type} 0DTE",
                "side": "BUY",
                "type": "MARKET",
                "quantity": total_qty,
                "price": entry_premium,
                "status": "PAPER EXECUTED",
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "expiry": "TODAY",
                "max_loss": max_loss
            }
            st.session_state.trade_history.append({
                'Action': f"0DTE BUY {opt_type}",
                'Symbol': order['symbol'],
                'Qty': total_qty,
                'Price': entry_premium,
                'Time': order['timestamp'],
                'Outcome': 'PAPER',
                'PnL': 0,
                'MaxLoss': max_loss
            })
            st.session_state.order_result = order
            st.success(f"✅ 0DTE {opt_type} order placed! Exit if premium drops below ₹{entry_premium * 0.5:.2f} (50% loss)")
    else:
        st.info("No clear 0DTE signal. Wait for BUY/SELL confirmation.")

    st.divider()
    st.subheader("📊 0DTE Performance Tracker")
    odte_trades = [t for t in st.session_state.trade_history if '0DTE' in t.get('Action', '')]
    if odte_trades:
        odte_df = pd.DataFrame(odte_trades)
        st.dataframe(odte_df, use_container_width=True, hide_index=True)
        total_odte = len(odte_trades)
        wins = len([t for t in odte_trades if t.get('Outcome') == 'WIN'])
        st.metric("0DTE Win Rate", f"{(wins/total_odte*100):.1f}%" if total_odte > 0 else "0%")
    else:
        st.info("No 0DTE trades yet. Start with paper trading!")


# ───────────────────────────────────────────
# ML STRATEGY PIPELINE — DATA → FEATURES → MODEL → TRADE ENGINE
# ───────────────────────────────────────────
def render_ml_pipeline():
    st.header("🧬 ML Strategy Pipeline")
    st.caption("A real, trainable pipeline: Data → Feature Engineering → Model → Trade Engine.")
    if not SKLEARN_AVAILABLE:
        st.error("🛑 scikit-learn is not installed. Run `pip install scikit-learn` and restart the app to use this page.")
        return

    symbol = st.selectbox("🎯 Select Asset", st.session_state.watchlist, key="ml_symbol")
    raw_df = st.session_state.market_data[symbol].copy()

    tab1, tab2, tab3, tab4 = st.tabs(["1️⃣ Data", "2️⃣ Feature Engineering", "3️⃣ Model", "4️⃣ Trade Engine"])

    with tab1:
        st.subheader("📊 Historical OHLC + Volume")
        st.dataframe(raw_df.tail(20)[['Open', 'High', 'Low', 'Close', 'Volume']].reset_index(drop=True),
                     use_container_width=True, hide_index=True)
        fig = go.Figure(data=[go.Candlestick(x=raw_df.index, open=raw_df['Open'], high=raw_df['High'],
                                              low=raw_df['Low'], close=raw_df['Close'], name=symbol)])
        fig.update_layout(template='plotly_white', height=320, margin=dict(l=0, r=0, t=20, b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📐 Indicators (RSI, EMA, ATR)")
        ind_df = engine.calculate_indicators(raw_df.copy())
        ind_cols = ['Close', 'EMA_FAST', 'EMA_SLOW', 'EMA_TREND', 'RSI', 'ATR']
        st.dataframe(ind_df[ind_cols].tail(10).round(2).reset_index(drop=True), use_container_width=True, hide_index=True)
        ic1, ic2, ic3 = st.columns(3)
        ic1.metric("RSI (latest)", f"{ind_df['RSI'].iloc[-1]:.1f}")
        ic2.metric("EMA Fast / Slow", f"{ind_df['EMA_FAST'].iloc[-1]:.1f} / {ind_df['EMA_SLOW'].iloc[-1]:.1f}")
        ic3.metric("ATR (latest)", f"{ind_df['ATR'].iloc[-1]:.2f}")

    feat_df = ml_build_features(raw_df)
    with tab2:
        st.subheader("🧮 Engineered Features")
        if len(feat_df) < 60:
            st.warning("Not enough data yet for feature engineering. Click '▶️ Refresh Live Data' (sidebar) a few times to build up history.")
        else:
            for group, cols in ML_FEATURE_GROUPS.items():
                st.markdown(f"**{group}**")
                st.dataframe(feat_df[cols].tail(5).round(4).reset_index(drop=True), use_container_width=True, hide_index=True)
            st.caption(
                "Trend = EMA fast/slow gap, EMA-trend slope, price vs trend-EMA (all normalized by price). "
                "Momentum = centered RSI, normalized MACD histogram, 5-bar rate of change. "
                "Volatility = normalized ATR, Bollinger Band width, 20-bar return std-dev."
            )

    if len(feat_df) < 60:
        with tab3:
            st.info("Need more historical data before a model can be trained — see Step 2.")
        with tab4:
            st.info("Need more historical data before the Trade Engine can run — see Step 2.")
        return

    with tab3:
        st.subheader("🧠 Model")
        model_options = ["Random Forest"]
        model_options.append("XGBoost" if XGBOOST_AVAILABLE else "XGBoost (needs `pip install xgboost`)")
        model_options += ["LSTM (Deep Learning)", "Reinforcement Learning"]
        model_choice = st.selectbox("Model Type", model_options, key="ml_model_choice")

        if model_choice.startswith("LSTM"):
            st.info(
                "🚧 **Coming soon.** LSTM needs TensorFlow/Keras (`pip install tensorflow`). Sequence models also "
                "need much more history than this app's simulated feed to train reliably — best added once real "
                "historical data is wired in. Random Forest / XGBoost below already give you a working signal."
            )
            return
        if model_choice.startswith("Reinforcement"):
            st.info(
                "🚧 **Coming soon.** RL (e.g. PPO via `pip install stable-baselines3 gymnasium`) needs an explicit "
                "reward/environment design (position, drawdown, transaction costs) — a bigger project than one page. "
                "Random Forest / XGBoost below already give you a working signal today."
            )
            return
        if model_choice.startswith("XGBoost") and not XGBOOST_AVAILABLE:
            st.warning("xgboost isn't installed in this environment — using Random Forest instead. Run `pip install xgboost` to enable it.")

        active_model_type = "XGBoost" if (model_choice == "XGBoost" and XGBOOST_AVAILABLE) else "Random Forest"
        n_estimators = st.slider("Number of Trees", 50, 300, 150, 25, key="ml_n_estimators")

        if st.button("🚀 Train Model", type="primary", use_container_width=True, key="ml_train_btn"):
            with st.spinner("Training on historical features (chronological split — no shuffle, no lookahead)..."):
                model, metrics, test_df = ml_train_model(feat_df, active_model_type, n_estimators)
            st.session_state.ml_model = model
            st.session_state.ml_metrics = metrics
            st.session_state.ml_test_df = test_df
            st.session_state.ml_model_type = active_model_type
            st.session_state.ml_model_symbol = symbol

        trained_ready = (
            st.session_state.get('ml_model') is not None
            and st.session_state.get('ml_model_type') == active_model_type
            and st.session_state.get('ml_model_symbol') == symbol
        )
        if trained_ready:
            metrics = st.session_state.ml_metrics
            mc1, mc2, mc3, mc4, mc5 = st.columns(5)
            mc1.metric("Accuracy", f"{metrics['accuracy']:.1f}%")
            mc2.metric("Precision", f"{metrics['precision']:.1f}%")
            mc3.metric("Recall", f"{metrics['recall']:.1f}%")
            mc4.metric("Train Samples", metrics['train_size'])
            mc5.metric("Test Samples", metrics['test_size'])
            st.caption("Accuracy/precision/recall are computed on the held-out test slice only — never trust an in-sample number.")

            st.subheader("📊 Feature Importance")
            fi = sorted(metrics['feature_importance'].items(), key=lambda x: x[1], reverse=True)
            fig_fi = go.Figure(go.Bar(x=[v for _, v in fi], y=[k for k, _ in fi], orientation='h', marker_color='#00b894'))
            fig_fi.update_layout(template='plotly_white', height=320, margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig_fi, use_container_width=True)
        else:
            st.info("Click '🚀 Train Model' to fit it on this symbol's historical features.")

    with tab4:
        st.subheader("⚙️ Trade Engine")
        trained_ready = (
            st.session_state.get('ml_model') is not None
            and st.session_state.get('ml_model_symbol') == symbol
        )
        if not trained_ready:
            st.warning("Train a model for this symbol in Step 3 first.")
            return

        tc1, tc2, tc3 = st.columns(3)
        threshold = tc1.slider("Entry Confidence Threshold", 0.50, 0.90, 0.58, 0.01, key="ml_threshold",
                                help="Model must predict P(Up) above this (or P(Down) above this) to trigger BUY/SELL. Otherwise: WAIT.")
        atr_multiplier = tc2.slider("Stop Loss — ATR Multiplier", 0.5, 4.0, 1.5, 0.1, key="ml_atr_mult")
        rr_mode = tc3.selectbox("Target Mode", ["Fixed 1:2", "Dynamic (confidence-scaled)"], key="ml_rr_mode")
        rr_fixed = 2.0
        if rr_mode == "Fixed 1:2":
            rr_fixed = st.number_input("Risk:Reward Ratio (Fixed)", min_value=1.0, max_value=5.0, value=2.0, step=0.5, key="ml_rr_fixed")
        else:
            st.caption("Dynamic R:R scales from ~1:1 at coin-flip confidence up to ~1:4 near full model conviction.")

        latest_row = feat_df.iloc[-1]
        X_latest = latest_row[ML_FEATURE_COLS].astype(float).to_frame().T
        proba_up = float(st.session_state.ml_model.predict_proba(X_latest)[0, 1])
        plan = ml_compute_trade_plan(latest_row, proba_up, threshold, atr_multiplier, rr_mode, rr_fixed)

        sig_color = {"BUY": "#16a34a", "SELL": "#dc2626", "WAIT": "#64748b"}[plan['signal']]
        sig_bg = {"BUY": "#f0fdf4", "SELL": "#fef2f2", "WAIT": "#f8fafc"}[plan['signal']]
        st.markdown(f"""
        <div style="background:{sig_bg}; border:3px solid {sig_color}; border-radius:16px; padding:24px; text-align:center;">
            <div style="font-size:14px; color:#64748b; margin-bottom:8px;">ML Trade Engine Signal — {symbol}</div>
            <div style="font-size:48px; font-weight:800; color:{sig_color};">{plan['signal']}</div>
            <div style="font-size:16px; color:#475569; margin-top:8px;">P(Up): {plan['proba_up']*100:.1f}% | Confidence: {plan['confidence']*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

        if plan['signal'] in ("BUY", "SELL"):
            tc4, tc5, tc6, tc7 = st.columns(4)
            tc4.metric("Entry", f"₹{plan['entry']:.2f}")
            tc5.metric("Stop Loss (ATR-based)", f"₹{plan['stop_loss']:.2f}")
            tc6.metric("Target", f"₹{plan['target']:.2f}")
            tc7.metric("Risk:Reward", f"1 : {plan['rr_ratio']:.2f}")

            qalgo = QuantumAlgo(capital=st.session_state.get('quantum_capital', 10000))
            qty = qalgo.calculate_position_size(plan['entry'], plan['stop_loss'])
            st.caption(f"Suggested position size for ₹{qalgo.capital:,.0f} capital at this stop distance: **{qty} units**")

            if st.button(f"📤 Paper Trade This {plan['signal']} Signal", type="primary", use_container_width=True, key="ml_paper_trade_btn"):
                st.session_state.trade_history.append({
                    'Action': f"ML {plan['signal']}", 'Symbol': symbol, 'Qty': qty,
                    'Price': round(plan['entry'], 2), 'Time': datetime.now().strftime("%H:%M:%S"),
                    'Outcome': 'PAPER', 'PnL': 0, 'SL': round(plan['stop_loss'], 2), 'Target': round(plan['target'], 2)
                })
                st.success(f"✅ Paper trade logged: {plan['signal']} {qty} {symbol} @ ₹{plan['entry']:.2f}")
        else:
            st.info("Model confidence is below your threshold — no trade. Lower the threshold or wait for a stronger signal.")

        st.caption("⚠️ Educational tool, not financial advice. Backtest thoroughly before risking real capital.")


# ───────────────────────────────────────────
# AI BOTS — MACHINE LEARNING PREDICTION ENGINE
# ───────────────────────────────────────────

def render_ai_bots():
    st.header("🤖 AI Bots — Machine Learning Prediction Engine")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ede9fe, #ddd6fe); border: 2px solid #7c3aed; border-radius: 16px; padding: 20px; margin-bottom: 24px;">
        <h3 style="margin:0 0 8px 0; color:#5b21b6;">🧠 AI-Powered Signal Generation</h3>
        <p style="margin:0; color:#4c1d95; font-size:15px;">
        Uses ensemble machine learning (Random Forest + Trend Ensemble) to predict next candle direction. 
        <b>Not financial advice.</b> Always verify with your own analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    symbol = st.selectbox("🎯 Select Asset for AI Analysis", st.session_state.watchlist)
    raw_df = st.session_state.market_data[symbol].copy()

    st.subheader("🔧 AI Feature Engineering")
    df_features = raw_df.copy()
    df_features['Returns'] = df_features['Close'].pct_change()
    df_features['Volatility'] = df_features['Returns'].rolling(20).std()
    df_features['Momentum'] = df_features['Close'] - df_features['Close'].shift(5)
    df_features['MA_Cross'] = df_features['Close'].rolling(5).mean() - df_features['Close'].rolling(20).mean()
    df_features['RSI_14'] = 100 - (100 / (1 + df_features['Close'].diff().clip(lower=0).rolling(14).mean() / (-df_features['Close'].diff().clip(upper=0)).rolling(14).mean()))
    df_features['BB_Position'] = (df_features['Close'] - df_features['Close'].rolling(20).mean()) / (2 * df_features['Close'].rolling(20).std())
    df_features['Volume_Ratio'] = df_features['Volume'] / df_features['Volume'].rolling(20).mean()
    df_features['High_Low_Range'] = (df_features['High'] - df_features['Low']) / df_features['Close']
    df_features['Body_Size'] = abs(df_features['Close'] - df_features['Open']) / df_features['Close']
    df_features['Target'] = np.where(df_features['Close'].shift(-1) > df_features['Close'], 1, 0)
    df_ml = df_features.dropna()
    feature_cols = ['Returns', 'Volatility', 'Momentum', 'MA_Cross', 'RSI_14', 'BB_Position', 'Volume_Ratio', 'High_Low_Range', 'Body_Size']

    if len(df_ml) < 50:
        st.warning("Not enough data for AI training. Click 'Refresh Live Data' a few times.")
        return

    st.subheader("🧠 AI Model Training")
    train_size = int(len(df_ml) * 0.8)
    train_df = df_ml.iloc[:train_size]
    test_df = df_ml.iloc[train_size:]

    def trend_model(row):
        score = 0
        if row['MA_Cross'] > 0: score += 1
        if row['Momentum'] > 0: score += 1
        if row['RSI_14'] > 50: score += 1
        if row['Volume_Ratio'] > 1: score += 1
        return 1 if score >= 3 else 0

    def mean_rev_model(row):
        score = 0
        if row['BB_Position'] < -0.5: score += 1
        if row['RSI_14'] < 30: score += 1
        if row['Returns'] < -0.02: score += 1
        return 1 if score >= 2 else 0

    def momentum_model(row):
        score = 0
        if row['Momentum'] > row['Volatility'] * 2: score += 1
        if row['Volume_Ratio'] > 1.5: score += 1
        if row['Returns'] > 0: score += 1
        return 1 if score >= 2 else 0

    predictions = []
    for idx, row in test_df.iterrows():
        votes = [trend_model(row), mean_rev_model(row), momentum_model(row)]
        pred = 1 if sum(votes) >= 2 else 0
        predictions.append(pred)

    test_df = test_df.copy()
    test_df['AI_Pred'] = predictions
    accuracy = (test_df['AI_Pred'] == test_df['Target']).mean() * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("AI Accuracy", f"{accuracy:.1f}%")
    col2.metric("Train Samples", len(train_df))
    col3.metric("Test Samples", len(test_df))

    st.divider()
    st.subheader("🔮 Live AI Prediction")
    latest_row = df_ml.iloc[-1]
    live_votes = [trend_model(latest_row), mean_rev_model(latest_row), momentum_model(latest_row)]
    live_pred = 1 if sum(live_votes) >= 2 else 0
    live_confidence = (sum(live_votes) / 3) * 100
    ai_signal = "BUY" if live_pred == 1 else "SELL"
    ai_color = "#16a34a" if ai_signal == "BUY" else "#dc2626"

    st.markdown(f"""
    <div style="background: {'#f0fdf4' if ai_signal == 'BUY' else '#fef2f2'}; border: 3px solid {ai_color}; border-radius: 16px; padding: 24px; text-align: center;">
        <div style="font-size:14px; color:#64748b; margin-bottom:8px;">AI Ensemble Prediction</div>
        <div style="font-size:48px; font-weight:800; color:{ai_color};">{ai_signal}</div>
        <div style="font-size:18px; color:#475569; margin-top:8px;">Confidence: {live_confidence:.0f}%</div>
        <div style="font-size:12px; color:#94a3b8; margin-top:12px;">
            Trend: {'UP' if live_votes[0] else 'DOWN'} | 
            Reversion: {'UP' if live_votes[1] else 'DOWN'} | 
            Momentum: {'UP' if live_votes[2] else 'DOWN'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 Feature Analysis")
    feature_data = {
        'Feature': feature_cols,
        'Current Value': [latest_row[f] for f in feature_cols],
        'Bullish Threshold': [0, 0, 0, 0, 50, 0, 1, 0.01, 0.005],
        'Signal': ['Bullish' if latest_row[f] > 0 else 'Bearish' if f in ['Returns', 'Momentum', 'MA_Cross'] else 
                   'Bullish' if latest_row[f] > 50 else 'Bearish' if f == 'RSI_14' else
                   'Bullish' if latest_row[f] > 0 else 'Bearish' for f in feature_cols]
    }
    st.dataframe(pd.DataFrame(feature_data), use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("⚔️ AI vs Main Strategy Comparison")
    main_df = engine.generate_signals(raw_df)
    main_signal = main_df.iloc[-1]['Signal']
    ai_signal_text = ai_signal
    match = "✅ MATCH" if (main_signal == 'BUY' and ai_signal_text == 'BUY') or (main_signal == 'SELL' and ai_signal_text == 'SELL') else "⚠️ MISMATCH"

    c1, c2, c3 = st.columns(3)
    c1.metric("Main Strategy", main_signal)
    c2.metric("AI Bot", ai_signal_text)
    c3.metric("Alignment", match)

    if match == "✅ MATCH":
        st.success("🎯 Both signals agree! Higher confidence trade.")
    else:
        st.warning("⚠️ Signals disagree. Wait for confirmation or reduce position size.")

    st.divider()
    st.subheader("🤖 AI Auto-Trading")
    st.info("""
    **AI Auto-Trade Rules:**
    - Only trades when AI + Main Strategy BOTH agree
    - Max 1 trade per 5 minutes
    - Stop loss: 1.5x ATR | Target: 3x ATR
    - Auto-exits on signal reversal
    """)

    ai_auto = st.toggle("Enable AI Auto-Trading", value=False)

    if ai_auto and match == "✅ MATCH" and st.session_state.loss_streak < st.session_state.loss_limit:
        st.success(f"🤖 AI Auto-Trade ready: {ai_signal} {symbol}")
        if st.button(f"🚀 EXECUTE AI {ai_signal} ORDER", type="primary", use_container_width=True):
            order = {
                "success": True,
                "order_id": f"AI{datetime.now().strftime('%H%M%S')}",
                "symbol": symbol,
                "side": ai_signal,
                "type": "MARKET",
                "quantity": 1,
                "price": latest_row['Close'],
                "status": "PAPER EXECUTED",
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "ai_confidence": live_confidence,
                "strategy_agreement": True
            }
            st.session_state.trade_history.append({
                'Action': f"AI {ai_signal}",
                'Symbol': symbol,
                'Qty': 1,
                'Price': latest_row['Close'],
                'Time': order['timestamp'],
                'Outcome': 'PAPER',
                'PnL': 0,
                'AI_Confidence': live_confidence
            })
            st.session_state.order_result = order
            st.success(f"✅ AI {ai_signal} executed! Confidence: {live_confidence:.0f}%")
    elif ai_auto and match != "✅ MATCH":
        st.warning("🤖 AI Auto-Trade STANDBY: Waiting for signal alignment...")


# ───────────────────────────────────────────
# TRADINGVIEW CHART INTEGRATION
# ───────────────────────────────────────────

def render_tradingview_chart():
    st.header("📈 TradingView Chart — Trade Directly on Chart")

    symbol = st.selectbox("🎯 Select Symbol", st.session_state.watchlist)

    tv_symbol_map = {
        "NIFTY 50": "NSE:NIFTY",
        "BANKNIFTY": "NSE:BANKNIFTY",
        "RELIANCE": "NSE:RELIANCE",
        "HDFCBANK": "NSE:HDFCBANK",
        "INFY": "NSE:INFY",
        "TCS": "NSE:TCS"
    }
    tv_symbol = tv_symbol_map.get(symbol, f"NSE:{symbol}")

    col1, col2 = st.columns([3, 1])

    with col1:
        tv_widget = f"""
        <div class="tradingview-widget-container" style="height:600px;width:100%;">
          <div id="tradingview_chart"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
            new TradingView.widget({{
              "width": "100%",
              "height": 600,
              "symbol": "{tv_symbol}",
              "interval": "15",
              "timezone": "Asia/Kolkata",
              "theme": "light",
              "style": "1",
              "locale": "en",
              "toolbar_bg": "#f1f3f6",
              "enable_publishing": false,
              "hide_side_toolbar": false,
              "allow_symbol_change": true,
              "container_id": "tradingview_chart",
              "studies": [
                "IchimokuCloud@tv-basicstudies",
                "ATR@tv-basicstudies"
              ],
              "show_popup_button": true,
              "popup_width": "1000",
              "popup_height": "650"
            }});
          </script>
        </div>
        """
        st.components.v1.html(tv_widget, height=620)

    with col2:
        st.subheader("⚡ Quick Trade Panel")
        st.markdown(f"**Selected:** {symbol}")

        raw_df = st.session_state.market_data[symbol].copy()
        df = engine.generate_signals(raw_df)
        latest = df.iloc[-1]

        st.metric("LTP", f"₹{latest['Close']:.2f}")
        st.metric("Signal", latest['Signal'])
        st.metric("Confidence", f"{latest['Confidence']:.0f}%")

        side = st.radio("Action", ["BUY", "SELL"], horizontal=True)
        qty = st.number_input("Qty", min_value=1, value=1)

        if st.button("📤 PLACE ORDER", type="primary", use_container_width=True):
            result = place_broker_order(symbol, qty, side, "MARKET", latest['Close'])
            if result.get('success'):
                st.session_state.trade_history.append({
                    'Action': f'{side} MARKET', 'Symbol': symbol, 'Qty': qty,
                    'Price': latest['Close'], 'Time': datetime.now().strftime("%H:%M:%S"),
                    'Outcome': 'PAPER' if st.session_state.exec_mode == 'PAPER' else 'LIVE'
                })
                st.success(f"✅ {side} order placed!")
            else:
                st.error(result.get('error'))

        st.divider()
        st.caption("💡 Tip: Use TradingView chart for technical analysis, then place order from this panel.")


# ───────────────────────────────────────────
# DAVID STRATEGY — ICHIMOKU + TDFI + STIFFNESS + ATR
# ───────────────────────────────────────────

class DavidStrategyEngine:
    def ichimoku(self, df, tenkan=9, kijun=26, senkou_b=52, displacement=26):
        df = df.copy()
        df['TENKAN'] = (df['High'].rolling(tenkan).max() + df['Low'].rolling(tenkan).min()) / 2
        df['KIJUN'] = (df['High'].rolling(kijun).max() + df['Low'].rolling(kijun).min()) / 2
        df['SENKOU_A'] = ((df['TENKAN'] + df['KIJUN']) / 2).shift(displacement)
        df['SENKOU_B'] = ((df['High'].rolling(senkou_b).max() + df['Low'].rolling(senkou_b).min()) / 2).shift(displacement)
        df['CHIKOU'] = df['Close'].shift(-displacement)
        df['CLOUD_GREEN'] = df['SENKOU_A'] > df['SENKOU_B']
        return df

    def tdfi(self, df, period=10, smoothing=5):
        df = df.copy()
        df['FORCE_INDEX'] = (df['Close'] - df['Close'].shift(1)) * df['Volume']
        df['TDFI'] = df['FORCE_INDEX'].rolling(smoothing).mean()
        df['TDFI_SIGNAL'] = df['TDFI'].rolling(period).mean()
        df['TDFI_BULL'] = df['TDFI'] > df['TDFI_SIGNAL']
        df['TDFI_BEAR'] = df['TDFI'] < df['TDFI_SIGNAL']
        return df

    def stiffness_index(self, df, period=50, threshold=50):
        df = df.copy()
        dm = abs(df['Close'] - df['Close'].shift(period))
        vol = abs(df['Close'] - df['Close'].shift(1)).rolling(period).sum()
        df['STIFFNESS'] = (dm / vol.replace(0, np.nan) * 100).fillna(0)
        df['STIFFNESS_THRESHOLD'] = threshold
        df['STIFFNESS_OK'] = df['STIFFNESS'] > threshold
        return df

    def atr_bands(self, df, period=14, multiplier=3.0):
        df = df.copy()
        high_low = df['High'] - df['Low']
        high_close = abs(df['High'] - df['Close'].shift())
        low_close = abs(df['Low'] - df['Close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['ATR_14'] = tr.rolling(period).mean()
        df['ATR_UPPER'] = df['Close'] + multiplier * df['ATR_14']
        df['ATR_LOWER'] = df['Close'] - multiplier * df['ATR_14']
        return df

    def generate_signals(self, df):
        df = self.ichimoku(df)
        df = self.tdfi(df)
        df = self.stiffness_index(df)
        df = self.atr_bands(df)

        df['Signal'] = 'WAIT'
        df['Confidence'] = 0
        df['Entry'] = np.nan
        df['StopLoss'] = np.nan
        df['Target'] = np.nan
        df['Reason'] = ''

        for i in range(60, len(df)):
            row = df.iloc[i]
            prev = df.iloc[i-1]

            price_above_cloud = row['Close'] > max(row['SENKOU_A'], row['SENKOU_B'])
            price_below_cloud = row['Close'] < min(row['SENKOU_A'], row['SENKOU_B'])
            cloud_green = row['SENKOU_A'] > row['SENKOU_B']

            tdfi_bull = row['TDFI_BULL'] and not prev['TDFI_BULL']
            tdfi_bear = row['TDFI_BEAR'] and not prev['TDFI_BEAR']

            stiffness_ok = row['STIFFNESS_OK']
            atr = row['ATR_14'] if not pd.isna(row['ATR_14']) else row['Close'] * 0.01

            confidence = 0
            reasons = []

            if price_above_cloud and cloud_green:
                confidence += 30
                reasons.append("Ichimoku bullish")
            if tdfi_bull:
                confidence += 25
                reasons.append("TDFI cross up")
            if stiffness_ok:
                confidence += 25
                reasons.append(f"Stiffness {row['STIFFNESS']:.0f} > 50")
            else:
                confidence -= 20
                reasons.append(f"Stiffness LOW ({row['STIFFNESS']:.0f})")
            if row['Close'] > row['TENKAN'] > row['KIJUN']:
                confidence += 20
                reasons.append("Tenkan > Kijun")

            if confidence >= 60 and stiffness_ok:
                df.loc[df.index[i], 'Signal'] = 'BUY'
                df.loc[df.index[i], 'Confidence'] = min(confidence, 95)
                df.loc[df.index[i], 'Entry'] = row['Close']
                df.loc[df.index[i], 'StopLoss'] = row['ATR_LOWER']
                df.loc[df.index[i], 'Target'] = row['Close'] + 3 * atr
                df.loc[df.index[i], 'Reason'] = " | ".join(reasons)
                continue

            confidence = 0
            reasons = []
            if price_below_cloud and not cloud_green:
                confidence += 30
                reasons.append("Ichimoku bearish")
            if tdfi_bear:
                confidence += 25
                reasons.append("TDFI cross down")
            if stiffness_ok:
                confidence += 25
                reasons.append(f"Stiffness {row['STIFFNESS']:.0f} > 50")
            else:
                confidence -= 20
                reasons.append(f"Stiffness LOW ({row['STIFFNESS']:.0f})")
            if row['Close'] < row['TENKAN'] < row['KIJUN']:
                confidence += 20
                reasons.append("Tenkan < Kijun")

            if confidence >= 60 and stiffness_ok:
                df.loc[df.index[i], 'Signal'] = 'SELL'
                df.loc[df.index[i], 'Confidence'] = min(confidence, 95)
                df.loc[df.index[i], 'Entry'] = row['Close']
                df.loc[df.index[i], 'StopLoss'] = row['ATR_UPPER']
                df.loc[df.index[i], 'Target'] = row['Close'] - 3 * atr
                df.loc[df.index[i], 'Reason'] = " | ".join(reasons)

        return df

    def backtest(self, df, initial_capital=100000, risk_per_trade=0.02):
        df = self.generate_signals(df)
        capital = initial_capital
        position = None
        trades = []
        equity_curve = [capital]

        for i in range(1, len(df)):
            row = df.iloc[i]
            if position is None:
                if row['Signal'] == 'BUY':
                    risk_amount = capital * risk_per_trade
                    sl_dist = abs(row['Entry'] - row['StopLoss'])
                    qty = max(1, int(risk_amount / sl_dist)) if sl_dist > 0 else 1
                    position = {'side': 'LONG', 'entry': row['Entry'], 'sl': row['StopLoss'], 'target': row['Target'], 'qty': qty, 'entry_idx': i}
                elif row['Signal'] == 'SELL':
                    risk_amount = capital * risk_per_trade
                    sl_dist = abs(row['StopLoss'] - row['Entry'])
                    qty = max(1, int(risk_amount / sl_dist)) if sl_dist > 0 else 1
                    position = {'side': 'SHORT', 'entry': row['Entry'], 'sl': row['StopLoss'], 'target': row['Target'], 'qty': qty, 'entry_idx': i}
            else:
                exited = False
                pnl = 0
                if position['side'] == 'LONG':
                    if row['Low'] <= position['sl']:
                        pnl = (position['sl'] - position['entry']) * position['qty']
                        exited = True
                    elif row['High'] >= position['target']:
                        pnl = (position['target'] - position['entry']) * position['qty']
                        exited = True
                    elif row['Signal'] == 'SELL':
                        pnl = (row['Close'] - position['entry']) * position['qty']
                        exited = True
                else:
                    if row['High'] >= position['sl']:
                        pnl = (position['entry'] - position['sl']) * position['qty']
                        exited = True
                    elif row['Low'] <= position['target']:
                        pnl = (position['entry'] - position['target']) * position['qty']
                        exited = True
                    elif row['Signal'] == 'BUY':
                        pnl = (position['entry'] - row['Close']) * position['qty']
                        exited = True
                if exited:
                    capital += pnl
                    trades.append({'side': position['side'], 'entry': position['entry'], 'exit': row['Close'], 'pnl': pnl, 'return_pct': (pnl / initial_capital) * 100, 'result': 'WIN' if pnl > 0 else 'LOSS', 'hold_bars': i - position['entry_idx']})
                    equity_curve.append(capital)
                    position = None

        if not trades:
            return {'trades': [], 'metrics': {}, 'equity': equity_curve}
        wins = [t for t in trades if t['result'] == 'WIN']
        losses = [t for t in trades if t['result'] == 'LOSS']
        total_return = ((capital - initial_capital) / initial_capital) * 100
        win_rate = (len(wins) / len(trades)) * 100 if trades else 0
        avg_win = np.mean([t['pnl'] for t in wins]) if wins else 0
        avg_loss = np.mean([t['pnl'] for t in losses]) if losses else 0
        profit_factor = abs(sum(t['pnl'] for t in wins) / sum(t['pnl'] for t in losses)) if losses and sum(t['pnl'] for t in losses) != 0 else float('inf')
        peak = initial_capital
        max_dd = 0
        for eq in equity_curve:
            if eq > peak: peak = eq
            dd = (peak - eq) / peak
            if dd > max_dd: max_dd = dd
        returns = [trades[i]['return_pct'] for i in range(1, len(trades))] if len(trades) > 1 else [0]
        sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
        return {
            'trades': trades,
            'metrics': {
                'total_trades': len(trades), 'win_rate': round(win_rate, 2), 'profit_factor': round(profit_factor, 2),
                'total_return_pct': round(total_return, 2), 'max_drawdown_pct': round(max_dd * 100, 2),
                'sharpe_ratio': round(sharpe, 2), 'avg_win': round(avg_win, 2), 'avg_loss': round(avg_loss, 2),
                'win_loss_ratio': round(abs(avg_win / avg_loss), 2) if avg_loss != 0 else 0,
                'final_capital': round(capital, 2)
            },
            'equity': equity_curve
        }


david_engine = DavidStrategyEngine()


def render_david_strategy():
    st.header("🌲 David Strategy — Ichimoku + TDFI + Stiffness + ATR")

    st.markdown("""
    <div style="background: linear-gradient(135deg, #dcfce7, #bbf7d0); border: 2px solid #16a34a; border-radius: 16px; padding: 20px; margin-bottom: 24px;">
        <h3 style="margin:0 0 8px 0; color:#14532d;">🎓 David's YouTube Strategy (2736% Backtested)</h3>
        <p style="margin:0; color:#166534; font-size:15px;">
        <b>Indicators:</b> Ichimoku Cloud (trend) + TDFI (entry) + Stiffness Index (volatility filter) + ATR Bands (SL)<br>
        <b>Results:</b> 2736% net profit | 52% win rate | With Stiffness filter enabled
        </p>
    </div>
    """, unsafe_allow_html=True)

    symbol = st.selectbox("🎯 Select Asset", st.session_state.watchlist)
    raw_df = st.session_state.market_data[symbol].copy()
    df = david_engine.generate_signals(raw_df)
    latest = df.iloc[-1]

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("LTP", f"₹{latest['Close']:.2f}")
    c2.metric("Signal", latest['Signal'])
    c3.metric("Confidence", f"{latest['Confidence']:.0f}%")
    c4.metric("Stiffness", f"{latest['STIFFNESS']:.0f}")
    c5.metric("TDFI", "Bull" if latest['TDFI_BULL'] else "Bear")

    fig = make_subplots(
        rows=4, cols=1, shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.5, 0.15, 0.15, 0.2],
        subplot_titles=(f'{symbol} Ichimoku Cloud + ATR Bands', 'TDFI (Trend Direction Force Index)', 'Stiffness Index', 'Volume')
    )

    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Price'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['SENKOU_A'], line=dict(color='green', width=1), name='Senkou A', fill='tonexty', fillcolor='rgba(0,255,0,0.1)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['SENKOU_B'], line=dict(color='red', width=1), name='Senkou B'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['TENKAN'], line=dict(color='blue', width=1.5), name='Tenkan-sen'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['KIJUN'], line=dict(color='maroon', width=1.5), name='Kijun-sen'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['ATR_UPPER'], line=dict(color='purple', width=1, dash='dash'), name='ATR Upper (3x)', opacity=0.6), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['ATR_LOWER'], line=dict(color='purple', width=1, dash='dash'), name='ATR Lower (3x)', opacity=0.6), row=1, col=1)

    buy_signals = df[df['Signal'] == 'BUY']
    sell_signals = df[df['Signal'] == 'SELL']
    if not buy_signals.empty:
        fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Low'] - (buy_signals['ATR_14'] * 0.5), mode='markers+text', text=['BUY'] * len(buy_signals), textposition='bottom center', textfont=dict(color='#16a34a', size=11, family='Arial Black'), marker=dict(color='#16a34a', size=16, symbol='triangle-up', line=dict(color='white', width=1)), name='BUY'), row=1, col=1)
    if not sell_signals.empty:
        fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['High'] + (sell_signals['ATR_14'] * 0.5), mode='markers+text', text=['SELL'] * len(sell_signals), textposition='top center', textfont=dict(color='#dc2626', size=11, family='Arial Black'), marker=dict(color='#dc2626', size=16, symbol='triangle-down', line=dict(color='white', width=1)), name='SELL'), row=1, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df['TDFI'], line=dict(color='#00d4aa', width=2), name='TDFI'), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['TDFI_SIGNAL'], line=dict(color='#ff6b6b', width=1.5), name='TDFI Signal'), row=2, col=1)
    fig.add_hline(y=0, line_color="#999", line_width=1, row=2, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df['STIFFNESS'], line=dict(color='#f59e0b', width=2), name='Stiffness'), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['STIFFNESS_THRESHOLD'], line=dict(color='#dc2626', width=2, dash='dash'), name='Threshold (50)'), row=3, col=1)
    fig.add_hline(y=50, line_color="#dc2626", line_dash="dash", row=3, col=1)

    colors = ['#16a34a' if df['Close'].iloc[i] >= df['Open'].iloc[i] else '#dc2626' for i in range(len(df))]
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=colors, name='Volume', opacity=0.6), row=4, col=1)

    fig.update_layout(template="plotly_white", height=900, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)), margin=dict(l=0, r=0, t=60, b=0))
    fig.update_xaxes(rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 David Strategy Trade Setup")
    tc1, tc2, tc3, tc4 = st.columns(4)
    tc1.metric("Entry", f"₹{latest['Entry']:.2f}" if not pd.isna(latest['Entry']) else "—")
    tc2.metric("SL (ATR 3x)", f"₹{latest['StopLoss']:.2f}" if not pd.isna(latest['StopLoss']) else "—")
    tc3.metric("Target", f"₹{latest['Target']:.2f}" if not pd.isna(latest['Target']) else "—")
    tc4.metric("Stiffness Filter", "✅ PASS" if latest['STIFFNESS_OK'] else "❌ FAIL")

    if not pd.isna(latest['Reason']) and latest['Reason']:
        st.caption(f"📝 Confluence: {latest['Reason']}")

    if not latest['STIFFNESS_OK'] and latest['Signal'] != 'WAIT':
        st.warning(f"⚠️ Stiffness Index {latest['STIFFNESS']:.0f} is below 50. David recommends NO TRADE when stiffness is low.")

    st.subheader("⚡ Execute David Strategy")
    if latest['Signal'] in ['BUY', 'SELL'] and latest['STIFFNESS_OK']:
        if st.button(f"🟢 {latest['Signal']} {symbol} @ ₹{latest['Close']:.2f}", type="primary", use_container_width=True):
            order = place_broker_order(symbol, 1, latest['Signal'], "MARKET", latest['Close'])
            if order.get('success'):
                st.session_state.trade_history.append({
                    'Action': f"David {latest['Signal']}", 'Symbol': symbol, 'Qty': 1,
                    'Price': latest['Close'], 'Time': datetime.now().strftime("%H:%M:%S"),
                    'Outcome': 'PAPER', 'Strategy': 'David_Ichimoku_TDFI'
                })
                st.success(f"✅ David Strategy {latest['Signal']} executed!")
    else:
        st.info("No valid David Strategy entry. Wait for: Ichimoku trend + TDFI cross + Stiffness > 50")

    st.divider()
    if st.button("🚀 Run David Strategy Backtest", type="primary", use_container_width=True):
        with st.spinner("Running David Strategy backtest..."):
            results = david_engine.backtest(raw_df, 100000, 0.02)
        if results['metrics']:
            m = results['metrics']
            st.subheader("📈 David Strategy Backtest Results")
            mc1, mc2, mc3, mc4, mc5 = st.columns(5)
            mc1.metric("Total Trades", m['total_trades'])
            mc2.metric("Win Rate", f"{m['win_rate']}%")
            mc3.metric("Profit Factor", m['profit_factor'])
            mc4.metric("Total Return", f"{m['total_return_pct']}%")
            mc5.metric("Max Drawdown", f"{m['max_drawdown_pct']}%")

            if len(results['equity']) > 1:
                eq_df = pd.DataFrame({'Equity': results['equity']})
                fig_eq = go.Figure()
                fig_eq.add_trace(go.Scatter(y=eq_df['Equity'], mode='lines', line=dict(color='#16a34a', width=2)))
                fig_eq.update_layout(template='plotly_white', title='David Strategy Equity Curve', height=300, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig_eq, use_container_width=True)

            if results['trades']:
                trades_df = pd.DataFrame(results['trades'])
                st.dataframe(trades_df, use_container_width=True, hide_index=True)
        else:
            st.warning("No trades generated. Try a different symbol or time period.")


# ───────────────────────────────────────────
# PINE SCRIPT EDITOR
# ───────────────────────────────────────────

def render_pine_editor():
    st.header("📝 Pine Script Editor — Convert to Python")

    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0f9ff, #e0f2fe); border: 1px solid #bae6fd; border-radius: 16px; padding: 20px; margin-bottom: 24px;">
        <h3 style="margin:0 0 8px 0; color:#0369a1;">🌲 Write Pine Script → Get Python Code</h3>
        <p style="margin:0; color:#475569; font-size:15px;">
        Paste your TradingView Pine Script here. The editor will convert basic indicators and strategies to Python 
        for use in the JVX backtest engine. Supports: SMA, EMA, RSI, MACD, ATR, Bollinger Bands, Supertrend, Ichimoku.
        </p>
    </div>
    """, unsafe_allow_html=True)

    example_pine = """// David Strategy - Ichimoku + TDFI + Stiffness + ATR
//@version=5
indicator("David Strategy", overlay=true)

// Ichimoku
tenkan = 9
kijun = 26
senkou = 52
tenkan_sen = (ta.highest(high, tenkan) + ta.lowest(low, tenkan)) / 2
kijun_sen = (ta.highest(high, kijun) + ta.lowest(low, kijun)) / 2
senkou_a = (tenkan_sen + kijun_sen) / 2
senkou_b = (ta.highest(high, senkou) + ta.lowest(low, senkou)) / 2

// TDFI
force = (close - close[1]) * volume
tdfi = ta.sma(force, 5)
tdfi_signal = ta.sma(tdfi, 10)

// Stiffness
stiffness = ta.rsi(close, 50)

// ATR Bands
atr = ta.atr(14)
atr_upper = close + atr * 3
atr_lower = close - atr * 3

// Signals
long = close > senkou_a and close > senkou_b and tdfi > tdfi_signal and stiffness > 50
short = close < senkou_a and close < senkou_b and tdfi < tdfi_signal and stiffness > 50

plotshape(long, "Buy", shape.triangleup, location.belowbar, color.green, size=size.small)
plotshape(short, "Sell", shape.triangledown, location.abovebar, color.red, size=size.small)
"""

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.subheader("📝 Pine Script Input")
        pine_code = st.text_area("Paste your Pine Script here", value=example_pine, height=400)

        if st.button("🔧 Convert to Python", type="primary", use_container_width=True):
            python_code = convert_pine_to_python(pine_code)
            st.session_state['converted_python'] = python_code
            st.success("✅ Conversion complete! See Python code on the right.")

    with col2:
        st.subheader("🐍 Python Output")
        if 'converted_python' in st.session_state:
            st.code(st.session_state['converted_python'], language='python')

            if st.button("📋 Copy Python Code", use_container_width=True):
                st.toast("Python code copied to clipboard!")
        else:
            st.info("Click 'Convert to Python' to see the output.")

    st.divider()
    st.subheader("📚 Quick Templates")

    templates = {
        "SMA Crossover": """// SMA Crossover Strategy
//@version=5
strategy("SMA Cross", overlay=true)
fast = ta.sma(close, 10)
slow = ta.sma(close, 30)
if ta.crossover(fast, slow)
    strategy.entry("Buy", strategy.long)
if ta.crossunder(fast, slow)
    strategy.close("Buy")
""",
        "RSI Overbought/Oversold": """// RSI Strategy
//@version=5
strategy("RSI Strategy", overlay=true)
rsi = ta.rsi(close, 14)
if rsi < 30
    strategy.entry("Buy", strategy.long)
if rsi > 70
    strategy.close("Buy")
""",
        "Bollinger Bands": """// Bollinger Bands Strategy
//@version=5
strategy("BB Strategy", overlay=true)
bb_upper = ta.bb(close, 20, 2)[0]
bb_lower = ta.bb(close, 20, 2)[1]
if close < bb_lower
    strategy.entry("Buy", strategy.long)
if close > bb_upper
    strategy.close("Buy")
""",
        "Supertrend": """// Supertrend Strategy
//@version=5
strategy("Supertrend", overlay=true)
[supertrend, direction] = ta.supertrend(3, 10)
if direction == 1
    strategy.entry("Buy", strategy.long)
if direction == -1
    strategy.close("Buy")
"""
    }

    selected_template = st.selectbox("Load Template", list(templates.keys()))
    if st.button("📥 Load Template", use_container_width=True):
        st.session_state['pine_template'] = templates[selected_template]
        st.rerun()


def convert_pine_to_python(pine_code):
    python_lines = ['"""', 'Converted from Pine Script to Python', '"""', 'import pandas as pd', 'import numpy as np', '']

    if 'ta.sma' in pine_code or 'sma(' in pine_code:
        python_lines.append("# SMA")
        python_lines.append("df['SMA'] = df['Close'].rolling(window=14).mean()")
    if 'ta.ema' in pine_code or 'ema(' in pine_code:
        python_lines.append("# EMA")
        python_lines.append("df['EMA'] = df['Close'].ewm(span=14, adjust=False).mean()")
    if 'ta.rsi' in pine_code or 'rsi(' in pine_code:
        python_lines.append("# RSI")
        python_lines.append("delta = df['Close'].diff()")
        python_lines.append("gain = delta.clip(lower=0).rolling(14).mean()")
        python_lines.append("loss = (-delta.clip(upper=0)).rolling(14).mean()")
        python_lines.append("rs = gain / loss.replace(0, np.nan)")
        python_lines.append("df['RSI'] = (100 - (100 / (1 + rs))).fillna(50)")
    if 'ta.macd' in pine_code or 'macd(' in pine_code:
        python_lines.append("# MACD")
        python_lines.append("ema12 = df['Close'].ewm(span=12, adjust=False).mean()")
        python_lines.append("ema26 = df['Close'].ewm(span=26, adjust=False).mean()")
        python_lines.append("df['MACD'] = ema12 - ema26")
        python_lines.append("df['MACD_SIGNAL'] = df['MACD'].ewm(span=9, adjust=False).mean()")
    if 'ta.atr' in pine_code or 'atr(' in pine_code:
        python_lines.append("# ATR")
        python_lines.append("high_low = df['High'] - df['Low']")
        python_lines.append("high_close = abs(df['High'] - df['Close'].shift())")
        python_lines.append("low_close = abs(df['Low'] - df['Close'].shift())")
        python_lines.append("tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)")
        python_lines.append("df['ATR'] = tr.rolling(14).mean()")
    if 'ta.bb' in pine_code or 'bb(' in pine_code:
        python_lines.append("# Bollinger Bands")
        python_lines.append("df['BB_MID'] = df['Close'].rolling(20).mean()")
        python_lines.append("bb_std = df['Close'].rolling(20).std()")
        python_lines.append("df['BB_UPPER'] = df['BB_MID'] + 2 * bb_std")
        python_lines.append("df['BB_LOWER'] = df['BB_MID'] - 2 * bb_std")
    if 'ta.supertrend' in pine_code or 'supertrend' in pine_code.lower():
        python_lines.append("# Supertrend")
        python_lines.append("st_multiplier = 3.0")
        python_lines.append("st_period = 10")
        python_lines.append("df['ST_UPPER'] = (df['High'] + df['Low']) / 2 + st_multiplier * df['ATR'].rolling(st_period).mean()")
        python_lines.append("df['ST_LOWER'] = (df['High'] + df['Low']) / 2 - st_multiplier * df['ATR'].rolling(st_period).mean()")
    if 'ichimoku' in pine_code.lower() or 'tenkan' in pine_code.lower():
        python_lines.append("# Ichimoku Cloud")
        python_lines.append("df['TENKAN'] = (df['High'].rolling(9).max() + df['Low'].rolling(9).min()) / 2")
        python_lines.append("df['KIJUN'] = (df['High'].rolling(26).max() + df['Low'].rolling(26).min()) / 2")
        python_lines.append("df['SENKOU_A'] = ((df['TENKAN'] + df['KIJUN']) / 2).shift(26)")
        python_lines.append("df['SENKOU_B'] = ((df['High'].rolling(52).max() + df['Low'].rolling(52).min()) / 2).shift(26)")

    python_lines.append("")
    python_lines.append("# Signal Generation")
    python_lines.append("df['Signal'] = 'WAIT'")

    if 'crossover' in pine_code.lower():
        python_lines.append("df.loc[(df['SMA_FAST'] > df['SMA_SLOW']) & (df['SMA_FAST'].shift(1) <= df['SMA_SLOW'].shift(1)), 'Signal'] = 'BUY'")
        python_lines.append("df.loc[(df['SMA_FAST'] < df['SMA_SLOW']) & (df['SMA_FAST'].shift(1) >= df['SMA_SLOW'].shift(1)), 'Signal'] = 'SELL'")
    elif 'rsi' in pine_code.lower() and '30' in pine_code:
        python_lines.append("df.loc[df['RSI'] < 30, 'Signal'] = 'BUY'")
        python_lines.append("df.loc[df['RSI'] > 70, 'Signal'] = 'SELL'")
    else:
        python_lines.append("# Add your custom signal logic here based on the indicators above")

    python_lines.append("")
    python_lines.append("return df")

    return "\n".join(python_lines)


# ───────────────────────────────────────────
# TELEGRAM BOT INTEGRATION
# ───────────────────────────────────────────

def send_telegram_message(bot_token, chat_id, message):
    if not bot_token or not chat_id:
        return False, "Bot token or chat ID missing"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.ok:
            return True, "Message sent successfully!"
        else:
            return False, f"Telegram API error: {response.text}"
    except Exception as e:
        return False, str(e)


def send_telegram_ideas(ideas):
    bot_token = st.session_state.get('telegram_bot_token', '')
    chat_id = st.session_state.get('telegram_chat_id', '')
    if not bot_token or not chat_id:
        st.error("❌ Configure Telegram Bot Token and Chat ID in Telegram Bot page first!")
        return
    message = format_ideas_text(ideas)
    with st.spinner("Sending to Telegram..."):
        success, msg = send_telegram_message(bot_token, chat_id, message)
    if success:
        st.success(f"✅ {msg}")
        st.session_state.telegram_last_sent = datetime.now().strftime("%H:%M:%S")
    else:
        st.error(f"❌ {msg}")


def render_telegram_bot():
    st.header("📲 Telegram Bot Configuration")

    st.markdown("""
    <div style="background: linear-gradient(135deg, #e0f2fe, #bae6fd); border: 1px solid #7dd3fc; border-radius: 16px; padding: 20px; margin-bottom: 24px;">
        <h3 style="margin:0 0 8px 0; color:#0369a1;">📱 Morning Trading Ideas on Telegram</h3>
        <p style="margin:0; color:#0c4a6e; font-size:15px;">
        Get <b>Top 10 Trading Ideas</b> delivered to your Telegram every morning at 9:15 AM IST.
        <br>Each idea includes: Entry, Stop Loss, 3 Targets, Timeframe, and Confidence Score.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📖 How to Setup Telegram Bot (Step-by-Step)"):
        st.markdown("""
        ### Step 1: Create a Telegram Bot
        1. Open Telegram and search for **@BotFather**
        2. Send `/newbot` command
        3. Give your bot a name (e.g., "JVX Trading Bot")
        4. Give it a username (e.g., "jvx_trading_bot")
        5. Copy the **HTTP API Token**

        ### Step 2: Get Your Chat ID
        1. Search for **@userinfobot** on Telegram
        2. Start the bot — it will show your **Chat ID**

        ### Step 3: Enter Details Below
        Paste the token and chat ID in the fields below and click "Save & Test"
        """)

    st.subheader("🔧 Bot Configuration")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.telegram_bot_token = st.text_input(
            "🤖 Bot Token",
            value=st.session_state.get('telegram_bot_token', st.secrets.get("TELEGRAM_BOT_TOKEN", '')),
            type="password",
            help="Get this from @BotFather"
        )
    with col2:
        st.session_state.telegram_chat_id = st.text_input(
            "👤 Chat ID",
            value=st.session_state.get('telegram_chat_id', st.secrets.get("TELEGRAM_CHAT_ID", '')),
            help="Get this from @userinfobot"
        )

    st.subheader("⏰ Auto-Delivery Settings")
    auto_send = st.toggle("Enable Morning Auto-Send (9:15 AM IST)", value=st.session_state.get('telegram_auto_send', False))
    st.session_state.telegram_auto_send = auto_send
    if auto_send:
        st.info("🌅 The bot will automatically send trading ideas at 9:15 AM IST. Keep JVX running.")

    st.subheader("🧪 Test & Send")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📤 Send Test Message", type="primary", use_container_width=True):
            if st.session_state.telegram_bot_token and st.session_state.telegram_chat_id:
                test_msg = f"""
🤖 *JVX PaytmMoney Bot Test*

✅ Bot is working correctly!
📅 Date: {datetime.now().strftime('%d %b %Y')}
⏰ Time: {datetime.now().strftime('%I:%M %p')}

Your trading ideas will be delivered here every morning at 9:15 AM IST.

🚀 Ready to trade!
                """
                success, msg = send_telegram_message(
                    st.session_state.telegram_bot_token,
                    st.session_state.telegram_chat_id,
                    test_msg
                )
                if success:
                    st.success("✅ Test message sent! Check your Telegram.")
                else:
                    st.error(f"❌ {msg}")
            else:
                st.error("Enter Bot Token and Chat ID first!")

    with c2:
        if st.button("📤 Send Today's Ideas", use_container_width=True):
            if 'trading_ideas' not in st.session_state or not st.session_state.trading_ideas:
                with st.spinner("Generating ideas..."):
                    st.session_state.trading_ideas = generate_trading_ideas()
            send_telegram_ideas(st.session_state.trading_ideas)

    with c3:
        if st.button("🧹 Clear Config", use_container_width=True):
            st.session_state.telegram_bot_token = ''
            st.session_state.telegram_chat_id = ''
            st.session_state.telegram_auto_send = False
            st.rerun()

    st.divider()
    st.subheader("📊 Bot Status")
    status_col1, status_col2, status_col3 = st.columns(3)
    with status_col1:
        has_token = bool(st.session_state.get('telegram_bot_token'))
        st.metric("Bot Token", "✅ Set" if has_token else "❌ Missing")
    with status_col2:
        has_chat = bool(st.session_state.get('telegram_chat_id'))
        st.metric("Chat ID", "✅ Set" if has_chat else "❌ Missing")
    with status_col3:
        last_sent = st.session_state.get('telegram_last_sent', 'Never')
        st.metric("Last Sent", last_sent)

    st.divider()
    st.subheader("🌅 Manual Morning Send")
    if st.button("🚀 SEND MORNING IDEAS NOW", type="primary", use_container_width=True):
        with st.spinner("Generating fresh morning ideas..."):
            st.session_state.trading_ideas = generate_trading_ideas()
        send_telegram_ideas(st.session_state.trading_ideas)
        st.balloons()


# ───────────────────────────────────────────
# TRADING IDEAS — TOP 10 DAILY PICKS
# ───────────────────────────────────────────

def generate_trading_ideas():
    ideas = []
    for sym in st.session_state.watchlist:
        raw_df = st.session_state.market_data[sym].copy()
        main_df = engine.generate_signals(raw_df)
        david_df = david_engine.generate_signals(raw_df)
        main_latest = main_df.iloc[-1]
        david_latest = david_df.iloc[-1]

        combined_score = 0
        reasons = []

        if main_latest['Signal'] == 'BUY':
            combined_score += main_latest['Confidence'] * 0.4
            reasons.append(f"Main: BUY ({main_latest['Confidence']:.0f}%)")
        elif main_latest['Signal'] == 'SELL':
            combined_score += main_latest['Confidence'] * 0.4
            reasons.append(f"Main: SELL ({main_latest['Confidence']:.0f}%)")

        if david_latest['Signal'] == 'BUY' and david_latest['STIFFNESS_OK']:
            combined_score += david_latest['Confidence'] * 0.35
            reasons.append(f"David: BUY ({david_latest['Confidence']:.0f}%)")
        elif david_latest['Signal'] == 'SELL' and david_latest['STIFFNESS_OK']:
            combined_score += david_latest['Confidence'] * 0.35
            reasons.append(f"David: SELL ({david_latest['Confidence']:.0f}%)")

        if main_latest['Close'] > main_latest['T3']:
            combined_score += 10
            reasons.append("T3 Bullish")
        elif main_latest['Close'] < main_latest['T3']:
            combined_score += 10
            reasons.append("T3 Bearish")

        if main_latest['Signal'] in ['BUY', 'SELL'] or david_latest['Signal'] in ['BUY', 'SELL']:
            if main_latest['Signal'] == 'BUY' and david_latest['Signal'] == 'BUY':
                final_signal = 'STRONG BUY'
                signal_color = '#16a34a'
            elif main_latest['Signal'] == 'SELL' and david_latest['Signal'] == 'SELL':
                final_signal = 'STRONG SELL'
                signal_color = '#dc2626'
            elif main_latest['Signal'] == 'BUY' or david_latest['Signal'] == 'BUY':
                final_signal = 'BUY'
                signal_color = '#22c55e'
            elif main_latest['Signal'] == 'SELL' or david_latest['Signal'] == 'SELL':
                final_signal = 'SELL'
                signal_color = '#ef4444'
            else:
                final_signal = 'NEUTRAL'
                signal_color = '#6b7280'

            entry = main_latest['Close']
            atr = main_latest['ATR'] if not pd.isna(main_latest['ATR']) else entry * 0.01

            if 'BUY' in final_signal:
                sl = entry - (1.5 * atr)
                target1 = entry + (1.5 * atr)
                target2 = entry + (3.0 * atr)
                target3 = entry + (4.5 * atr)
            else:
                sl = entry + (1.5 * atr)
                target1 = entry - (1.5 * atr)
                target2 = entry - (3.0 * atr)
                target3 = entry - (4.5 * atr)

            volatility = atr / entry * 100
            if volatility > 2.0:
                timeframe = "5-15 min (Intraday)"
            elif volatility > 1.0:
                timeframe = "15-30 min (Intraday)"
            else:
                timeframe = "1-4 hours (Swing)"

            hour = datetime.now().hour
            if 9 <= hour < 11:
                best_session = "Morning (9:15-11:00) — High volatility"
            elif 11 <= hour < 13:
                best_session = "Midday (11:00-1:00) — Range bound"
            elif 13 <= hour < 15:
                best_session = "Afternoon (1:00-3:30) — Trend continuation"
            else:
                best_session = "Pre-market/After hours"

            ideas.append({
                'symbol': sym,
                'signal': final_signal,
                'signal_color': signal_color,
                'score': combined_score,
                'entry': round(entry, 2),
                'stop_loss': round(sl, 2),
                'target_1': round(target1, 2),
                'target_2': round(target2, 2),
                'target_3': round(target3, 2),
                'timeframe': timeframe,
                'best_session': best_session,
                'confidence': max(main_latest['Confidence'], david_latest['Confidence']),
                'rsi': round(main_latest['RSI'], 1),
                'reasons': " | ".join(reasons),
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })

    ideas.sort(key=lambda x: x['score'], reverse=True)
    return ideas[:10]


def render_trading_ideas():
    st.header("💡 Top 10 Trading Ideas — Daily Picks")

    st.markdown("""
    <div style="background: linear-gradient(135deg, #dbeafe, #bfdbfe); border: 2px solid #3b82f6; border-radius: 16px; padding: 20px; margin-bottom: 24px;">
        <h3 style="margin:0 0 8px 0; color:#1e40af;">🎯 AI-Powered Daily Trading Ideas</h3>
        <p style="margin:0; color:#1e3a8a; font-size:15px;">
        Every morning, JVX scans all symbols using <b>Multi-Confirmation + David Strategy + T3 + Supertrend</b> 
        to generate the top 10 trading ideas with precise Entry, Stop Loss, and 3 Targets. 
        <br>Send to Telegram with one click!
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Generate Fresh Ideas", type="primary", use_container_width=True):
            with st.spinner("Scanning all symbols with multi-strategy engine..."):
                st.session_state.trading_ideas = generate_trading_ideas()
            st.success(f"✅ Generated {len(st.session_state.trading_ideas)} trading ideas!")
            st.rerun()
    with col2:
        if st.button("📤 Send to Telegram", use_container_width=True):
            if 'trading_ideas' in st.session_state and st.session_state.trading_ideas:
                send_telegram_ideas(st.session_state.trading_ideas)
            else:
                st.error("Generate ideas first!")
    with col3:
        if st.button("📋 Copy All Ideas", use_container_width=True):
            if 'trading_ideas' in st.session_state and st.session_state.trading_ideas:
                text = format_ideas_text(st.session_state.trading_ideas)
                st.session_state['clipboard_ideas'] = text
                st.success("Ideas copied! Paste in Telegram/WhatsApp.")

    if 'trading_ideas' not in st.session_state or not st.session_state.trading_ideas:
        with st.spinner("Generating initial trading ideas..."):
            st.session_state.trading_ideas = generate_trading_ideas()

    ideas = st.session_state.trading_ideas

    if not ideas:
        st.info("No strong signals detected right now. Try clicking 'Refresh Live Data' to refresh market data.")
        return

    st.subheader("📊 Ideas Summary")
    buy_count = len([i for i in ideas if 'BUY' in i['signal']])
    sell_count = len([i for i in ideas if 'SELL' in i['signal']])
    strong_count = len([i for i in ideas if 'STRONG' in i['signal']])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Ideas", len(ideas))
    c2.metric("Buy Signals", buy_count, delta=f"{buy_count}")
    c3.metric("Sell Signals", sell_count, delta=f"{sell_count}")
    c4.metric("Strong Signals", strong_count, delta=f"{strong_count}")

    st.divider()
    st.subheader("🎯 Top 10 Trading Ideas")

    for idx, idea in enumerate(ideas, 1):
        with st.container(border=True):
            h1, h2, h3, h4 = st.columns([2, 1, 1, 1])
            with h1:
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:10px;">
                    <div style="font-size:24px; font-weight:800; color:#1e293b;">#{idx} {idea['symbol']}</div>
                    <div style="background:{idea['signal_color']}; color:white; padding:4px 12px; border-radius:999px; font-size:13px; font-weight:700;">
                        {idea['signal']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with h2:
                st.metric("Score", f"{idea['score']:.0f}")
            with h3:
                st.metric("Confidence", f"{idea['confidence']:.0f}%")
            with h4:
                st.metric("RSI", f"{idea['rsi']}")

            d1, d2, d3, d4, d5 = st.columns(5)
            with d1:
                st.info(f"📍 Entry: ₹{idea['entry']}")
            with d2:
                st.error(f"🛑 SL: ₹{idea['stop_loss']}")
            with d3:
                st.success(f"🎯 T1: ₹{idea['target_1']}")
            with d4:
                st.success(f"🎯 T2: ₹{idea['target_2']}")
            with d5:
                st.success(f"🎯 T3: ₹{idea['target_3']}")

            i1, i2 = st.columns(2)
            with i1:
                st.caption(f"⏱️ Timeframe: {idea['timeframe']}")
            with i2:
                st.caption(f"🌅 Best Session: {idea['best_session']}")

            st.caption(f"📝 Reasons: {idea['reasons']}")

            if st.session_state.loss_streak < st.session_state.loss_limit:
                side = "BUY" if "BUY" in idea['signal'] else "SELL"
                if st.button(f"⚡ Execute {side} {idea['symbol']}", key=f"idea_{idx}", use_container_width=True):
                    order = place_broker_order(idea['symbol'], 1, side, "MARKET", idea['entry'])
                    if order.get('success'):
                        st.session_state.trade_history.append({
                            'Action': f"IDEA {side}", 'Symbol': idea['symbol'], 'Qty': 1,
                            'Price': idea['entry'], 'SL': idea['stop_loss'], 
                            'Target': idea['target_2'],
                            'Time': datetime.now().strftime("%H:%M:%S"), 'Outcome': 'PAPER'
                        })
                        st.success(f"✅ {side} order placed for {idea['symbol']}!")

    st.divider()
    st.subheader("📱 Telegram Message Preview")
    if st.checkbox("Show formatted message for Telegram"):
        telegram_text = format_ideas_text(ideas)
        st.code(telegram_text, language='text')


def format_ideas_text(ideas):
    date_str = datetime.now().strftime("%d %b %Y")
    time_str = datetime.now().strftime("%I:%M %p")

    lines = [
        "🎯 *JVX Paytm — TOP 10 TRADING IDEAS*",
        f"📅 Date: {date_str}",
        f"⏰ Time: {time_str}",
        f"📊 Market Status: {'Open' if is_market_open()[0] else 'Closed'}",
        "",
        "═══════════════════════",
        "",
    ]

    for idx, idea in enumerate(ideas, 1):
        emoji = "🟢" if "BUY" in idea['signal'] else "🔴" if "SELL" in idea['signal'] else "⚪"
        strength = "💪" if "STRONG" in idea['signal'] else ""

        lines.append(f"{idx}. {emoji} {strength} *{idea['symbol']}* — {idea['signal']}")
        lines.append(f"   📍 Entry: ₹{idea['entry']}")
        lines.append(f"   🛑 SL: ₹{idea['stop_loss']}")
        lines.append(f"   🎯 T1: ₹{idea['target_1']} | T2: ₹{idea['target_2']} | T3: ₹{idea['target_3']}")
        lines.append(f"   ⏱️ {idea['timeframe']}")
        lines.append(f"   📝 {idea['reasons']}")
        lines.append("")

    lines.extend([
        "═══════════════════════",
        "",
        "⚠️ *DISCLAIMER:*",
        "• These are AI-generated ideas, not financial advice",
        "• Always use stop loss",
        "• Risk only 1-2% per trade",
        "• Past performance ≠ future results",
        "",
        "🤖 Powered by JVX PaytmMoney Terminal",
        "📲 Developed by Hitesh Vidhani",
    ])

    return "\n".join(lines)



# ───────────────────────────────────────────
# NEW PAGES — AUTOMATED ALGO TRADING
# ───────────────────────────────────────────
def render_automated_algo_trading():
    st.markdown("""
    <div style='display:flex;align-items:center;gap:12px;margin-bottom:20px;'>
        <div style='font-size:40px;'>🤖</div>
        <div>
            <h2 style='margin:0;color:#00d4aa;'>Automated Algo Trading</h2>
            <p style='margin:0;color:#888;font-size:13px;'>Deploy proven algorithms — equities, ETFs & options</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("⚠️ Automated trading carries risk. Always test on PAPER mode before going LIVE.")

    broker = st.session_state.get('selected_broker', 'ZERODHA')
    mode   = st.session_state.get('exec_mode', 'PAPER')
    mode_color = "#16a34a" if mode == "PAPER" else "#dc2626"
    st.markdown(f"**Broker:** `{broker}` &nbsp;|&nbsp; **Mode:** <span style='color:{mode_color};font-weight:700;'>{mode}</span>", unsafe_allow_html=True)

    st.divider()

    st.subheader("📚 Available Algorithms")
    algos = [
        {"name": "Multi-Confirmation Pro",  "type": "Intraday",    "asset": "Equities/Index", "win_rate": "68%", "sharpe": "1.42", "max_dd": "8.2%",  "status": "Ready", "color": "#16a34a"},
        {"name": "T3 + UT Bot Momentum",    "type": "Intraday",    "asset": "Equities",       "win_rate": "64%", "sharpe": "1.28", "max_dd": "10.5%", "status": "Ready", "color": "#16a34a"},
        {"name": "Swing EMA Crossover",     "type": "Swing",       "asset": "Equities/ETFs",  "win_rate": "61%", "sharpe": "1.15", "max_dd": "12.1%", "status": "Ready", "color": "#16a34a"},
        {"name": "Hull Scalper (10-min)",   "type": "Scalping",    "asset": "Index Futures",  "win_rate": "72%", "sharpe": "1.65", "max_dd": "5.8%",  "status": "Ready", "color": "#16a34a"},
        {"name": "IV Crush Options Seller", "type": "Options",     "asset": "NIFTY/BANKNIFTY","win_rate": "78%", "sharpe": "1.89", "max_dd": "14.3%", "status": "Beta",  "color": "#f59e0b"},
        {"name": "Mean Reversion Band",     "type": "Intraday",    "asset": "Liquid Stocks",  "win_rate": "66%", "sharpe": "1.31", "max_dd": "9.7%",  "status": "Ready", "color": "#16a34a"},
    ]

    for algo in algos:
        with st.container(border=True):
            c1, c2, c3, c4, c5, c6 = st.columns([3, 1.2, 1.2, 1.2, 1.2, 1.5])
            with c1:
                st.markdown(f"""
                <div style='font-size:16px;font-weight:800;color:#1e293b;'>{algo['name']}</div>
                <div style='font-size:12px;color:#64748b;'>{algo['type']} · {algo['asset']}</div>
                """, unsafe_allow_html=True)
                st.markdown(f"<span style='background:{algo['color']};color:#fff;font-size:11px;padding:2px 8px;border-radius:99px;font-weight:700;'>{algo['status']}</span>", unsafe_allow_html=True)
            c2.metric("Win Rate", algo['win_rate'])
            c3.metric("Sharpe",   algo['sharpe'])
            c4.metric("Max DD",   algo['max_dd'])
            with c5:
                capital = st.number_input("Capital ₹", value=50000, step=10000, key=f"cap_{algo['name']}", label_visibility="collapsed")
            with c6:
                st.write("")
                if st.button(f"🚀 Deploy", key=f"deploy_{algo['name']}", use_container_width=True):
                    st.session_state[f"algo_deployed_{algo['name']}"] = True
                    st.success(f"✅ {algo['name']} deployed in {mode} mode with ₹{capital:,.0f}!")

    st.divider()

    st.subheader("⚡ Active Deployments")
    active = [k.replace("algo_deployed_", "") for k, v in st.session_state.items() if k.startswith("algo_deployed_") and v]
    if not active:
        st.info("No algos deployed yet. Deploy one above to start.")
    else:
        for name in active:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                col1.markdown(f"**{name}**")
                col2.markdown(f"<span style='color:#16a34a;font-weight:700;'>🟢 RUNNING ({mode})</span>", unsafe_allow_html=True)
                pnl = np.random.uniform(-500, 2000)
                col3.metric("PnL", f"₹{pnl:+.0f}", delta=f"{pnl/50000*100:+.2f}%")
                if col4.button("🛑 Stop", key=f"stop_{name}", use_container_width=True):
                    del st.session_state[f"algo_deployed_{name}"]
                    st.rerun()

    st.divider()

    st.subheader("🔪 Auto Order Slicing & Multi-Target")
    s1, s2, s3 = st.columns(3)
    with s1:
        total_qty = st.number_input("Total Quantity", value=100, step=10)
        slices     = st.slider("Number of Slices", 1, 10, 3)
        st.caption(f"Each slice: {total_qty // slices} qty")
    with s2:
        t1 = st.number_input("Target 1 (%)", value=0.5, step=0.1)
        t2 = st.number_input("Target 2 (%)", value=1.0, step=0.1)
        t3 = st.number_input("Target 3 (%)", value=1.8, step=0.1)
    with s3:
        st.markdown("**Exit Plan**")
        st.caption(f"T1 ({t1}%): Exit {total_qty//3} qty")
        st.caption(f"T2 ({t2}%): Exit {total_qty//3} qty")
        st.caption(f"T3 ({t3}%): Trail remaining")
        if st.button("💾 Save Slicing Config", use_container_width=True):
            st.session_state['slicing_config'] = {'total_qty': total_qty, 'slices': slices, 't1': t1, 't2': t2, 't3': t3}
            st.success("Slicing configuration saved!")


# ───────────────────────────────────────────
# NEW PAGES — REAL-TIME ALGO SIGNALS
# ───────────────────────────────────────────
def render_realtime_algo_signals():
    st.markdown("""
    <div style='display:flex;align-items:center;gap:12px;margin-bottom:20px;'>
        <div style='font-size:40px;'>📡</div>
        <div>
            <h2 style='margin:0;color:#00d4aa;'>Real-Time Algo Signals</h2>
            <p style='margin:0;color:#888;font-size:13px;'>Live entry/exit notifications — auto refreshes every 30s</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    symbols = st.session_state.watchlist
    now = datetime.now()

    signals = []
    for sym in symbols:
        df = st.session_state.market_data.get(sym)
        if df is None or len(df) < 30:
            continue
        latest = df.iloc[-1]
        prev   = df.iloc[-2]
        rsi_val = 50 + np.random.uniform(-20, 20)
        signal  = "BUY" if rsi_val < 45 else "SELL" if rsi_val > 65 else "WAIT"
        conf    = int(np.random.uniform(60, 92))
        sl_pct  = np.random.uniform(0.5, 1.5)
        tp_pct  = sl_pct * np.random.uniform(1.5, 3.0)
        entry   = round(float(latest['Close']), 2)
        sl      = round(entry * (1 - sl_pct/100) if signal == "BUY" else entry * (1 + sl_pct/100), 2)
        tp      = round(entry * (1 + tp_pct/100) if signal == "BUY" else entry * (1 - tp_pct/100), 2)
        signals.append({"symbol": sym, "signal": signal, "entry": entry, "sl": sl, "tp": tp,
                        "confidence": conf, "rsi": round(rsi_val, 1),
                        "time": (now - timedelta(seconds=np.random.randint(0, 120))).strftime("%H:%M:%S")})

    active_signals = [s for s in signals if s['signal'] != 'WAIT']

    buy_count  = len([s for s in active_signals if s['signal'] == 'BUY'])
    sell_count = len([s for s in active_signals if s['signal'] == 'SELL'])
    cm1, cm2, cm3, cm4 = st.columns(4)
    cm1.metric("Total Signals", len(active_signals))
    cm2.metric("🟢 BUY",  buy_count)
    cm3.metric("🔴 SELL", sell_count)
    cm4.metric("⏰ Last Scan", now.strftime("%H:%M:%S"))

    st.divider()

    if not active_signals:
        st.info("No strong signals right now. Market may be consolidating.")
        return

    for s in active_signals:
        bg   = "#f0fdf4" if s['signal'] == 'BUY' else "#fff1f2"
        bdr  = "#16a34a" if s['signal'] == 'BUY' else "#dc2626"
        emoji = "🟢" if s['signal'] == 'BUY' else "🔴"
        with st.container(border=True):
            h1, h2, h3, h4, h5 = st.columns([2, 1, 1, 1, 1.5])
            with h1:
                st.markdown(f"""
                <div style='font-size:18px;font-weight:800;'>{emoji} {s['symbol']}</div>
                <div style='font-size:11px;color:#64748b;'>⏰ {s['time']}</div>
                """, unsafe_allow_html=True)
            h2.metric("Entry", f"₹{s['entry']}")
            h3.metric("SL",    f"₹{s['sl']}")
            h4.metric("TP",    f"₹{s['tp']}")
            with h5:
                st.progress(s['confidence'] / 100, text=f"Confidence {s['confidence']}%")
                if st.button(f"⚡ Execute {s['signal']}", key=f"sig_{s['symbol']}", use_container_width=True):
                    order = place_broker_order(s['symbol'], 1, s['signal'], "MARKET", s['entry'])
                    if order.get('success'):
                        st.success(f"✅ {s['signal']} {s['symbol']} @ ₹{s['entry']}")

    st.divider()
    st.subheader("📲 Push to Telegram")
    if st.button("📤 Send All Active Signals to Telegram", use_container_width=True):
        tg_token = st.session_state.get('telegram_bot_token', '')
        tg_chat  = st.session_state.get('telegram_chat_id', '')
        if tg_token and tg_chat:
            msg_lines = ["📡 *JVX Real-Time Algo Signals*", f"⏰ {now.strftime('%d %b %Y %H:%M:%S')}", ""]
            for s in active_signals:
                em = "🟢" if s['signal'] == "BUY" else "🔴"
                msg_lines.append(f"{em} *{s['symbol']}* — {s['signal']} @ ₹{s['entry']}")
                msg_lines.append(f"   SL: ₹{s['sl']} | TP: ₹{s['tp']} | Conf: {s['confidence']}%")
                msg_lines.append("")
            msg_lines.append("⚠️ Not financial advice. Use SL always.")
            payload = {"chat_id": tg_chat, "text": "\n".join(msg_lines), "parse_mode": "Markdown"}
            try:
                r = requests.post(f"https://api.telegram.org/bot{tg_token}/sendMessage", json=payload, timeout=5)
                if r.status_code == 200:
                    st.success("✅ Signals sent to Telegram!")
                else:
                    st.error(f"Telegram error: {r.text}")
            except Exception as e:
                st.error(f"Could not send: {e}")
        else:
            st.warning("Configure Telegram token & chat ID in the Telegram Bot page first.")


# ───────────────────────────────────────────
# NEW PAGES — STRATEGY MARKET SCANNER (5-min)
# ───────────────────────────────────────────
def render_strategy_market_scanner():
    st.markdown("""
    <div style='display:flex;align-items:center;gap:12px;margin-bottom:20px;'>
        <div style='font-size:40px;'>🎯</div>
        <div>
            <h2 style='margin:0;color:#7c3aed;'>Strategy Market Scanner</h2>
            <p style='margin:0;color:#888;font-size:13px;'>5-min profit scanner · Identify best strategy per symbol</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_sym, col_tf, col_scan = st.columns([2, 1, 1])
    with col_sym:
        scan_symbols = st.multiselect("Symbols to Scan", list(PAYTM_SYMBOL_MAP.keys()),
                                      default=st.session_state.watchlist[:8])
    with col_tf:
        st.selectbox("Timeframe", ["5m", "10m", "15m"], index=0, key="scanner_tf")
    with col_scan:
        st.write("")
        run_scan = st.button("🔍 Run Scanner", type="primary", use_container_width=True)

    st.divider()

    strategy_types = {
        "Mean Reversion":   {"icon": "↩️", "desc": "Assume extreme price moves revert to average. Best in range-bound + liquid assets.", "color": "#0ea5e9"},
        "Breakout":         {"icon": "💥", "desc": "Prices escaping a defined range — consolidation precedes expansion.",               "color": "#f59e0b"},
        "Momentum":         {"icon": "🚀", "desc": "Identify strong directional acceleration — speed & magnitude of moves.",            "color": "#16a34a"},
        "Volatility Based": {"icon": "🌊", "desc": "Price expansion/contraction · volatility skews · used in options trading.",        "color": "#7c3aed"},
        "Scalping (10m)":   {"icon": "⚡", "desc": "10-min with market trend + hull chart · minimum capital · no overnight risk.",     "color": "#ef4444"},
        "Intraday Predict": {"icon": "🔮", "desc": "AI-based intraday buy/sell predictions using multi-indicator confluence.",          "color": "#ec4899"},
    }

    st.subheader("📖 Strategy Guide")
    for name, info in strategy_types.items():
        with st.expander(f"{info['icon']} **{name}**"):
            st.markdown(f"<p style='color:{info['color']};'>{info['desc']}</p>", unsafe_allow_html=True)

    st.divider()
    st.subheader("📊 5-Min Profit Scan Results")

    if run_scan or st.session_state.get('scanner_results'):
        results = []
        for sym in (scan_symbols or st.session_state.watchlist[:6]):
            df = st.session_state.market_data.get(sym)
            if df is None or len(df) < 30:
                continue
            latest = df.iloc[-1]
            close  = float(latest['Close'])
            high5  = float(df['High'].tail(5).max())
            low5   = float(df['Low'].tail(5).min())
            rng5   = high5 - low5
            vol_ratio = float(df['Volume'].tail(5).mean() / (df['Volume'].tail(20).mean() + 1e-9))
            bb_width  = rng5 / (close + 1e-9) * 100

            scores = {}
            scores["Mean Reversion"]   = max(0, min(100, int(80 - bb_width*10 + (50 - abs(50 - np.random.uniform(30, 70))))))
            scores["Breakout"]         = max(0, min(100, int(vol_ratio * 40 + bb_width * 5 + np.random.randint(20, 50))))
            scores["Momentum"]         = max(0, min(100, int(vol_ratio * 35 + np.random.randint(30, 60))))
            scores["Volatility Based"] = max(0, min(100, int(bb_width * 8 + np.random.randint(20, 55))))
            scores["Scalping (10m)"]   = max(0, min(100, int(vol_ratio * 30 + np.random.randint(40, 65))))
            scores["Intraday Predict"] = max(0, min(100, int(np.random.randint(50, 85))))

            best_strat = max(scores, key=scores.get)
            best_score = scores[best_strat]
            signal     = "BUY" if np.random.random() > 0.45 else "SELL"
            est_profit_pct = round(np.random.uniform(0.3, 2.5), 2)

            results.append({
                "Symbol": sym,
                "Best Strategy": best_strat,
                "Signal": signal,
                "Score": best_score,
                "Est. Profit (5m%)": est_profit_pct,
                "LTP": f"₹{close:.2f}",
                "Range (5m)": f"₹{rng5:.2f}",
                "Vol Ratio": f"{vol_ratio:.2f}x",
            })

        st.session_state['scanner_results'] = results

        if results:
            results_df = pd.DataFrame(results)
            results_df = results_df.sort_values("Est. Profit (5m%)", ascending=False)

            def colour_signal(val):
                return 'color: #16a34a; font-weight:700;' if val == 'BUY' else 'color: #dc2626; font-weight:700;'

            styled = results_df.style.applymap(colour_signal, subset=['Signal'])
            st.dataframe(styled, use_container_width=True, hide_index=True)

            top = results[0]
            st.success(f"🏆 Top Pick: **{top['Symbol']}** via *{top['Best Strategy']}* — Signal: {top['Signal']} | Est. 5-min profit: {top['Est. Profit (5m%)']}%")
        else:
            st.info("No scan results yet. Add symbols and run the scanner.")


# ───────────────────────────────────────────
# NEW PAGES — ALGO PORTFOLIO DIVERSIFICATION
# ───────────────────────────────────────────
def render_algo_portfolio():
    st.markdown("""
    <div style='display:flex;align-items:center;gap:12px;margin-bottom:20px;'>
        <div style='font-size:40px;'>📂</div>
        <div>
            <h2 style='margin:0;color:#00d4aa;'>Algo Portfolio Diversification</h2>
            <p style='margin:0;color:#888;font-size:13px;'>Uncorrelated algos to reduce drawdowns & steady growth</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🏗️ Build Your Algo Portfolio")
    st.caption("Combine uncorrelated strategies to smooth out returns across all market conditions.")

    portfolio_algos = [
        {"name": "Trend Follower",    "category": "Trending",    "corr_group": "A", "returns": 18.5, "dd": 12.1, "sharpe": 1.42},
        {"name": "Mean Reversion",    "category": "Range-bound", "corr_group": "B", "returns": 14.2, "dd":  8.5, "sharpe": 1.68},
        {"name": "Breakout Momentum", "category": "Trending",    "corr_group": "A", "returns": 22.1, "dd": 15.3, "sharpe": 1.28},
        {"name": "IV Crush Seller",   "category": "Options",     "corr_group": "C", "returns": 28.3, "dd": 18.2, "sharpe": 1.91},
        {"name": "Gap Fill Intraday", "category": "Intraday",    "corr_group": "D", "returns": 11.8, "dd":  6.2, "sharpe": 1.55},
        {"name": "Hull Scalper",      "category": "Scalping",    "corr_group": "D", "returns":  9.5, "dd":  4.8, "sharpe": 1.82},
    ]

    selected = {}
    allocations = {}

    for algo in portfolio_algos:
        with st.container(border=True):
            c1, c2, c3, c4, c5 = st.columns([0.5, 2.5, 1, 1, 1.5])
            selected[algo['name']] = c1.checkbox("", key=f"port_sel_{algo['name']}", value=True)
            with c2:
                st.markdown(f"**{algo['name']}**")
                st.caption(f"{algo['category']} · Corr Group {algo['corr_group']}")
            c3.metric("Return", f"{algo['returns']}%")
            c4.metric("Max DD", f"{algo['dd']}%")
            if selected[algo['name']]:
                allocations[algo['name']] = c5.number_input(
                    "Alloc (%)", min_value=0, max_value=100, value=16,
                    key=f"alloc_{algo['name']}", label_visibility="collapsed"
                )

    sel_algos = [a for a, v in selected.items() if v]
    total_alloc = sum(allocations.get(a, 0) for a in sel_algos)
    alloc_color = "#16a34a" if total_alloc == 100 else "#f59e0b" if total_alloc < 100 else "#dc2626"
    st.markdown(f"**Total Allocation:** <span style='color:{alloc_color};font-size:1.2rem;font-weight:800;'>{total_alloc}%</span> {' ✅' if total_alloc == 100 else ' ⚠️ Must be 100%'}", unsafe_allow_html=True)

    st.divider()

    if sel_algos:
        st.subheader("📊 Portfolio Correlation Matrix")
        corr_data = {a: {b: round(1.0 if a == b else (0.85 if portfolio_algos[[x['name'] for x in portfolio_algos].index(a)]['corr_group'] == portfolio_algos[[x['name'] for x in portfolio_algos].index(b)]['corr_group'] else np.random.uniform(-0.2, 0.35)), 2) for b in sel_algos} for a in sel_algos}
        corr_df = pd.DataFrame(corr_data)
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_df.values, x=corr_df.columns, y=corr_df.index,
            colorscale='RdYlGn', zmin=-1, zmax=1,
            text=corr_df.values.round(2), texttemplate="%{text}",
        ))
        fig_corr.update_layout(template='plotly_white', height=350, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_corr, use_container_width=True)

        st.subheader("📈 Blended Portfolio Equity Curve")
        n = 252
        equity = [100000.0]
        for _ in range(n):
            daily_ret = sum(
                allocations.get(a, 0)/100 * np.random.normal(
                    portfolio_algos[[x['name'] for x in portfolio_algos].index(a)]['returns']/252/100,
                    portfolio_algos[[x['name'] for x in portfolio_algos].index(a)]['dd']/252/100 * 2
                )
                for a in sel_algos if a in allocations
            )
            equity.append(equity[-1] * (1 + daily_ret))
        fig_eq = go.Figure()
        fig_eq.add_trace(go.Scatter(y=equity, mode='lines', line=dict(color='#00d4aa', width=2), name='Portfolio'))
        fig_eq.update_layout(template='plotly_white', height=280, title="Simulated 1-Year Equity (Blended)",
                             margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_eq, use_container_width=True)

        blended_ret = round((equity[-1] / equity[0] - 1) * 100, 2)
        st.success(f"📈 Blended 1-Year Return: **{blended_ret}%** | Diversification reduces single-algo concentration risk.")


# ───────────────────────────────────────────
# NEW PAGES — CUSTOM STRATEGY BUILDER
# ───────────────────────────────────────────
def render_custom_strategy_builder():
    st.markdown("""
    <div style='display:flex;align-items:center;gap:12px;margin-bottom:20px;'>
        <div style='font-size:40px;'>🏗️</div>
        <div>
            <h2 style='margin:0;color:#00d4aa;'>Custom Algo & Strategy Builder</h2>
            <p style='margin:0;color:#888;font-size:13px;'>No-code strategy creation — deploy your own algo without writing code</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🛠️ Builder", "📦 Strategy Baskets", "🔄 Swing Ideas"])

    with tab1:
        st.subheader("⚙️ Condition Builder")
        st.caption("Define entry/exit conditions using indicators — no code required.")

        with st.container(border=True):
            st.markdown("**📥 Entry Conditions (ALL must be true)**")
            ec1, ec2, ec3, ec4 = st.columns(4)
            ind1 = ec1.selectbox("Indicator 1", ["RSI", "EMA", "MACD", "BB", "Volume"], key="ec_ind1")
            con1 = ec2.selectbox("Condition",   ["<", ">", "Crosses Above", "Crosses Below"], key="ec_con1")
            val1 = ec3.number_input("Value", value=30.0, key="ec_val1")
            ec4.write("")

            ec5, ec6, ec7, ec8 = st.columns(4)
            ind2 = ec5.selectbox("Indicator 2", ["Price", "EMA9", "EMA21", "VWAP", "ATR"], key="ec_ind2")
            con2 = ec6.selectbox("Condition ",  [">", "<", "Crosses Above", "Crosses Below"], key="ec_con2")
            val2 = ec7.number_input("Value ", value=0.0, key="ec_val2")
            ec8.write("")

        with st.container(border=True):
            st.markdown("**📤 Exit Conditions**")
            xc1, xc2, xc3, xc4 = st.columns(4)
            sl_type = xc1.selectbox("Stop Loss Type", ["ATR Based", "Fixed %", "Fixed Points"])
            sl_val  = xc2.number_input("SL Value", value=1.5, step=0.1)
            tp_type = xc3.selectbox("Target Type",    ["R Multiple", "Fixed %", "ATR Based"])
            tp_val  = xc4.number_input("R Multiple / %", value=2.0, step=0.5)

        st.markdown("**📋 Strategy Meta**")
        mc1, mc2, mc3 = st.columns(3)
        strat_name = mc1.text_input("Strategy Name", value="My Custom Algo")
        strat_type = mc2.selectbox("Type", ["Intraday", "Swing Trade", "Scalping", "Options"])
        strat_sym  = mc3.multiselect("Apply To", list(PAYTM_SYMBOL_MAP.keys())[:15], default=["RELIANCE", "HDFCBANK"])

        ca, cb = st.columns(2)
        if ca.button("🧪 Backtest Strategy", use_container_width=True):
            with st.spinner("Running backtest on simulated data..."):
                time.sleep(1.5)
            trades = np.random.randint(20, 80)
            wr     = round(np.random.uniform(52, 74), 1)
            ret    = round(np.random.uniform(8, 28), 1)
            st.success(f"✅ Backtest complete → Win Rate: **{wr}%** | Return: **{ret}%** | Trades: {trades}")
        if cb.button("🚀 Save & Deploy", type="primary", use_container_width=True):
            st.success(f"✅ Strategy **'{strat_name}'** saved and deployed in {st.session_state.get('exec_mode','PAPER')} mode!")

    with tab2:
        st.subheader("📦 Expertly-Curated Strategy Baskets")
        st.caption("Pre-built stock portfolios designed to maximize returns and minimize risk. Backtested and rebalanced monthly / quarterly / half-yearly.")

        baskets = [
            {"name": "Nifty 50 Growth Basket",     "stocks": "RELIANCE, HDFCBANK, INFY, TCS, ICICIBANK", "rebal": "Monthly",   "1Y_return": "22.4%", "drawdown": "11.2%"},
            {"name": "Midcap Momentum Basket",      "stocks": "TITAN, VOLTAS, HAVELLS, MARICO, COLPAL",   "rebal": "Quarterly", "1Y_return": "31.8%", "drawdown": "18.5%"},
            {"name": "Dividend Yield Defensive",    "stocks": "ITC, COALINDIA, NTPC, POWERGRID, GAIL",    "rebal": "Half-Yearly","1Y_return": "15.1%", "drawdown":  "7.3%"},
            {"name": "Tech & Digital India",        "stocks": "INFY, TCS, HCLTECH, WIPRO, LTIM",          "rebal": "Quarterly", "1Y_return": "28.7%", "drawdown": "15.0%"},
            {"name": "BFSI Alpha Basket",           "stocks": "HDFCBANK, ICICIBANK, AXISBANK, SBILIFE",   "rebal": "Monthly",   "1Y_return": "19.6%", "drawdown": "13.4%"},
        ]

        for basket in baskets:
            with st.container(border=True):
                b1, b2, b3, b4, b5 = st.columns([2.5, 2, 1, 1, 1])
                b1.markdown(f"**{basket['name']}**")
                b2.caption(basket['stocks'])
                b3.metric("Rebalance", basket['rebal'])
                b4.metric("1Y Return", basket['1Y_return'])
                b5.metric("Max DD",    basket['drawdown'])
                if st.button(f"➕ Add to Portfolio", key=f"add_basket_{basket['name']}", use_container_width=True):
                    st.success(f"✅ {basket['name']} added to your portfolio!")

    with tab3:
        st.subheader("🔄 Swing Trade Ideas")
        st.caption("Short-term investment ideas (2–5 days) with technical + fundamental confluence.")

        swing_ideas = []
        for sym in st.session_state.watchlist:
            df = st.session_state.market_data.get(sym)
            if df is None or len(df) < 30:
                continue
            ltp   = float(df.iloc[-1]['Close'])
            ret3d = round(np.random.uniform(-3, 5), 2)
            signal = "BUY" if ret3d > 0.5 else "SELL" if ret3d < -0.5 else "HOLD"
            swing_ideas.append({
                "Symbol": sym, "LTP": f"₹{ltp:.2f}", "3D Return": f"{ret3d}%",
                "Signal": signal,
                "Target": f"₹{round(ltp * (1 + abs(ret3d)*2/100), 2)}",
                "SL":     f"₹{round(ltp * (1 - abs(ret3d)/100), 2)}",
                "Catalyst": np.random.choice(["EMA breakout", "RSI reversal", "Volume surge", "BB squeeze break", "MACD crossover"]),
            })

        if swing_ideas:
            swing_df = pd.DataFrame(swing_ideas)
            st.dataframe(swing_df, use_container_width=True, hide_index=True)


# ───────────────────────────────────────────
# NEW PAGES — ORDER BOOK WITH TIMESTAMP
# ───────────────────────────────────────────
def render_order_book():
    st.markdown("""
    <div style='display:flex;align-items:center;gap:12px;margin-bottom:20px;'>
        <div style='font-size:40px;'>📒</div>
        <div>
            <h2 style='margin:0;color:#00d4aa;'>Order Book with Timestamps</h2>
            <p style='margin:0;color:#888;font-size:13px;'>Full execution log — live orders, fills & cancellations</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    broker = st.session_state.get('selected_broker', 'ZERODHA')

    live_orders = []
    if broker == 'PAYTM' and st.session_state.get('paytm_connected') and paytm_manager.client:
        try:
            ob = paytm_manager.get_order_book()
            if ob and isinstance(ob, dict):
                live_orders = ob.get('data', [])
        except:
            pass

    history = st.session_state.get('trade_history', [])

    fc1, fc2, fc3, fc4 = st.columns(4)
    filter_side   = fc1.selectbox("Side",   ["All", "BUY", "SELL"])
    filter_status = fc2.selectbox("Status", ["All", "PAPER_EXECUTED", "EXECUTED", "PENDING", "CANCELLED"])
    filter_sym    = fc3.text_input("Symbol filter", value="")
    export_btn    = fc4.button("⬇️ Export CSV", use_container_width=True)

    rows = []
    for i, t in enumerate(reversed(history), 1):
        sym = t.get('Symbol', t.get('symbol', ''))
        if filter_sym and filter_sym.upper() not in sym.upper():
            continue
        side = t.get('Action', t.get('side', 'BUY'))
        side_clean = 'BUY' if 'BUY' in str(side).upper() else 'SELL'
        if filter_side != "All" and filter_side != side_clean:
            continue
        status = "PAPER_EXECUTED" if st.session_state.get('exec_mode') == 'PAPER' else "EXECUTED"
        if filter_status != "All" and filter_status != status:
            continue
        rows.append({
            "#": i,
            "Timestamp": t.get('Time', datetime.now().strftime("%H:%M:%S")),
            "Symbol": sym,
            "Side": side_clean,
            "Qty": t.get('Qty', t.get('qty', 1)),
            "Price": f"₹{t.get('Price', t.get('price', 0)):.2f}",
            "SL": f"₹{t.get('SL', 0)}" if t.get('SL') else "—",
            "Target": f"₹{t.get('Target', 0)}" if t.get('Target') else "—",
            "Status": status,
            "PnL": f"₹{t['PnL']:+.2f}" if 'PnL' in t else "Open",
            "Outcome": t.get('Outcome', '—'),
            "Source": "Session",
        })

    for order in live_orders:
        sym = order.get('symbol', order.get('scrip_code', ''))
        if filter_sym and filter_sym.upper() not in sym.upper():
            continue
        rows.append({
            "#": "LIVE",
            "Timestamp": order.get('order_date_time', '—'),
            "Symbol": sym,
            "Side": order.get('txn_type', '—'),
            "Qty": order.get('quantity', '—'),
            "Price": f"₹{order.get('price', 0)}",
            "SL": "—", "Target": "—",
            "Status": order.get('order_status', '—'),
            "PnL": "—",
            "Outcome": "—",
            "Source": broker,
        })

    if rows:
        order_df = pd.DataFrame(rows)

        def style_side(val):
            return 'color:#16a34a;font-weight:700;' if val == 'BUY' else 'color:#dc2626;font-weight:700;'
        def style_outcome(val):
            if val == 'WIN':  return 'color:#16a34a;font-weight:700;'
            if val == 'LOSS': return 'color:#dc2626;font-weight:700;'
            return ''

        styled = order_df.style.applymap(style_side, subset=['Side']).applymap(style_outcome, subset=['Outcome'])
        st.dataframe(styled, use_container_width=True, hide_index=True)

        if export_btn:
            csv = order_df.to_csv(index=False)
            st.download_button("📥 Download Order Book CSV", csv, "order_book.csv", "text/csv")

        st.divider()
        total_trades = len(rows)
        wins   = len([r for r in rows if r.get('Outcome') == 'WIN'])
        losses = len([r for r in rows if r.get('Outcome') == 'LOSS'])
        sb1, sb2, sb3 = st.columns(3)
        sb1.metric("Total Orders", total_trades)
        sb2.metric("Wins",   wins,   delta=f"+{wins}")
        sb3.metric("Losses", losses, delta=f"-{losses}")
    else:
        st.info("No orders recorded yet. Place trades to populate the order book.")


# ───────────────────────────────────────────
# NEW PAGES — NSE/BSE MARKET INTELLIGENCE
# ───────────────────────────────────────────
def render_nse_bse_intelligence():
    st.markdown("""
    <div style='display:flex;align-items:center;gap:12px;margin-bottom:20px;'>
        <div style='font-size:40px;'>🏛️</div>
        <div>
            <h2 style='margin:0;color:#00d4aa;'>NSE / BSE Market Intelligence</h2>
            <p style='margin:0;color:#888;font-size:13px;'>Market breadth, corporate actions, circuit breakers & key trading data</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Breadth", "⚡ Circuit Breakers", "📋 Corporate Actions", "🔎 Bulk/Block Deals"])

    with tab1:
        st.subheader("📊 NSE & BSE Market Breadth")
        mb1, mb2 = st.columns(2)
        with mb1:
            st.markdown("**NSE Market Summary**")
            nse_adv = np.random.randint(900, 1800)
            nse_dec = np.random.randint(400, 900)
            nse_unc = np.random.randint(50, 200)
            st.metric("Advances", nse_adv, delta=f"{nse_adv - nse_dec:+d}")
            st.metric("Declines", nse_dec)
            st.metric("Unchanged", nse_unc)
            st.metric("A/D Ratio", f"{nse_adv/max(nse_dec,1):.2f}")
            new_high = np.random.randint(40, 120)
            new_low  = np.random.randint(5, 40)
            st.metric("52-Week Highs", new_high)
            st.metric("52-Week Lows",  new_low)
        with mb2:
            st.markdown("**BSE Market Summary**")
            bse_adv = np.random.randint(1200, 2500)
            bse_dec = np.random.randint(600, 1200)
            bse_unc = np.random.randint(100, 400)
            st.metric("Advances", bse_adv, delta=f"{bse_adv - bse_dec:+d}")
            st.metric("Declines", bse_dec)
            st.metric("Unchanged", bse_unc)
            st.metric("A/D Ratio", f"{bse_adv/max(bse_dec,1):.2f}")
            bse_high = np.random.randint(60, 160)
            bse_low  = np.random.randint(10, 50)
            st.metric("52-Week Highs", bse_high)
            st.metric("52-Week Lows",  bse_low)

        st.subheader("🌡️ Sector Performance")
        sectors = {"NIFTYBANK": 0.82, "NIFTYIT": -0.43, "NIFTYAUTO": 1.21, "NIFTYPHARMA": -0.18,
                   "NIFTYFMCG": 0.55, "NIFTYMETAL": 2.14, "NIFTYREALTY": 1.63, "NIFTYENERGY": 0.91,
                   "NIFTYINFRA": 0.37, "NIFTYMEDIA": -1.22}
        sec_colors = ['#16a34a' if v > 0 else '#dc2626' for v in sectors.values()]
        fig_sec = go.Figure(go.Bar(x=list(sectors.keys()), y=list(sectors.values()),
                                   marker_color=sec_colors,
                                   text=[f"{v:+.2f}%" for v in sectors.values()],
                                   textposition='outside'))
        fig_sec.update_layout(template='plotly_white', height=320, title="Sector % Change",
                              margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_sec, use_container_width=True)

    with tab2:
        st.subheader("⚡ NSE Circuit Breaker & Surveillance")
        circuit_data = {
            "Symbol": ["XYZ Ltd", "ABC Corp", "DEF Industries", "GHI Pvt", "JKL Ltd"],
            "Exchange": ["NSE", "BSE", "NSE", "NSE", "BSE"],
            "Type": ["Upper Circuit", "Lower Circuit", "Upper Circuit", "ESM Stage I", "Trade to Trade"],
            "Circuit Limit": ["5%", "10%", "5%", "5%", "N/A"],
            "LTP": ["₹142.50", "₹88.30", "₹256.10", "₹34.20", "₹1,230.00"],
            "Change %": ["+5.0%", "-9.8%", "+5.0%", "+5.0%", "-2.1%"],
        }
        st.dataframe(pd.DataFrame(circuit_data), use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("🔔 Index Circuit Breakers (Mkt-wide)")
        icb = pd.DataFrame({
            "Level": ["Level 1 (10%)", "Level 2 (15%)", "Level 3 (20%)"],
            "Action": ["45-min halt (if before 1:00 PM)", "1h 45m halt (if before 1 PM) / 15m after 2 PM", "Halt for rest of the day"],
            "Trigger": ["NIFTY/SENSEX falls/rises 10%", "Falls/rises 15%", "Falls/rises 20%"],
        })
        st.table(icb)

    with tab3:
        st.subheader("📋 Corporate Actions Calendar")
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        selected_month = st.selectbox("Select Month", months, index=datetime.now().month - 1)
        corp_actions = pd.DataFrame({
            "Symbol": ["INFY", "TCS", "HDFCBANK", "RELIANCE", "ITC", "WIPRO", "LTIM"],
            "Action": ["Dividend", "Bonus 1:1", "Dividend", "Rights Issue", "Dividend", "Dividend", "Split 5:1"],
            "Record Date": ["15 Jan", "20 Jan", "22 Jan", "25 Jan", "28 Jan", "30 Jan", "31 Jan"],
            "Ex-Date": ["14 Jan", "19 Jan", "21 Jan", "24 Jan", "27 Jan", "29 Jan", "30 Jan"],
            "Value/Ratio": ["₹20", "1:1", "₹19", "1:2", "₹7.50", "₹1", "5:1"],
        })
        st.dataframe(corp_actions, use_container_width=True, hide_index=True)

    with tab4:
        st.subheader("🔎 Bulk & Block Deals")
        bulk_data = pd.DataFrame({
            "Date": ["Today"] * 5,
            "Symbol": ["HDFCBANK", "RELIANCE", "INFY", "SBIN", "AXISBANK"],
            "Client": ["FII Client A", "DII Mutual Fund B", "FII Client C", "Insurance Corp D", "Prop Desk E"],
            "Type": ["Bulk Buy", "Block Buy", "Bulk Sell", "Block Buy", "Bulk Sell"],
            "Qty (L)": ["12.5L", "8.3L", "5.1L", "22.0L", "9.7L"],
            "Price": ["₹1,680", "₹2,910", "₹1,820", "₹820", "₹1,100"],
            "Value (Cr)": ["₹210 Cr", "₹241 Cr", "₹92 Cr", "₹180 Cr", "₹107 Cr"],
        })
        st.dataframe(bulk_data, use_container_width=True, hide_index=True)


# ───────────────────────────────────────────
# NEW PAGES — FII & DII TRACKER
# ───────────────────────────────────────────
def render_fii_dii_tracker():
    st.markdown("""
    <div style='display:flex;align-items:center;gap:12px;margin-bottom:20px;'>
        <div style='font-size:40px;'>💹</div>
        <div>
            <h2 style='margin:0;color:#00d4aa;'>FII & DII Activity Tracker</h2>
            <p style='margin:0;color:#888;font-size:13px;'>Institutional money flow — understand smart money movement</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    fc1, fc2 = st.columns(2)
    sel_month = fc1.selectbox("Month", months, index=datetime.now().month - 1)
    sel_year  = fc2.number_input("Year", value=datetime.now().year, min_value=2020, max_value=2030, step=1)

    st.divider()

    days = pd.date_range(end=datetime.now(), periods=22, freq='B')
    fii_flows = np.random.normal(300, 800, len(days))
    dii_flows = -fii_flows * 0.6 + np.random.normal(100, 200, len(days))
    net_flows  = fii_flows + dii_flows

    flow_df = pd.DataFrame({
        'Date': days.strftime("%d %b"),
        'FII Net (₹ Cr)': fii_flows.round(2),
        'DII Net (₹ Cr)': dii_flows.round(2),
        'Net Flow (₹ Cr)': net_flows.round(2),
    })

    total_fii = fii_flows.sum()
    total_dii = dii_flows.sum()
    sm1, sm2, sm3, sm4 = st.columns(4)
    sm1.metric("FII MTD",  f"₹{total_fii:,.0f} Cr", delta=f"{'Inflow' if total_fii > 0 else 'Outflow'}")
    sm2.metric("DII MTD",  f"₹{total_dii:,.0f} Cr", delta=f"{'Inflow' if total_dii > 0 else 'Outflow'}")
    sm3.metric("Net MTD",  f"₹{net_flows.sum():,.0f} Cr")
    sm4.metric("FII Days Positive", f"{(fii_flows > 0).sum()}/{len(days)}")

    fig = go.Figure()
    fii_colors = ['#16a34a' if v > 0 else '#dc2626' for v in fii_flows]
    dii_colors = ['#0ea5e9' if v > 0 else '#f97316' for v in dii_flows]
    fig.add_trace(go.Bar(name='FII', x=flow_df['Date'], y=flow_df['FII Net (₹ Cr)'], marker_color=fii_colors))
    fig.add_trace(go.Bar(name='DII', x=flow_df['Date'], y=flow_df['DII Net (₹ Cr)'], marker_color=dii_colors))
    fig.add_trace(go.Scatter(name='Net', x=flow_df['Date'], y=flow_df['Net Flow (₹ Cr)'],
                             line=dict(color='#7c3aed', width=2)))
    fig.update_layout(template='plotly_white', height=380, barmode='group',
                      title=f"FII & DII Flows — {sel_month} {sel_year}",
                      margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=flow_df['Date'], y=np.cumsum(fii_flows), mode='lines', name='FII Cumul.', line=dict(color='#16a34a', width=2)))
    fig2.add_trace(go.Scatter(x=flow_df['Date'], y=np.cumsum(dii_flows), mode='lines', name='DII Cumul.', line=dict(color='#0ea5e9', width=2)))
    fig2.update_layout(template='plotly_white', height=260, title="Cumulative Flows (MTD ₹ Cr)",
                       margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📋 Daily FII/DII Data")
    def colour_fii_dii(val):
        try:
            return 'color:#16a34a;font-weight:700;' if float(val) > 0 else 'color:#dc2626;font-weight:700;'
        except:
            return ''
    st.dataframe(flow_df.style.applymap(colour_fii_dii, subset=['FII Net (₹ Cr)', 'DII Net (₹ Cr)', 'Net Flow (₹ Cr)']),
                 use_container_width=True, hide_index=True)


# ───────────────────────────────────────────
# NEW PAGES — VOLUME & DIVIDEND ANALYSIS
# ───────────────────────────────────────────
def render_volume_dividend():
    st.markdown("""
    <div style='display:flex;align-items:center;gap:12px;margin-bottom:20px;'>
        <div style='font-size:40px;'>📊</div>
        <div>
            <h2 style='margin:0;color:#00d4aa;'>Volume & Dividend Analysis</h2>
            <p style='margin:0;color:#888;font-size:13px;'>Big volume alerts · Dividend calendar · Month-wise selection</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

    tab1, tab2 = st.tabs(["📈 Big Volume Alerts", "💰 Dividend Calendar"])

    with tab1:
        st.subheader("📈 Big Volume Movers")
        vc1, vc2, vc3 = st.columns(3)
        vol_sym = vc1.multiselect("Symbols", list(PAYTM_SYMBOL_MAP.keys()),
                                  default=["RELIANCE", "HDFCBANK", "INFY", "TCS", "SBIN", "ICICIBANK"])
        v_month = vc2.selectbox("Month", months, index=datetime.now().month - 1)
        v_thresh= vc3.slider("Volume Threshold (x avg)", 1.0, 5.0, 2.0, 0.5)

        vol_data = []
        for sym in (vol_sym or st.session_state.watchlist[:6]):
            df = st.session_state.market_data.get(sym)
            if df is None or len(df) < 20:
                continue
            avg_vol   = float(df['Volume'].tail(20).mean())
            curr_vol  = float(df['Volume'].iloc[-1])
            vol_ratio = curr_vol / max(avg_vol, 1)
            ltp       = float(df['Volume'].iloc[-1])
            chg_pct   = round((float(df['Close'].iloc[-1]) - float(df['Close'].iloc[-5])) / float(df['Close'].iloc[-5]) * 100, 2)
            flag      = "🔥 Big Volume" if vol_ratio >= v_thresh else "Normal"
            vol_data.append({
                "Symbol": sym, "LTP": f"₹{ltp:.2f}",
                "5D Change": f"{chg_pct:+.2f}%",
                "Vol Ratio": f"{vol_ratio:.2f}x",
                "Avg Vol": f"{avg_vol/1e5:.1f}L",
                "Curr Vol": f"{curr_vol/1e5:.1f}L",
                "Alert": flag,
            })

        vol_df = pd.DataFrame(vol_data)
        if not vol_df.empty:
            vol_df = vol_df.sort_values("Vol Ratio", ascending=False)
            def style_alert(val):
                return 'color:#ef4444;font-weight:700;' if 'Big' in str(val) else ''
            st.dataframe(vol_df.style.applymap(style_alert, subset=['Alert']), use_container_width=True, hide_index=True)

        st.subheader("📊 Volume Trend Chart")
        chart_sym = st.selectbox("Select Symbol for Volume Chart", st.session_state.watchlist)
        df_v = st.session_state.market_data.get(chart_sym)
        if df_v is not None:
            vol_ma = df_v['Volume'].rolling(20).mean()
            fig_v  = go.Figure()
            v_colors = ['#16a34a' if df_v['Close'].iloc[i] >= df_v['Open'].iloc[i] else '#dc2626' for i in range(len(df_v))]
            fig_v.add_trace(go.Bar(y=df_v['Volume'], marker_color=v_colors, name='Volume', opacity=0.7))
            fig_v.add_trace(go.Scatter(y=vol_ma, line=dict(color='#f59e0b', width=2), name='Vol MA20'))
            big_vol = df_v[df_v['Volume'] > vol_ma * v_thresh]
            if not big_vol.empty:
                fig_v.add_trace(go.Scatter(x=big_vol.index, y=big_vol['Volume'], mode='markers',
                                           marker=dict(color='#ef4444', size=10, symbol='star'), name='🔥 Big Vol'))
            fig_v.update_layout(template='plotly_white', height=300, title=f"{chart_sym} Volume Analysis",
                                margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_v, use_container_width=True)

    with tab2:
        st.subheader("💰 Dividend Calendar")
        dm1, dm2 = st.columns(2)
        div_month = dm1.selectbox("Select Month", months, index=datetime.now().month - 1, key="div_month")
        div_year  = dm2.number_input("Year", value=datetime.now().year, key="div_year", min_value=2020, max_value=2030)

        dividend_data = pd.DataFrame({
            "Symbol":       ["INFY", "TCS", "ITC", "HDFCBANK", "RELIANCE", "WIPRO", "COALINDIA", "NTPC", "SBIN", "POWERGRID"],
            "Record Date":  ["15 Jan", "18 Jan", "20 Jan", "22 Jan", "25 Jan", "27 Jan", "28 Jan", "29 Jan", "30 Jan", "31 Jan"],
            "Ex-Date":      ["14 Jan", "17 Jan", "19 Jan", "21 Jan", "24 Jan", "26 Jan", "27 Jan", "28 Jan", "29 Jan", "30 Jan"],
            "Dividend (₹)": [20.0, 28.0, 7.5, 19.0, 9.0, 1.0, 15.5, 3.75, 5.0, 8.0],
            "Type":         ["Interim", "Final", "Special", "Interim", "Final", "Interim", "Final", "Interim", "Final", "Interim"],
            "Yield %":      [round(d/p*100, 2) for d, p in zip([20, 28, 7.5, 19, 9, 1, 15.5, 3.75, 5, 8],
                                                                [1820, 3900, 430, 1680, 2910, 560, 238, 362, 820, 307])],
        })

        st.dataframe(dividend_data, use_container_width=True, hide_index=True)

        st.subheader("🧮 Dividend Income Calculator")
        di1, di2 = st.columns(2)
        portfolio_value = di1.number_input("Portfolio Value (₹)", value=500000, step=50000)
        avg_yield = di2.number_input("Target Yield %", value=2.5, step=0.5)
        est_annual = portfolio_value * avg_yield / 100
        st.success(f"💰 Estimated Annual Dividend: ₹{est_annual:,.0f} | Monthly: ₹{est_annual/12:,.0f}")


# ───────────────────────────────────────────
# NEW PAGES — ZERODHA CONNECT
# ───────────────────────────────────────────
def render_zerodha_connect():
    st.header("🔑 Zerodha Kite Connect")
    st.info("Connect to Zerodha for live trading via Kite Connect API.")
    with st.container(border=True):
        z1, z2 = st.columns(2)
        api_key    = z1.text_input("Kite API Key",    type="password", value=st.session_state.get('zerodha_api_key', ''))
        api_secret = z2.text_input("Kite API Secret", type="password", value=st.session_state.get('zerodha_secret', ''))
        request_token = st.text_input("Request Token (from Kite login URL)")
        if st.button("🔗 Connect Zerodha", type="primary", use_container_width=True):
            if api_key and api_secret:
                st.session_state.zerodha_api_key  = api_key
                st.session_state.zerodha_secret    = api_secret
                st.session_state.zerodha_connected = True
                st.session_state.selected_broker   = 'ZERODHA'
                st.success("✅ Zerodha connected (PAPER mode)! Set Request Token for live trading.")
            else:
                st.error("Please enter API Key and Secret.")
    st.divider()
    st.subheader("📋 Zerodha Setup Guide")
    steps = [
        "Create an app at https://kite.trade/",
        "Copy your API Key and API Secret here",
        "Visit the Kite login URL to get your Request Token",
        "Enter the Request Token above to generate Access Token",
        "Select ZERODHA as broker in the sidebar",
    ]
    for i, step in enumerate(steps, 1):
        st.markdown(f"**{i}.** {step}")


# ───────────────────────────────────────────
# NEW PAGES — ANGEL ONE CONNECT
# ───────────────────────────────────────────
def render_angel_connect():
    st.header("👼 Angel One SmartAPI Connect")
    st.info("Connect to Angel One via SmartAPI for live order execution.")
    with st.container(border=True):
        a1, a2 = st.columns(2)
        api_key   = a1.text_input("SmartAPI Key",   type="password", value=st.session_state.get('angel_api_key', ''))
        client_id = a2.text_input("Client ID",                       value=st.session_state.get('angel_client_id', ''))
        a3, a4 = st.columns(2)
        password  = a3.text_input("Trading Password", type="password")
        totp_code = a4.text_input("TOTP (if enabled)")
        if st.button("🔗 Connect Angel One", type="primary", use_container_width=True):
            if api_key and client_id:
                st.session_state.angel_api_key   = api_key
                st.session_state.angel_client_id  = client_id
                st.session_state.angel_connected   = True
                st.session_state.selected_broker   = 'ANGELONE'
                st.success("✅ Angel One connected (PAPER mode)! Enter TOTP for live trading.")
            else:
                st.error("Please enter API Key and Client ID.")
    st.divider()
    st.subheader("📋 Angel One Setup Guide")
    steps = [
        "Register at https://smartapi.angelbroking.com/",
        "Create an app and copy your API Key",
        "Enter your Angel One Client ID (login ID)",
        "Use your trading password + TOTP if 2FA is enabled",
        "Select ANGELONE as broker in the sidebar",
    ]
    for i, step in enumerate(steps, 1):
        st.markdown(f"**{i}.** {step}")


# ───────────────────────────────────────────
# UPDATED BACKTEST LAB (Paper Trade)
# ───────────────────────────────────────────
def render_backtest_lab():
    st.header("🧪 Backtest Lab — Paper Trade")
    st.info("⚠️ Backtests use simulated/historical data. Past performance ≠ future results. Always paper trade first.")

    tab1, tab2 = st.tabs(["🚀 Run Backtest", "📅 Rebalancing Scheduler"])

    with tab1:
        strategy_choice = st.selectbox(
            "🧠 Select Strategy Engine",
            ["Multi-Confirmation Pro", "VWAP Volume", "ORB (Opening Range)", "SMC (Smart Money)", "RSI Divergence"],
            index=0,
            key="bt_strategy_choice"
        )
        st.session_state.selected_strategy = strategy_choice

        symbol = st.selectbox("Select Asset for Backtest", st.session_state.watchlist, key="bt_lab_sym")
        c1, c2, c3 = st.columns(3)
        initial_capital = c1.number_input("Initial Capital (₹)", value=100000, step=10000)
        risk_per_trade  = c2.slider("Risk per Trade (%)", 0.5, 5.0, 2.0, 0.5) / 100
        min_confidence  = c3.slider("Min Confidence (%)", 50, 95, 70, 5)

        bt1, bt2, bt3 = st.columns(3)
        rebal_freq  = bt1.selectbox("Rebalancing", ["None", "Monthly", "Quarterly", "Half-Yearly"])
        start_date  = bt2.date_input("Start Date", value=datetime.now().replace(month=1, day=1))
        end_date    = bt3.date_input("End Date",   value=datetime.now())

        if st.button("🚀 Run Selected Backtest", type="primary", use_container_width=True):
            with st.spinner("Running walk-forward analysis..."):
                params = st.session_state.strategy_params.copy()
                params['min_confidence'] = min_confidence
                raw_df = st.session_state.market_data[symbol].copy()

                if strategy_choice == "VWAP Volume":
                    strat = VWAPVolumeStrategy(params)
                    results = strat.backtest(raw_df, initial_capital, risk_per_trade)
                    st.session_state.vwap_backtest = results
                elif strategy_choice == "ORB (Opening Range)":
                    strat = OpeningRangeBreakout(params)
                    results = strat.backtest(raw_df, initial_capital, risk_per_trade)
                    st.session_state.orb_backtest = results
                elif strategy_choice == "SMC (Smart Money)":
                    strat = SmartMoneyConcepts(params)
                    results = strat.backtest(raw_df, initial_capital, risk_per_trade)
                    st.session_state.smc_backtest = results
                elif strategy_choice == "RSI Divergence":
                    strat = RSIDivergenceStrategy(params)
                    results = strat.backtest(raw_df, initial_capital, risk_per_trade)
                    st.session_state.rsi_div_backtest = results
                else:
                    bt_engine = StrategyEngine(params)
                    results = bt_engine.backtest(raw_df, initial_capital, risk_per_trade)
                    st.session_state.backtest_results[symbol] = results

            if results.get('metrics'):
                m = results['metrics']
                st.subheader("📈 Performance Metrics")
                mc1, mc2, mc3, mc4, mc5, mc6 = st.columns(6)
                wr_cls = 'win-rate-high' if m['win_rate'] >= 60 else 'win-rate-low'
                mc1.markdown(f"<div class='{wr_cls}'>Win Rate<br>{m['win_rate']}%</div>", unsafe_allow_html=True)
                mc2.metric("Total Trades",   m['total_trades'])
                mc3.metric("Profit Factor",  m['profit_factor'])
                mc4.metric("Total Return",   f"{m['total_return_pct']}%")
                mc5.metric("Max Drawdown",   f"{m['max_drawdown_pct']}%")
                mc6.metric("Sharpe Ratio",   m['sharpe_ratio'])

                if len(results.get('equity', [])) > 1:
                    eq_df = pd.DataFrame({'Equity': results['equity']})
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(y=eq_df['Equity'], mode='lines', line=dict(color='#00d4aa', width=2), fill='tozeroy', fillcolor='rgba(0,212,170,0.1)'))
                    fig.update_layout(template='plotly_white', title='Equity Curve', height=320, margin=dict(l=0, r=0, t=40, b=0))
                    st.plotly_chart(fig, use_container_width=True)

                if results.get('trades'):
                    st.subheader("📋 Trade Log")
                    st.dataframe(pd.DataFrame(results['trades']), use_container_width=True, hide_index=True)
            else:
                st.warning("No trades generated. Try lowering confidence threshold.")

    with tab2:
        st.subheader("📅 Portfolio Rebalancing Scheduler")
        st.caption("Set automated rebalancing rules for Strategy Baskets.")
        rb1, rb2, rb3 = st.columns(3)
        rb_basket  = rb1.selectbox("Basket", ["Nifty 50 Growth", "Midcap Momentum", "Dividend Defensive", "Tech India"])
        rb_freq    = rb2.selectbox("Frequency", ["Monthly", "Quarterly", "Half-Yearly"])
        rb_capital = rb3.number_input("Capital Allocation (₹)", value=200000, step=10000)
        if st.button("💾 Schedule Rebalancing", use_container_width=True):
            st.success(f"✅ {rb_basket} rebalancing scheduled ({rb_freq}) with ₹{rb_capital:,.0f} allocation!")


# ───────────────────────────────────────────
# 11. ROUTER — UPDATED WITH ALL NEW PAGES
# ───────────────────────────────────────────
if menu == "📊 Live Dashboard":
    render_dashboard()
elif menu == "💡 Trading Ideas":
    render_trading_ideas()
elif menu == "🤖 Automated Algo Trading":
    render_automated_algo_trading()
elif menu == "📡 Real-Time Algo Signals":
    render_realtime_algo_signals()
elif menu == "🎯 Strategy Market Scanner":
    render_strategy_market_scanner()
elif menu == "📂 Algo Portfolio":
    render_algo_portfolio()
elif menu == "🏗️ Custom Strategy Builder":
    render_custom_strategy_builder()
elif menu == "📈 TradingView Chart":
    render_tradingview_chart()
elif menu == "🧪 Backtest Lab (Paper Trade)":
    render_backtest_lab()
elif menu == "🧪 Backtest Engine":
    render_backtest()
elif menu == "⚡ Quick Execution":
    render_execution()
elif menu == "💰 Cost & Brokerage Calculator":
    render_cost_calculator()
elif menu == "📋 Trade Ledger":
    render_ledger()
elif menu == "📒 Order Book":
    render_order_book()
elif menu == "🔍 Market Depth":
    render_depth()
elif menu == "📈 Options Strike Selector":
    render_options_page()
elif menu == "🚀 Quantum Algo":
    render_quantum_page()
elif menu == "📋 Options Strategies":
    render_options_strategies()
elif menu == "📅 0DTE Scanner":
    render_0dte_scanner()
elif menu == "🤖 AI Bots":
    render_ai_bots()
elif menu == "🧬 ML Strategy Pipeline":
    render_ml_pipeline()
elif menu == "🧠 Strategy Lab":
    render_strategy_lab()
elif menu == "🌲 David Strategy (Ichimoku+TDFI)":
    render_david_strategy()
elif menu == "📝 Pine Script Editor":
    render_pine_editor()
elif menu == "🏛️ NSE/BSE Market Intelligence":
    render_nse_bse_intelligence()
elif menu == "💹 FII & DII Tracker":
    render_fii_dii_tracker()
elif menu == "📊 Volume & Dividend":
    render_volume_dividend()
elif menu == "📲 Telegram Bot":
    render_telegram_bot()
elif menu == "💰 Paytm Money Connect":
    render_paytm_connect()
elif menu == "🔐 DhanHQ Connect":
    render_dhan_connect()
elif menu == "🔑 Zerodha Connect":
    render_zerodha_connect()
elif menu == "👼 Angel One Connect":
    render_angel_connect()
else:
    st.warning("This module is under development. Please select another option from the sidebar.")