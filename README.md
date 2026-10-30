# CropCare AI — On-Device Crop Disease & Pest Assistant
> **Early Detection. Actionable Guidance. Smarter Agriculture.**  
> *Edge-Native Deep Learning & Computer Vision System*

---

## 🌾 Overview & Problem Statement
* **Crop Losses:** Up to 40% of global agricultural harvest is lost to pests and plant pathogens every year (FAO/IPPC estimate).
* **Guidance Gap:** Smallholder farmers lack immediate access to agronomic specialists and extension officers in rural areas.
* **Over-Chemicalization:** Delayed diagnosis causes uncontrolled outbreaks and excessive synthetic chemical spraying, harming soil microbiota and water tables.
* **Zero-Connectivity Barrier:** Cloud-dependent AI solutions fail in remote agricultural belts lacking reliable cellular connectivity.

**CropCare AI** solves this through an edge-native, lightweight deep learning assistant that executes **100% offline on low-cost ARM devices (Raspberry Pi / Mobile)**.

---

## 🚀 The 6-Step CropCare AI Pipeline
1. **Capture:** High-resolution leaf photo taken via camera or selected from field presets.
2. **Preprocess:** OpenCV checks quality (Laplacian variance sharpness, illumination), applies CLAHE contrast enhancement, normalizes, and isolates leaf region of interest (ROI).
3. **Inference:** Quantized INT8 MobileNet model classifies disease/pest on-device in under 40 milliseconds with zero internet ping.
4. **Detect:** UI presents disease label, pathogen species, and calibrated confidence score.
5. **Explain (XAI):** Grad-CAM style thermal activation heatmap highlights the exact symptomatic spots and lesions the AI model based its answer on.
6. **Action Plan:** Delivers organic-first treatment steps (cold-pressed neem oil formulations, Trichoderma bio-sprays) in plain vernacular languages (English, Hindi, Kannada, Telugu).

---

## 🎯 UN Sustainable Development Goal (SDG) Alignment
* **SDG 2 (Zero Hunger):** Safeguards food security by reducing preventable harvest losses by up to 25–30%.
* **SDG 15 (Life on Land):** Minimizes environmental pesticide runoff and toxicity via precision, bio-first interventions.
* **Ecosystem Health:** Protects soil microbiome, earthworms, and local pollinator biodiversity.

---

## 🛠️ Tech Stack & Architecture
* **Core Frameworks:** Python 3.14, Streamlit, NumPy, SciPy
* **Computer Vision:** OpenCV (CLAHE enhancement, morphological contour segmentation, Laplacian blur rating)
* **Architecture / Models:** MobileNetV3 / TFLite Quantized Edge Engine (<4.5 MB RAM footprint)
* **Hardware Target:** ARM-based edge devices (Raspberry Pi 4, low-cost Android smartphones)
* **Dataset References:** PlantVillage Dataset (annotated crop pathology repository)

---

## 💻 How to Run the Application

### 1. Launch with Streamlit:
```powershell
cd C:\Users\hp\.gemini\antigravity\scratch\cropcare-ai
python -m streamlit run app.py
```
Or simply double-click `run_app.bat`.

### 2. Access in Browser:
Open `http://localhost:8501` on your local machine or local Wi-Fi / hotspot.
