"""
CropCare Pro - Retailer Edition (Artisanal Botanical Atelier)
On-Device Diagnostic & Smart Stock Dispensing Terminal for Agri-Input Retailers & Krishi Kendras.
Crafted with bespoke botanical apothecary aesthetics, vernacular localization, and multi-tier monetization.
"""

import os
import sys

# Ensure repository root is always in sys.path for Streamlit Cloud (/mount/src/cropcare-ai)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import io
import time
import json
import urllib.parse
import urllib.request
import importlib
import numpy as np
import cv2
from PIL import Image
import streamlit as st

# Force hot-reload of local modules on Streamlit Cloud to prevent stale in-memory caching
import knowledge_base
import engine
import translations
importlib.reload(knowledge_base)
importlib.reload(engine)
importlib.reload(translations)

from knowledge_base import DISEASE_DATABASE, EDGE_BENCHMARKS, MONETIZATION_TIERS
from engine import (
    run_edge_inference,
    assess_image_quality,
    preprocess_leaf_image
)
from translations import UI_TRANSLATIONS


class SafeTranslationDict(dict):
    """Dictionary that never raises KeyError, falling back safely to English or key title."""
    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        en_table = UI_TRANSLATIONS.get("en", {})
        if key in en_table:
            return en_table[key]
        return key.replace("_", " ").title()
        
    def get(self, key, default=None):
        if key in self:
            return super().get(key, default)
        en_table = UI_TRANSLATIONS.get("en", {})
        if key in en_table:
            return en_table.get(key, default)
        return default if default is not None else key.replace("_", " ").title()

# ---------------------------------------------------------
# Page Configuration & Artisanal Botanical Atelier Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="CropCare Pro | Agri-Retailer Station",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Artisanal CSS: Handcrafted botanical typography, parchment textures, gold filigree accents
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,850;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">

