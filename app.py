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
import urllib.parse
import numpy as np
import cv2
from PIL import Image
import streamlit as st

from knowledge_base import DISEASE_DATABASE, EDGE_BENCHMARKS, MONETIZATION_TIERS
from engine import (
    run_edge_inference,
    assess_image_quality,
    preprocess_leaf_image
)
from translations import UI_TRANSLATIONS

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


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
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
    
    # Active language translation dictionary
    T = UI_TRANSLATIONS.get(st.session_state["language"], UI_TRANSLATIONS["en"])
    
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
        else:
            st.markdown(f"### **{T['step2_title']}**")
            st.info(T["awaiting_result_hint"])


# =========================================================
# MODE 1: RETAIL INVOICE & APOTHECARY PRESCRIPTION GENERATOR
# =========================================================
elif nav_mode_index == 1:
    st.markdown(f"### **{T['inv_title']}**")
    st.markdown(f"<p style='color: #475569;'>{T['inv_desc']}</p>", unsafe_allow_html=True)
    
    if st.session_state["current_tier"] == "starter":
        st.warning("🔒 **Branded Invoice Generation is locked on the Free Starter plan.** Upgrade to Krishi Kendra Pro to print branded receipts with your shop GST and send 1-click WhatsApp prescriptions.")
        if st.button("⭐ Unlock Branded Receipts (Switch to Pro Plan Demo)"):
            st.session_state["current_tier"] = "pro"
            st.rerun()
            
    col_shop, col_cust = st.columns(2)
    with col_shop:
        st.markdown("##### **Shop & Dealership Details:**")
        st.session_state["shop_name"] = st.text_input(T["shop_name_label"], value=st.session_state["shop_name"])
        st.session_state["shop_gst"] = st.text_input(T["shop_gst_label"], value=st.session_state["shop_gst"])
        st.session_state["shop_phone"] = st.text_input(T["shop_phone_label"], value=st.session_state["shop_phone"])
        
    with col_cust:
        st.markdown("##### **Farmer / Customer Details:**")
        st.session_state["farmer_name"] = st.text_input("Customer Name", value=st.session_state["farmer_name"])
        st.session_state["farmer_phone"] = st.text_input("Customer WhatsApp No.", value=st.session_state["farmer_phone"])
        st.session_state["farmer_village"] = st.text_input("Farmer Village", value=st.session_state["farmer_village"])

    st.markdown("---")
    
    # Cart items editor
    st.markdown("##### **Prescribed Products & Billing Items:**")
    
    if not st.session_state["cart_items"] and st.session_state["inference_result"]:
        top_skus = st.session_state["inference_result"]["disease_info"].get("retail_inventory", [])
        if top_skus:
            st.session_state["cart_items"] = [{
                "sku_id": top_skus[0]["sku_id"],
                "name": top_skus[0]["name"],
                "pack_size": top_skus[0]["pack_size"],
                "price": top_skus[0]["mrp"],
                "dosage": top_skus[0]["dosage"]
            }]
            if len(top_skus) > 1 and top_skus[1].get("is_primary"):
                st.session_state["cart_items"].append({
                    "sku_id": top_skus[1]["sku_id"],
                    "name": top_skus[1]["name"],
                    "pack_size": top_skus[1]["pack_size"],
                    "price": top_skus[1]["mrp"],
                    "dosage": top_skus[1]["dosage"]
                })

    for i, item in enumerate(st.session_state["cart_items"]):
        c1, c2, c3, c4 = st.columns([3, 1.5, 1.5, 0.8])
        with c1:
            st.write(f"**{i+1}. {item['name']}** ({item['pack_size']})")
            st.caption(f"Dosage: {item['dosage']}")
        with c2:
            st.write(f"₹ {item['price']}")
        with c3:
            st.write("Qty: 1")
        with c4:
            if st.button("🗑️", key=f"del_cart_{i}"):
                st.session_state["cart_items"].pop(i)
                st.rerun()

    total_invoice_amt = sum(item["price"] for item in st.session_state["cart_items"])
    
    # ------------------ ARTISANAL VISUAL PRESCRIPTION SLIP ------------------
    diag_name = st.session_state["inference_result"]["disease_info"]["disease_name"] if st.session_state["inference_result"] else "Crop Pathology Check"
    crop_name = st.session_state["inference_result"]["disease_info"]["crop"] if st.session_state["inference_result"] else "Vegetable"
    
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
    
    # Build text receipt for copy / download
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
    
    with st.expander("📄 View Plain Text Memo (Raw Format)"):
        st.code(receipt_text, language="text")
    
    col_act1, col_act2, col_act3 = st.columns(3)
    with col_act1:
        st.download_button(
            T["btn_download_bill"],
            data=receipt_text,
            file_name=f"Prescription_Bill_{st.session_state['farmer_phone']}.txt",
            mime="text/plain",
            type="primary"
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
        if st.button("🧹 Clear Cart for Next Farmer"):
            st.session_state["cart_items"] = []
            st.rerun()


# =========================================================
# MODE 2: MONETIZATION PLANS & SUBSCRIPTION TIERS
# =========================================================
elif nav_mode_index == 2:
    st.markdown(f"### **{T['tier_section_title']}**")
    st.markdown(f"<p style='color: #475569;'>{T['tier_section_sub']}</p>", unsafe_allow_html=True)
    
    tier_col1, tier_col2, tier_col3 = st.columns(3)
    
    # Tier 1: Starter
    with tier_col1:
        t1 = MONETIZATION_TIERS["starter"]
        is_cur1 = (st.session_state["current_tier"] == "starter")
        border1 = "3px solid #0f172a" if is_cur1 else "1.5px solid #cbd5e1"
        st.markdown(f"""
        <div style="background: #ffffff; border: {border1}; border-radius: 14px; padding: 24px; box-shadow: 0 4px 14px rgba(15,23,42,0.05); min-height: 480px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <span style="background: #f1f5f9; color: #334155; font-size: 0.72rem; font-weight: 800; padding: 4px 10px; border-radius: 12px; letter-spacing: 0.5px;">{t1['badge']}</span>
                <h3 style="margin: 10px 0 2px 0; color: #0f172a; font-family: 'Playfair Display', serif;">{t1['name']}</h3>
                <div style="font-size: 2.0rem; font-weight: 850; color: #0f172a; margin: 8px 0;">₹ 0 <span style="font-size: 0.85rem; color: #475569; font-weight: 500;">/ forever</span></div>
                <p style="font-size: 0.85rem; color: #334155; line-height: 1.5;">{t1['description']}</p>
                <div style="border-top: 1px solid #e2e8f0; margin: 14px 0; padding-top: 12px;">
                    <strong style="font-size: 0.82rem; color: #0f172a;">{T['included_features']}</strong>
                    <ul style="font-size: 0.80rem; color: #1e293b; padding-left: 18px; margin-top: 6px; line-height: 1.6;">
                        {''.join(['<li>' + f + '</li>' for f in t1['features']])}
                    </ul>
                    <strong style="font-size: 0.82rem; color: #64748b;">{T['locked_features']}</strong>
                    <ul style="font-size: 0.78rem; color: #64748b; padding-left: 18px; margin-top: 4px; line-height: 1.5;">
                        {''.join(['<li>🔒 ' + f + '</li>' for f in t1['locked_features']])}
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Starter Plan", key="btn_tier_starter", disabled=is_cur1):
            st.session_state["current_tier"] = "starter"
            st.rerun()

    # Tier 2: Pro (High Contrast Clean Finish)
    with tier_col2:
        t2 = MONETIZATION_TIERS["pro"]
        is_cur2 = (st.session_state["current_tier"] == "pro")
        border2 = "3px solid #15803d" if is_cur2 else "2px solid #15803d"
        st.markdown(f"""
        <div style="background: #ffffff; border: {border2}; border-radius: 14px; padding: 24px; box-shadow: 0 8px 24px rgba(21,128,61,0.12); min-height: 480px; display: flex; flex-direction: column; justify-content: space-between; position: relative;">
            <div style="position: absolute; top: -11px; right: 20px; background: #d97706; color: #ffffff; font-size: 0.70rem; font-weight: 850; padding: 2px 10px; border-radius: 12px; letter-spacing: 0.8px;">★ ARTISAN DEALER CHOICE ★</div>
            <div>
                <span style="background: #15803d; color: #ffffff; font-size: 0.72rem; font-weight: 800; padding: 4px 10px; border-radius: 12px; letter-spacing: 0.5px;">{t2['badge']}</span>
                <h3 style="margin: 10px 0 2px 0; color: #0f172a; font-family: 'Playfair Display', serif;">{t2['name']}</h3>
                <div style="font-size: 2.0rem; font-weight: 850; color: #0f172a; margin: 8px 0;">₹ 499 <span style="font-size: 0.85rem; color: #475569; font-weight: 500;">/ month</span></div>
                <p style="font-size: 0.85rem; color: #334155; line-height: 1.5;">{t2['description']}</p>
                <div style="border-top: 1px solid #e2e8f0; margin: 14px 0; padding-top: 12px;">
                    <strong style="font-size: 0.82rem; color: #0f172a;">{T['included_features']}</strong>
                    <ul style="font-size: 0.80rem; color: #1e293b; padding-left: 18px; margin-top: 6px; line-height: 1.6;">
                        {''.join(['<li>✅ ' + f + '</li>' for f in t2['features']])}
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Pro Dealer Plan", key="btn_tier_pro", type="primary" if not is_cur2 else "secondary", disabled=is_cur2):
            st.session_state["current_tier"] = "pro"
            st.rerun()

    # Tier 3: Enterprise
    with tier_col3:
        t3 = MONETIZATION_TIERS["enterprise"]
        is_cur3 = (st.session_state["current_tier"] == "enterprise")
        border3 = "3px solid #7c3aed" if is_cur3 else "1.5px solid #cbd5e1"
        st.markdown(f"""
        <div style="background: #ffffff; border: {border3}; border-radius: 14px; padding: 24px; box-shadow: 0 4px 14px rgba(15,23,42,0.05); min-height: 480px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <span style="background: #f5f3ff; color: #6d28d9; font-size: 0.72rem; font-weight: 800; padding: 4px 10px; border-radius: 12px; letter-spacing: 0.5px;">{t3['badge']}</span>
                <h3 style="margin: 10px 0 2px 0; color: #0f172a; font-family: 'Playfair Display', serif;">{t3['name']}</h3>
                <div style="font-size: 2.0rem; font-weight: 850; color: #0f172a; margin: 8px 0;">₹ 1,999 <span style="font-size: 0.85rem; color: #475569; font-weight: 500;">/ month</span></div>
                <p style="font-size: 0.85rem; color: #334155; line-height: 1.5;">{t3['description']}</p>
                <div style="border-top: 1px solid #e2e8f0; margin: 14px 0; padding-top: 12px;">
                    <strong style="font-size: 0.82rem; color: #0f172a;">{T['included_features']}</strong>
                    <ul style="font-size: 0.80rem; color: #1e293b; padding-left: 18px; margin-top: 6px; line-height: 1.6;">
                        {''.join(['<li>🚀 ' + f + '</li>' for f in t3['features']])}
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Enterprise Plan", key="btn_tier_ent", disabled=is_cur3):
            st.session_state["current_tier"] = "enterprise"
            st.rerun()

    st.markdown("---")
    st.markdown(f"#### **{T['roi_box_title']}**")
    st.info(f"💡 **Current Plan Impact ({tier_info['name']}):** {tier_info['roi_projection']}")


# =========================================================
# MODE 3: EXPLAINABLE AI & LESION HEATMAP
# =========================================================
elif nav_mode_index == 3:
    st.markdown(f"### **{T['xai_title']}**")
    st.markdown(f"<p style='color: #475569;'>{T['xai_desc']}</p>", unsafe_allow_html=True)
    
    if st.session_state["inference_result"] is None:
        load_sample_image("Tomato_Early_Blight.jpg", "Tomato___Early_Blight")
        
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
        st.markdown(f'<div class="specimen-tag" style="background: #fef2f2; color: #991b1b; border-color: #fecaca;">PLATE 02 • GRAD-CAM ACTIVATION MAP</div></div>', unsafe_allow_html=True)
        st.caption(T["xai_col2_sub"])
        
    with col_img3:
        st.markdown(f"##### **{T['xai_col3_title']}**")
        st.markdown('<div class="specimen-mount">', unsafe_allow_html=True)
        st.image(res["annotated_img"])
        st.markdown(f'<div class="specimen-tag">PLATE 03 • {res["lesion_count"]} LESION CLUSTERS</div></div>', unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.markdown(f"#### **{T['xai_metrics_title']}**")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(T["metric_necrotic"], f"{res['lesion_coverage_pct']}%")
    m2.metric(T["metric_chlorosis"], f"{res['chlorosis_coverage_pct']}%")
    m3.metric(T["metric_severity"], res["severity"].split()[0])
    m4.metric(T["metric_sharpness"], f"{res['quality_info']['laplacian_var']:.1f}")


# =========================================================
# MODE 4: OUTBREAK RADAR & PRE-STOCKING FORECAST
# =========================================================
elif nav_mode_index == 4:
    st.markdown(f"### **{T['radar_title']}**")
    st.markdown(f"<p style='color: #475569;'>{T['radar_desc']}</p>", unsafe_allow_html=True)
    
    col_sliders, col_risk = st.columns([1.1, 1.2], gap="large")
    
    with col_sliders:
        st.markdown(f"##### **{T['radar_inputs_title']}**")
        temp = st.slider(T["radar_temp"], min_value=10.0, max_value=42.0, value=26.0, step=0.5)
        rh = st.slider(T["radar_rh"], min_value=30, max_value=100, value=88, step=1)
        leaf_wetness_hours = st.slider(T["radar_wetness"], min_value=0.0, max_value=18.0, value=5.5, step=0.5)
        crop_target = st.selectbox(T["radar_crop"], ["Tomato", "Potato", "Corn", "Rice"])
        
    with col_risk:
        st.markdown(f"##### **{T['radar_pred_title']}**")
        
        risk_score = 0.0
        if 20.0 <= temp <= 29.0:
            risk_score += 35.0
        elif 15.0 <= temp <= 32.0:
            risk_score += 20.0
        else:
            risk_score += 5.0
            
        if rh >= 85:
            risk_score += 35.0
        elif rh >= 70:
            risk_score += 20.0
        else:
            risk_score += 5.0
            
        risk_score += min(leaf_wetness_hours * 5.5, 30.0)
        risk_score = min(round(risk_score, 1), 100.0)
        
        if risk_score > 70:
            status_color = "#b91c1c"
            status_text = T["risk_high_text"]
            advice = T["risk_high_adv"]
        elif risk_score > 40:
            status_color = "#b45309"
            status_text = T["risk_mod_text"]
            advice = T["risk_mod_adv"]
        else:
            status_color = "#15803d"
            status_text = T["risk_low_text"]
            advice = T["risk_low_adv"]

        st.markdown(f"""
        <div style='background: #fffdfa; border-radius: 14px; border: 2.5px solid {status_color}; padding: 24px; box-shadow: 0 6px 18px rgba(0,0,0,0.06);'>
            <div style='font-size: 0.82rem; color: #64748b; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;'>{T["radar_sim_label"]}</div>
            <div style='font-family: \"Playfair Display\", serif; font-size: 3.0rem; font-weight: 850; color: {status_color}; line-height: 1.1;'>{risk_score}%</div>
            <div style='font-size: 1.15rem; font-weight: 800; color: {status_color}; margin-top: 4px; margin-bottom: 12px;'>{status_text}</div>
            <p style='color: #2d3748; font-size: 0.95rem; line-height: 1.55; font-weight: 500;'>{advice}</p>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# MODE 5: EDGE HARDWARE BENCHMARKS
# =========================================================
elif nav_mode_index == 5:
    st.markdown(f"### **{T['bench_title']}**")
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
        
    st.markdown("---")
    
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
# MODE 6: DEALER ROI & BUSINESS IMPACT
# =========================================================
elif nav_mode_index == 6:
    st.markdown(f"### **{T['roi_page_title']}**")
    st.markdown(f"<p style='color: #475569;'>{T['roi_page_desc']}</p>", unsafe_allow_html=True)
    
    st.markdown(f"#### **{T['calc_title']}**")
    c1, c2, c3 = st.columns(3)
    with c1:
        monthly_farmers = st.slider(T["calc_farmers"], min_value=10, max_value=500, value=120, step=10)
    with c2:
        avg_basket = st.slider(T["calc_avg_basket"], min_value=100, max_value=2500, value=650, step=50)
    with c3:
        margin_pct = st.slider(T["calc_margin"], min_value=10, max_value=50, value=28, step=1)
        
    monthly_sales = monthly_farmers * avg_basket
    gross_profit = monthly_sales * (margin_pct / 100.0)
    plan_cost = MONETIZATION_TIERS[st.session_state["current_tier"]]["price_inr"]
    net_roi = gross_profit - plan_cost
    
    m1, m2, m3 = st.columns(3)
    m1.metric(T["metric_monthly_revenue"], f"₹ {monthly_sales:,.0f}")
    m2.metric(T["metric_monthly_profit"], f"₹ {gross_profit:,.0f}")
    m3.metric(T["metric_net_gain"], f"₹ {net_roi:,.0f}", delta=f"+{(net_roi / max(plan_cost, 1))*100:.0f}% ROI" if plan_cost > 0 else "Free Plan")
    
    st.markdown("---")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f"""
        <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-top: 5px solid #d97706; border-radius: 12px; padding: 22px; box-shadow: 0 4px 12px rgba(15,23,42,0.04);">
            <h3 style="color: #0f172a; margin-top: 0; font-family: 'Playfair Display', serif;">{T['sdg2_title']}</h3>
            <p style="color: #334155; line-height: 1.55;">{T['sdg2_desc']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"""
        <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-top: 5px solid #16a34a; border-radius: 12px; padding: 22px; box-shadow: 0 4px 12px rgba(15,23,42,0.04);">
            <h3 style="color: #0f172a; margin-top: 0; font-family: 'Playfair Display', serif;">{T['sdg15_title']}</h3>
            <p style="color: #334155; line-height: 1.55;">{T['sdg15_desc']}</p>
        </div>
        """, unsafe_allow_html=True)
