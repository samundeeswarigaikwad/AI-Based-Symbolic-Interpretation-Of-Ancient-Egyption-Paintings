import os
from collections import Counter
from datetime import datetime, timedelta, timezone
from io import BytesIO

import cv2
import numpy as np
import pandas as pd
import streamlit as st
from pymongo import MongoClient
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfgen import canvas

from knowledge_base import SYMBOL_MEANINGS, SYMBOL_NORMALIZATION
from modules.detector import detect_symbols
from symbolic_interpreter import generate_interpretation


# =============================================================================
# CONFIG & CONSTANTS
# =============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
DETECTED_DIR = os.path.join(BASE_DIR, "static", "detections")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = "egyptian_symbol_system"
MONGO_COLLECTION = "detection"
IST_TZ = timezone(timedelta(hours=5, minutes=30), name="IST")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DETECTED_DIR, exist_ok=True)

st.set_page_config(
    page_title="Egyptian Symbol System",
    page_icon="𓂀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# THEME CSS — Luxury Archaeological Museum aesthetic
# =============================================================================

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Cinzel+Decorative:wght@700;900&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap');

/* ── Root palette ── */
:root {
    --bg:           #100e0a;
    --bg-deep:      #0a0804;
    --surface:      #1a1610;
    --surface-2:    #211c14;
    --surface-3:    #2a2418;
    --border:       #4a3c1e;
    --border-gold:  #9a7c2e;
    --border-bright:#c9a227;
    --text:         #f0e6cc;
    --text-dim:     #c4aa7a;
    --muted:        #8a7354;
    --gold:         #d4af37;
    --gold-bright:  #f0d060;
    --gold-dark:    #8a6e1a;
    --accent:       #c9943a;
    --accent-2:     #a06820;
    --shadow:       0 16px 48px rgba(0,0,0,0.7);
    --shadow-sm:    0 4px 18px rgba(0,0,0,0.4);
    --glow:         0 0 30px rgba(212,175,55,0.12);
    --glow-strong:  0 0 50px rgba(212,175,55,0.25);
}

/* ── Background with hieroglyph SVG pattern ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section[data-testid="stMain"] > div {
    background-color: var(--bg) !important;
    background-image:
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'%3E%3Cg fill='none' opacity='0.035'%3E%3Cpath d='M40 8 L40 18 M40 12 L36 8 M40 12 L44 8' stroke='%23d4af37' stroke-width='1.5' stroke-linecap='round'/%3E%3Ccircle cx='40' cy='22' r='4' stroke='%23d4af37' stroke-width='1.2'/%3E%3Cellipse cx='40' cy='32' rx='6' ry='3' stroke='%23d4af37' stroke-width='1'/%3E%3Cpath d='M34 32 L30 44 M46 32 L50 44' stroke='%23d4af37' stroke-width='1.2' stroke-linecap='round'/%3E%3Cpath d='M30 44 L26 56 M50 44 L54 56' stroke='%23d4af37' stroke-width='1' stroke-linecap='round'/%3E%3Cpath d='M58 20 L68 20 M63 15 L63 28' stroke='%23d4af37' stroke-width='1' stroke-linecap='round'/%3E%3Ccircle cx='63' cy='13' r='3' stroke='%23d4af37' stroke-width='1'/%3E%3Cpath d='M12 55 Q18 48 24 55 Q18 62 12 55Z' stroke='%23d4af37' stroke-width='1'/%3E%3Cpath d='M12 35 L12 45 M8 38 L16 38' stroke='%23d4af37' stroke-width='1' stroke-linecap='round'/%3E%3C/g%3E%3C/svg%3E"),
        radial-gradient(ellipse at 20% 10%, rgba(201,162,39,0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 90%, rgba(160,104,32,0.05) 0%, transparent 50%),
        linear-gradient(160deg, #161209 0%, #100e0a 40%, #0d0b08 100%) !important;
    color: var(--text) !important;
    font-family: 'EB Garamond', 'Palatino Linotype', Georgia, serif !important;
}

[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer { display: none !important; }

/* ── Custom scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--gold-dark), var(--border-gold));
    border-radius: 3px;
}

/* ── Navbar ── */
.ess-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2rem;
    height: 62px;
    background: linear-gradient(90deg, #0d0b07 0%, #181308 50%, #0d0b07 100%);
    border-bottom: 1px solid var(--border-gold);
    box-shadow: 0 1px 0 var(--gold-dark), var(--glow);
    position: sticky;
    top: 0;
    z-index: 999;
    margin-bottom: 1.5rem;
}
.ess-navbar-brand {
    font-family: 'Cinzel Decorative', 'Cinzel', serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--gold) !important;
    text-decoration: none;
    letter-spacing: 1.5px;
    text-shadow: 0 0 20px rgba(212,175,55,0.4);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.ess-navbar-links { display: flex; gap: 0.2rem; align-items: center; }
.ess-nav-btn {
    background: none; border: none;
    font-family: 'Cinzel', serif;
    font-size: 0.78rem; font-weight: 600;
    color: var(--muted); cursor: pointer;
    padding: 0.35rem 0.9rem;
    border-radius: 4px;
    letter-spacing: 0.8px;
    transition: color 0.2s, background 0.2s;
    text-transform: uppercase;
}
.ess-nav-btn:hover { color: var(--gold); background: rgba(212,175,55,0.06); }
.ess-nav-btn.active {
    background: linear-gradient(135deg, rgba(201,162,39,0.18), rgba(160,104,32,0.1));
    color: var(--gold-bright) !important;
    border: 1px solid var(--border-gold);
}

/* ── Cards ── */
.ess-card {
    background: linear-gradient(145deg, var(--surface) 0%, var(--surface-2) 100%);
    border: 1px solid var(--border);
    border-top: 1px solid var(--border-gold);
    border-radius: 4px;
    padding: 1.5rem;
    box-shadow: var(--shadow), inset 0 1px 0 rgba(212,175,55,0.08);
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.3s ease, border-color 0.3s ease;
}
.ess-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, var(--gold-dark) 25%, var(--gold) 50%, var(--gold-dark) 75%, transparent 100%);
}
.ess-card:hover {
    box-shadow: var(--shadow), var(--glow);
    border-color: var(--border-gold);
}
.ess-card-title {
    font-family: 'Cinzel', serif;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--gold);
    margin: 0 0 0.8rem;
    padding-bottom: 0.6rem;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
}

/* ── Hero ── */
.ess-hero {
    background: linear-gradient(160deg, #18130a 0%, #0f0c07 60%, #0a0804 100%);
    border: 1px solid var(--border-gold);
    border-radius: 4px;
    padding: 4rem 3rem;
    text-align: center;
    box-shadow: var(--shadow), var(--glow);
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.ess-hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse at 50% 0%, rgba(212,175,55,0.1) 0%, transparent 60%),
        radial-gradient(ellipse at 50% 100%, rgba(212,175,55,0.04) 0%, transparent 40%);
    pointer-events: none;
}
.ess-hero::after {
    content: '\1F200';
    position: absolute;
    font-size: 14rem;
    opacity: 0.018;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    line-height: 1;
    color: var(--gold);
    pointer-events: none;
}
.ess-hero-title {
    font-family: 'Cinzel Decorative', 'Cinzel', serif;
    font-size: clamp(1.1rem, 2.2vw, 1.7rem);
    font-weight: 700;
    color: var(--gold-bright);
    margin: 0 0 1rem 0;
    position: relative;
    letter-spacing: 2.5px;
    text-shadow: 0 0 40px rgba(212,175,55,0.35);
    line-height: 1.45;
}
.ess-hero-sub {
    font-family: 'EB Garamond', serif;
    font-size: 1.2rem;
    font-style: italic;
    color: var(--text-dim);
    margin: 0 auto 2rem auto;
    max-width: 540px;
    position: relative;
    line-height: 1.75;
}

