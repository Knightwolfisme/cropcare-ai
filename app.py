"""
CropCare AI - On-Device Crop Disease & Pest Assistant
Edge-Native Agricultural Intelligence Engine
Fully Internationalized across English, Hindi, Kannada, and Telugu.
"""

import os
import io
import time
import base64
import numpy as np
import cv2
from PIL import Image
import streamlit as st

from knowledge_base import DISEASE_DATABASE, EDGE_BENCHMARKS
from engine import (
    run_edge_inference,
    assess_image_quality,
    preprocess_leaf_image
)
from translations import UI_TRANSLATIONS

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="CropCare AI | On-Device Crop Disease Assistant",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for crisp, high-contrast readability across all themes
st.markdown("""
<style>
    /* Global App Container */
    .stApp {
        background-color: #f8fafc !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    /* Ensure all text in main container is crisp and high-contrast */
    [data-testid="stMain"] {
        color: #0f172a !important;
        background-color: #f8fafc !important;
    }
    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] h4,
    [data-testid="stMain"] h5,
    [data-testid="stMain"] h6 {
        color: #0f172a !important;
        font-weight: 750 !important;
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
    
    /* Radio buttons and inputs */
    [data-testid="stRadio"] label p,
    [data-testid="stWidgetLabel"] label p {
        color: #0f172a !important;
        font-weight: 650 !important;
        font-size: 0.95rem !important;
    }
    [data-testid="stRadio"] div[role="radiogroup"] label {
        color: #0f172a !important;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab"] {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }
    .stTabs [aria-selected="true"] {
        color: #1b4d3e !important;
        font-weight: 750 !important;
        border-bottom-color: #1b4d3e !important;
    }
    
    /* Alert / Warning Boxes */
    [data-testid="stAlert"] {
        background-color: #fef3c7 !important;
        border: 1px solid #f59e0b !important;
        border-radius: 8px !important;
    }
    [data-testid="stAlert"] p {
        color: #78350f !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #0f172a !important;
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #64748b !important;
    }
    
    /* Header Banner */
    .brand-header {
        background: linear-gradient(135deg, #1b4d3e 0%, #2d6a4f 100%);
        color: white;
        padding: 24px 28px;
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(27, 77, 62, 0.15);
        margin-bottom: 20px;
    }
    .brand-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        color: #ffffff !important;
    }
    .brand-subtitle {
        font-size: 1.05rem;
        color: #d8f3dc !important;
        margin-top: 4px;
        font-weight: 400;
    }
    .brand-meta {
        margin-top: 12px;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        font-size: 0.85rem;
    }
    .badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        font-weight: 650;
        font-size: 0.8rem;
    }
    .badge-offline {
        background-color: #52b788;
        color: #081c15 !important;
    }
    .badge-sdg2 {
        background-color: #d97706;
        color: white !important;
    }
    .badge-sdg15 {
        background-color: #16a34a;
        color: white !important;
    }
    .badge-team {
        background-color: rgba(255, 255, 255, 0.22);
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.35);
    }
    
    /* Cards & Components */
    .crop-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
        margin-bottom: 18px;
    }
    
    .action-step {
        background: #f0fdf4;
        border: 1px solid #86efac;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 0.95rem;
        color: #14532d !important;
        font-weight: 500;
    }
    .action-step strong {
        color: #14532d !important;
    }
    
    /* Pill Tag */
    .meta-pill {
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        color: #1e293b !important;
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


# Auto-load default sample on very first launch
if st.session_state["current_image"] is None:
    load_sample_image("Tomato_Early_Blight.jpg", "Tomato___Early_Blight")


# ---------------------------------------------------------
# Sidebar Navigation & Settings
# ---------------------------------------------------------
with st.sidebar:
    # 100% Offline SVG Logo
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
        <div style="background: linear-gradient(135deg, #1b4d3e, #2d6a4f); width: 46px; height: 46px; border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 3px 8px rgba(27,77,62,0.25);">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>
                <path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>
            </svg>
        </div>
        <div>
            <div style="font-size: 1.2rem; font-weight: 800; color: #0f172a; line-height: 1.1;">CropCare AI</div>
            <div style="font-size: 0.72rem; color: #475569; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Biotech & Vision Edge</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Vernacular Language Selector
    lang_display_names = {
        "en": "🇬🇧 English",
        "hi": "🇮🇳 हिन्दी (Hindi)",
        "kn": "🌾 ಕನ್ನಡ (Kannada)",
        "te": "🌱 తెలుగు (Telugu)"
    }
    
    selected_lang = st.selectbox(
        "🗣️ Farmer Language / भाषा / ಭಾಷೆ / భాష",
        options=list(lang_display_names.keys()),
        format_func=lambda x: lang_display_names[x],
        index=list(lang_display_names.keys()).index(st.session_state["language"])
    )
    st.session_state["language"] = selected_lang
    
    # Active language translation dictionary
    T = UI_TRANSLATIONS.get(selected_lang, UI_TRANSLATIONS["en"])
    
    st.markdown("---")
    
    # Navigation Modes (Dynamically translated)
    current_modes = T["nav_modes"]
    selected_mode_text = st.radio(
        T["nav_label"],
        current_modes,
        index=st.session_state["nav_index"]
    )
    # Track index so changing languages preserves current page
    nav_mode_index = current_modes.index(selected_mode_text)
    st.session_state["nav_index"] = nav_mode_index
    
    st.markdown("---")
    
    # Offline Edge Engine Status
    st.markdown(f"""
    <div style='background: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; padding: 12px;'>
        <div style='font-size: 0.85rem; font-weight: 750; color: #166534;'>
            {T["edge_engine_active"]}
        </div>
        <div style='font-size: 0.8rem; color: #15803d; margin-top: 4px; line-height: 1.4;'>
            {T["edge_engine_desc"]}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(T["sidebar_footer"], unsafe_allow_html=True)


# ---------------------------------------------------------
# Header Banner (Dynamically Translated)
# ---------------------------------------------------------
st.markdown(f"""
<div class="brand-header">
    <div>
        <div class="brand-title">{T["brand_title"]}</div>
        <div class="brand-subtitle">{T["brand_subtitle"]}</div>
    </div>
    <div class="brand-meta">
        <span class="badge badge-offline">{T["badge_offline"]}</span>
        <span class="badge badge-sdg2">{T["badge_sdg2"]}</span>
        <span class="badge badge-sdg15">{T["badge_sdg15"]}</span>
        <span class="badge badge-team">{T["badge_edition"]}</span>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# MODE 0: DISEASE DIAGNOSIS & ACTION PLAN
# =========================================================
if nav_mode_index == 0:
    col_input, col_result = st.columns([1.05, 1.35], gap="large")
    
    # ------------------ LEFT COLUMN: INPUT ------------------
    with col_input:
        st.markdown(f"### **{T['step1_title']}**")
        st.caption(T["step1_caption"])
        
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
                st.session_state["current_image_name"] = "Field_Camera_Capture.jpg"
                st.session_state["preset_hint"] = None
                with st.spinner("Processing on-device quantized model..."):
                    st.session_state["inference_result"] = run_edge_inference(img_rgb)
                    
        elif input_method == T["method_upload"]:
            uploaded_file = st.file_uploader(T["upload_label"], type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                pil_img = Image.open(uploaded_file)
                img_rgb = np.array(pil_img.convert("RGB"))
                st.session_state["current_image"] = img_rgb
                st.session_state["current_image_name"] = uploaded_file.name
                st.session_state["preset_hint"] = None
                if st.button(T["btn_diagnose_upload"], type="primary"):
                    with st.spinner("Running OpenCV preprocessing & MobileNet inference..."):
                        st.session_state["inference_result"] = run_edge_inference(img_rgb)

        # Display current input image & image quality card
        if st.session_state["current_image"] is not None:
            st.markdown("<br>", unsafe_allow_html=True)
            st.image(st.session_state["current_image"], caption=T["leaf_img_caption"])
            
            # Quality assessment badge
            if st.session_state["inference_result"]:
                q_info = st.session_state["inference_result"]["quality_info"]
                q_color = "#15803d" if q_info["is_acceptable"] else "#b45309"
                q_bg = "#f0fdf4" if q_info["is_acceptable"] else "#fffbeb"
                q_border = "#86efac" if q_info["is_acceptable"] else "#fde68a"
                
                # Localize status string
                if q_info["quality_status"] == "Good":
                    q_status_trans = T["quality_good"]
                elif "Blurry" in q_info["quality_status"]:
                    q_status_trans = T["quality_blurry"]
                elif "Dark" in q_info["quality_status"]:
                    q_status_trans = T["quality_dark"]
                else:
                    q_status_trans = T["quality_glare"]
                    
                st.markdown(f"""
                <div style='background: {q_bg}; border: 1px solid {q_border}; border-radius: 8px; padding: 10px 14px; margin-top: 8px;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='font-size: 0.85rem; font-weight: 700; color: #0f172a;'>{T["cv_quality_title"]}</span>
                        <span style='color: {q_color}; font-weight: 800; font-size: 0.85rem;'>{q_status_trans}</span>
                    </div>
                    <div style='font-size: 0.78rem; color: #475569; margin-top: 4px;'>
                        {T["cv_sharpness"]} <strong>{q_info["laplacian_var"]:.1f}</strong> | {T["cv_brightness"]} <strong>{q_info["mean_brightness"]:.1f}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(T["awaiting_leaf_hint"])

    # ------------------ RIGHT COLUMN: DIAGNOSTIC & ACTION PLAN ------------------
    with col_result:
        if st.session_state["inference_result"] is not None:
            res = st.session_state["inference_result"]
            top_info = res["disease_info"]
            lang = st.session_state["language"]
            trans = top_info["translations"].get(lang, top_info["translations"]["en"])
            
            # Localize severity label
            if "Healthy" in res["severity"]:
                sev_label = T["sev_healthy"]
            elif "Mild" in res["severity"]:
                sev_label = T["sev_mild"]
            elif "Moderate" in res["severity"]:
                sev_label = T["sev_moderate"]
            else:
                sev_label = T["sev_severe"]

            # Low Confidence Warning Alert
            if res["low_confidence_flag"]:
                st.warning(T["low_conf_warning"])
                
            # Diagnosis Banner
            st.markdown(f"### **{T['step2_title']}**")
            
            diag_html = f"""
            <div style="background: #ffffff; border-radius: 12px; border: 2.5px solid {res['severity_color']}; padding: 18px 22px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <div>
                        <span style="font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.5px; color: #475569; font-weight: 700;">{T["detected_condition"]}</span>
                        <h2 style="margin: 3px 0 0 0; color: #0f172a !important; font-size: 1.85rem; font-weight: 800;">{trans['label']}</h2>
                        <div style="color: #334155 !important; font-size: 0.92rem; margin-top: 3px; font-style: italic; font-weight: 500;">{top_info['pathogen']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 2.2rem; font-weight: 850; color: {res['severity_color']}; line-height: 1.1;">{res['top_confidence_pct']}%</div>
                        <div style="font-size: 0.72rem; color: #475569; font-weight: 700; letter-spacing: 0.5px;">{T["confidence_score"]}</div>
                    </div>
                </div>
                <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid #e2e8f0; display: flex; flex-wrap: wrap; gap: 10px;">
                    <span class="meta-pill">{T["crop_label"]} <strong>{top_info['crop']}</strong></span>
                    <span class="meta-pill">{T["severity_label"]} <strong style="color: {res['severity_color']};">{sev_label}</strong></span>
                    <span class="meta-pill">{T["lesion_area_label"]} <strong>{res['lesion_coverage_pct']}%</strong></span>
                    <span class="meta-pill">{T["inference_latency_label"]} <strong>{res['inference_time_ms']} ms</strong></span>
                </div>
            </div>
            """
            st.markdown(diag_html, unsafe_allow_html=True)
            
            # Vernacular Audio Readout (Text-to-Speech via Web API)
            speech_text = f"{trans['label']}. {trans['step1']} {trans['step2']} {trans['step3']}"
            st.markdown(f"""
            <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 16px;'>
                <button onclick="
                    const synth = window.speechSynthesis;
                    synth.cancel();
                    const utter = new SpeechSynthesisUtterance(`{speech_text}`);
                    utter.rate = 0.9;
                    synth.speak(utter);
                " style='background-color: #1b4d3e; color: #ffffff; border: none; padding: 9px 18px; border-radius: 6px; font-size: 0.92rem; font-weight: 700; cursor: pointer; box-shadow: 0 2px 6px rgba(27,77,62,0.25);'>
                    {T["audio_btn"]} ({lang_display_names[lang]})
                </button>
                <span style='font-size: 0.82rem; color: #475569; font-weight: 500;'>{T["audio_caption"]}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Action Plan Section
            st.markdown(f"### **{T['step3_title']}**")
            st.caption(T["step3_caption"])
            
            tab_immediate, tab_bio, tab_cultural, tab_chemical = st.tabs([
                T["tab_immediate"],
                T["tab_bio"],
                T["tab_cultural"],
                T["tab_chemical"]
            ])
            
            with tab_immediate:
                st.markdown(f"**{T['guidance_directive']}** *{trans['tagline']}*")
                for step_txt in [trans["step1"], trans["step2"], trans["step3"]]:
                    st.markdown(f"""
                    <div class="action-step">
                        <strong>{T['action_prefix']}</strong> {step_txt}
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown(f"##### **{T['detailed_steps_title']}**")
                for item in top_info["action_plan"]["immediate_actions"]:
                    st.markdown(f"• {item}")
                    
            with tab_bio:
                st.markdown(f"##### **{T['organic_rec_title']}**")
                for treat in top_info["action_plan"]["organic_bio_treatments"]:
                    st.markdown(f"""
                    <div style='background: #f0fdf4; border-left: 4px solid #16a34a; padding: 10px 14px; margin-bottom: 8px; border-radius: 4px; color: #14532d; font-weight: 500;'>
                        🌱 {treat}
                    </div>
                    """, unsafe_allow_html=True)
                st.info(T["neem_tip"])
                
            with tab_cultural:
                st.markdown(f"##### **{T['cultural_title']}**")
                for prac in top_info["action_plan"]["cultural_prevention"]:
                    st.markdown(f"• **{prac}**")
                    
            with tab_chemical:
                st.markdown(f"##### **{T['chemical_title']}**")
                st.warning(top_info["action_plan"]["chemical_advisory"])
                st.caption(T["chemical_sdg_caption"])

            # Ranked Probability Breakdown
            with st.expander(T["prediction_dist_title"]):
                for cand in res["ranked_predictions"]:
                    c_key = cand["class_key"]
                    c_name = top_info["translations"].get(lang, {}).get("label", cand["disease_name"]) if c_key == res["top_class"] else cand["disease_name"]
                    st.write(f"**{c_name}** ({cand['crop']})")
                    st.progress(cand["confidence"])
                    st.caption(f"Score: {cand['confidence_pct']}%")
        else:
            st.markdown(f"### **{T['step2_title']}**")
            st.info(T["awaiting_result_hint"])


# =========================================================
# MODE 1: EXPLAINABLE AI & HEATMAP INSPECTOR
# =========================================================
elif nav_mode_index == 1:
    st.markdown(f"### **{T['xai_title']}**")
    st.markdown(f"<p style='color: #334155;'>{T['xai_desc']}</p>", unsafe_allow_html=True)
    
    if st.session_state["inference_result"] is None:
        load_sample_image("Tomato_Early_Blight.jpg", "Tomato___Early_Blight")
        
    res = st.session_state["inference_result"]
    col_img1, col_img2, col_img3 = st.columns(3)
    
    with col_img1:
        st.markdown(f"##### **{T['xai_col1_title']}**")
        st.image(res["enhanced_img"], caption=T["xai_col1_caption"])
        st.caption(f"Coverage: {res['prep_info']['leaf_coverage_ratio']*100:.1f}%")
        
    with col_img2:
        st.markdown(f"##### **{T['xai_col2_title']}**")
        st.image(res["heatmap_img"], caption=T["xai_col2_caption"])
        st.caption(T["xai_col2_sub"])
        
    with col_img3:
        st.markdown(f"##### **{T['xai_col3_title']}**")
        st.image(res["annotated_img"], caption=T["xai_col3_caption"])
        st.caption(f"Count: {res['lesion_count']}")
        
    st.markdown("---")
    
    # Feature Metrics
    st.markdown(f"#### **{T['xai_metrics_title']}**")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(T["metric_necrotic"], f"{res['lesion_coverage_pct']}%")
    m2.metric(T["metric_chlorosis"], f"{res['chlorosis_coverage_pct']}%")
    m3.metric(T["metric_severity"], res["severity"].split()[0])
    m4.metric(T["metric_sharpness"], f"{res['quality_info']['laplacian_var']:.1f}")


# =========================================================
# MODE 2: MICROCLIMATE OUTBREAK RADAR
# =========================================================
elif nav_mode_index == 2:
    st.markdown(f"### **{T['radar_title']}**")
    st.markdown(f"<p style='color: #334155;'>{T['radar_desc']}</p>", unsafe_allow_html=True)
    
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
        <div style='background: #ffffff; border-radius: 12px; border: 2.5px solid {status_color}; padding: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);'>
            <div style='font-size: 0.85rem; color: #475569; font-weight: 700; text-transform: uppercase;'>{T["radar_sim_label"]}</div>
            <div style='font-size: 2.8rem; font-weight: 850; color: {status_color}; line-height: 1.1;'>{risk_score}%</div>
            <div style='font-size: 1.1rem; font-weight: 800; color: {status_color}; margin-top: 4px; margin-bottom: 10px;'>{status_text}</div>
            <p style='color: #1e293b; font-size: 0.95rem; line-height: 1.5; font-weight: 500;'>{advice}</p>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# MODE 3: EDGE HARDWARE BENCHMARKS
# =========================================================
elif nav_mode_index == 3:
    st.markdown(f"### **{T['bench_title']}**")
    st.markdown(f"<p style='color: #334155;'>{T['bench_desc']}</p>", unsafe_allow_html=True)
    
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
# MODE 4: IMPACT & SDG ASSESSMENT
# =========================================================
elif nav_mode_index == 4:
    st.markdown(f"### **{T['sdg_title']}**")
    st.markdown(f"<p style='color: #334155;'>{T['sdg_desc']}</p>", unsafe_allow_html=True)
    
    col_sdg2, col_sdg15 = st.columns(2)
    
    with col_sdg2:
        st.markdown(f"""
        <div class="crop-card" style="border-top: 5px solid #d97706;">
            <h3 style="color: #92400e; margin-top: 0;">{T["sdg2_title"]}</h3>
            <p style="color: #334155; line-height: 1.5;">
                {T["sdg2_prob"]}
            </p>
            <p style="color: #334155; line-height: 1.5;">
                {T["sdg2_imp"]}
            </p>
            <div style="background: #fef3c7; border-radius: 8px; padding: 12px; margin-top: 12px; color: #92400e;">
                <strong>{T["sdg2_rec"]}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_sdg15:
        st.markdown(f"""
        <div class="crop-card" style="border-top: 5px solid #16a34a;">
            <h3 style="color: #166534; margin-top: 0;">{T["sdg15_title"]}</h3>
            <p style="color: #334155; line-height: 1.5;">
                {T["sdg15_prob"]}
            </p>
            <p style="color: #334155; line-height: 1.5;">
                {T["sdg15_imp"]}
            </p>
            <div style="background: #dcfce7; border-radius: 8px; padding: 12px; margin-top: 12px; color: #166534;">
                <strong>{T["sdg15_rec"]}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Financial Savings Calculator
    st.markdown(f"#### **{T['calc_title']}**")
    acres = st.number_input(T["calc_acres"], min_value=0.5, max_value=50.0, value=2.5, step=0.5)
    
    chem_saved = acres * 1850
    yield_saved = acres * 8200
    total_benefit = chem_saved + yield_saved
    
    b1, b2, b3 = st.columns(3)
    b1.metric(T["calc_pesticide_cut"], f"₹ {chem_saved:,.0f}")
    b2.metric(T["calc_crop_saved"], f"₹ {yield_saved:,.0f}")
    b3.metric(T["calc_profit_boost"], f"₹ {total_benefit:,.0f}", delta="+ Gain")


# =========================================================
# MODE 5: AGRONOMIST CONSULTATION TICKET
# =========================================================
elif nav_mode_index == 5:
    st.markdown(f"### **{T['ticket_title']}**")
    st.markdown(f"<p style='color: #334155;'>{T['ticket_desc']}</p>", unsafe_allow_html=True)
    
    if st.session_state["inference_result"] is None:
        load_sample_image("Tomato_Early_Blight.jpg", "Tomato___Early_Blight")
        
    res = st.session_state["inference_result"]
    
    farmer_name = st.text_input(T["farmer_name_label"], value="Ramesh Kumar")
    farmer_village = st.text_input(T["farmer_village_label"], value="Anekal, Bengaluru Rural")
    farmer_notes = st.text_area(T["farmer_notes_label"], value="Spots appeared after two consecutive foggy mornings. Lower foliage started dropping.")
    
    ticket_text = f"""============================================================
CROPCARE AI - AGRONOMIST CONSULTATION PACKET
Agricultural Extension & Field Diagnostics Unit
============================================================
Ticket ID: CC-AGRI-{int(time.time())}
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

FARMER DETAILS:
- Name: {farmer_name}
- Village / District: {farmer_village}
- Field Notes: {farmer_notes}

ON-DEVICE AI DIAGNOSTIC FINDINGS:
- Target Crop: {res['disease_info']['crop']}
- Pathogen Indicated: {res['disease_info']['disease_name']} ({res['disease_info']['pathogen']})
- Model Confidence: {res['top_confidence_pct']}%
- Foliar Damage Severity: {res['severity']}
- Lesion Surface Coverage: {res['lesion_coverage_pct']}%
- Chlorosis Ratio: {res['chlorosis_coverage_pct']}%
- Sharpness Score: {res['quality_info']['laplacian_var']:.1f}
- Quality Status: {res['quality_info']['quality_status']}

RECOMMENDED FIRST-LINE BIO-TREATMENTS:
{chr(10).join(['* ' + t for t in res['disease_info']['action_plan']['organic_bio_treatments']])}

EXTENSION OFFICER DISPOSITION:
[ ] Approved AI Recommendation
[ ] Prescribe Secondary Lab Culture
[ ] Field Inspection Scheduled
============================================================
"""
    st.download_button(
        T["btn_download_ticket"],
        data=ticket_text,
        file_name=f"CropCare_Ticket_{int(time.time())}.txt",
        mime="text/plain",
        type="primary"
    )
    
    st.code(ticket_text, language="text")