<style>
    /* Global Background & Root Atmosphere */
    .stApp {
        background-color: #f8fafc !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }
    
    [data-testid="stMain"] {
        color: #0f172a !important;
        background-color: #f8fafc !important;
    }
    
    /* Editorial Typography - High Contrast Charcoal Black */
    h1, h2, h3, .serif-font {
        font-family: 'Playfair Display', Georgia, serif !important;
        letter-spacing: -0.3px;
    }
    
    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] h4,
    [data-testid="stMain"] h5,
    [data-testid="stMain"] h6 {
        color: #0f172a !important;
        font-weight: 800 !important;
    }
    [data-testid="stMain"] p,
    [data-testid="stMain"] span,
    [data-testid="stMain"] li {
        color: #1e293b !important;
    }
    [data-testid="stMain"] [data-testid="stCaptionContainer"] p,
    [data-testid="stMain"] .stCaption {
        color: #475569 !important;
        font-weight: 500 !important;
    }
    
    /* Widget & Radio Labels */
    [data-testid="stRadio"] label p,
    [data-testid="stWidgetLabel"] label p {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    
    /* Tabs: Handcrafted Underline */
    .stTabs [data-baseweb="tab"] {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 0.94rem !important;
        border-bottom: 2px solid transparent !important;
        padding: 10px 18px !important;
    }
    .stTabs [aria-selected="true"] {
        color: #0f172a !important;
        font-weight: 800 !important;
        border-bottom: 2.5px solid #15803d !important;
    }
    
    /* Sidebar: Warm Clean Crisp Linen */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1.5px solid #e2e8f0 !important;
        box-shadow: 2px 0 12px rgba(15, 23, 42, 0.04) !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #0f172a !important;
    }
    
    /* Primary Action Buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #15803d 0%, #166534 100%) !important;
        color: #ffffff !important;
        border: 1px solid #15803d !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(21, 128, 61, 0.22) !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1.5px) !important;
        box-shadow: 0 6px 18px rgba(21, 128, 61, 0.35) !important;
        background: #14532d !important;
    }
    
    /* Artisanal Header Banner */
    .artisan-header {
        background: radial-gradient(circle at 12% 18%, #143e2b 0%, #0d2818 60%, #06180f 100%);
        color: #ffffff;
        padding: 26px 32px;
        border-radius: 16px;
        border: 1px solid rgba(212, 175, 55, 0.45);
        box-shadow: 0 10px 30px rgba(7, 25, 17, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.12);
        margin-bottom: 22px;
        position: relative;
        overflow: hidden;
    }
    .artisan-header::after {
        content: "";
        position: absolute;
        top: 0; right: 0; bottom: 0; width: 220px;
        background: radial-gradient(circle, rgba(212, 175, 55, 0.12) 0%, transparent 70%);
        pointer-events: none;
    }
    .artisan-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2.35rem;
        font-weight: 850;
        margin: 0;
        letter-spacing: -0.5px;
        color: #ffffff !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .artisan-subtitle {
        font-size: 1.02rem;
        color: #f1f5f9 !important;
        margin-top: 5px;
        font-weight: 450;
        letter-spacing: 0.2px;
    }
    
    /* Artisanal Badges - High Contrast Text */
    .artisan-meta {
        margin-top: 14px;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
    }
    .badge-artisan {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 0.3px;
    }
    .badge-gold {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #78350f !important;
        border: 1px solid #d97706;
    }
    .badge-emerald {
        background: #047857;
        color: #ffffff !important;
        border: 1px solid #34d399;
    }
    .badge-parchment {
        background: rgba(255, 255, 255, 0.22);
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.45);
    }
    
    /* Apothecary Product SKU Card */
    .apothecary-sku {
        background: #ffffff;
        border: 1.5px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 14px;
        transition: all 0.25s ease;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        position: relative;
    }
    .apothecary-sku:hover {
        border-color: #15803d;
        box-shadow: 0 6px 18px rgba(21, 128, 61, 0.12);
        transform: translateY(-1px);
    }
    
    /* Apothecary Vintage Prescription Memo Card */
    .apothecary-receipt {
        background: #ffffff;
        border: 2px dashed #cbd5e1;
        border-radius: 14px;
        padding: 30px 34px;
        margin: 18px 0;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        font-family: 'Playfair Display', Georgia, serif;
        position: relative;
    }
    .apothecary-receipt::before {
        content: "✦ OFFICIAL KRISHI KENDRA DISPENSARY ✦";
        display: block;
        text-align: center;
        font-size: 0.76rem;
        letter-spacing: 3px;
        color: #0f172a;
        font-weight: 700;
        margin-bottom: 12px;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 8px;
    }
    .receipt-watermark {
        position: absolute;
        top: 45%; right: 40px;
        transform: translateY(-50%) rotate(-14deg);
        border: 2.5px solid rgba(185, 28, 28, 0.35);
        color: rgba(185, 28, 28, 0.38);
        font-size: 1.15rem;
        font-weight: 900;
        letter-spacing: 2.5px;
        padding: 8px 18px;
        border-radius: 8px;
        text-transform: uppercase;
        pointer-events: none;
    }
    
    /* Museum Specimen Slide Mount for XAI */
    .specimen-mount {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
        text-align: center;
        position: relative;
    }
    .specimen-tag {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        color: #0f172a;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 4px;
        display: inline-block;
        margin-top: 8px;
    }
    
    /* High Contrast Action Steps */
    .action-step-artisan {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4.5px solid #15803d;
        padding: 12px 18px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 10px;
        font-size: 0.95rem;
        color: #0f172a !important;
        font-weight: 500;
    }
    
    /* Crisp Info Pill Tag */
    .artisan-pill {
        background: #ffffff;
        border: 1.5px solid #cbd5e1;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.84rem;
        color: #0f172a !important;
        font-weight: 600;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "language" not in st.session_state:
    st.session_state["language"] = "en"
if "current_image" not in st.session_state:
    st.session_state["current_image"] = None
if "current_image_name" not in st.session_state:
    st.session_state["current_image_name"] = None
if "inference_result" not in st.session_state:
    st.session_state["inference_result"] = None
if "preset_hint" not in st.session_state:
    st.session_state["preset_hint"] = None
if "nav_index" not in st.session_state:
    st.session_state["nav_index"] = 0
if "current_tier" not in st.session_state:
    st.session_state["current_tier"] = "pro"
if "cart_items" not in st.session_state:
    st.session_state["cart_items"] = []
if "farmer_name" not in st.session_state:
    st.session_state["farmer_name"] = "Shivanna Gowda"
if "farmer_phone" not in st.session_state:
    st.session_state["farmer_phone"] = "9845012345"
if "farmer_village" not in st.session_state:
    st.session_state["farmer_village"] = "Kolar Rural, Karnataka"
if "shop_name" not in st.session_state:
    st.session_state["shop_name"] = "Kisan Seva Krishi Kendra & Pesticides"
if "shop_gst" not in st.session_state:
    st.session_state["shop_gst"] = "29AAAAA0000A1Z5 / LIC-KA-8492"
if "shop_phone" not in st.session_state:
    st.session_state["shop_phone"] = "080-28394411 / 9448011223"
if "scans_used_this_month" not in st.session_state:
    st.session_state["scans_used_this_month"] = 14
if "weather_risk_factor" not in st.session_state:
    st.session_state["weather_risk_factor"] = 1.25
if "weather_city_name" not in st.session_state:
    st.session_state["weather_city_name"] = "Kolar, Karnataka (Tomato & Veg Belt)"
if "apply_weather_factor" not in st.session_state:
    st.session_state["apply_weather_factor"] = True


# ---------------------------------------------------------
# Helper Functions & Live Data Integrations
# ---------------------------------------------------------
INDIAN_AGRI_DISTRICTS = {
    "Kolar, Karnataka (Tomato & Veg Belt)": {"lat": 13.136, "lon": 78.129, "crop": "Tomato"},
    "Nashik, Maharashtra (Onion & Horticulture)": {"lat": 19.997, "lon": 73.789, "crop": "Tomato"},
    "Guntur, Andhra Pradesh (Chilli & Cotton)": {"lat": 16.306, "lon": 80.436, "crop": "Chilli"},
    "Karnal, Haryana (Paddy & Wheat Belt)": {"lat": 29.685, "lon": 76.990, "crop": "Rice"},
    "Shimla, Himachal Pradesh (Apple & Potato)": {"lat": 31.104, "lon": 77.173, "crop": "Potato"},
    "Varanasi, Uttar Pradesh (Gangetic Plains)": {"lat": 25.317, "lon": 82.973, "crop": "Tomato"},
    "Baramati / Pune, Maharashtra (Maize & Sugarcane)": {"lat": 18.152, "lon": 74.577, "crop": "Corn"},
}


@st.cache_data(ttl=600)
def fetch_live_weather(lat: float, lon: float) -> dict:
    """Queries Open-Meteo live API to extract microclimate data and compute disease surge risk factor."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,relative_humidity_2m_max&timezone=auto"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CropCareAI/1.0"})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode("utf-8"))
            current = data.get("current", {})
            daily = data.get("daily", {})
            temp = float(current.get("temperature_2m", 26.0))
            rh = float(current.get("relative_humidity_2m", 70.0))
            wind = float(current.get("wind_speed_10m", 12.0))
            rain_prob = float(daily.get("precipitation_probability_max", [45.0])[0]) if daily.get("precipitation_probability_max") else 40.0
            
            # Epidemiological disease pressure scoring
            risk = 10.0
            if 18.0 <= temp <= 29.0:
                risk += 35.0
            elif 14.0 <= temp <= 33.0:
                risk += 20.0
            else:
                risk += 5.0
                
            if rh >= 80.0:
                risk += 35.0
            elif rh >= 65.0:
                risk += 20.0
            else:
                risk += 5.0
                
            risk += min(rain_prob * 0.30, 30.0)
            risk_score = round(min(max(risk, 5.0), 100.0), 1)
            
            # Risk factor multiplier for economic calculations (bounded 0.85x to 1.65x)
            factor = round(1.0 + (risk_score - 40.0) / 100.0, 2)
            factor = max(0.85, min(factor, 1.65))
            
            return {
                "success": True,
                "temp": temp,
                "rh": rh,
                "wind": wind,
                "rain_prob": rain_prob,
                "risk_score": risk_score,
                "factor": factor,
                "is_live": True
            }
    except Exception as e:
        return {
            "success": False,
            "temp": 26.5,
            "rh": 76.0,
            "wind": 10.5,
            "rain_prob": 55.0,
            "risk_score": 70.0,
            "factor": 1.30,
            "is_live": False,
            "error": str(e)
        }
def load_sample_image(filename: str, hint_key: str):
    sample_dir = os.path.join(os.path.dirname(__file__), "samples")
    path = os.path.join(sample_dir, filename)
    if os.path.exists(path):
        img_bgr = cv2.imread(path)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        st.session_state["current_image"] = img_rgb
        st.session_state["current_image_name"] = filename
        st.session_state["preset_hint"] = hint_key
        st.session_state["inference_result"] = run_edge_inference(img_rgb, hint_key)
        st.session_state["scans_used_this_month"] += 1


def format_inr(val: float) -> str:
    """Formats large figures into Indian Crores (Cr), Lakhs (L), or standard thousands."""
    abs_v = abs(val)
    if abs_v >= 10_000_000:
        return f"₹ {val / 10_000_000:.2f} Cr"
    elif abs_v >= 100_000:
        return f"₹ {val / 100_000:.2f} L"
    else:
        return f"₹ {val:,.0f}"


# Agronomic benchmarks for per-acre economic modeling
CROP_ACRE_BENCHMARKS = {
    "Tomato": {
        "avg_yield_tonnes": 18.0,
        "market_price_per_kg": 18.0,
        "gross_acre_value": 324000,
        "typical_sprays": 6,
        "default_cost_per_spray": 950,
        "default_loss_prevented_pct": 30.0,
    },
    "Potato": {
        "avg_yield_tonnes": 15.0,
        "market_price_per_kg": 15.0,
        "gross_acre_value": 225000,
        "typical_sprays": 5,
        "default_cost_per_spray": 850,
        "default_loss_prevented_pct": 28.0,
    },
    "Corn / Maize": {
        "avg_yield_tonnes": 3.2,
        "market_price_per_kg": 21.0,
        "gross_acre_value": 67200,
        "typical_sprays": 3,
        "default_cost_per_spray": 650,
        "default_loss_prevented_pct": 22.0,
    },
    "Rice / Paddy": {
        "avg_yield_tonnes": 2.8,
        "market_price_per_kg": 23.0,
        "gross_acre_value": 64400,
        "typical_sprays": 4,
        "default_cost_per_spray": 750,
        "default_loss_prevented_pct": 25.0,
    },
    "Chilli / Capsicum": {
        "avg_yield_tonnes": 8.0,
        "market_price_per_kg": 45.0,
        "gross_acre_value": 360000,
        "typical_sprays": 7,
        "default_cost_per_spray": 1100,
        "default_loss_prevented_pct": 35.0,
    },
    "Cotton": {
        "avg_yield_tonnes": 1.2,
        "market_price_per_kg": 72.0,
        "gross_acre_value": 86400,
        "typical_sprays": 5,
        "default_cost_per_spray": 900,
        "default_loss_prevented_pct": 28.0,
    }
}


# Auto-load default sample on launch
if st.session_state["current_image"] is None:
    load_sample_image("Tomato_Early_Blight.jpg", "Tomato___Early_Blight")


# ---------------------------------------------------------
# Sidebar Navigation & Settings
# ---------------------------------------------------------
with st.sidebar:
    # Handcrafted Atelier Seal Logo
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #e2e8f0;">
        <div style="background: #15803d; width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(21,128,61,0.25);">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
        </div>
        <div>
            <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.25rem; font-weight: 850; color: #0f172a; line-height: 1.1;">CropCare Pro</div>
            <div style="font-size: 0.70rem; color: #b45309; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">Botanical Retail POS</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Vernacular Language Selector
    lang_display_names = {
        "en": "🇬🇧 English",
        "hi": "🇮🇳 हिन्दी (Hindi)",
        "kn": "🌾 ಕನ್ನಡ (Kannada)",
        "te": "🌱 తెలుగు (Telugu)"
    }
    
    # key="language" binds directly to session_state — no manual assignment needed,
    # avoids the double-rerun caused by writing to session_state after widget return.
    st.selectbox(
        "🗣️ Shopkeeper / Counter Language",
        options=list(lang_display_names.keys()),
        format_func=lambda x: lang_display_names[x],
        key="language"
    )
    
    # Active language translation dictionary (wrapped defensively against KeyErrors)
    raw_t = UI_TRANSLATIONS.get(st.session_state["language"], UI_TRANSLATIONS.get("en", {}))
    T = SafeTranslationDict(raw_t)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation Modes
    # Radio bound via key to avoid manual session_state write triggering extra rerun.
    # We store nav_index as int; on language change, clamp to valid range.
    current_modes = T["nav_modes"]
    safe_nav_index = min(st.session_state["nav_index"], len(current_modes) - 1)
    selected_mode_text = st.radio(
        T["nav_label"],
        current_modes,
        index=safe_nav_index
    )
    nav_mode_index = current_modes.index(selected_mode_text)
    # Only write back if the index actually changed — avoids spurious state diffs
    if nav_mode_index != st.session_state["nav_index"]:
        st.session_state["nav_index"] = nav_mode_index
    
    st.markdown("---")
    
    # Current Active Plan Badge (Artisanal Finishes)
    tier_info = MONETIZATION_TIERS[st.session_state["current_tier"]]
    st.markdown(f"""
    <div style='background: #ffffff; border: 1.5px solid #d4af37; border-radius: 10px; padding: 14px 16px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <span style='font-size: 0.72rem; font-weight: 800; color: #854d0e; letter-spacing: 0.5px;'>RETAIL TIER</span>
            <span style='background: {tier_info["color"]}; color: #ffffff; padding: 3px 8px; border-radius: 12px; font-size: 0.68rem; font-weight: 750;'>{tier_info["name"].split()[0]}</span>
        </div>
        <div style='font-family: \"Playfair Display\", serif; font-size: 1.05rem; font-weight: 850; color: #0f172a; margin-top: 5px;'>{tier_info["name"]}</div>
        <div style='font-size: 0.80rem; color: #b45309; font-weight: 700;'>{tier_info["billing_period"]}</div>
        <div style='font-size: 0.76rem; color: #475569; margin-top: 6px; border-top: 1px dashed #e2e8f0; padding-top: 6px;'>
            Counter Scans: <strong style='color: #0f172a;'>{st.session_state["scans_used_this_month"]}</strong> / {"Unlimited" if tier_info["scan_limit_monthly"] > 1000 else tier_info["scan_limit_monthly"]}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Offline Edge Engine Status
    st.markdown(f"""
    <div style='background: #ffffff; border: 1.5px solid #e2e8f0; border-left: 4.5px solid #15803d; border-radius: 8px; padding: 12px 14px;'>
        <div style='font-size: 0.80rem; font-weight: 800; color: #0f172a; letter-spacing: 0.3px;'>
            {T["edge_engine_active"]}
        </div>
        <div style='font-size: 0.76rem; color: #334155; margin-top: 4px; line-height: 1.45;'>
            {T["edge_engine_desc"]}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(f"✦ {T['sidebar_footer']} ✦", unsafe_allow_html=True)


# ---------------------------------------------------------
# Artisanal Header Banner
# ---------------------------------------------------------
st.markdown(f"""
<div class="artisan-header">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
            <div class="artisan-title">{T["brand_title"]}</div>
            <div class="artisan-subtitle">{T["brand_subtitle"]}</div>
        </div>
        <div style="text-align: right; display: none; @media(min-width: 768px){{display: block;}}">
            <span style="font-family: 'Playfair Display', Georgia, serif; font-size: 0.85rem; color: #fde68a; font-style: italic;">Atelier Dispensary</span>
        </div>
    </div>
    <div class="artisan-meta">
        <span class="badge-artisan badge-emerald">{T["badge_offline"]}</span>
        <span class="badge-artisan badge-gold">🏆 {tier_info["name"]}</span>
        <span class="badge-artisan badge-parchment">🏛️ {st.session_state["shop_name"]}</span>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# MODE 0: COUNTER DIAGNOSIS & STOCK DISPENSER
# =========================================================
if nav_mode_index == 0:
    col_input, col_result = st.columns([1.05, 1.35], gap="large")
    
    # ------------------ LEFT COLUMN: CUSTOMER CHECK-IN & SCAN ------------------
    with col_input:
        st.markdown(f"### **{T['step1_title']}**")
        st.caption(T["step1_caption"])
        
        # Farmer customer profile inputs in artisanal styling
        with st.expander("📋 Farmer Customer Ledger (For Prescription & Record)", expanded=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                st.session_state["farmer_name"] = st.text_input(T["farmer_name_label"], value=st.session_state["farmer_name"])
            with f_col2:
                st.session_state["farmer_phone"] = st.text_input(T["farmer_phone_label"], value=st.session_state["farmer_phone"])
            st.session_state["farmer_village"] = st.text_input(T["farmer_village_label"], value=st.session_state["farmer_village"])

        input_methods = [T["method_presets"], T["method_camera"], T["method_upload"]]
        input_method = st.radio(
            T["input_method_label"],
            input_methods,
            horizontal=True
        )
        
        if input_method == T["method_presets"]:
            st.markdown(f"##### **{T['sample_lib_title']}**")
            
            sample_keys = [
                ("Tomato___Early_Blight", "Tomato_Early_Blight.jpg"),
                ("Tomato___Late_Blight", "Tomato_Late_Blight.jpg"),
                ("Tomato___Bacterial_Spot", "Tomato_Bacterial_Spot.jpg"),
                ("Tomato___Healthy", "Tomato_Healthy.jpg"),
                ("Corn___Common_Rust", "Corn_Common_Rust.jpg"),
                ("Rice___Blast", "Rice_Blast.jpg")
            ]
            
            selected_sample_item = st.selectbox(
                T["sample_lib_title"],
                options=sample_keys,
                format_func=lambda s: T["sample_options"].get(s[0], s[0])
            )
            
            if st.button(T["btn_load_diagnose"], type="primary"):
                load_sample_image(selected_sample_item[1], selected_sample_item[0])
                
        elif input_method == T["method_camera"]:
            camera_img = st.camera_input(T["camera_label"])
            if camera_img is not None:
                pil_img = Image.open(camera_img)
                img_rgb = np.array(pil_img.convert("RGB"))
                st.session_state["current_image"] = img_rgb
                st.session_state["current_image_name"] = "Counter_Cam_Scan.jpg"
                st.session_state["preset_hint"] = None
                with st.spinner("Processing offline MobileNet model..."):
                    st.session_state["inference_result"] = run_edge_inference(img_rgb)
                    st.session_state["scans_used_this_month"] += 1
                    
        elif input_method == T["method_upload"]:
            uploaded_file = st.file_uploader(T["upload_label"], type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                pil_img = Image.open(uploaded_file)
                img_rgb = np.array(pil_img.convert("RGB"))
                st.session_state["current_image"] = img_rgb
                st.session_state["current_image_name"] = uploaded_file.name
                st.session_state["preset_hint"] = None
                if st.button(T["btn_diagnose_upload"], type="primary"):
                    with st.spinner("Processing leaf..."):
                        st.session_state["inference_result"] = run_edge_inference(img_rgb)
                        st.session_state["scans_used_this_month"] += 1

        # Display current input image & image quality card
        if st.session_state["current_image"] is not None:
            st.markdown("<br>", unsafe_allow_html=True)
            st.image(st.session_state["current_image"], caption=T["leaf_img_caption"])
            
            # Quality assessment badge
            if st.session_state["inference_result"]:
                q_info = st.session_state["inference_result"]["quality_info"]
                q_badge_color = "#15803d" if q_info["is_acceptable"] else "#b45309"
                q_border = "#86efac" if q_info["is_acceptable"] else "#fde68a"
                
                if q_info["quality_status"] == "Good":
                    q_status_trans = T["quality_good"]
                elif "Blurry" in q_info["quality_status"]:
                    q_status_trans = T["quality_blurry"]
                elif "Dark" in q_info["quality_status"]:
                    q_status_trans = T["quality_dark"]
                else:
                    q_status_trans = T["quality_glare"]
                    
                st.markdown(f"""
                <div style='background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 8px; padding: 10px 14px; margin-top: 8px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span style='font-size: 0.85rem; font-weight: 700; color: #0f172a;'>{T["cv_quality_title"]}</span>
                        <span style='color: #ffffff; background: {q_badge_color}; font-weight: 800; font-size: 0.76rem; padding: 3px 8px; border-radius: 4px;'>{q_status_trans}</span>
                    </div>
                    <div style='font-size: 0.78rem; color: #475569; margin-top: 6px;'>
                        {T["cv_sharpness"]} <strong style='color: #0f172a;'>{q_info["laplacian_var"]:.1f}</strong> | {T["cv_brightness"]} <strong style='color: #0f172a;'>{q_info["mean_brightness"]:.1f}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(T["awaiting_leaf_hint"])

    # ------------------ RIGHT COLUMN: DIAGNOSTIC & STOCK DISPENSING ------------------
    with col_result:
        if st.session_state["inference_result"] is not None:
            res = st.session_state["inference_result"]
            top_info = res["disease_info"]
            lang = st.session_state["language"]
            trans = top_info["translations"].get(lang, top_info["translations"]["en"])
            
            if "Healthy" in res["severity"]:
                sev_label = T["sev_healthy"]
            elif "Mild" in res["severity"]:
                sev_label = T["sev_mild"]
            elif "Moderate" in res["severity"]:
                sev_label = T["sev_moderate"]
            else:
                sev_label = T["sev_severe"]

            if res["low_confidence_flag"]:
                st.warning(T["low_conf_warning"])
                
            # Artisanal Diagnosis Banner
            st.markdown(f"### **{T['step2_title']}**")
            
            diag_html = f"""
            <div style="background: #ffffff; border-radius: 14px; border: 2px solid #cbd5e1; border-top: 6px solid {res['severity_color']}; padding: 20px 24px; box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06); margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <div>
                        <span style="font-size: 0.76rem; text-transform: uppercase; letter-spacing: 1px; color: #475569; font-weight: 800;">{T["detected_condition"]}</span>
                        <h2 style="margin: 3px 0 0 0; color: #0f172a !important; font-family: 'Playfair Display', Georgia, serif; font-size: 2.0rem; font-weight: 850;">{trans['label']}</h2>
                        <div style="color: #475569 !important; font-size: 0.95rem; margin-top: 3px; font-style: italic; font-weight: 500;">{top_info['pathogen']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 2.3rem; font-weight: 850; color: {res['severity_color']}; line-height: 1.1;">{res['top_confidence_pct']}%</div>
                        <div style="font-size: 0.68rem; color: #64748b; font-weight: 750; letter-spacing: 0.8px;">{T["confidence_score"]}</div>
                    </div>
                </div>
                <div style="margin-top: 16px; padding-top: 14px; border-top: 1px solid #e2e8f0; display: flex; flex-wrap: wrap; gap: 10px;">
                    <span class="artisan-pill">{T["crop_label"]} <strong style="color: #0f172a;">{top_info['crop']}</strong></span>
                    <span class="artisan-pill">{T["severity_label"]} <strong style="color: {res['severity_color']};">{sev_label}</strong></span>
                    <span class="artisan-pill">{T["lesion_area_label"]} <strong style="color: #0f172a;">{res['lesion_coverage_pct']}%</strong></span>
                    <span class="artisan-pill">{T["inference_latency_label"]} <strong style="color: #0f172a;">{res['inference_time_ms']} ms</strong></span>
                </div>
            </div>
            """
            st.markdown(diag_html, unsafe_allow_html=True)
            
            # Read Aloud to Farmer Audio Button
            speech_text = f"{trans['label']}. {trans['step1']} {trans['step2']} {trans['step3']}"
            st.markdown(f"""
            <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 18px;'>
                <button onclick="
                    const synth = window.speechSynthesis;
                    synth.cancel();
                    const utter = new SpeechSynthesisUtterance(`{speech_text}`);
                    utter.rate = 0.9;
                    synth.speak(utter);
                " style='background: linear-gradient(135deg, #0e3827, #1b4d36); color: #ffffff; border: 1px solid #d4af37; padding: 10px 20px; border-radius: 8px; font-size: 0.92rem; font-weight: 700; cursor: pointer; box-shadow: 0 4px 12px rgba(14,56,39,0.25);'>
                    {T["audio_btn"]} ({lang_display_names[lang]})
                </button>
                <span style='font-size: 0.82rem; color: #526154; font-weight: 500;'>{T["audio_caption"]}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Stock Dispensing & Bill Section
            st.markdown(f"### **{T['step3_title']}**")
            st.caption(T["step3_caption"])
            
            tab_stock, tab_agri, tab_cult, tab_chem = st.tabs([
                T["inventory_tab"],
                T["agronomy_tab"],
                T["cultural_tab"],
                T["chemical_tab"]
            ])
            
            # Tab 1: In-Stock Products to Dispense
            with tab_stock:
                st.markdown(f"##### **{T['stock_sku_header']}**")
                
                stock_items = top_info.get("retail_inventory", [])
                for idx, sku in enumerate(stock_items):
                    p_badge = "🌟 MASTER BIO-FORMULA" if sku.get("is_primary") else "ALTERNATIVE / SECONDARY"
                    p_badge_bg = "#fef3c7" if sku.get("is_primary") else "#f1f5f9"
                    p_badge_color = "#92400e" if sku.get("is_primary") else "#334155"
                    
                    st.markdown(f"""
                    <div class="apothecary-sku">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <span style="background: {p_badge_bg}; color: {p_badge_color}; font-size: 0.70rem; font-weight: 800; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px;">{p_badge}</span>
                                <h4 style="margin: 6px 0 2px 0; color: #0f172a; font-family: 'Playfair Display', Georgia, serif; font-size: 1.2rem;">{sku['name']}</h4>
                                <div style="font-size: 0.82rem; color: #475569;">Brand: <strong style="color: #0f172a;">{sku['brand']}</strong> | Pack: <strong style="color: #0f172a;">{sku['pack_size']}</strong> | Class: <strong style="color: #0f172a;">{sku['category']}</strong></div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 1.4rem; font-weight: 850; color: #0f172a;">₹ {sku['mrp']}</div>
                                <div style="font-size: 0.76rem; font-weight: 750; color: #0f172a; margin-top: 3px;"><span style="background: #f1f5f9; color: #0f172a; padding: 3px 7px; border-radius: 4px; border: 1px solid #cbd5e1;">Margin: <strong style="color: #15803d;">{sku['margin_pct']}%</strong> (₹{sku['mrp'] - sku['dealer_price']})</span></div>
                            </div>
                        </div>
                        <div style="margin-top: 10px; font-size: 0.86rem; color: #1e293b; background: #f8fafc; border: 1px solid #e2e8f0; padding: 10px 14px; border-radius: 6px;">
                            <strong style="color: #0f172a;">{T['dosage_label']}</strong> {sku['dosage']}<br>
                            <span style="font-size: 0.80rem; color: #475569;">{sku['usage_notes']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    b_col1, b_col2 = st.columns([1.2, 2.8])
                    with b_col1:
                        if st.button(f"➕ Add to Bill (#{idx+1})", key=f"btn_add_sku_{sku['sku_id']}"):
                            st.session_state["cart_items"].append({
                                "sku_id": sku["sku_id"],
                                "name": sku["name"],
                                "pack_size": sku["pack_size"],
                                "price": sku["mrp"],
                                "dosage": sku["dosage"]
                            })
                            st.toast(f"Added {sku['name']} to Customer Bill!", icon="🛒")
                    with b_col2:
                        st.caption(f"Stock Status: **{sku['in_stock']} units ready** on shelf.")
                        
                st.info(T["neem_tip"])
                
                # Cart Summary and Shortcut to Bill
                if st.session_state["cart_items"]:
                    total_cart_val = sum(item["price"] for item in st.session_state["cart_items"])
                    st.markdown(f"""
                    <div style='background: #ffffff; border: 2px solid #d4af37; border-radius: 10px; padding: 14px 18px; margin-top: 14px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 12px rgba(212,175,55,0.15);'>
                        <div>
                            <span style='font-size: 0.82rem; font-weight: 800; color: #92400e; text-transform: uppercase;'>ORDER TOTAL ({len(st.session_state['cart_items'])} ITEMS PRESCRIBED)</span>
                            <div style='font-family: \"Playfair Display\", serif; font-size: 1.4rem; font-weight: 850; color: #0f172a;'>Total Bill: ₹ {total_cart_val}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("🧾 View & Print Botanical Prescription Bill →", type="primary"):
                        st.session_state["nav_index"] = 1
                        st.rerun()

            with tab_agri:
                st.markdown(f"**{T['guidance_directive']}** *{trans['tagline']}*")
                for step_txt in [trans["step1"], trans["step2"], trans["step3"]]:
                    st.markdown(f"""
                    <div class="action-step-artisan">
                        <strong>{T['action_prefix']}</strong> {step_txt}
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown(f"##### **{T['detailed_steps_title']}**")
                for item in top_info["action_plan"]["immediate_actions"]:
                    st.markdown(f"• {item}")
                    
            with tab_cult:
                st.markdown(f"##### **{T['cultural_title']}**")
                for prac in top_info["action_plan"]["cultural_prevention"]:
                    st.markdown(f"• **{prac}**")
                    
            with tab_chem:
                st.markdown(f"##### **{T['chemical_title']}**")
                st.warning(top_info["action_plan"]["chemical_advisory"])
                st.caption(T["chemical_sdg_caption"])
                # -------------------------------------------------------------
                # Explainable AI & Lesion Heatmap Visual Proof (Expander)
                # -------------------------------------------------------------
                with st.expander("🔬 " + T["xai_title"], expanded=False):
                    st.markdown(f"<p style='color: #475569;'>{T['xai_desc']}</p>", unsafe_allow_html=True)
                    res = st.session_state["inference_result"]
                    col_img1, col_img2, col_img3 = st.columns(3)
                    with col_img1:
                        st.markdown(f"##### **{T['xai_col1_title']}**")
                        st.markdown('<div class="specimen-mount">', unsafe_allow_html=True)
                        st.image(res["enhanced_img"])
                        st.markdown(f'<div class="specimen-tag">PLATE 01 • FOLIAR CONTOUR ({res["prep_info"]["leaf_coverage_ratio"]*100:.1f}%)</div></div>', unsafe_allow_html=True)
                    with col_img2:
                        st.markdown(f"##### **{T['xai_col2_title']}**")
                        st.markdown('<div class="specimen-mount">', unsafe_allow_html=True)
                        st.image(res["heatmap_img"])
                        st.markdown('<div class="specimen-tag" style="background: #fef2f2; color: #991b1b; border-color: #fecaca;">PLATE 02 • GRAD-CAM ACTIVATION MAP</div></div>', unsafe_allow_html=True)
                        st.caption(T["xai_col2_sub"])
                    with col_img3:
                        st.markdown(f"##### **{T['xai_col3_title']}**")
                        st.markdown('<div class="specimen-mount">', unsafe_allow_html=True)
                        st.image(res["annotated_img"])
                        st.markdown(f'<div class="specimen-tag">PLATE 03 • {res["lesion_count"]} LESION CLUSTERS</div></div>', unsafe_allow_html=True)

                    st.markdown(f"##### **{T['xai_metrics_title']}**")
                    mx1, mx2, mx3, mx4 = st.columns(4)
                    mx1.metric(T["metric_necrotic"], f"{res['lesion_coverage_pct']}%")
                    mx2.metric(T["metric_chlorosis"], f"{res['chlorosis_coverage_pct']}%")
                    mx3.metric(T["metric_severity"], res["severity"].split()[0])
                    mx4.metric(T["metric_sharpness"], f"{res['quality_info']['laplacian_var']:.1f}")

                # -------------------------------------------------------------
                # Branded Botanical Prescription Slip & Instant Cash Memo
                # -------------------------------------------------------------
                st.markdown("---")
                st.markdown(f"### **{T['inv_title']}**")
                st.caption(T["inv_desc"])

                # Auto-populate cart with primary recommendation if empty
                if not st.session_state["cart_items"] and top_info.get("retail_inventory"):
                    primary_sku = top_info["retail_inventory"][0]
                    st.session_state["cart_items"].append({
                        "sku_id": primary_sku["sku_id"],
                        "name": primary_sku["name"],
                        "pack_size": primary_sku["pack_size"],
                        "price": primary_sku["mrp"],
                        "dosage": primary_sku["dosage"]
                    })

                # Cart items manager
                if st.session_state["cart_items"]:
                    st.markdown("##### **Prescribed Items in Prescription:**")
                    for i, itm in enumerate(st.session_state["cart_items"]):
                        ci1, ci2, ci3, ci4 = st.columns([3, 1.5, 1.2, 0.8])
                        with ci1:
                            st.write(f"**{i+1}. {itm['name']}** ({itm['pack_size']})")
                            st.caption(f"Dosage: {itm['dosage']}")
                        with ci2:
                            st.write(f"₹ {itm['price']}")
                        with ci3:
                            st.write("Qty: 1")
                        with ci4:
                            if st.button("🗑️", key=f"del_cart_{i}"):
                                st.session_state["cart_items"].pop(i)
                                st.rerun()

                    total_invoice_amt = sum(item["price"] for item in st.session_state["cart_items"])

                    # Apothecary receipt view
                    diag_name = st.session_state["inference_result"]["disease_info"]["disease_name"]
                    crop_name = st.session_state["inference_result"]["disease_info"]["crop"]
                    items_rows_html = "".join([
                        f"""<tr>
                            <td style='padding: 8px 4px; border-bottom: 1px solid #ebdccb; font-size: 0.95rem;'>
                                <strong>{idx+1}. {itm['name']}</strong> ({itm['pack_size']})<br>
                                <span style='font-size: 0.80rem; color: #64748b; font-family: sans-serif;'>Dosage: {itm['dosage']}</span>
                            </td>
                            <td style='padding: 8px 4px; border-bottom: 1px solid #ebdccb; text-align: right; font-weight: 700; font-size: 0.95rem;'>₹ {itm['price']}</td>
                        </tr>""" for idx, itm in enumerate(st.session_state["cart_items"])
                    ])

                    visual_memo_html = f"""
                    <div class="apothecary-receipt">
                        <div class="receipt-watermark">AUTHENTICATED</div>
                        <div style="text-align: center; margin-bottom: 16px;">
                            <h2 style="margin: 0; color: #0f172a; font-size: 1.8rem;">{st.session_state['shop_name']}</h2>
                            <div style="font-size: 0.82rem; color: #854d0e; font-family: sans-serif; letter-spacing: 0.5px;">GSTIN/Lic: {st.session_state['shop_gst']} • Tel: {st.session_state['shop_phone']}</div>
                            <div style="font-size: 0.78rem; color: #475569; margin-top: 4px; font-family: sans-serif;">Receipt: POS-CK-{int(time.time())} • Date: {time.strftime('%d %B %Y, %H:%M')}</div>
                        </div>
                        
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px; font-family: sans-serif; font-size: 0.85rem; display: flex; justify-content: space-between;">
                            <div>
                                <div>Customer: <strong style='color: #0f172a;'>{st.session_state['farmer_name']}</strong></div>
                                <div>Location: <strong style='color: #0f172a;'>{st.session_state['farmer_village']}</strong></div>
                            </div>
                            <div style="text-align: right;">
                                <div>Tested Crop: <strong style='color: #0f172a;'>{crop_name}</strong></div>
                                <div>Diagnosis: <strong style="color: #b91c1c;">{diag_name}</strong></div>
                            </div>
                        </div>
                        
                        <table style="width: 100%; border-collapse: collapse; margin-bottom: 14px;">
                            <thead>
                                <tr style="border-bottom: 1.5px solid #d4af37; text-align: left; font-size: 0.80rem; color: #854d0e; text-transform: uppercase;">
                                    <th style="padding: 4px;">Prescribed Item & Spray Dosage</th>
                                    <th style="padding: 4px; text-align: right;">Amount</th>
                                </tr>
                            </thead>
                            <tbody>
                                {items_rows_html}
                            </tbody>
                        </table>
                        
                        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 2px solid #0f172a; padding-top: 12px; margin-top: 8px;">
                            <div style="font-size: 0.85rem; color: #475569; font-family: sans-serif;">Knapsack spray volume: 15L • Safe organic treatment</div>
                            <div style="text-align: right;">
                                <span style="font-size: 0.85rem; color: #475569; font-family: sans-serif;">TOTAL CASH DUE:</span>
                                <span style="font-size: 1.6rem; font-weight: 900; color: #0f172a; margin-left: 8px;">₹ {total_invoice_amt}</span>
                            </div>
                        </div>
                    </div>
                    """
                    st.markdown(visual_memo_html, unsafe_allow_html=True)

                    # Text format for download & WhatsApp
                    receipt_text = f"""============================================================
{st.session_state['shop_name'].upper()}
Reg/GSTIN: {st.session_state['shop_gst']}
Ph: {st.session_state['shop_phone']}
============================================================
OFFICIAL RETAIL TREATMENT PRESCRIPTION & CASH MEMO
Receipt No: POS-CK-{int(time.time())}
Date/Time : {time.strftime('%Y-%m-%d %H:%M')}

CUSTOMER DETAILS:
Farmer Name : {st.session_state['farmer_name']}
Mobile No.  : {st.session_state['farmer_phone']}
Village     : {st.session_state['farmer_village']}

DIAGNOSTIC FINDING (CropCare Pro On-Device Scan):
Crop Tested : {crop_name}
Disease ID  : {diag_name}
Status      : Verified on-device counter diagnosis

PRESCRIBED PRODUCTS DISPENSED:
------------------------------------------------------------
"""
                    for idx, itm in enumerate(st.session_state["cart_items"]):
                        receipt_text += f"{idx+1}. {itm['name']} ({itm['pack_size']})\n"
                        receipt_text += f"   Dosage : {itm['dosage']}\n"
                        receipt_text += f"   Price  : Rs. {itm['price']}\n\n"

                    receipt_text += f"""------------------------------------------------------------
TOTAL CASH AMOUNT : Rs. {total_invoice_amt}
------------------------------------------------------------
IMPORTANT SPRAYING INSTRUCTIONS FOR FARMER:
1. Spray only during early morning (6:30-9:30 AM) or dusk.
2. Mix thoroughly in clean water; use 15-liter knapsack sprayer.
3. Keep away from children and wear mask during spraying.
4. For repeat consultation, bring this receipt to counter.
============================================================
Thank you for visiting {st.session_state['shop_name']}!
Empowering Farmers with Accessible AI & Smart Agriculture.
============================================================
"""
                    col_act1, col_act2, col_act3 = st.columns(3)
                    with col_act1:
                        st.download_button(
                            T["btn_download_bill"],
                            data=receipt_text,
                            file_name=f"Prescription_Bill_{st.session_state['farmer_phone']}.txt",
                            mime="text/plain",
                            type="primary",
                            key="btn_down_p_bill"
                        )
                    with col_act2:
                        encoded_msg = urllib.parse.quote(receipt_text)
                        clean_phone = st.session_state['farmer_phone'].replace("+", "").replace("-", "").strip()
                        wa_url = f"https://wa.me/91{clean_phone}?text={encoded_msg}"
                        st.markdown(f"""
                        <a href="{wa_url}" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #25D366, #128C7E); color: white; padding: 10px 20px; border-radius: 8px; font-weight: 700; text-decoration: none; text-align: center; width: 100%; box-shadow: 0 4px 12px rgba(37,211,102,0.25);">
                            📲 Send Bill via WhatsApp
                        </a>
                        """, unsafe_allow_html=True)
                    with col_act3:
                        if st.button("🧹 Clear Prescribed Items", key="btn_clr_cart_main"):
                            st.session_state["cart_items"] = []
                            st.rerun()

        else:
            st.markdown(f"### **{T['step2_title']}**")
            st.info(T["awaiting_result_hint"])


# =========================================================
# MODE 1: LIVE WEATHER RADAR & OUTBREAK FORECASTER
# =========================================================
elif nav_mode_index == 1:
    st.markdown(f"### **{T['radar_title']}**")
    st.markdown(f"<p style='color: #475569;'>{T['radar_desc']}</p>", unsafe_allow_html=True)
    
    col_dist, col_btn = st.columns([2.5, 1.2])
    with col_dist:
        district_keys = list(INDIAN_AGRI_DISTRICTS.keys())
        default_d_idx = 0
        if st.session_state["weather_city_name"] in district_keys:
            default_d_idx = district_keys.index(st.session_state["weather_city_name"])
            
        selected_district = st.selectbox(
            "📍 Select Agricultural District & Crop Cluster:",
            district_keys,
            index=default_d_idx
        )
        st.session_state["weather_city_name"] = selected_district
        
    with col_btn:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        refresh_weather = st.button("🔄 Sync Live Satellite Telemetry", type="primary")

    # Fetch live weather data
    coord = INDIAN_AGRI_DISTRICTS[selected_district]
    weather_data = fetch_live_weather(coord["lat"], coord["lon"])
    
    # Update active risk factor in session state
    st.session_state["weather_risk_factor"] = weather_data["factor"]
    
    # Status Banner
    if weather_data["is_live"]:
        st.success(f"🟢 **Connected to Live Open-Meteo Meteorological Feed** for **{selected_district}** (Lat: {coord['lat']}, Lon: {coord['lon']})")
    else:
        st.warning(f"⚠️ Using Offline Meteorological Simulation for {selected_district}")

    # Microclimate Metrics Cards
    st.markdown("##### **Current Atmospheric Readings:**")
    w1, w2, w3, w4 = st.columns(4)
    w1.metric("🌡️ Temperature", f"{weather_data['temp']} °C", delta="Optimal Spore Zone" if 18 <= weather_data['temp'] <= 29 else "Sub-optimal")
    w2.metric("💧 Relative Humidity", f"{weather_data['rh']} %", delta="High Fungal Risk" if weather_data['rh'] >= 80 else "Normal")
    w3.metric("🌧️ Rain / Dew Probability", f"{weather_data['rain_prob']} %", delta="Foliar Wetness" if weather_data['rain_prob'] >= 50 else "Dry Foliage")
    w4.metric("💨 Wind Speed", f"{weather_data['wind']} km/h", delta="Spore Dispersal")

    st.markdown("---")
    
    # Outbreak Risk Display & Factor Multiplier
    col_risk_card, col_stock_adv = st.columns([1.1, 1.3], gap="large")
    
    risk_score = weather_data["risk_score"]
    factor_val = weather_data["factor"]
    
    if risk_score > 70:
        status_color = "#b91c1c"
        status_bg = "#fef2f2"
        status_text = T["risk_high_text"]
        advice = T["risk_high_adv"]
        badge_level = "CRITICAL OUTBREAK WARNING"
    elif risk_score > 40:
        status_color = "#b45309"
        status_bg = "#fffbeb"
        status_text = T["risk_mod_text"]
        advice = T["risk_mod_adv"]
        badge_level = "ELEVATED VIGILANCE REQUIRED"
    else:
        status_color = "#15803d"
        status_bg = "#f0fdf4"
        status_text = T["risk_low_text"]
        advice = T["risk_low_adv"]
        badge_level = "WEATHER CONDITIONS SAFE"

    with col_risk_card:
        st.markdown(f"""
        <div style='background: {status_bg}; border-radius: 14px; border: 2.5px solid {status_color}; padding: 24px; box-shadow: 0 6px 18px rgba(0,0,0,0.06);'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='font-size: 0.72rem; color: #475569; font-weight: 800; text-transform: uppercase;'>{T["radar_sim_label"]}</span>
                <span style='background: {status_color}; color: #ffffff; font-size: 0.68rem; font-weight: 800; padding: 2px 8px; border-radius: 10px;'>{badge_level}</span>
            </div>
            <div style='font-family: "Playfair Display", serif; font-size: 3.2rem; font-weight: 850; color: {status_color}; line-height: 1.1; margin-top: 8px;'>{risk_score}%</div>
            <div style='font-size: 1.1rem; font-weight: 800; color: {status_color}; margin-top: 4px; margin-bottom: 12px;'>{status_text}</div>
            <div style='background: #ffffff; border: 1.5px dashed {status_color}; border-radius: 8px; padding: 10px 14px; margin-top: 10px;'>
                <div style='font-size: 0.76rem; font-weight: 800; color: #475569;'>ACTIVE REVENUE SIMULATOR MULTIPLIER:</div>
                <div style='font-size: 1.35rem; font-weight: 850; color: {status_color};'>⚡ {factor_val:.2f}× Disease Surge Factor</div>
                <div style='font-size: 0.72rem; color: #64748b;'>This multiplier is actively coupled to the Revenue & Per-Acre Simulator.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_stock_adv:
        st.markdown(f"""
        <div style='background: #ffffff; border-radius: 14px; border: 1.5px solid #cbd5e1; padding: 24px; box-shadow: 0 4px 14px rgba(15,23,42,0.04); height: 100%;'>
            <div style='font-size: 0.80rem; font-weight: 800; color: #854d0e; text-transform: uppercase;'>🏪 KRISHI KENDRA PRE-STOCKING ADVISORY</div>
            <h3 style='margin: 8px 0 10px 0; color: #0f172a; font-family: "Playfair Display", serif;'>Immediate Procurement Plan</h3>
            <p style='color: #1e293b; font-size: 0.95rem; line-height: 1.55; margin-bottom: 14px;'>{advice}</p>
            <div style='border-top: 1px solid #e2e8f0; padding-top: 12px;'>
                <strong style='font-size: 0.82rem; color: #0f172a;'>Recommended Counter Stocking Checklist:</strong>
                <ul style='font-size: 0.82rem; color: #334155; margin-top: 6px; padding-left: 20px; line-height: 1.6;'>
                    <li><strong>Bio-Fungicide:</strong> Copper Hydroxide 53.8% DF (25+ units)</li>
                    <li><strong>Organic Protectant:</strong> Cold-Pressed Neem Oil 10,000 PPM (40+ bottles)</li>
                    <li><strong>Soil Inoculant:</strong> Trichoderma viride 1.5% WP (30+ kg)</li>
                    <li><strong>Foliar Fortifier:</strong> Chelated Zinc & Boron Micronutrient Mix</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Technical Edge Hardware Benchmarks in Expander
    with st.expander(f"⚡ {T['bench_title']}", expanded=False):
        st.markdown(f"<p style='color: #475569;'>{T['bench_desc']}</p>", unsafe_allow_html=True)
        devices = list(EDGE_BENCHMARKS.keys())
        latencies = [EDGE_BENCHMARKS[d]["latency_ms"] for d in devices]
        energies = [EDGE_BENCHMARKS[d]["energy_per_infer_joules"] for d in devices]
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown(f"##### **{T['bench_lat_title']}**")
            st.bar_chart(dict(zip(devices, latencies)))
        with col_t2:
            st.markdown(f"##### **{T['bench_eng_title']}**")
            st.bar_chart(dict(zip(devices, energies)))
            
        st.markdown(f"##### **{T['bench_matrix_title']}**")
        st.dataframe(
            [
                {
                    T["col_profile"]: dev,
                    T["col_runtime"]: data["runtime"],
                    T["col_latency"]: data["latency_ms"],
                    T["col_ram"]: data["ram_mb"],
                    T["col_offline"]: T["val_offline_yes"] if data["offline"] else T["val_offline_no"],
                    T["col_energy"]: data["energy_per_infer_joules"]
                }
                for dev, data in EDGE_BENCHMARKS.items()
            ],
            use_container_width=True
        )


# =========================================================
# MODE 2: REVENUE & PER-ACRE IMPACT SIMULATOR
# =========================================================
elif nav_mode_index == 2:
    st.markdown(f"### **{T['roi_page_title']}**")
    st.markdown(f"<p style='color: #475569;'>{T['roi_page_desc']}</p>", unsafe_allow_html=True)
    
    # Dynamic Weather Multiplier Control Bar
    weather_factor = st.session_state.get("weather_risk_factor", 1.25)
    weather_city = st.session_state.get("weather_city_name", "Regional Weather Station")
    
    col_w_bar1, col_w_bar2 = st.columns([3, 1.2])
    with col_w_bar1:
        st.session_state["apply_weather_factor"] = st.checkbox(
            f"⛅ Apply Live Meteorological Outbreak Multiplier ({weather_factor:.2f}× from {weather_city})",
            value=st.session_state.get("apply_weather_factor", True)
        )
    with col_w_bar2:
        eff_factor = weather_factor if st.session_state["apply_weather_factor"] else 1.00
        st.markdown(f"<div style='text-align: right; font-weight: 800; color: #0f172a; font-size: 0.95rem;'>Active Multiplier: <span style='color: #15803d; font-size: 1.15rem;'>{eff_factor:.2f}×</span></div>", unsafe_allow_html=True)

    if st.session_state["apply_weather_factor"] and eff_factor > 1.0:
        st.info(f"🌾 **Live Microclimate Modulation:** High disease pressure ({weather_city}) increases input spray requirements and potential yield losses by **+{int((eff_factor - 1.0)*100)}%**, accurately scaling shop turnover and crop wealth protected.")

    # 3 Consolidated Sub-Tabs Max
    tab_acre, tab_net, tab_plans = st.tabs([
        T["roi_tab_acre"],
        T["roi_tab_network"],
        "💎 3. Monetization Tiers & Regional SDG Impact"
    ])
    
    # ------------------ TAB 1: PER-ACRE FIELD ECONOMICS ------------------
    with tab_acre:
        st.markdown(f"#### **{T['acre_calc_header']}**")
        st.caption("Calculates localized field chemistry costs, yield protection, and scales to village/taluk command clusters.")
        
        crop_options = list(CROP_ACRE_BENCHMARKS.keys())
        c_sel1, c_sel2 = st.columns([1.2, 1.8])
        with c_sel1:
            sel_crop = st.selectbox(T["acre_crop_label"], crop_options, index=0)
        with c_sel2:
            st.info(f"🌾 **{sel_crop} Economics:** Benchmark Yield: **{CROP_ACRE_BENCHMARKS[sel_crop]['avg_yield_tonnes']} T/Acre** · Market Price: **₹{CROP_ACRE_BENCHMARKS[sel_crop]['market_price_per_kg']}/kg** · Gross Acre Value: **{format_inr(CROP_ACRE_BENCHMARKS[sel_crop]['gross_acre_value'])}/Acre**")

        c_data = CROP_ACRE_BENCHMARKS[sel_crop]
        
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            farmer_holding = st.slider(T["acre_holding_label"], min_value=1.0, max_value=40.0, value=4.0, step=0.5)
        with f_col2:
            base_sprays = c_data["typical_sprays"]
            mod_sprays = min(12, max(2, round(base_sprays * eff_factor)))
            sprays_per_acre = st.slider(T["acre_sprays_label"], min_value=2, max_value=12, value=mod_sprays, step=1)
        with f_col3:
            cost_per_spray = st.slider(T["acre_spray_cost_label"], min_value=300, max_value=2500, value=c_data["default_cost_per_spray"], step=50)

        base_loss_prev = c_data["default_loss_prevented_pct"]
        mod_loss_prev = min(50.0, base_loss_prev * (eff_factor ** 0.5))
        loss_prevent_pct = st.slider(T["acre_loss_prevent_label"], min_value=10.0, max_value=50.0, value=round(mod_loss_prev, 1), step=1.0)
        
        # Per-Acre Formulas
        per_acre_input_cost = sprays_per_acre * cost_per_spray
        wasted_chemicals_saved = round(cost_per_spray * max(1, round(sprays_per_acre * 0.33)))
        harvest_value_protected_acre = round(c_data["gross_acre_value"] * (loss_prevent_pct / 100.0))
        total_farmer_gain = round(farmer_holding * (harvest_value_protected_acre + wasted_chemicals_saved))
        
        st.markdown("---")
        st.markdown("##### **Individual Farmer Balance Sheet (Per Acre & Farm Total):**")
        
        m_a1, m_a2, m_a3, m_a4 = st.columns(4)
        m_a1.metric(T["acre_metric_cost_title"], f"₹ {per_acre_input_cost:,.0f} / Ac", help="Total input spray budget per acre over the crop season")
        m_a2.metric(T["acre_metric_wasted_saved"], f"₹ {wasted_chemicals_saved:,.0f} / Ac", delta="Saved from Misdiagnosis")
        m_a3.metric(T["acre_metric_harvest_saved"], f"₹ {harvest_value_protected_acre:,.0f} / Ac", delta=f"+{loss_prevent_pct:.0f}% Yield Saved")
        m_a4.metric(T["acre_metric_net_family"], f"₹ {total_farmer_gain:,.0f}", delta=f"{farmer_holding:.1f} Acres Combined")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Regional Command Scale Section (Crores Scale)
        st.markdown(f"#### **{T['acre_banner_title']}**")
        st.caption("Expand field-level calculations across the entire geographical territory / village clusters commanded by your Krishi Kendra.")
        
        command_acres = st.slider(T["acre_command_label"], min_value=500, max_value=30000, value=3500, step=500)
        dealer_margin_acre = st.slider("Retailer Average Margin on Bio-Chemical Inputs (%)", min_value=15, max_value=45, value=28, step=1)
        
        cluster_harvest_wealth_saved = command_acres * harvest_value_protected_acre
        cluster_kendra_sales = command_acres * per_acre_input_cost
        cluster_kendra_margin = cluster_kendra_sales * (dealer_margin_acre / 100.0)
        
        st.markdown(f"""
        <div style="background: #ffffff; border: 2px solid #15803d; border-radius: 14px; padding: 24px; box-shadow: 0 8px 24px rgba(21,128,61,0.08); margin-top: 10px;">
            <div style="font-size: 0.80rem; font-weight: 800; color: #15803d; letter-spacing: 0.8px; text-transform: uppercase;">COMMAND AREA COVERAGE: {command_acres:,} CULTIVATED ACRES</div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-top: 14px;">
                <div style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 10px; padding: 18px;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #475569;">{T['acre_banner_crop_saved']}</div>
                    <div style="font-size: 2.1rem; font-weight: 900; color: #15803d; font-family: 'Playfair Display', serif; margin-top: 4px;">{format_inr(cluster_harvest_wealth_saved)}</div>
                    <div style="font-size: 0.72rem; color: #64748b; margin-top: 4px;">Food produce saved from rotting across {command_acres:,} acres</div>
                </div>
                <div style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 10px; padding: 18px;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #475569;">{T['acre_banner_sales']}</div>
                    <div style="font-size: 2.1rem; font-weight: 900; color: #0f172a; font-family: 'Playfair Display', serif; margin-top: 4px;">{format_inr(cluster_kendra_sales)}</div>
                    <div style="font-size: 0.72rem; color: #64748b; margin-top: 4px;">Total fertilizer, bio-fungicide & pesticide retail billing</div>
                </div>
                <div style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 10px; padding: 18px;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #475569;">{T['acre_banner_margin']}</div>
                    <div style="font-size: 2.1rem; font-weight: 900; color: #b45309; font-family: 'Playfair Display', serif; margin-top: 4px;">{format_inr(cluster_kendra_margin)}</div>
                    <div style="font-size: 0.72rem; color: #64748b; margin-top: 4px;">Net retail gross profit at {dealer_margin_acre}% gross margin</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ------------------ TAB 2: DEALERSHIP NETWORK CRORE SCALE ------------------
    with tab_net:
        st.markdown(f"#### **{T['roi_tab_network']}**")
        st.caption("Simulate commercial financial returns across standalone kiosks, taluk dealer networks, and multi-district distribution chains.")
        
        scale_mode = st.radio(
            T["net_scale_label"],
            [T["net_scale_opt1"], T["net_scale_opt2"], T["net_scale_opt3"]],
            horizontal=True
        )
        
        if scale_mode == T["net_scale_opt1"]:
            def_farmers = 2200
            def_spend = 18500
            def_penetration = 65
            def_margin = 28
            scale_name = "Single Flagship Krishi Kendra"
        elif scale_mode == T["net_scale_opt2"]:
            def_farmers = 14000
            def_spend = 19500
            def_penetration = 70
            def_margin = 27
            scale_name = "Taluk / Block Retail Franchise (10 Counters)"
        else:
            def_farmers = 65000
            def_spend = 21000
            def_penetration = 75
            def_margin = 25
            scale_name = "District Distributor & FPO Enterprise (50 Counters)"
            
        n_col1, n_col2 = st.columns(2)
        with n_col1:
            farmers_count = st.slider(T["net_farmers_slider"], min_value=200, max_value=100000, value=def_farmers, step=200)
            annual_spend = st.slider(T["net_spend_slider"], min_value=3000, max_value=75000, value=def_spend, step=1000)
        with n_col2:
            ai_adoption = st.slider(T["net_adoption_slider"], min_value=20, max_value=100, value=def_penetration, step=5)
            dealer_margin_net = st.slider(T["net_margin_slider"], min_value=10, max_value=45, value=def_margin, step=1)
            
        active_diagnosed_farmers = farmers_count * (ai_adoption / 100.0)
        annual_network_turnover = active_diagnosed_farmers * annual_spend * eff_factor
        annual_gross_dealer_profit = annual_network_turnover * (dealer_margin_net / 100.0)
        regional_crop_wealth_protected = active_diagnosed_farmers * 78000 * eff_factor
        
        plan_id = st.session_state["current_tier"]
        annual_saas_cost = MONETIZATION_TIERS[plan_id]["price_inr"] * 12
        net_commercial_gain = annual_gross_dealer_profit - annual_saas_cost
        
        st.markdown(f"""
        <div style="background: #ffffff; border: 2px solid #0f172a; border-radius: 14px; padding: 24px; box-shadow: 0 8px 24px rgba(15,23,42,0.08); margin-top: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 16px;">
                <span style="font-size: 0.85rem; font-weight: 800; color: #0f172a; text-transform: uppercase;">COMMERCIAL PROJECTION · {scale_name}</span>
                <span style="background: #0f172a; color: #ffffff; padding: 4px 12px; border-radius: 20px; font-size: 0.76rem; font-weight: 700;">{farmers_count:,} FARMERS REGISTERED</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px;">
                <div style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 10px; padding: 18px;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #475569;">{T['net_metric_turnover']}</div>
                    <div style="font-size: 2.3rem; font-weight: 900; color: #0f172a; font-family: 'Playfair Display', serif; margin-top: 6px;">{format_inr(annual_network_turnover)}</div>
                    <div style="font-size: 0.74rem; color: #64748b; margin-top: 4px;">Annual input sales through AI-prescribed recommendations</div>
                </div>
                <div style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 10px; padding: 18px;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #475569;">{T['net_metric_profit']}</div>
                    <div style="font-size: 2.3rem; font-weight: 900; color: #15803d; font-family: 'Playfair Display', serif; margin-top: 6px;">{format_inr(annual_gross_dealer_profit)}</div>
                    <div style="font-size: 0.74rem; color: #64748b; margin-top: 4px;">Earned at {dealer_margin_net}% gross profit margin</div>
                </div>
                <div style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 10px; padding: 18px;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #475569;">{T['net_metric_crop_wealth']}</div>
                    <div style="font-size: 2.3rem; font-weight: 900; color: #b45309; font-family: 'Playfair Display', serif; margin-top: 6px;">{format_inr(regional_crop_wealth_protected)}</div>
                    <div style="font-size: 0.74rem; color: #64748b; margin-top: 4px;">Farm harvest value saved across {active_diagnosed_farmers:,.0f} treated farms</div>
                </div>
            </div>
            <div style="margin-top: 16px; padding-top: 14px; border-top: 1px dashed #cbd5e1; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <span style="font-size: 0.88rem; color: #334155;">Annual CropCare Pro Subscription: <strong>₹ {annual_saas_cost:,} / year</strong></span>
                <span style="font-size: 1.05rem; font-weight: 850; color: #15803d;">Net Dealer ROI: +{((net_commercial_gain / max(annual_saas_cost, 1)) * 100):,.0f}% Return</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ------------------ TAB 3: MONETIZATION TIERS & REGIONAL SDG IMPACT ------------------
    with tab_plans:
        st.markdown(f"#### **{T['tier_section_title']}**")
        st.caption(T['tier_section_sub'])
        
        tier_col1, tier_col2, tier_col3 = st.columns(3)
        
        # Tier 1: Starter
        with tier_col1:
            t1 = MONETIZATION_TIERS["starter"]
            is_cur1 = (st.session_state["current_tier"] == "starter")
            border1 = "3px solid #0f172a" if is_cur1 else "1.5px solid #cbd5e1"
            st.markdown(f"""
            <div style="background: #ffffff; border: {border1}; border-radius: 14px; padding: 22px; box-shadow: 0 4px 14px rgba(15,23,42,0.05); min-height: 440px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <span style="background: #f1f5f9; color: #334155; font-size: 0.72rem; font-weight: 800; padding: 4px 10px; border-radius: 12px; letter-spacing: 0.5px;">{t1['badge']}</span>
                    <h3 style="margin: 10px 0 2px 0; color: #0f172a; font-family: 'Playfair Display', serif;">{t1['name']}</h3>
                    <div style="font-size: 1.8rem; font-weight: 850; color: #0f172a; margin: 8px 0;">₹ 0 <span style="font-size: 0.85rem; color: #475569; font-weight: 500;">/ forever</span></div>
                    <p style="font-size: 0.82rem; color: #334155; line-height: 1.45;">{t1['description']}</p>
                    <div style="border-top: 1px solid #e2e8f0; margin: 12px 0; padding-top: 10px;">
                        <strong style="font-size: 0.80rem; color: #0f172a;">{T['included_features']}</strong>
                        <ul style="font-size: 0.78rem; color: #1e293b; padding-left: 18px; margin-top: 6px; line-height: 1.5;">
                            {''.join(['<li>' + f + '</li>' for f in t1['features']])}
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Select Starter Plan", key="btn_tier_starter_sub", disabled=is_cur1):
                st.session_state["current_tier"] = "starter"
                st.rerun()

        # Tier 2: Pro
        with tier_col2:
            t2 = MONETIZATION_TIERS["pro"]
            is_cur2 = (st.session_state["current_tier"] == "pro")
            border2 = "3px solid #15803d" if is_cur2 else "2px solid #15803d"
            st.markdown(f"""
            <div style="background: #ffffff; border: {border2}; border-radius: 14px; padding: 22px; box-shadow: 0 8px 24px rgba(21,128,61,0.12); min-height: 440px; display: flex; flex-direction: column; justify-content: space-between; position: relative;">
                <div style="position: absolute; top: -11px; right: 20px; background: #d97706; color: #ffffff; font-size: 0.68rem; font-weight: 850; padding: 2px 10px; border-radius: 12px; letter-spacing: 0.8px;">★ ARTISAN DEALER CHOICE ★</div>
                <div>
                    <span style="background: #15803d; color: #ffffff; font-size: 0.72rem; font-weight: 800; padding: 4px 10px; border-radius: 12px; letter-spacing: 0.5px;">{t2['badge']}</span>
                    <h3 style="margin: 10px 0 2px 0; color: #0f172a; font-family: 'Playfair Display', serif;">{t2['name']}</h3>
                    <div style="font-size: 1.8rem; font-weight: 850; color: #0f172a; margin: 8px 0;">₹ 499 <span style="font-size: 0.85rem; color: #475569; font-weight: 500;">/ month</span></div>
                    <p style="font-size: 0.82rem; color: #334155; line-height: 1.45;">{t2['description']}</p>
                    <div style="border-top: 1px solid #e2e8f0; margin: 12px 0; padding-top: 10px;">
                        <strong style="font-size: 0.80rem; color: #0f172a;">{T['included_features']}</strong>
                        <ul style="font-size: 0.78rem; color: #1e293b; padding-left: 18px; margin-top: 6px; line-height: 1.5;">
                            {''.join(['<li>✅ ' + f + '</li>' for f in t2['features']])}
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Select Pro Dealer Plan", key="btn_tier_pro_sub", type="primary" if not is_cur2 else "secondary", disabled=is_cur2):
                st.session_state["current_tier"] = "pro"
                st.rerun()

        # Tier 3: Enterprise
        with tier_col3:
            t3 = MONETIZATION_TIERS["enterprise"]
            is_cur3 = (st.session_state["current_tier"] == "enterprise")
            border3 = "3px solid #7c3aed" if is_cur3 else "1.5px solid #cbd5e1"
            st.markdown(f"""
            <div style="background: #ffffff; border: {border3}; border-radius: 14px; padding: 22px; box-shadow: 0 4px 14px rgba(15,23,42,0.05); min-height: 440px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <span style="background: #f5f3ff; color: #6d28d9; font-size: 0.72rem; font-weight: 800; padding: 4px 10px; border-radius: 12px; letter-spacing: 0.5px;">{t3['badge']}</span>
                    <h3 style="margin: 10px 0 2px 0; color: #0f172a; font-family: 'Playfair Display', serif;">{t3['name']}</h3>
                    <div style="font-size: 1.8rem; font-weight: 850; color: #0f172a; margin: 8px 0;">₹ 1,999 <span style="font-size: 0.85rem; color: #475569; font-weight: 500;">/ month</span></div>
                    <p style="font-size: 0.82rem; color: #334155; line-height: 1.45;">{t3['description']}</p>
                    <div style="border-top: 1px solid #e2e8f0; margin: 12px 0; padding-top: 10px;">
                        <strong style="font-size: 0.80rem; color: #0f172a;">{T['included_features']}</strong>
                        <ul style="font-size: 0.78rem; color: #1e293b; padding-left: 18px; margin-top: 6px; line-height: 1.5;">
                            {''.join(['<li>🚀 ' + f + '</li>' for f in t3['features']])}
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Select Enterprise Plan", key="btn_tier_ent_sub", disabled=is_cur3):
                st.session_state["current_tier"] = "enterprise"
                st.rerun()

        st.markdown("---")
        
        # UN SDG 2 and SDG 15 Impact Metrics
        st.markdown("#### **Regional Food Security & UN SDG Impact (Command Cluster):**")
        food_tonnes_saved = round((3500 * (15.0 * 0.28) * eff_factor), 1)
        toxic_runoff_averted_kg = round(3500 * 2.8 * eff_factor, 1)
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown(f"""
            <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-top: 5px solid #d97706; border-radius: 12px; padding: 22px; box-shadow: 0 4px 12px rgba(15,23,42,0.04);">
                <span style="background: #fef3c7; color: #92400e; font-size: 0.72rem; font-weight: 800; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px;">UN SDG 2: ZERO HUNGER</span>
                <h3 style="color: #0f172a; margin-top: 8px; font-family: 'Playfair Display', serif;">{T['sdg2_title']}</h3>
                <div style="font-size: 2.2rem; font-weight: 900; color: #d97706; font-family: 'Playfair Display', serif; margin: 8px 0;">{food_tonnes_saved:,} Tonnes</div>
                <div style="font-size: 0.82rem; color: #475569; font-weight: 600;">Food Harvest Saved from Blight & Rot in Cluster</div>
                <p style="color: #334155; line-height: 1.55; margin-top: 10px;">{T['sdg2_desc']}</p>
            </div>
            """, unsafe_allow_html=True)
        with col_s2:
            st.markdown(f"""
            <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-top: 5px solid #16a34a; border-radius: 12px; padding: 22px; box-shadow: 0 4px 12px rgba(15,23,42,0.04);">
                <span style="background: #dcfce7; color: #166534; font-size: 0.72rem; font-weight: 800; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px;">UN SDG 15: LIFE ON LAND</span>
                <h3 style="color: #0f172a; margin-top: 8px; font-family: 'Playfair Display', serif;">{T['sdg15_title']}</h3>
                <div style="font-size: 2.2rem; font-weight: 900; color: #15803d; font-family: 'Playfair Display', serif; margin: 8px 0;">{toxic_runoff_averted_kg:,} kg</div>
                <div style="font-size: 0.82rem; color: #475569; font-weight: 600;">Synthetic Chemical Residues Averted from Groundwater</div>
                <p style="color: #334155; line-height: 1.55; margin-top: 10px;">{T['sdg15_desc']}</p>
            </div>
            """, unsafe_allow_html=True)