/* ── Home page ── */
.home-wrap { width: min(920px, 94%); margin: 1.5rem auto 1rem; }
.home-quote {
    font-size: 1.15rem;
    line-height: 1.85;
    max-width: 700px;
    margin: 0;
    font-style: italic;
    color: var(--text-dim);
    text-align: center !important;
    width: 100%;
    display: block;
    font-family: 'EB Garamond', serif;
}
.home-quote-wrap {
    width: 100%;
    display: flex;
    justify-content: center;
    margin-top: 0.4rem;
}

/* ── Primary buttons ── */
.stButton > button, .stDownloadButton > button {
    border: 1px solid var(--border-gold) !important;
    background: linear-gradient(180deg, #2a1f08 0%, #1a1306 100%) !important;
    color: var(--gold) !important;
    border-radius: 3px !important;
    font-family: 'Cinzel', serif !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    padding: 0.65rem 1.2rem !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.5), inset 0 1px 0 rgba(212,175,55,0.12) !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: linear-gradient(180deg, #3d2e0c 0%, #261d08 100%) !important;
    border-color: var(--gold) !important;
    box-shadow: 0 6px 24px rgba(0,0,0,0.6), 0 0 20px rgba(212,175,55,0.18) !important;
    transform: translateY(-1px);
    color: var(--gold-bright) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, var(--surface) 0%, var(--surface-2) 100%) !important;
    border: 1px solid var(--border) !important;
    border-top: 1px solid var(--border-gold) !important;
    border-radius: 4px !important;
    padding: 1.2rem !important;
    box-shadow: var(--shadow-sm), inset 0 1px 0 rgba(212,175,55,0.06) !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
[data-testid="stMetricLabel"] {
    font-family: 'Cinzel', serif !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    color: var(--muted) !important;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}
[data-testid="stMetricValue"] {
    font-family: 'Cinzel Decorative', 'Cinzel', serif !important;
    color: var(--gold) !important;
    font-size: 1.55rem !important;
    text-shadow: 0 0 20px rgba(212,175,55,0.25);
}

/* ── DataFrames ── */
[data-testid="stDataFrame"] {
    border-radius: 4px !important;
    overflow: hidden;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
}
.stDataFrame thead tr th {
    background: linear-gradient(180deg, #221a09 0%, #1a1306 100%) !important;
    color: var(--gold) !important;
    font-family: 'Cinzel', serif !important;
    font-weight: 600 !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-bottom: 1px solid var(--border-gold) !important;
}

/* ── Sliders ── */
[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg, var(--gold-dark), var(--gold)) !important;
}

/* ── Inputs ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextInput"] > div > div > input,
[data-testid="stNumberInput"] > div > div > input {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 3px !important;
    color: var(--text) !important;
    font-family: 'EB Garamond', serif !important;
    font-size: 1rem !important;
}
[data-testid="stTextInput"] > div > div > input:focus {
    border-color: var(--border-gold) !important;
    box-shadow: 0 0 0 2px rgba(212,175,55,0.1) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1px dashed var(--border-gold) !important;
    border-radius: 4px !important;
    padding: 1.5rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--gold) !important;
    background: var(--surface-2) !important;
}
[data-testid="stFileUploader"] button {
    background: linear-gradient(180deg, #2a1f08 0%, #1a1306 100%) !important;
    border: 1px solid var(--border-gold) !important;
    color: var(--gold) !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border-gold) !important;
    gap: 0 !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    font-family: 'Cinzel', serif !important;
    font-weight: 600 !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border-radius: 3px 3px 0 0 !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s;
}
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(180deg, var(--surface-3) 0%, var(--surface) 100%) !important;
    color: var(--gold) !important;
    border: 1px solid var(--border-gold) !important;
    border-bottom: 1px solid var(--surface) !important;
    text-shadow: 0 0 12px rgba(212,175,55,0.25);
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
}

/* ── Alert boxes ── */
[data-testid="stAlert"] {
    border-radius: 4px !important;
    font-family: 'EB Garamond', serif !important;
    font-size: 1rem !important;
}

/* ── Radio nav ── */
[data-testid="stRadio"] > label {
    font-family: 'Cinzel', serif !important;
    font-weight: 600 !important;
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.5px;
}
[data-testid="stRadio"] div[role="radiogroup"] {
    gap: 0.35rem;
    margin-top: 0.2rem;
    margin-bottom: 0.25rem;
    flex-wrap: wrap;
}
[data-testid="stRadio"] div[role="radiogroup"] label {
    border: 1px solid transparent;
    background: transparent;
    border-radius: 3px;
    padding: 0.4rem 0.8rem;
    box-shadow: none;
    transition: all 0.2s;
}
[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
    background: rgba(212,175,55,0.08);
    border-color: var(--border-gold);
}
[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) span {
    color: var(--gold) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #0f0d08 0%, #0c0b07 100%) !important;
    border-right: 1px solid var(--border-gold) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.5);
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] .stMarkdown {
    color: var(--text-dim) !important;
    font-family: 'EB Garamond', serif !important;
}

/* ── Headings ── */
h1, h2, h3 {
    font-family: 'Cinzel', serif !important;
    color: var(--gold) !important;
    letter-spacing: 1px;
}
h2 {
    font-size: 1.05rem !important;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.7rem;
    margin-bottom: 1.4rem !important;
}

/* ── Divider ── */
hr { border-color: var(--border-gold) !important; opacity: 0.3; }

/* ── Symbol chips ── */
.sym-chip {
    display: inline-block;
    background: linear-gradient(135deg, #221a07 0%, #1a1305 100%);
    border: 1px solid var(--border-gold);
    color: var(--gold);
    border-radius: 2px;
    padding: 0.2rem 0.7rem;
    font-size: 0.74rem;
    font-weight: 600;
    font-family: 'Cinzel', serif;
    letter-spacing: 0.8px;
    margin: 0.18rem 0.15rem;
    text-transform: uppercase;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4), inset 0 1px 0 rgba(212,175,55,0.08);
    transition: all 0.2s;
}
.sym-chip:hover {
    background: linear-gradient(135deg, #2e2209 0%, #211807 100%);
    border-color: var(--gold);
    box-shadow: 0 2px 12px rgba(0,0,0,0.5), 0 0 10px rgba(212,175,55,0.12);
}

/* ── Interpretation block ── */
.interp-block {
    background: linear-gradient(145deg, #161009 0%, #110d07 100%);
    border-left: 3px solid var(--gold-dark);
    border-top: 1px solid var(--border);
    border-right: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    border-radius: 0 4px 4px 0;
    padding: 1.4rem 1.6rem 1.4rem 2rem;
    font-family: 'EB Garamond', serif;
    font-size: 1.1rem;
    line-height: 1.85;
    color: var(--text);
    margin-top: 0.6rem;
    position: relative;
    box-shadow: var(--shadow-sm);
    font-style: italic;
}

/* ── Stat chip ── */
.stat-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: linear-gradient(135deg, var(--surface-2), var(--surface-3));
    border: 1px solid var(--border-gold);
    border-radius: 3px;
    padding: 0.25rem 0.65rem;
    font-size: 0.74rem;
    font-weight: 700;
    font-family: 'Cinzel', serif;
    color: var(--gold);
    margin-right: 0.4rem;
    letter-spacing: 0.5px;
}

/* ── Footer ── */
.ess-footer {
    text-align: center;
    padding: 2rem;
    color: var(--muted);
    font-size: 0.9rem;
    font-family: 'EB Garamond', serif;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
    opacity: 0.7;
    font-style: italic;
}

/* ── Confidence bar ── */
.conf-bar-wrap {
    background: var(--surface-3);
    border-radius: 99px;
    height: 5px;
    overflow: hidden;
    margin-top: 5px;
    border: 1px solid var(--border);
}
.conf-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--gold-dark) 0%, var(--gold) 60%, var(--gold-bright) 100%);
    border-radius: 99px;
    transition: width 0.6s ease;
    box-shadow: 0 0 8px rgba(212,175,55,0.35);
}

/* ── Detection controls label ── */
.det-ctrl-label {
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 0.15rem;
    font-family: 'Cinzel', serif;
}

/* ── About list ── */
.about-list li {
    padding: 0.3rem 0;
    font-family: 'EB Garamond', serif;
    font-size: 1.08rem;
    line-height: 1.7;
    color: var(--text-dim);
}
.about-list li::marker { color: var(--gold); }

/* ── Dictionary entries ── */
.dict-entry {
    background: linear-gradient(145deg, var(--surface) 0%, var(--surface-2) 100%);
    border: 1px solid var(--border);
    border-left: 3px solid var(--border-gold);
    border-radius: 0 4px 4px 0;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.5rem;
    box-shadow: var(--shadow-sm);
    transition: border-left-color 0.2s, box-shadow 0.2s;
}
.dict-entry:hover {
    border-left-color: var(--gold);
    box-shadow: var(--shadow-sm), 0 0 15px rgba(212,175,55,0.07);
}
.dict-word {
    font-family: 'Cinzel', serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--gold);
    margin-bottom: 0.25rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.dict-meaning {
    font-family: 'EB Garamond', serif;
    font-size: 1.05rem;
    font-style: italic;
    line-height: 1.55;
    color: var(--text-dim);
}
.dict-meta {
    color: var(--muted);
    font-family: 'Cinzel', serif;
    font-size: 0.72rem;
    margin-bottom: 0.8rem;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

/* ── General text ── */
p, li, span { font-family: 'EB Garamond', serif; }

/* ── Caption ── */
[data-testid="stCaptionContainer"] p {
    font-family: 'EB Garamond', serif !important;
    color: var(--muted) !important;
    font-style: italic;
}
</style>
"""


DARK_MODE_CSS = """
<style>
/* Dark mode = default obsidian palette — no overrides needed. */
</style>
"""

LIGHT_MODE_CSS = """
<style>
/* ══════════════════════════════════════════════
   Light / Sandy mode — full override
   ══════════════════════════════════════════════ */
:root {
    --bg:           #f5ead6;
    --bg-deep:      #e8d5b5;
    --surface:      #fdf6ea;
    --surface-2:    #f5e9d2;
    --surface-3:    #ecd9bb;
    --border:       #c8a97a;
    --border-gold:  #9a6f2e;
    --border-bright:#7a4e18;
    --text:         #1e1208;
    --text-dim:     #4a2e14;
    --muted:        #7a5530;
    --gold:         #6b3d10;
    --gold-bright:  #3d2008;
    --gold-dark:    #9a6424;
    --accent:       #8b4513;
    --accent-2:     #6b3410;
    --shadow:       0 12px 32px rgba(100,60,20,0.18);
    --shadow-sm:    0 4px 14px rgba(100,60,20,0.1);
    --glow:         0 0 20px rgba(120,80,30,0.08);
    --glow-strong:  0 0 40px rgba(120,80,30,0.15);
}

/* ── Background ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section[data-testid="stMain"] > div {
    background-color: var(--bg) !important;
    background-image:
        radial-gradient(ellipse at 20% 10%, rgba(180,120,50,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 90%, rgba(160,100,40,0.06) 0%, transparent 50%),
        linear-gradient(160deg, #faebd7 0%, #f5e6cc 40%, #ecdcba 100%) !important;
    color: var(--text) !important;
}

/* ── Global text reset — catches every Streamlit text node ── */
[data-testid="stAppViewContainer"] *:not(button):not(.sym-chip):not(.ess-card-title):not(.dict-word):not([data-testid="stMetricValue"]) {
    color: var(--text) !important;
}

/* Re-apply selective overrides on top of the global reset */
[data-testid="stMetricValue"] * { color: var(--accent) !important; text-shadow: none !important; }
[data-testid="stMetricLabel"] * { color: var(--muted) !important; }
[data-testid="stCaptionContainer"] p { color: var(--muted) !important; font-style: italic; }
.dict-meta { color: var(--muted) !important; }
h1, h2, h3 { color: var(--accent) !important; }
.ess-card-title { color: var(--accent) !important; }
.dict-word { color: var(--accent) !important; }
.sym-chip { color: var(--text) !important; }
.ess-hero-title { color: var(--text) !important; text-shadow: none !important; }
.ess-hero-sub { color: var(--text-dim) !important; }
.ess-navbar-brand { color: var(--text) !important; text-shadow: none !important; }
.ess-nav-btn { color: var(--muted) !important; }
.ess-nav-btn:hover { color: var(--accent) !important; }
.interp-block { color: var(--text) !important; }
.dict-meaning { color: var(--text-dim) !important; }
.home-quote { color: var(--text-dim) !important; }
[data-testid="stSidebar"] * { color: var(--text-dim) !important; }

/* ── Navbar ── */
.ess-navbar {
    background: linear-gradient(90deg, #f0e2c8 0%, #ead5b0 50%, #f0e2c8 100%) !important;
    border-bottom: 1px solid var(--border-gold) !important;
    box-shadow: 0 2px 12px rgba(100,60,20,0.12) !important;
}
.ess-nav-btn:hover { background: rgba(110,60,16,0.07) !important; }
.ess-nav-btn.active {
    background: rgba(110,60,16,0.1) !important;
    border: 1px solid var(--border-gold) !important;
    color: var(--accent) !important;
}

/* ── Cards ── */
.ess-card {
    background: linear-gradient(145deg, var(--surface) 0%, var(--surface-2) 100%) !important;
    border-color: var(--border) !important;
    border-top-color: var(--border-gold) !important;
    box-shadow: var(--shadow), inset 0 1px 0 rgba(255,255,255,0.5) !important;
}
.ess-card::before {
    background: linear-gradient(90deg, transparent 0%, var(--border-gold) 25%, var(--gold-dark) 50%, var(--border-gold) 75%, transparent 100%) !important;
}
.ess-card-title { border-bottom-color: var(--border) !important; }

/* ── Hero ── */
.ess-hero {
    background: linear-gradient(160deg, #faebd5 0%, #f0dfc0 60%, #e8d4aa 100%) !important;
    border-color: var(--border-gold) !important;
    box-shadow: var(--shadow), 0 0 40px rgba(120,80,30,0.08) !important;
}
.ess-hero::before {
    background: radial-gradient(ellipse at 50% 0%, rgba(140,80,20,0.08) 0%, transparent 60%) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, var(--surface) 0%, var(--surface-2) 100%) !important;
    border-color: var(--border) !important;
    border-top-color: var(--border-gold) !important;
    box-shadow: var(--shadow-sm) !important;
}
[data-testid="stMetric"]::before {
    background: linear-gradient(90deg, transparent, var(--border-gold), transparent) !important;
}

/* ── Buttons ── */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(180deg, #f0e0c0 0%, #e0cca0 100%) !important;
    border-color: var(--border-gold) !important;
    color: var(--text) !important;
    box-shadow: 0 4px 12px rgba(100,60,20,0.15) !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: linear-gradient(180deg, #e8d4aa 0%, #d4bb88 100%) !important;
    border-color: var(--accent) !important;
    box-shadow: 0 6px 20px rgba(100,60,20,0.2) !important;
}
/* Don't let global * override button text */
.stButton > button *, .stDownloadButton > button * {
    color: var(--text) !important;
}

/* ── Inputs ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextInput"] > div > div > input,
[data-testid="stNumberInput"] > div > div > input {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border-color: var(--border-gold) !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: #fff8ec !important;
    border: 1px dashed var(--border-gold) !important;
}
[data-testid="stFileUploaderDropzone"] * {
    color: var(--text) !important;
    opacity: 1 !important;
}
[data-testid="stFileUploader"] button {
    background: linear-gradient(180deg, #f0e0c0 0%, #e0cca0 100%) !important;
    border-color: var(--border-gold) !important;
    color: var(--text) !important;
}
[data-testid="stFileUploader"] button * { color: var(--text) !important; }

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    border-bottom-color: var(--border-gold) !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] { color: var(--muted) !important; }
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(180deg, var(--surface-3) 0%, var(--surface) 100%) !important;
    color: var(--accent) !important;
    border-color: var(--border-gold) !important;
    text-shadow: none !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] * { color: inherit !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #f0e2c8 0%, #e8d5b0 100%) !important;
    border-right-color: var(--border-gold) !important;
    box-shadow: 2px 0 16px rgba(100,60,20,0.1) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar-track { background: var(--surface-2) !important; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--border-gold), var(--border)) !important;
}

/* ── Symbol chips ── */
.sym-chip {
    background: linear-gradient(135deg, #f0e0c0 0%, #e4d0a8 100%) !important;
    border-color: var(--border-gold) !important;
    box-shadow: 0 2px 6px rgba(100,60,20,0.12) !important;
}
.sym-chip:hover {
    background: linear-gradient(135deg, #e8d4aa 0%, #d8c090 100%) !important;
    border-color: var(--accent) !important;
}

/* ── Interpretation block ── */
.interp-block {
    background: linear-gradient(145deg, #fdf5e6 0%, #f5e9d0 100%) !important;
    border-left-color: var(--border-gold) !important;
    border-top-color: var(--border) !important;
    border-right-color: var(--border) !important;
    border-bottom-color: var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ── Stat chip ── */
.stat-chip {
    background: linear-gradient(135deg, var(--surface-2), var(--surface-3)) !important;
    border-color: var(--border-gold) !important;
    color: var(--accent) !important;
}
.stat-chip * { color: var(--accent) !important; }

/* ── Dict entries ── */
.dict-entry {
    background: linear-gradient(145deg, var(--surface) 0%, var(--surface-2) 100%) !important;
    border-color: var(--border) !important;
    border-left-color: var(--border-gold) !important;
}
.dict-entry:hover { border-left-color: var(--accent) !important; }

/* ── DataFrames ── */
[data-testid="stDataFrame"] { border-color: var(--border) !important; }
.stDataFrame thead tr th {
    background: linear-gradient(180deg, #e8d4a8 0%, #ddc898 100%) !important;
    border-bottom-color: var(--border-gold) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border-color: var(--border) !important;
}

/* ── Radio ── */
[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
    background: rgba(110,60,16,0.08) !important;
    border-color: var(--border-gold) !important;
}
[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) span {
    color: var(--accent) !important;
}

/* ── Confidence bar ── */
.conf-bar-wrap { background: var(--surface-3) !important; border-color: var(--border) !important; }
.conf-bar-fill {
    background: linear-gradient(90deg, var(--gold-dark) 0%, var(--accent) 100%) !important;
    box-shadow: none !important;
}

/* ── HR ── */
hr { border-color: var(--border-gold) !important; }

/* ── Bulb button ── */
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] [data-testid="stButton"] > button,
[data-testid="stSidebar"] div[data-testid="stButton"] button {
    background: radial-gradient(circle at 48% 34%, #fffdf5 0%, #f8e9c9 58%, #d7b47a 100%) !important;
    border: 1.5px solid #8d652c !important;
    box-shadow: inset 0 1px 1px rgba(255,255,255,0.7), 0 2px 8px rgba(112, 72, 23, 0.22) !important;
}
[data-testid="stSidebar"] .stButton > button:hover,
[data-testid="stSidebar"] [data-testid="stButton"] > button:hover,
[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
    box-shadow: inset 0 1px 1px rgba(255,255,255,0.8), 0 4px 12px rgba(112, 72, 23, 0.26) !important;
    filter: brightness(1.02) !important;
}
[data-testid="stSidebar"] .stButton > button:active,
[data-testid="stSidebar"] [data-testid="stButton"] > button:active,
[data-testid="stSidebar"] div[data-testid="stButton"] button:active {
    box-shadow: inset 0 1px 1px rgba(255,255,255,0.75), 0 2px 8px rgba(112, 72, 23, 0.24) !important;
    filter: brightness(1) !important;
    transform: none !important;
}
[data-testid="stSidebar"] .stButton > button:focus,
[data-testid="stSidebar"] .stButton > button:focus-visible,
[data-testid="stSidebar"] [data-testid="stButton"] > button:focus,
[data-testid="stSidebar"] [data-testid="stButton"] > button:focus-visible,
[data-testid="stSidebar"] div[data-testid="stButton"] button:focus,
[data-testid="stSidebar"] div[data-testid="stButton"] button:focus-visible {
    outline: none !important;
    box-shadow: inset 0 1px 1px rgba(255,255,255,0.75), 0 2px 8px rgba(112, 72, 23, 0.24) !important;
}

/* ── Sliders ── */
[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg, var(--border-gold), var(--accent)) !important;
}

/* ── Alert / info boxes ── */
[data-testid="stAlert"] {
    background: var(--surface) !important;
    border-color: var(--border) !important;
}
[data-testid="stAlert"] * { color: var(--text) !important; }
</style>
"""

BULB_TOGGLE_CSS = """
<style>
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] [data-testid="stButton"] > button,
[data-testid="stSidebar"] div[data-testid="stButton"] button {
    width: 52px !important;
    min-width: 52px !important;
    height: 52px !important;
    border-radius: 50% !important;
    border: 1px solid var(--border-gold) !important;
    padding: 0 !important;
    margin: 0 auto 0.3rem auto !important;
    display: block !important;
    background: radial-gradient(circle at 50% 34%, #fff7d7 0%, #f0c86a 52%, #8b5f1f 100%) !important;
    border: 1.5px solid #8f6a21 !important;
    box-shadow: 0 0 0 2px rgba(235, 192, 90, 0.22), 0 0 26px rgba(235, 192, 90, 0.42), 0 0 52px rgba(235, 192, 90, 0.2) !important;
    transition: box-shadow 0.3s ease, filter 0.25s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover,
[data-testid="stSidebar"] [data-testid="stButton"] > button:hover,
[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
    box-shadow: 0 0 0 3px rgba(245, 210, 120, 0.3), 0 0 42px rgba(245, 210, 120, 0.62), 0 0 78px rgba(245, 210, 120, 0.3) !important;
    filter: brightness(1.05) !important;
    transform: none !important;
}
[data-testid="stSidebar"] .stButton > button p,
[data-testid="stSidebar"] [data-testid="stButton"] > button p,
[data-testid="stSidebar"] div[data-testid="stButton"] button p {
    font-size: 1.2rem !important;
    line-height: 1 !important;
}
.theme-mode-label {
    text-align: center;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.7rem;
    font-family: 'Cinzel', serif;
}
</style>
"""


# =============================================================================
# MONGODB HELPERS
# =============================================================================

@st.cache_resource(show_spinner=False)
def init_mongo_collection():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        client.admin.command("ping")
        db = client[MONGO_DB_NAME]
        return db[MONGO_COLLECTION]
    except Exception:
        return None


def save_detection_record(record: dict) -> None:
    col = init_mongo_collection()
    if col is None:
        return
    col.insert_one(record)


def parse_record_datetime(value):
    if isinstance(value, datetime):
        dt = value
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    if isinstance(value, str) and value.strip():
        cleaned = value.replace("Z", "+00:00")
        try:
            dt = datetime.fromisoformat(cleaned)
            if dt.tzinfo is None:
                return dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except ValueError:
            return None
    return None


def format_history_records(raw_records: list[dict]) -> list[dict]:
    formatted = []
    for rec in raw_records:
        symbols = rec.get("symbols", [])
        if isinstance(symbols, str):
            symbols = [s.strip() for s in symbols.split(",") if s.strip()]
        elif not isinstance(symbols, list):
            symbols = []

        confidence = rec.get("confidence", 0.0)
        try:
            confidence = float(confidence)
        except (TypeError, ValueError):
            confidence = 0.0
        if confidence > 1.0:
            confidence /= 100.0
        confidence = max(0.0, min(confidence, 1.0))

        dt_value = parse_record_datetime(rec.get("timestamp"))
        display_timestamp = (
            dt_value.astimezone(IST_TZ).strftime("%Y-%m-%d %H:%M:%S IST")
            if dt_value else "Unknown"
        )

        formatted.append({
            "image_name":          rec.get("image_name") or "Unknown image",
            "detected_image_name": rec.get("detected_image_name") or "",
            "symbols":             symbols,
            "confidence":          confidence,
            "fusion_text":         rec.get("fusion_text") or "",
            "final_interpretation":rec.get("final_interpretation") or "",
            "timestamp":           rec.get("timestamp"),
            "parsed_timestamp":    dt_value,
            "display_timestamp":   display_timestamp,
        })

    formatted.sort(
        key=lambda r: (r["parsed_timestamp"] is not None, r["parsed_timestamp"]),
        reverse=True,
    )
    return formatted


def safe_image_path(base_dir: str, filename: str) -> str | None:
    if not filename:
        return None
    safe_name = os.path.basename(filename)
    path = os.path.join(base_dir, safe_name)
    return path if os.path.isfile(path) else None


# =============================================================================
# PDF REPORT BUILDER
# =============================================================================

def draw_wrapped_text(c, text, x, y, max_width, font_name, font_size, leading=14):
    lines = simpleSplit(text or "", font_name, font_size, max_width)
    obj = c.beginText(x, y)
    obj.setFont(font_name, font_size)
    obj.setLeading(leading)
    for line in lines:
        obj.textLine(line)
    c.drawText(obj)
    return obj.getY()


def draw_section_card(c, x, y_top, width, height, heading):
    y_bottom = y_top - height
    c.setFillColor(colors.HexColor("#F7F1E6"))
    c.setStrokeColor(colors.HexColor("#D8C7AA"))
    c.roundRect(x, y_bottom, width, height, 8, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#3A2A18"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 12, y_top - 18, heading)


def draw_stat_chip(c, x, y, label, value):
    label_text = f"{label}: {value}"
    chip_w = max(120, min(320, 16 + len(label_text) * 5.2))
    max_chars = max(10, int((chip_w - 16) / 4.9))
    if len(label_text) > max_chars:
        label_text = label_text[: max_chars - 1].rstrip() + "..."
    c.setFillColor(colors.HexColor("#EFE3CF"))
    c.setStrokeColor(colors.HexColor("#D2B48C"))
    c.roundRect(x, y - 14, chip_w, 20, 10, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#3A2A18"))
    c.setFont("Helvetica", 9)
    c.drawString(x + 8, y - 1, label_text)
    return chip_w


def draw_image_block(c, image_path, heading, y, page_width, margin):
    if not image_path:
        return y
    draw_section_card(c, margin, y, page_width - 2 * margin, 236, heading)
    y -= 30
    reader = ImageReader(image_path)
    img_w, img_h = reader.getSize()
    available_w = page_width - 2 * margin - 24
    max_h = 176
    scale = min(available_w / img_w, max_h / img_h)
    draw_w, draw_h = img_w * scale, img_h * scale
    x = margin + ((page_width - 2 * margin) - draw_w) / 2
    y_img = y - draw_h
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#D8C7AA"))
    c.roundRect(x - 6, y_img - 6, draw_w + 12, draw_h + 12, 6, fill=1, stroke=1)
    c.drawImage(reader, x, y_img, width=draw_w, height=draw_h, preserveAspectRatio=True, mask="auto")
    return y_img - 20


def build_report_pdf(row: dict) -> bytes:
    input_path   = safe_image_path(UPLOAD_DIR, row.get("image_name", ""))
    detected_path = safe_image_path(DETECTED_DIR, row.get("detected_image_name", ""))
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    page_w, page_h = letter
    margin = 40
    y = page_h - margin

    pdf.setTitle(f"detection_report_{row.get('image_name', 'report')}")

    # Header
    pdf.setFillColor(colors.HexColor("#6B4F2A"))
    pdf.rect(0, page_h - 68, page_w, 68, fill=1, stroke=0)
    pdf.setFillColor(colors.HexColor("#F7EEDB"))
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(margin, page_h - 32, "Egyptian Symbol Detection Report")
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(page_w - margin, page_h - 34,
                        datetime.now(IST_TZ).strftime("Generated %Y-%m-%d %H:%M IST"))
    y = page_h - 68 - 16

    # Summary
    summary_items = [
        ("Image", row.get("image_name", "Unknown")),
        ("Confidence", f"{row.get('confidence', 0.0) * 100:.2f}%"),
        ("Timestamp", row.get("display_timestamp", "Unknown")),
    ]
    inner_left = margin + 12
    inner_right = margin + (page_w - 2 * margin) - 12
    widths = [max(120, min(320, 16 + len(f"{k}: {v}") * 5.2)) for k, v in summary_items]

    row_count = 1
    x_cursor = inner_left
    for w in widths:
        if x_cursor + w > inner_right and x_cursor > inner_left:
            row_count += 1
            x_cursor = inner_left
        x_cursor += w + 8

    summary_h = 58 + (row_count - 1) * 26
    draw_section_card(pdf, margin, y, page_w - 2 * margin, summary_h, "Detection Summary")

    y_meta = y - 36
    x_cursor = inner_left
    row_idx = 0
    for (label, value), w in zip(summary_items, widths):
        if x_cursor + w > inner_right and x_cursor > inner_left:
            row_idx += 1
            x_cursor = inner_left
        chip_y = y_meta - (row_idx * 26)
        chip_w = draw_stat_chip(pdf, x_cursor, chip_y, label, value)
        x_cursor += chip_w + 8

    y -= summary_h + 12

    # Symbols
    symbols_text = ", ".join(row.get("symbols", [])) or "No symbols detected"
    draw_section_card(pdf, margin, y, page_w - 2 * margin, 52, "Detected Symbols")
    draw_wrapped_text(pdf, symbols_text, margin + 12, y - 34, page_w - 2 * margin - 24, "Helvetica", 10)
    y -= 64

    # Fusion
    fusion_text = row.get("fusion_text") or "No fusion rule applied."
    draw_section_card(pdf, margin, y, page_w - 2 * margin, 88, "Fusion Interpretation")
    y = draw_wrapped_text(pdf, fusion_text, margin + 12, y - 34, page_w - 2 * margin - 24, "Helvetica", 10) - 14

    if y < 260:
        pdf.showPage(); y = page_h - margin - 10

    # Final
    final_text = row.get("final_interpretation") or "No interpretation available."
    draw_section_card(pdf, margin, y, page_w - 2 * margin, 108, "Final Interpretation")
    y = draw_wrapped_text(pdf, final_text, margin + 12, y - 34, page_w - 2 * margin - 24, "Helvetica", 10) - 16

    if y < 180:
        pdf.showPage(); y = page_h - margin - 10

    y = draw_image_block(pdf, input_path, "Input Image", y, page_w, margin)
    if detected_path:
        if y < 220:
            pdf.showPage(); y = page_h - margin
        draw_image_block(pdf, detected_path, "Annotated Image", y, page_w, margin)

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()


# =============================================================================
# PIPELINE
# =============================================================================
#complete analysis by detecting symbols, generating interpretation, saving results, and returning output for display.
def run_analysis_pipeline(image_path: str, image_name: str, params: dict) -> dict:
    detections, detected_image_path = detect_symbols(
        image_path,
        conf_threshold=params["confidence_threshold"],
        iou_threshold=params["iou_threshold"],
        max_symbols=params["max_symbols"],
        output_dir=DETECTED_DIR,
    )
    report = generate_interpretation(detections)
    record = {
        "image_name":          image_name,
        "detected_image_name": os.path.basename(detected_image_path) if detected_image_path else "",
        "symbols":             report.get("detected_symbols", []),
        "confidence":          float(report.get("confidence_score", 0.0)),
        "fusion_text":         report.get("fusion_text") or "",
        "final_interpretation":report.get("final_paragraph") or "",
        "timestamp":           datetime.now(timezone.utc).isoformat(),
    }
    save_detection_record(record)
    return {
        "image_path":          image_path,
        "detected_image_path": detected_image_path,
        "report":              report,
        "record":              record,
    }


def build_dashboard_data(records):
    total = len(records)
    avg_conf = sum(float(r.get("confidence", 0)) for r in records) / total if total else 0.0
    sym_counter = Counter()
    for row in records:
        for s in row.get("symbols", []):
            sym_counter[s] += 1
    top_syms = sym_counter.most_common(8)
    top_name = top_syms[0][0] if top_syms else "-"

    day_counter = Counter()
    for row in records:
        dt = row.get("parsed_timestamp")
        if dt:
            day_counter[dt.astimezone(IST_TZ).strftime("%Y-%m-%d")] += 1
    timeline_labels = sorted(day_counter.keys())[-7:]
    timeline_points = [{"label": d, "count": day_counter[d]} for d in timeline_labels]

    return {
        "total_records":  total,
        "avg_confidence": avg_conf,
        "top_symbol_name":top_name,
        "top_symbols":    top_syms,
        "timeline_points":timeline_points,
    }


# =============================================================================
# RENDER HELPERS "Session state preserves app status such as page, theme, camera, and latest result."
# =============================================================================

def render_symbol_chips(symbols: list) -> str:
    return "".join(f'<span class="sym-chip">{s}</span>' for s in symbols)


def render_conf_bar(value: float) -> str:
    pct = int(value * 100)
    return (
        f'<div class="conf-bar-wrap">'
        f'<div class="conf-bar-fill" style="width:{pct}%"></div>'
        f'</div>'
    )


def render_analysis_result(result: dict):
    report = result["report"]
    st.markdown("---")

    # Images side by side
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ess-card-title">📷 Uploaded Image</div>', unsafe_allow_html=True)
        st.image(result["image_path"], use_container_width=True)
    with col2:
        st.markdown('<div class="ess-card-title">🔍 Detected Image</div>', unsafe_allow_html=True)
        dp = result.get("detected_image_path")
        if dp and os.path.exists(dp):
            st.image(dp, use_container_width=True)
        else:
            st.image(result["image_path"], use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Metrics row
    m1, m2 = st.columns(2)
    syms = report.get("detected_symbols", [])
    m1.metric("𓂀 Detected Symbols", len(syms))
    m2.metric("📊 Confidence",        f"{report.get('confidence_score', 0.0):.2%}")

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="ess-card-title">Detected Symbols</div>', unsafe_allow_html=True)
        if syms:
            st.markdown(render_symbol_chips(syms), unsafe_allow_html=True)
        else:
            st.info("No symbols detected.")

        st.markdown("<br>", unsafe_allow_html=True)
        ranked = report.get("ranked_detections", [])
        if ranked:
            df = pd.DataFrame([{
                "Symbol":     d["symbol"],
                "Count":      d["count"],
                "Confidence": f"{float(d['confidence']):.2%}",
            } for d in ranked])
            st.dataframe(df, use_container_width=True, hide_index=True)

    with col_b:
        st.markdown('<div class="ess-card-title">Interpretation Result</div>', unsafe_allow_html=True)

        st.markdown("**Final Interpretation:**")
        final = report.get("final_paragraph") or "No interpretation available."
        st.markdown(f'<div class="interp-block">{final}</div>', unsafe_allow_html=True)


# =============================================================================
# SESSION STATE
# =============================================================================

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"
if "camera_active" not in st.session_state:
    st.session_state.camera_active = False
if "camera_widget_version" not in st.session_state:
    st.session_state.camera_widget_version = 0


# =============================================================================
# INJECT CSS
# =============================================================================

combined_css = THEME_CSS + BULB_TOGGLE_CSS
if st.session_state.theme_mode == "light":
    combined_css += LIGHT_MODE_CSS
st.markdown(combined_css, unsafe_allow_html=True)


# =============================================================================
# NAVBAR
# =============================================================================

PAGES = ["Home", "Analyze", "Dashboard", "Symbol Dictionary", "History", "About"]

st.markdown('<span class="ess-navbar-brand">𓂀 Egyptian Symbol System</span>', unsafe_allow_html=True)

selected_page = st.radio(
    "Navigation",
    PAGES,
    index=PAGES.index(st.session_state.page),
    horizontal=True,
    label_visibility="collapsed",
)
if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()

st.markdown('<hr style="margin:0.35rem 0 1.2rem 0">', unsafe_allow_html=True)

page = st.session_state.page

# =============================================================================
# SIDEBAR — detection settings (always visible)
# =============================================================================

with st.sidebar:
    st.markdown("### Theme")
    if st.button("💡", key="bulb_theme_toggle", help="Toggle dark and light theme"):
        st.session_state.theme_mode = "dark" if st.session_state.theme_mode == "light" else "light"
        st.rerun()
    st.markdown("---")

    st.markdown("### ⚙️ Detection Settings")
    conf_threshold = st.slider("Confidence Threshold", 0.25, 0.95, 0.65, 0.05)
    iou_threshold  = st.slider("IoU Threshold",        0.30, 0.80, 0.60, 0.05)
    max_symbols    = st.slider("Max Symbols",          1,    20,   10,   1)

    params = {
        "confidence_threshold": conf_threshold,
        "iou_threshold":        iou_threshold,
        "max_symbols":          max_symbols,
    }

    st.markdown("---")
    mongo_collection = init_mongo_collection()


# =============================================================================
# PAGE: HOME
# =============================================================================

if page == "Home":
    st.markdown(
        """
        <div class="home-wrap">
          <div class="ess-hero">
              <h1 class="ess-hero-title">AI-Based Symbolic Interpretation<br>of Ancient Egyptian Paintings</h1>
                            <div class="home-quote-wrap">
                                <p class="home-quote">From painted symbols to hidden meaning, where ancient voices meet modern intelligence.</p>
                            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, c, _ = st.columns([3, 2, 3])
    with c:
        if st.button("Analyze", use_container_width=True):
            st.session_state.page = "Analyze"
            st.rerun()


# =============================================================================
# PAGE: ANALYZE
# =============================================================================

elif page == "Analyze":
    st.markdown("## Symbol Analysis")

    tab_upload, tab_live = st.tabs(["📁  Upload Image", "📷  Live Camera"])

    # ── Upload tab ──
    with tab_upload:
        st.markdown('<div class="ess-card-title">Upload Image</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose an image", type=["jpg", "jpeg", "png", "bmp", "webp"],
            label_visibility="collapsed",
        )
        run_btn = st.button("🔍  Run Detection", type="primary", use_container_width=True)

        if run_btn and uploaded_file is not None:
            _, ext = os.path.splitext(uploaded_file.name)
            ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
            safe_name  = f"upload_{ts}{ext.lower() or '.jpg'}"
            upload_path = os.path.join(UPLOAD_DIR, safe_name)
            with open(upload_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            with st.spinner("Running detection and interpretation…"):
                st.session_state.latest_result = run_analysis_pipeline(upload_path, safe_name, params)
        elif run_btn:
            st.warning("Please upload an image first.")

    # ── Live Camera tab ──
    with tab_live:
        st.markdown('<div class="ess-card-title">Live Camera Capture</div>', unsafe_allow_html=True)

        cam_col1, cam_col2 = st.columns(2)
        with cam_col1:
            if st.button("▶ Start Camera", key="start_live_camera", use_container_width=True):
                st.session_state.camera_active = True
                st.rerun()
        with cam_col2:
            if st.button("■ Stop Camera", key="stop_live_camera", use_container_width=True):
                st.session_state.camera_active = False
                # Force a fresh camera widget instance when restarted.
                st.session_state.camera_widget_version += 1
                st.rerun()

        snapshot = None
        if st.session_state.camera_active:
            snapshot = st.camera_input(
                "Take a picture",
                label_visibility="collapsed",
                key=f"live_camera_input_{st.session_state.camera_widget_version}",
            )
        else:
            st.info("Camera is stopped. Click Start Camera to enable live capture.")

        analyze_live = st.button("🔍  Analyze Capture", type="primary")

        if analyze_live and snapshot is not None:
            frame_bytes = snapshot.getvalue()
            frame_array = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
            if frame_array is None:
                st.error("Could not decode captured image.")
            else:
                ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
                safe_name   = f"live_capture_{ts}.jpg"
                upload_path = os.path.join(UPLOAD_DIR, safe_name)
                cv2.imwrite(upload_path, frame_array)
                with st.spinner("Running detection and interpretation…"):
                    st.session_state.latest_result = run_analysis_pipeline(upload_path, safe_name, params)
        elif analyze_live:
            st.warning("Please take a picture first.")

    # ── Result ──
    if st.session_state.latest_result is not None:
        render_analysis_result(st.session_state.latest_result)


# =============================================================================
# PAGE: DASHBOARD
# =============================================================================

elif page == "Dashboard":
    st.markdown("## Detection Dashboard")

    mongo_collection = init_mongo_collection()
    if mongo_collection is None:
        st.info("Dashboard is unavailable because MongoDB is not connected.")
    else:
        raw_records = list(mongo_collection.find({}, {"_id": 0}))
        records = format_history_records(raw_records)
        data    = build_dashboard_data(records)

        # KPIs
        k1, k2, k3 = st.columns(3)
        k1.metric("📋 Total Detections",   data["total_records"])
        k2.metric("📊 Average Confidence", f"{data['avg_confidence']:.2%}")
        k3.metric("🏆 Most Frequent Symbol", data["top_symbol_name"])

        st.markdown("<br>", unsafe_allow_html=True)

        col_sym, col_tl = st.columns(2)

        with col_sym:
            st.markdown('<div class="ess-card-title">Top Symbols</div>', unsafe_allow_html=True)
            if data["top_symbols"]:
                top_df = pd.DataFrame(data["top_symbols"], columns=["Symbol", "Count"])
                st.dataframe(top_df, use_container_width=True, hide_index=True)
            else:
                st.info("No symbol statistics yet.")

        with col_tl:
            st.markdown('<div class="ess-card-title">Detections in Last 7 Days</div>', unsafe_allow_html=True)
            if data["timeline_points"]:
                tl_df = pd.DataFrame(data["timeline_points"]).set_index("label")
                st.bar_chart(tl_df)
            else:
                st.info("No timeline data available.")


# =============================================================================
# PAGE: SYMBOL DICTIONARY
# =============================================================================

elif page == "Symbol Dictionary":
    st.markdown("## Symbol Dictionary")

    query = st.text_input("🔎  Search symbol", placeholder="e.g. ankh")

    all_entries = [
        {"Symbol": sym, "Meaning": meaning}
        for sym, meaning in sorted(SYMBOL_MEANINGS.items())
    ]

    entries = all_entries
    search_mode = "all"

    if query:
        q = query.strip().lower()
        canonical = SYMBOL_NORMALIZATION.get(q, q).strip().lower()

        # Priority 1: exact symbol match.
        exact_matches = [e for e in all_entries if e["Symbol"].lower() == canonical]
        if exact_matches:
            entries = exact_matches
            search_mode = "exact"
        else:
            # Priority 2: suggest symbols starting with the typed prefix.
            entries = [e for e in all_entries if e["Symbol"].lower().startswith(q)]
            search_mode = "prefix"
    if entries:
        if search_mode == "exact":
            st.markdown("<div class='dict-meta'>Exact match found.</div>", unsafe_allow_html=True)
        elif search_mode == "prefix":
            st.markdown(
                f"<div class='dict-meta'>Showing symbols starting with '{query.strip()}'.</div>",
                unsafe_allow_html=True,
            )

        grouped_entries = {}
        for entry in entries:
            symbol = entry["Symbol"]
            group_key = symbol[0].upper() if symbol and symbol[0].isalpha() else "#"
            grouped_entries.setdefault(group_key, []).append(entry)

        for group_key in sorted(grouped_entries.keys()):
            st.markdown(f"### {group_key}")
            for item in grouped_entries[group_key]:
                st.markdown(
                    f"""
                    <div class="dict-entry">
                        <div class="dict-word">{item['Symbol']}</div>
                        <div class="dict-meaning">{item['Meaning']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("No dictionary entry found for that symbol.")


# =============================================================================
# PAGE: HISTORY
# =============================================================================

elif page == "History":
    st.markdown("## Detection History")

    mongo_collection = init_mongo_collection()
    if mongo_collection is None:
        st.info("History is unavailable because MongoDB is not connected.")
    else:
        raw_records = list(mongo_collection.find({}, {"_id": 0}))
        records = format_history_records(raw_records)

        if not records:
            st.info("No history records found.")
        else:
            search_col, conf_col = st.columns([2, 1])
            with search_col:
                history_query = st.text_input(
                    "Search history",
                    placeholder="Search by image name or symbol",
                    key="history_search_query",
                ).strip().lower()
            with conf_col:
                min_conf = st.slider("Min confidence", 0.0, 1.0, 0.0, 0.05, key="history_min_conf")

            filtered_records = []
            for row in records:
                image_name = (row.get("image_name") or "").lower()
                symbols_text = " ".join(row.get("symbols") or []).lower()
                matches_query = (not history_query) or (history_query in image_name) or (history_query in symbols_text)
                matches_conf = float(row.get("confidence", 0.0)) >= float(min_conf)
                if matches_query and matches_conf:
                    filtered_records.append(row)

            if not filtered_records:
                st.info("No records match the current search/filter.")
            else:
                k1, k2, k3 = st.columns(3)
                avg_conf = sum(float(r.get("confidence", 0.0)) for r in filtered_records) / len(filtered_records)
                k1.metric("Records", len(filtered_records))
                k2.metric("Average Confidence", f"{avg_conf:.2%}")
                k3.metric("Latest", filtered_records[0].get("display_timestamp", "-"))

                history_df = pd.DataFrame([
                    {
                        "Image": r["image_name"],
                        "Symbols": ", ".join(r["symbols"]) if r["symbols"] else "-",
                        "Confidence": f"{r['confidence']:.2%}",
                        "Date": r["display_timestamp"],
                    }
                    for r in filtered_records
                ])
                st.caption("Tip: select a table row to view that record's details.")
                table_event = st.dataframe(
                    history_df,
                    use_container_width=True,
                    hide_index=True,
                    on_select="rerun",
                    selection_mode="single-row",
                    key="history_table",
                )

                st.markdown("### Record Details")

                sel_idx = st.session_state.get("history_selected_idx", 0)
                selected_rows = []
                if hasattr(table_event, "selection") and hasattr(table_event.selection, "rows"):
                    selected_rows = list(table_event.selection.rows)
                elif isinstance(table_event, dict):
                    selected_rows = list(table_event.get("selection", {}).get("rows", []))

                if selected_rows:
                    sel_idx = int(selected_rows[0])
                    st.session_state.history_selected_idx = sel_idx

                if sel_idx < 0 or sel_idx >= len(filtered_records):
                    sel_idx = 0
                sel = filtered_records[sel_idx]

                # Images
                img_col, det_col = st.columns(2)
                input_path = safe_image_path(UPLOAD_DIR, sel["image_name"])
                detected_path = safe_image_path(DETECTED_DIR, sel["detected_image_name"])
                with img_col:
                    st.markdown("**📷 Uploaded Image**")
                    if input_path:
                        st.image(input_path, use_container_width=True)
                    else:
                        st.info("Image file not found on disk.")
                with det_col:
                    st.markdown("**🔍 Detected Image**")
                    if detected_path:
                        st.image(detected_path, use_container_width=True)
                    else:
                        st.info("Detected image not found on disk.")

                # Symbols & interpretation
                st.markdown("**Detected Symbols**")
                if sel["symbols"]:
                    st.markdown(render_symbol_chips(sel["symbols"]), unsafe_allow_html=True)
                else:
                    st.caption("No symbols.")

                st.markdown("**Final Interpretation**")
                interp = sel.get("final_interpretation") or "No interpretation available."
                st.markdown(f'<div class="interp-block">{interp}</div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                act1, act2 = st.columns(2)
                with act1:
                    pdf_bytes = build_report_pdf(sel)
                    safe_base = os.path.splitext(os.path.basename(sel["image_name"]))[0] or "detection"
                    st.download_button(
                        "⬇️  Download PDF Report",
                        data=pdf_bytes,
                        file_name=f"report_{safe_base}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                with act2:
                    if st.button("🗑️  Delete Record", type="secondary", use_container_width=True, key=f"delete_{sel.get('timestamp', '')}"):
                        mongo_collection.delete_one(
                            {
                                "image_name": sel["image_name"],
                                "timestamp": sel["timestamp"],
                            }
                        )
                        for p in (input_path, detected_path):
                            if p and os.path.isfile(p):
                                try:
                                    os.remove(p)
                                except OSError:
                                    pass
                        st.success("Record deleted.")
                        st.rerun()


# =============================================================================
# PAGE: ABOUT
# =============================================================================

elif page == "About":
    st.markdown(
        """
        <h2 style="font-family:'Cormorant Garamond',serif;font-size:1.5rem;margin-bottom:0.6rem;">
            About This App
        </h2>
        <p style="font-family:'Source Sans 3',sans-serif;font-size:1.08rem;line-height:1.7;color:var(--muted);max-width:700px;">
            This app helps you understand ancient Egyptian symbols from paintings.
            Upload an image or use live camera capture, and the system will detect symbols and generate
            a clear final interpretation.
        </p>
        <p style="margin-top:0.5rem;font-family:'Source Sans 3',sans-serif;font-size:1rem;color:var(--muted);">
            Simple workflow. Clear output. Easy to use.
        </p>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """<div class="ess-card">
            <div class="ess-card-title">How To Use</div>
            <ul class="about-list" style="padding-left:1.2rem;">
                <li>Go to Analyze and upload an image or open live camera.</li>
                <li>Click detection/analyze to process the image.</li>
                <li>View detected symbols and the final interpretation.</li>
                <li>Open History to review previous results.</li>
                <li>Download a PDF report when needed.</li>
            </ul>
            </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """<div class="ess-card">
            <div class="ess-card-title">What You Get</div>
            <ul class="about-list" style="padding-left:1.2rem;">
                <li>Fast symbol detection from paintings.</li>
                <li>Clear, readable final interpretation output.</li>
                <li>Searchable symbol dictionary.</li>
                <li>History page with record details.</li>
                <li>Exportable PDF report for documentation.</li>
            </ul>
            </div>""",
            unsafe_allow_html=True,
        )


# =============================================================================
# FOOTER
# =============================================================================
