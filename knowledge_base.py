"""
CropCare AI Pro - Retailer Knowledge Base, Smart Inventory & Monetization Tiers
Designed for Agri-Input Retailers, Krishi Kendra Dealers, and Pesticide/Fertilizer Shopkeepers.
Bridges over-the-counter leaf diagnosis with instant retail product dispensing and monetization.
"""

from typing import Dict, Any, List

# ---------------------------------------------------------
# Retail Monetization Tiers for Agri-Shopkeepers
# ---------------------------------------------------------
MONETIZATION_TIERS: Dict[str, Dict[str, Any]] = {
    "starter": {
        "id": "starter",
        "name": "Kendra Starter (Free)",
        "badge": "FREE FOREVER",
        "price_inr": 0,
        "billing_period": "Free",
        "scan_limit_monthly": 30,
        "color": "#64748b",
        "description": "Essential diagnostic tool for small village fertilizer & seed kiosks.",
        "features": [
            "Up to 30 farmer leaf counter scans/month",
            "100% Offline Edge MobileNet diagnosis",
            "Basic disease identification & generic treatment recipes",
            "Standard digital screen view",
            "Basic camera capture & file upload"
        ],
        "locked_features": [
            "Shop-branded billing invoice & prescription generation",
            "Automatic stock SKU matching & inventory pricing",
            "Direct WhatsApp prescription sending to farmer",
            "Local vernacular voice audio readout for walk-in farmers",
            "Hyper-local outbreak risk radar for inventory pre-stocking",
            "Multi-branch counter sync & bulk customer SMS broadcasts"
        ],
        "roi_projection": "Helps build farmer footfall and establishes trust with free initial leaf health checks."
    },
    "pro": {
        "id": "pro",
        "name": "Krishi Kendra Pro",
        "badge": "MOST POPULAR FOR RETAILERS",
        "price_inr": 499,
        "billing_period": "₹499 / month (or ₹4,999 / year - Save 17%)",
        "scan_limit_monthly": 999999,  # Unlimited
        "color": "#16a34a",
        "description": "Complete retail sales booster & automated prescription POS for agri-input dealers.",
        "features": [
            "⚡ UNLIMITED counter leaf scans (100% offline)",
            "🏪 Custom Shop Branding: Prints receipts with your Shop Name, GSTIN & Phone",
            "📦 Smart Inventory Linker: Automatically matches diagnosed disease to your in-stock SKUs",
            "🧾 1-Click WhatsApp Prescription Slip & Invoice to customer's mobile",
            "🔊 Multilingual Voice Assistant: Speaks instructions in Hindi, Kannada, Telugu, English",
            "⛅ Outbreak Radar: 7-day predictive outbreak forecast to order stock before demand surges",
            "💰 Retail Margin Tracker: View profit margins on recommended bio-pesticides & treatments"
        ],
        "locked_features": [
            "Multi-branch dealership sync (enterprise)",
            "Bulk outbreak SMS broadcasts to 5,000+ farmer phonebook"
        ],
        "roi_projection": "Increases average farmer basket size by ₹350–₹700 per visit. Eliminates wrong pesticide returns. Pays for itself with just 2 farmer visits/month!"
    },
    "enterprise": {
        "id": "enterprise",
        "name": "Distributor & Multi-Branch Enterprise",
        "badge": "FOR AGRI-DEALERSHIPS & CHAINS",
        "price_inr": 1999,
        "billing_period": "₹1,999 / month (or ₹19,999 / year)",
        "scan_limit_monthly": 999999,
        "color": "#7c3aed",
        "description": "For large agri-distributors, FPOs, and multi-location pesticide retail networks.",
        "features": [
            "🏢 Multi-Branch License: Sync up to 10 retail counter terminals across districts",
            "📲 Outbreak Broadcast Engine: Send bulk SMS alerts to 5,000+ local farmers during blight risks",
            "📊 Wholesale ERP & Stock Connector: Custom CSV/API integration with your billing software",
            "👨‍🔬 Priority Agronomist Video Escalation: 15-minute SLA with certified university pathologists",
            "📈 Regional Demand Heatmap: See which diseases are peaking across nearby villages",
            "🏷️ Custom White-Labeling: Deploy under your own dealership brand name"
        ],
        "locked_features": [],
        "roi_projection": "Drives ₹45,000–₹1,20,000 in additional seasonal inventory turns through timely regional outbreak advisories."
    }
}


# ---------------------------------------------------------
# Retail Shop Database: Diseases, Pathology & In-Stock SKUs
# ---------------------------------------------------------
DISEASE_DATABASE: Dict[str, Dict[str, Any]] = {
    "Tomato___Early_Blight": {
        "crop": "Tomato",
        "disease_name": "Early Blight",
        "pathogen": "Alternaria solani (Fungus)",
        "symptoms": "Concentric brown-to-black ringed lesions ('target board' spots) surrounded by chlorotic yellow halos, predominantly starting on older bottom leaves.",
        "severity_thresholds": {
            "mild": "Less than 5% leaf area affected. Spotting confined to lower foliage.",
            "moderate": "5% - 25% leaf area affected. Lesions coalescing, early yellowing.",
            "severe": "Over 25% leaf area affected. Defoliation progressing upward to stems."
        },
        "retail_inventory": [
            {
                "sku_id": "SKU-NEEM-10K",
                "name": "EcoShield Neem Gold 10,000 PPM",
                "brand": "KrishiBio Organics",
                "category": "Bio-Pesticide",
                "pack_size": "250 ml",
                "mrp": 280,
                "dealer_price": 195,
                "margin_pct": 30.3,
                "dosage": "30-40 ml per 15L Knapsack Pump (2.5 ml/L)",
                "in_stock": 42,
                "is_primary": True,
                "usage_notes": "Spray early morning or evening. Acts as repellent and disrupts fungal spore wall."
            },
            {
                "sku_id": "SKU-TRICHO-WP",
                "name": "Tricho-Care Bio-Fungicide (Trichoderma viride 1% WP)",
                "brand": "GreenCrop Biotech",
                "category": "Bio-Control Agent",
                "pack_size": "500 gm",
                "mrp": 210,
                "dealer_price": 140,
                "margin_pct": 33.3,
                "dosage": "50 gm per 15L Knapsack Pump (3.5 gm/L)",
                "in_stock": 28,
                "is_primary": True,
                "usage_notes": "Beneficial fungus that parasitizes Alternaria hyphae. Mix with water and apply to foliage and roots."
            },
            {
                "sku_id": "SKU-MANCO-75",
                "name": "Mancozeb 75% WP Contact Protectant",
                "brand": "AgroChem India",
                "category": "Curative Chemical",
                "pack_size": "500 gm",
                "mrp": 320,
                "dealer_price": 255,
                "margin_pct": 20.3,
                "dosage": "30 gm per 15L Pump (2 gm/L)",
                "in_stock": 18,
                "is_primary": False,
                "usage_notes": "Dispense ONLY if foliar damage exceeds 25% or persistent rain prevents bio-control."
            }
        ],
        "action_plan": {
            "immediate_actions": [
                "Advise farmer to immediately prune infected bottom leaves and burn outside plot boundary.",
                "Sanitize pruning tools with 10% bleach or rubbing spirit between beds."
            ],
            "organic_bio_treatments": [
                "Dispense EcoShield Neem 10,000 PPM (2.5 ml/L) mixed with Tricho-Care WP (5g/L).",
                "Foliar potassium bicarbonate bio-wash to alter leaf surface pH against Alternaria spores."
            ],
            "cultural_prevention": [
                "Advise drip watering at root zone only; overhead sprinkling splashes spores onto upper leaves.",
                "Ensure minimum 60 cm plant spacing to improve canopy airflow."
            ],
            "chemical_advisory": "Recommend synthetic contact fungicide (Mancozeb 75%) strictly as fallback if canopy defoliation exceeds economic injury threshold (>25%)."
        },
        "environmental_risk": {
            "temp_optimum": "24°C - 29°C",
            "humidity_threshold": "> 80% RH",
            "critical_leaf_wetness": "2 to 4 consecutive hours"
        },
        "translations": {
            "en": {
                "label": "Tomato Early Blight",
                "tagline": "Alternaria fungal infection. Recommend Bio-Fungicide + Neem Gold bundle.",
                "step1": "Prune infected lower foliage immediately and discard away from field.",
                "step2": "Apply EcoShield Neem Gold (35ml/pump) + Tricho-Care Bio-Fungicide.",
                "step3": "Water at base only; instruct farmer to halt overhead irrigation."
            },
            "hi": {
                "label": "टमाटर अगेती झुलसा (Early Blight)",
                "tagline": "अल्टरनेरिया फफूंद संक्रमण। जैविक कवकनाशी + नीम तेल का कॉम्बो दें।",
                "step1": "किसान से कहें कि रोगी पत्तों को काटकर तुरंत खेत से दूर नष्ट करे।",
                "step2": "इकोशील्ड नीम गोल्ड (35ml/पंप) + ट्राइको-केयर जैविक कवकनाशी का घोल छिड़कें।",
                "step3": "पौधे की जड़ में ही पानी दें, ऊपर से पानी का छिड़काव तुरंत बंद कराएं।"
            },
            "kn": {
                "label": "ಟೊಮೆಟೊ ಮುಂಗಾರು ರೋಗ (Early Blight)",
                "tagline": "ಆಲ್ಟರ್ನೇರಿಯಾ ಶಿಲೀಂಧ್ರ ಸೋಂಕು. ಜೈವಿಕ ಶಿಲೀಂಧ್ರನಾಶಕ + ಬೇವಿನ ಎಣ್ಣೆ ಕಾಂಬೋ ಶಿಫಾರಸು ಮಾಡಿ.",
                "step1": "ಸೋಂಕಿತ ಕೆಳಗಿನ ಎಲೆಗಳನ್ನು ತಕ್ಷಣ ಕತ್ತರಿಸಿ ಹೊಲದಿಂದ ಹೊರಗೆ ನಾಶಮಾಡಲು ತಿಳಿಸಿ.",
                "step2": "ಬೇವಿನ ಎಣ್ಣೆ (35ml/ಪಂಪ್) + ಟ್ರೈಕೋ-ಕೇರ್ ಜೈವಿಕ ಶಿಲೀಂಧ್ರನಾಶಕ ಸಿಂಪಡಿಸಿ.",
                "step3": "ಗಿಡದ ಬುಡಕ್ಕೆ ಮಾತ್ರ ನೀರುಣಿಸಿ, ಎಲೆಗಳ ಮೇಲೆ ನೀರು ಸಿಂಪಡಿಸುವುದನ್ನು ನಿಲ್ಲಿಸಿ."
            },
            "te": {
                "label": "టమోటా ముందస్తు తెగులు (Early Blight)",
                "tagline": "ఆల్టర్నేరియా ఫంగస్ తెగులు. బయో-శిలీంధ్రనాశకం + వేప నూనె కాంబో సిఫారసు చేయండి.",
                "step1": "తెగులు సోకిన క్రింది ఆకులను వెంటనే తొలగించి దూరంగా కాల్చివేయమని చెప్పండి.",
                "step2": "వేప నూనె (35ml/పంప్) + ట్రైకో-కేర్ బయో-స్ప్రే పిచికారీ చేయించండి.",
                "step3": "మొక్కల మొదట్లోనే నీరు పోయాలి; ఆకులపై నీరు పడనివ్వకండి."
            }
        }
    },
    "Tomato___Late_Blight": {
        "crop": "Tomato",
        "disease_name": "Late Blight",
        "pathogen": "Phytophthora infestans (Oomycete)",
        "symptoms": "Irregular large water-soaked pale to purplish-brown lesions. Undersides often show delicate white fungal-like downy sporulation during damp mornings.",
        "severity_thresholds": {
            "mild": "Small water-soaked patches on tips of scattered leaves.",
            "moderate": "Fast spreading dark blotches across stems and foliage.",
            "severe": "Widespread blight, rapid tissue death, and foul-smelling collapse."
        },
        "retail_inventory": [
            {
                "sku_id": "SKU-COPPER-OX",
                "name": "Kocide Bio-Shield Copper Hydroxide 53.8% DF",
                "brand": "DuPont / Corteva",
                "category": "Bio-Approved Fungicide",
                "pack_size": "250 gm",
                "mrp": 380,
                "dealer_price": 275,
                "margin_pct": 27.6,
                "dosage": "35 gm per 15L Knapsack Pump (2.2 gm/L)",
                "in_stock": 22,
                "is_primary": True,
                "usage_notes": "High potency copper protective barrier preventing Phytophthora oospore entry."
            },
            {
                "sku_id": "SKU-BORDEAUX-PACK",
                "name": "ReadyBordeaux 1% Instant Micronized Powder",
                "brand": "KrishiBio Organics",
                "category": "Organic Protectant",
                "pack_size": "1 kg",
                "mrp": 260,
                "dealer_price": 180,
                "margin_pct": 30.8,
                "dosage": "100 gm per 15L Pump",
                "in_stock": 35,
                "is_primary": True,
                "usage_notes": "Classic organic copper sulfate + lime protectant. Highly residual wash-off resistance."
            },
            {
                "sku_id": "SKU-CYMOX-MAN",
                "name": "Curzate Cymoxanil 8% + Mancozeb 64% WP",
                "brand": "AgroChem India",
                "category": "Systemic Curative",
                "pack_size": "500 gm",
                "mrp": 590,
                "dealer_price": 460,
                "margin_pct": 22.0,
                "dosage": "35 gm per 15L Pump",
                "in_stock": 14,
                "is_primary": False,
                "usage_notes": "High urgency curative systemic. Recommend if field epidemic is spreading within 48h."
            }
        ],
        "action_plan": {
            "immediate_actions": [
                "URGENT: Advise farmer to decontaminate field edges and rogue out collapsed plants immediately.",
                "Instruct farmer not to walk through wet field foliage to prevent physical spore dispersal."
            ],
            "organic_bio_treatments": [
                "Dispense ReadyBordeaux 1% or Kocide Copper Hydroxide protectant.",
                "Apply Bacillus amyloliquefaciens microbial bio-spray onto healthy buffer plants."
            ],
            "cultural_prevention": [
                "Stake plants high to improve air velocity through bottom canopy.",
                "Eradicate nightshade weeds and volunteer potato hosts near tomato plots."
            ],
            "chemical_advisory": "If rain is continuous and disease is severe, dispense Cymoxanil + Mancozeb systemic formulation."
        },
        "environmental_risk": {
            "temp_optimum": "15°C - 22°C (Cool and humid)",
            "humidity_threshold": "> 90% RH",
            "critical_leaf_wetness": "6+ hours"
        },
        "translations": {
            "en": {
                "label": "Tomato Late Blight",
                "tagline": "High-urgency Oomycete blight. Recommend Copper Hydroxide / Bordeaux bundle.",
                "step1": "Rogue out and burn badly blighted plants outside field immediately.",
                "step2": "Dispense Kocide Copper Bio-Shield or ReadyBordeaux 1% immediately.",
                "step3": "Ensure farmer improves field drainage and prunes low hanging branches."
            },
            "hi": {
                "label": "टमाटर पछेती झुलसा (Late Blight)",
                "tagline": "गंभीर संक्रामक बीमारी। तुरंत कॉपर कवकनाशी या बोर्डो मिश्रण दें।",
                "step1": "रोगग्रस्त पौधों को तुरंत उखाड़कर खेत से बाहर ले जाकर जलाएं।",
                "step2": "कोसाइड कॉपर हाइड्रोक्साइड या रेडी-बोर्डो मिश्रण 1% का छिड़काव कराएं।",
                "step3": "खेत में हवा का संचार बढ़ाएं और पानी का जमाव तुरंत खत्म करें।"
            },
            "kn": {
                "label": "ಟೊಮೆಟೊ ತಡವಾದ ರೋಗ (Late Blight)",
                "tagline": "ತೀವ್ರ ಸಾಂಕ್ರಾಮಿಕ ರೋಗ. ತಾಮ್ರದ ಜೈವಿಕ ಕೀಟನಾಶಕ ಅಥವಾ ಬೋರ್ಡೋ ಮಿಶ್ರಣ ನೀಡಿ.",
                "step1": "ತೀವ್ರವಾಗಿ ಬಾಧಿತ ಗಿಡಗಳನ್ನು ತಕ್ಷಣ ಕಿತ್ತು ಹೊಲದಿಂದ ಹೊರಗೆ ಸುಟ್ಟುಹಾಕಿ.",
                "step2": "ತಾಮ್ರದ ಜೈವಿಕ ಕೀಟನಾಶಕ ಅಥವಾ ಬೋರ್ಡೋ ಮಿಶ್ರಣ 1% ಸಿಂಪಡಿಸಲು ತಿಳಿಸಿ.",
                "step3": "ಗಾಳಿಯಾಡುವಿಕೆಯನ್ನು ಹೆಚ್ಚಿಸಿ ಮತ್ತು ನಿಂತ ನೀರನ್ನು ತೆರವುಗೊಳಿಸಿ."
            },
            "te": {
                "label": "టమోటా లేట్ బ్లైట్ తెగులు",
                "tagline": "తీవ్రమైన ఫంగస్ తెగులు. కాపర్ బయో-స్ప్రే లేదా బోర్డో మిశ్రమం సిఫారసు చేయండి.",
                "step1": "బాధిత మొక్కలను తొలగించి వెంటనే దూరంగా కాల్చివేయమని చెప్పండి.",
                "step2": "కాపర్ బయో-షీల్డ్ లేదా బోర్డో మిశ్రమాన్ని వెంటనే పిచికారీ చేయించండి.",
                "step3": "మొక్కల మధ్య గాలి ప్రసరణ ఉండేలా చూసుకోండి."
            }
        }
    },
    "Tomato___Bacterial_Spot": {
        "crop": "Tomato",
        "disease_name": "Bacterial Spot",
        "pathogen": "Xanthomonas perforans / euvesicatoria (Bacterium)",
        "symptoms": "Numerous small (1-3mm), dark brown to black circular lesions with translucent oily margins and chlorotic haloes. Spots may tear leaves as they dry.",
        "severity_thresholds": {
            "mild": "Scattered circular pinprick spots without leaf loss.",
            "moderate": "Dense spotting, localized leaf yellowing and curling.",
            "severe": "Widespread scorch, defoliation exposing green fruit to sunscald."
        },
        "retail_inventory": [
            {
                "sku_id": "SKU-BACTO-STOP",
                "name": "BactoStop Streptomycin + Tetracycline 90:10 SP",
                "brand": "AgroChem India",
                "category": "Agricultural Bactericide",
                "pack_size": "50 gm",
                "mrp": 120,
                "dealer_price": 82,
                "margin_pct": 31.7,
                "dosage": "6 gm per 15L Knapsack Pump (with Copper)",
                "in_stock": 55,
                "is_primary": True,
                "usage_notes": "Mix with copper oxychloride for synergistic bacterial control."
            },
            {
                "sku_id": "SKU-COPPER-OXY",
                "name": "Blitox 50 Copper Oxychloride 50% WP",
                "brand": "Rallis India / Tata",
                "category": "Bactericide / Fungicide",
                "pack_size": "500 gm",
                "mrp": 310,
                "dealer_price": 235,
                "margin_pct": 24.2,
                "dosage": "45 gm per 15L Pump (3 gm/L)",
                "in_stock": 31,
                "is_primary": True,
                "usage_notes": "Essential companion to BactoStop. Provides surface bactericidal barrier."
            },
            {
                "sku_id": "SKU-BIO-SILICA",
                "name": "SilicaShield Bio-Barrier Foliar Spray",
                "brand": "GreenCrop Biotech",
                "category": "Plant Immunity Booster",
                "pack_size": "500 ml",
                "mrp": 340,
                "dealer_price": 225,
                "margin_pct": 33.8,
                "dosage": "30 ml per 15L Pump",
                "in_stock": 19,
                "is_primary": False,
                "usage_notes": "Strengthens epidermal leaf cell walls against bacterial perforation."
            }
        ],
        "action_plan": {
            "immediate_actions": [
                "Tell farmer NOT to enter field while foliage is wet from morning dew or rain.",
                "Sterilize harvesting crates and equipment."
            ],
            "organic_bio_treatments": [
                "Dispense Blitox Copper Oxychloride + BactoStop combination.",
                "SilicaShield foliar booster to fortify leaf epidermis."
            ],
            "cultural_prevention": [
                "Advise farmer to purchase certified pathogen-tested seed for next crop nursery.",
                "Avoid using unchlorinated pond water for foliar spraying."
            ],
            "chemical_advisory": "Copper + Streptocycline tank mix is the agronomic gold standard for bacterial speck/spot."
        },
        "environmental_risk": {
            "temp_optimum": "25°C - 30°C",
            "humidity_threshold": "> 85% RH",
            "critical_leaf_wetness": "Frequent rain splashes"
        },
        "translations": {
            "en": {
                "label": "Tomato Bacterial Spot",
                "tagline": "Xanthomonas bacterial pathogen. Recommend Copper + Bactericide combo.",
                "step1": "Instruct farmer not to touch or prune plants when wet.",
                "step2": "Dispense Blitox Copper Oxychloride (45g) + BactoStop (6g) per pump.",
                "step3": "Add SilicaShield foliar booster for cell wall thickness."
            },
            "hi": {
                "label": "टमाटर जीवाणु धब्बा (Bacterial Spot)",
                "tagline": "जीवाणु जनित रोग। कॉपर ऑक्सीक्लोराइड + जीवाणुनाशी का मिश्रण दें।",
                "step1": "किसान को सख्त हिदायत दें कि पत्तियां गीली होने पर खेत में काम न करे।",
                "step2": "ब्लाइटॉक्स कॉपर (45g) + बैक्टोस्टॉप (6g) प्रति पंप का घोल तैयार कराएं।",
                "step3": "पौधों की रोग प्रतिरोधक क्षमता बढ़ाने के लिए सिलिका टॉनिक दें।"
            },
            "kn": {
                "label": "ಟೊಮೆಟೊ ಬ್ಯಾಕ್ಟೀರಿಯಾ ಚುಕ್ಕೆ ರೋಗ",
                "tagline": "ಬ್ಯಾಕ್ಟೀರಿಯಾ ಸೋಂಕು. ತಾಮ್ರದ ಆಕ್ಸಿಕ್ಲೋರೈಡ್ + ಬ್ಯಾಕ್ಟೀರಿಯಾನಾಶಕ ಕಾಂಬೋ ನೀಡಿ.",
                "step1": "ಎಲೆಗಳು ತೇವವಿರುವಾಗ ಗಿಡಗಳನ್ನು ಮುಟ್ಟದಂತೆ ರೈತರಿಗೆ ಸೂಚಿಸಿ.",
                "step2": "ಬ್ಲೈಟಾಕ್ಸ್ ಕಾಪರ್ (45g) + ಬ್ಯಾಕ್ಟೋಸ್ಟಾಪ್ (6g) ಪ್ರತಿ ಪಂಪಿಗೆ ಬೆರೆಸಿ ಕೊಡಿ.",
                "step3": "ಗಿಡಗಳ ರಕ್ಷಣೆಗೆ ಸಿಲಿಕಾ ರಕ್ಷಾ ಕವಚ ಸ್ಪ್ರೇ ನೀಡಿ."
            },
            "te": {
                "label": "టమోటా బ్యాక్టీరియల్ స్పాట్",
                "tagline": "బాక్టీరియా తెగులు. కాపర్ ఆక్సిక్లోరైడ్ + బ్యాక్టీరిసైడ్ కాంబినేషన్ ఇవ్వండి.",
                "step1": "ఆకులు తడిగా ఉన్నప్పుడు మొక్కలను తాకవద్దని రైతుకు చెప్పండి.",
                "step2": "బ్లైటాక్స్ కాపర్ (45g) + బాక్టోస్టాప్ (6g) పంపునకు కలిపి పిచికారీ చేయించండి.",
                "step3": "మొక్కల రోగనిరోధక శక్తికి సిలికా బయో-స్ప్రే అందించండి."
            }
        }
    },
    "Tomato___Healthy": {
        "crop": "Tomato",
        "disease_name": "Healthy Foliage",
        "pathogen": "None (No Pathogen Detected)",
        "symptoms": "Uniform deep green leaves, well-formed venation, absence of necrotic lesions, chlorosis, or bacterial speckling.",
        "severity_thresholds": {
            "mild": "N/A",
            "moderate": "N/A",
            "severe": "N/A"
        },
        "retail_inventory": [
            {
                "sku_id": "SKU-SEAWEED-TONIC",
                "name": "Biozyme Seaweed Bio-Stimulant Tonic",
                "brand": "Biostadt India",
                "category": "Plant Growth Promoter",
                "pack_size": "250 ml",
                "mrp": 290,
                "dealer_price": 195,
                "margin_pct": 32.7,
                "dosage": "30 ml per 15L Knapsack Pump (2 ml/L)",
                "in_stock": 60,
                "is_primary": True,
                "usage_notes": "Stimulates chlorophyll density, root vigor, and abiotic stress resistance."
            },
            {
                "sku_id": "SKU-MICRONUT-CHEL",
                "name": "Multi-Micro Zinc-Boron-Iron Chelated Mix",
                "brand": "KrishiBio Organics",
                "category": "Micronutrient",
                "pack_size": "500 gm",
                "mrp": 240,
                "dealer_price": 160,
                "margin_pct": 33.3,
                "dosage": "25 gm per 15L Pump",
                "in_stock": 40,
                "is_primary": True,
                "usage_notes": "Prevents blossom end rot and enhances fruit setting."
            }
        ],
        "action_plan": {
            "immediate_actions": [
                "Reassure farmer: Zero pathogen damage detected! Do NOT sell unnecessary chemical sprays.",
                "Encourage preventative crop nutrition and organic bio-stimulants."
            ],
            "organic_bio_treatments": [
                "Recommend Biozyme Seaweed Tonic + Chelated Micronutrients for maximum yield quality.",
                "Maintain mycorrhiza soil colonization."
            ],
            "cultural_prevention": [
                "Keep mulch in place to conserve moisture.",
                "Maintain scheduled weekly crop scouting."
            ],
            "chemical_advisory": "ZERO chemical pesticide required. Avoid unnecessary chemical applications to save farmer money and protect beneficial insects."
        },
        "environmental_risk": {
            "temp_optimum": "18°C - 28°C",
            "humidity_threshold": "40% - 70% RH",
            "critical_leaf_wetness": "Dry canopy"
        },
        "translations": {
            "en": {
                "label": "Healthy Tomato Leaf",
                "tagline": "No disease detected. Upsell preventive bio-stimulants & micronutrients.",
                "step1": "Reassure farmer: leaf is healthy. Advise against chemical spraying.",
                "step2": "Dispense Biozyme Seaweed Tonic (30ml/pump) for lush green growth.",
                "step3": "Offer Chelated Micronutrients for fruit setting and higher market yield."
            },
            "hi": {
                "label": "स्वस्थ टमाटर की पत्ती",
                "tagline": "कोई बीमारी नहीं। किसान को अनावश्यक कीटनाशक न बेचें, जैविक टॉनिक दें।",
                "step1": "किसान को आश्वस्त करें कि फसल बिल्कुल स्वस्थ है।",
                "step2": "बायोजाइम समुद्री शैवाल टॉनिक (30ml/पंप) दें जिससे फसल और चमकदार बने।",
                "step3": "फूल और फल वृद्धि हेतु चिलेटेड माइक्रोन्यूट्रिएंट्स की सिफारिश करें।"
            },
            "kn": {
                "label": "ಆರೋಗ್ಯಕರ ಟೊಮೆಟೊ ಎಲೆ",
                "tagline": "ಯಾವುದೇ ರೋಗವಿಲ್ಲ. ರಾಸಾಯನಿಕ ಬೇಡ, ಜೈವಿಕ ಟಾನಿಕ್ ಮತ್ತು ಪೋಷಕಾಂಶ ನೀಡಿ.",
                "step1": "ರೈತರಿಗೆ ಧೈರ್ಯ ಹೇಳಿ: ಬೆಳೆ ಸಂಪೂರ್ಣ ಆರೋಗ್ಯಕರವಾಗಿದೆ.",
                "step2": "ಸಾವಯವ ಸಮುದ್ರ ಪಾಚಿ ಟಾನಿಕ್ (30ml/ಪಂಪ್) ಶಿಫಾರಸು ಮಾಡಿ.",
                "step3": "ಹೂವು-ಕಾಯಿ ಕಚ್ಚಲು ಸೂಕ್ಷ್ಮ ಪೋಷಕಾಂಶಗಳ ಮಿಶ್ರಣ ನೀಡಿ."
            },
            "te": {
                "label": "ఆరోగ్యకరమైన టమోటా ఆకు",
                "tagline": "తెగుళ్లు లేవు. రసాయనాలు ఇవ్వవద్దు, సేంద్రీయ టానిక్ అందించండి.",
                "step1": "ఆకు ఆరోగ్యంగా ఉందని రైతుకు భరోసా ఇవ్వండి.",
                "step2": "బయో-టోనిక్ (30ml/పంప్) ఇచ్చి మంచి ఎదుగుదలకు సూచించండి.",
                "step3": "పూత, కాత రాలకుండా మైక్రోన్యూట్రియెంట్స్ కాంబో అందించండి."
            }
        }
    },
    "Corn___Common_Rust": {
        "crop": "Corn (Maize)",
        "disease_name": "Common Rust",
        "pathogen": "Puccinia sorghi (Fungus)",
        "symptoms": "Cinnamon-brown to golden-orange powdery pustules (uredinia) bursting on both upper and lower leaf surfaces, causing leaf tissue roughness.",
        "severity_thresholds": {
            "mild": "Scattered pustules across lower whorls.",
            "moderate": "Pustules coalescing, leaf tips chlorotic.",
            "severe": "Extensive chlorosis, early grain fill impairment."
        },
        "retail_inventory": [
            {
                "sku_id": "SKU-SULFUR-80",
                "name": "Sulfex Bio-Sulfur 80% WDG (Fungicide + Acaricide)",
                "brand": "Excel Crop Care",
                "category": "Bio-Allowed Fungicide",
                "pack_size": "1 kg",
                "mrp": 230,
                "dealer_price": 165,
                "margin_pct": 28.3,
                "dosage": "40 gm per 15L Knapsack Pump (2.5 gm/L)",
                "in_stock": 48,
                "is_primary": True,
                "usage_notes": "Sustained vapor action destroys rust spore germination tubes. Also provides plant sulfur nutrition."
            },
            {
                "sku_id": "SKU-AZOXY-TEBU",
                "name": "Custodia Azoxystrobin 11% + Tebuconazole 18.3% SC",
                "brand": "ADAMA India",
                "category": "Broad Spectrum Systemic",
                "pack_size": "250 ml",
                "mrp": 780,
                "dealer_price": 610,
                "margin_pct": 21.8,
                "dosage": "20 ml per 15L Pump",
                "in_stock": 16,
                "is_primary": False,
                "usage_notes": "Premium curative systemic for high-value sweet corn / seed plots if rust crosses 20% canopy."
            }
        ],
        "action_plan": {
            "immediate_actions": [
                "Instruct farmer to check cob level leaves (leaves 8-12) to assess grain fill risk."
            ],
            "organic_bio_treatments": [
                "Dispense Sulfex 80% WDG micronized sulfur bio-spray.",
                "Combine with Cold-pressed Neem extract for pustule dessication."
            ],
            "cultural_prevention": [
                "Ensure balanced potash application; avoid excess urea."
            ],
            "chemical_advisory": "Azoxystrobin + Tebuconazole recommended only if rust appears prior to silking stage."
        },
        "environmental_risk": {
            "temp_optimum": "16°C - 25°C",
            "humidity_threshold": "> 95% RH or high dew",
            "critical_leaf_wetness": "Overnight dew periods"
        },
        "translations": {
            "en": {
                "label": "Corn Common Rust",
                "tagline": "Puccinia rust pustules detected. Dispense Sulfex 80% WDG bio-spray.",
                "step1": "Sell Sulfex Bio-Sulfur (40g/pump) to stop fungal spore spread.",
                "step2": "Advise farmer to inspect upper leaves near corn cob.",
                "step3": "Recommend balanced potash to strengthen stalk and blade tissue."
            },
            "hi": {
                "label": "मक्का सामान्य रतुआ (Common Rust)",
                "tagline": "पत्तियों पर रतुआ के फफोले। सल्फैक्स 80% घुलनशील सल्फर दें।",
                "step1": "सल्फैक्स सल्फर 80% डब्लूडीजी (40 ग्राम/पंप) की सिफारिश करें।",
                "step2": "भुट्टे के पास वाले ऊपरी पत्तों पर विशेष निगरानी रखने को कहें।",
                "step3": "पोटाश खाद का प्रयोग बढ़ाएं जिससे पत्तियां मजबूत रहें।"
            },
            "kn": {
                "label": "ಮೆಕ್ಕೆಜೋಳದ ಸಾಮಾನ್ಯ ತುಕ್ಕು ರೋಗ",
                "tagline": "ಮೆಕ್ಕೆಜೋಳದ ತುಕ್ಕು ರೋಗ. ಸಲ್ಫೆಕ್ಸ್ 80% ಜೈವಿಕ ಗಂಧಕ ನೀಡಿ.",
                "step1": "ಸಲ್ಫೆಕ್ಸ್ 80% ಗಂಧಕ (40 ಗ್ರಾಂ/ಪಂಪ್) ಸಿಂಪಡಿಸಲು ಕೊಡಿ.",
                "step2": "ತೆನೆಯ ಸಮೀಪವಿರುವ ಮೇಲಿನ ಎಲೆಗಳನ್ನು ಪರೀಕ್ಷಿಸಲು ತಿಳಿಸಿ.",
                "step3": "ಕಾಂಡ ಮತ್ತು ಎಲೆ ಗಟ್ಟಿಯಾಗಲು ಪೊಟ್ಯಾಷ್ ರಸಗೊಬ್ಬರ ನೀಡಿ."
            },
            "te": {
                "label": "మొక్కజొన్న సాధారణ తుప్పు తెగులు",
                "tagline": "ఆకులపై తుప్పు మచ్చలు. సల్ఫెక్స్ 80% సల్ఫర్ బయో-స్ప్రే ఇవ్వండి.",
                "step1": "సల్ఫెక్స్ 80% సల్ఫర్ (40 గ్రా/పంప్) పిచికారీ చేయడానికి ఇవ్వండి.",
                "step2": "కంకి వద్ద ఉన్న ఆకులను జాగ్రత్తగా గమనించమని చెప్పండి.",
                "step3": "ఆకు దృఢత్వానికి పొటాష్ ఎరువును అందించండి."
            }
        }
    },
    "Rice___Blast": {
        "crop": "Rice (Paddy)",
        "disease_name": "Rice Blast",
        "pathogen": "Magnaporthe oryzae (Fungus)",
        "symptoms": "Spindle-shaped or diamond-like eye lesions with greyish-white necrotic centres and reddish-brown borders on leaves and leaf collars.",
        "severity_thresholds": {
            "mild": "Isolated spindle spots on vegetative tillers.",
            "moderate": "Lesions merging, leaf tip blighting.",
            "severe": "Neck rot risk, severe panicle empty grain loss."
        },
        "retail_inventory": [
            {
                "sku_id": "SKU-PSEUDO-FL",
                "name": "Bio-Fluo (Pseudomonas fluorescens 1.5% WP)",
                "brand": "GreenCrop Biotech",
                "category": "Bio-Bactericide / Fungicide",
                "pack_size": "1 kg",
                "mrp": 240,
                "dealer_price": 160,
                "margin_pct": 33.3,
                "dosage": "50 gm per 15L Knapsack Pump",
                "in_stock": 38,
                "is_primary": True,
                "usage_notes": "Produces phenazine antibiotics that stop blast germination. Induces systemic acquired resistance (SAR)."
            },
            {
                "sku_id": "SKU-TRICYCLAZOLE",
                "name": "Baan Tricyclazole 75% WP",
                "brand": "Indofil Industries",
                "category": "Melanin Biosynthesis Inhibitor",
                "pack_size": "250 gm",
                "mrp": 460,
                "dealer_price": 365,
                "margin_pct": 20.7,
                "dosage": "18 gm per 15L Pump (1.2 gm/L)",
                "in_stock": 25,
                "is_primary": False,
                "usage_notes": "High specificity blast curative. Dispense if neck blast threatens at booting stage."
            },
            {
                "sku_id": "SKU-BIO-POTASH",
                "name": "K-Mobilizer Bio-Potash Solubilizing Bacteria",
                "brand": "KrishiBio Organics",
                "category": "Bio-Fertilizer",
                "pack_size": "500 ml",
                "mrp": 280,
                "dealer_price": 185,
                "margin_pct": 33.9,
                "dosage": "30 ml per 15L Pump",
                "in_stock": 20,
                "is_primary": True,
                "usage_notes": "Enhances silicon & potassium uptake to harden paddy leaf sheath."
            }
        ],
        "action_plan": {
            "immediate_actions": [
                "CRITICAL ADVICE: Instruct farmer to immediately STOP excess urea / nitrogenous fertilizer application (excess N promotes blast)."
            ],
            "organic_bio_treatments": [
                "Dispense Pseudomonas fluorescens bio-agent + Bio-Potash combo.",
                "Foliar bio-silicon formulation to harden cell wall against fungus appressoria."
            ],
            "cultural_prevention": [
                "Maintain uniform thin standing water layer in paddy basins."
            ],
            "chemical_advisory": "Dispense Tricyclazole 75% WP at panicle emergence if weather shows continuous night mist and blast covers >5% leaf area."
        },
        "environmental_risk": {
            "temp_optimum": "20°C - 26°C",
            "humidity_threshold": "> 90% RH",
            "critical_leaf_wetness": "Extended nocturnal leaf wetness"
        },
        "translations": {
            "en": {
                "label": "Paddy Rice Blast",
                "tagline": "Magnaporthe blast detected. Dispense Pseudomonas bio-agent + stop excess urea.",
                "step1": "URGENT: Advise farmer to immediately stop top-dressing urea/nitrogen.",
                "step2": "Dispense Pseudomonas fluorescens Bio-Agent (50g/pump) for blast containment.",
                "step3": "Provide Bio-Potash to harden leaf sheath and prevent neck blast."
            },
            "hi": {
                "label": "धान का झोंका रोग (Rice Blast)",
                "tagline": "राइस ब्लास्ट फफूंद। स्यूडोमोनास जैविक दवा दें और यूरिया तुरंत बंद कराएं।",
                "step1": "किसान से तुरंत कहें कि यूरिया खाद का छिड़काव बिल्कुल रोक दे।",
                "step2": "स्यूडोमोनास फ्लोरेसेंस जैविक पाउडर (50 ग्राम/पंप) की बिक्री करें।",
                "step3": "पत्ती की परत को मजबूत करने के लिए बायो-पोटाश घोल दें।"
            },
            "kn": {
                "label": "ಭತ್ತದ ಬೆಂಕಿ ರೋಗ (Rice Blast)",
                "tagline": "ಭತ್ತದ ಬೆಂಕಿ ರೋಗ ಪತ್ತೆ. ಸ್ಯುಡೋಮೊನಾಸ್ ನೀಡಿ ಮತ್ತು ಯೂರಿಯಾ ನಿಲ್ಲಿಸಲು ತಿಳಿಸಿ.",
                "step1": "ಹೆಚ್ಚುವರಿ ಯೂರಿಯಾ ಗೊಬ್ಬರ ಕೊಡುವುದನ್ನು ತಕ್ಷಣ ನಿಲ್ಲಿಸಲು ತಿಳಿಸಿ.",
                "step2": "ಸ್ಯುಡೋಮೊನಾಸ್ ಫ್ಲೋರೆಸೆನ್ಸ್ ಜೈವಿಕ ಪುಡಿ (50 ಗ್ರಾಂ/ಪಂಪ್) ಸಿಂಪಡಿಸಲು ಕೊಡಿ.",
                "step3": "ಎಲೆ ರಕ್ಷಣೆಗೆ ಜೈವಿಕ ಪೊಟ್ಯಾಷ್ ದ್ರಾವಣ ನೀಡಿ."
            },
            "te": {
                "label": "వరి అగ్గి తెగులు (Rice Blast)",
                "tagline": "వరి అగ్గి తెగులు. సూడోమోనాస్ బయో-మందు ఇవ్వండి, యూరియా ఆపండి.",
                "step1": "యూరియా ఎరువు వాడకాన్ని వెంటనే ఆపమని రైతుకు గట్టిగా చెప్పండి.",
                "step2": "సూడోమోనాస్ ఫ్లోరోసెన్స్ బయో-పౌడర్ (50 గ్రా/పంప్) ఇవ్వండి.",
                "step3": "ఆకు దృఢత్వానికి బయో-పొటాష్ లిక్విడ్ అందించండి."
            }
        }
    },
    "Potato___Early_Blight": {
        "crop": "Potato",
        "disease_name": "Early Blight",
        "pathogen": "Alternaria solani",
        "symptoms": "Dark brown, dry, leathery target-pattern spots with concentric rings. Lower foliage yellowing and tuber bulking impairment.",
        "severity_thresholds": {
            "mild": "Under 5% foliar lesions on bottom canopy.",
            "moderate": "10-25% foliar loss, lesions expanding to middle canopy.",
            "severe": "Severe early defoliation reducing tuber bulking."
        },
        "retail_inventory": [
            {
                "sku_id": "SKU-POTATO-NEEM",
                "name": "EcoShield Neem Gold 10,000 PPM",
                "brand": "KrishiBio Organics",
                "category": "Bio-Pesticide",
                "pack_size": "250 ml",
                "mrp": 280,
                "dealer_price": 195,
                "margin_pct": 30.3,
                "dosage": "35 ml per 15L Knapsack Pump",
                "in_stock": 35,
                "is_primary": True,
                "usage_notes": "Essential early morning spray. Protects lower leaves and prevents tuber spore transmission."
            },
            {
                "sku_id": "SKU-POTATO-TRICHO",
                "name": "Tricho-Care Bio-Fungicide (Trichoderma viride 1% WP)",
                "brand": "GreenCrop Biotech",
                "category": "Bio-Control Agent",
                "pack_size": "500 gm",
                "mrp": 210,
                "dealer_price": 140,
                "margin_pct": 33.3,
                "dosage": "50 gm per 15L Knapsack Pump",
                "in_stock": 25,
                "is_primary": True,
                "usage_notes": "Outcompetes Alternaria mycelium and fortifies root rhizosphere."
            }
        ],
        "action_plan": {
            "immediate_actions": ["Advise pruning infected lower potato leaves and ridging soil high over developing tubers."],
            "organic_bio_treatments": ["Dispense EcoShield Neem + Tricho-Care bio-fungicide combo."],
            "cultural_prevention": ["Avoid excessive overhead irrigation; keep furrow lines clean."],
            "chemical_advisory": "Mancozeb 75% WP or Chlorothalonil only if disease covers >20% foliage during tuberization."
        },
        "environmental_risk": {
            "temp_optimum": "24°C - 30°C",
            "humidity_threshold": "> 75% RH",
            "critical_leaf_wetness": "Alternating wet and dry periods"
        },
        "translations": {
            "en": {
                "label": "Potato Early Blight",
                "tagline": "Alternaria spots detected. Dispense Neem Gold + Trichoderma bundle.",
                "step1": "Prune infected lower foliage immediately.",
                "step2": "Dispense EcoShield Neem Gold (35ml/pump) + Tricho-Care WP.",
                "step3": "Ridge soil high to protect developing tubers from spore wash-off."
            },
            "hi": {
                "label": "आलू अगेती झुलसा (Early Blight)",
                "tagline": "आलू की पत्तियों पर छल्लेदार धब्बे। नीम तेल + ट्राइकोडर्मा का कॉम्बो दें।",
                "step1": "रोगी पत्तियों को तुरंत काटकर खेत से दूर नष्ट कराएं।",
                "step2": "नीम तेल (35ml/पंप) + ट्राइको-केयर जैविक कवकनाशी का छिड़काव कराएं।",
                "step3": "आलू के कंदों पर अच्छी मिट्टी चढ़ाएं ताकि सुरक्षा बनी रहे।"
            },
            "kn": {
                "label": "ಆಲೂಗಡ್ಡೆ ಮುಂಗಾರು ರೋಗ (Early Blight)",
                "tagline": "ಆಲೂಗಡ್ಡೆಯಲ್ಲಿ ಚುಕ್ಕೆ ರೋಗ. ಬೇವಿನ ಎಣ್ಣೆ + ಟ್ರೈಕೋಡರ್ಮಾ ನೀಡಿ.",
                "step1": "ಸೋಂಕಿತ ಕೆಳಗಿನ ಎಲೆಗಳನ್ನು ತಕ್ಷಣ ಕತ್ತರಿಸಿ.",
                "step2": "ಬೇವಿನ ಎಣ್ಣೆ ಮತ್ತು ಟ್ರೈಕೋಡರ್ಮಾ ದ್ರಾವಣ ಸಿಂಪಡಿಸಲು ಕೊಡಿ.",
                "step3": "ಗೆಡ್ಡೆಗಳಿಗೆ ಮಣ್ಣನ್ನು ಸರಿಯಾಗಿ ಮುಚ್ಚಲು ತಿಳಿಸಿ."
            },
            "te": {
                "label": "బంగాళాదుంప ఎర్లీ బ్లైట్",
                "tagline": "ఆకులపై వలయాకార మచ్చలు. వేప నూనె + ట్రైకోడెర్మా కాంబో ఇవ్వండి.",
                "step1": "తెగులు సోకిన ఆకులను కత్తిరించి కాల్చండి.",
                "step2": "వేప నూనె + ట్రైకో-కేర్ బయో-స్ప్రే పిచికారీ చేయించండి.",
                "step3": "దుంపలపై మట్టి సమృద్ధిగా ఉండేలా చూడండి."
            }
        }
    },
    "Potato___Late_Blight": {
        "crop": "Potato",
        "disease_name": "Late Blight",
        "pathogen": "Phytophthora infestans",
        "symptoms": "Water-soaked dark lesions spreading rapidly across foliage and stems; white downy mold under humid conditions. High tuber rot risk.",
        "severity_thresholds": {
            "mild": "Isolated dark water spots on terminal leaves.",
            "moderate": "Fast spreading stem rot and dark foliar blotches.",
            "severe": "Canopy collapse within 48-72 hours, tuber rot risk."
        },
        "retail_inventory": [
            {
                "sku_id": "SKU-POTATO-COPPER",
                "name": "Kocide Bio-Shield Copper Hydroxide 53.8% DF",
                "brand": "DuPont / Corteva",
                "category": "Bio-Approved Fungicide",
                "pack_size": "250 gm",
                "mrp": 380,
                "dealer_price": 275,
                "margin_pct": 27.6,
                "dosage": "35 gm per 15L Knapsack Pump",
                "in_stock": 20,
                "is_primary": True,
                "usage_notes": "Potent copper protectant preventing tuber rot and sporulation."
            },
            {
                "sku_id": "SKU-POTATO-CURZATE",
                "name": "Curzate Cymoxanil 8% + Mancozeb 64% WP",
                "brand": "AgroChem India",
                "category": "Systemic Curative",
                "pack_size": "500 gm",
                "mrp": 590,
                "dealer_price": 460,
                "margin_pct": 22.0,
                "dosage": "35 gm per 15L Pump",
                "in_stock": 15,
                "is_primary": False,
                "usage_notes": "High emergency systemic if field collapse is imminent."
            }
        ],
        "action_plan": {
            "immediate_actions": ["Dehaulm (cut haulms at ground level) 10-14 days before harvest if late blight threatens tubers."],
            "organic_bio_treatments": ["Dispense Kocide Copper Bio-Shield or Bordeaux mixture 1%."],
            "cultural_prevention": ["Hill up ridges to create deep protective soil cover over potato tubers."],
            "chemical_advisory": "Cymoxanil + Mancozeb systemic formulation if cold wet weather epidemic is active."
        },
        "environmental_risk": {
            "temp_optimum": "12°C - 20°C",
            "humidity_threshold": "> 90% RH",
            "critical_leaf_wetness": "Persistent mist or fog"
        },
        "translations": {
            "en": {
                "label": "Potato Late Blight",
                "tagline": "Phytophthora blight detected. Dispense Kocide Copper Protectant immediately.",
                "step1": "Dehaulm or cut blighted foliage to save developing tubers.",
                "step2": "Dispense Kocide Copper Bio-Shield (35g/pump) without delay.",
                "step3": "Ensure soil mounds cover tubers completely."
            },
            "hi": {
                "label": "आलू पछेती झुलसा (Late Blight)",
                "tagline": "गंभीर झुलसा रोग। कंदों को सड़ने से बचाने के लिए तुरंत कोसाइड कॉपर दें।",
                "step1": "संक्रमित पत्तों को तुरंत काटें और खेत से बाहर करें।",
                "step2": "कोसाइड कॉपर कवकनाशी (35 ग्राम/पंप) का तुरंत छिड़काव कराएं।",
                "step3": "कंदों को मिट्टी से अच्छी तरह ढक कर रखें।"
            },
            "kn": {
                "label": "ಆಲೂಗಡ್ಡೆ ತಡವಾದ ರೋಗ (Late Blight)",
                "tagline": "ತೀವ್ರ ರೋಗ. ಗೆಡ್ಡೆಗಳನ್ನು ಉಳಿಸಲು ತಾಮ್ರದ ಕೀಟನಾಶಕ ಕೊಡಿ.",
                "step1": "ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತಕ್ಷಣ ತೆಗೆದುಹಾಕಿ.",
                "step2": "ತಾಮ್ರದ ಜೈವಿಕ ಕೀಟನಾಶಕ ಸಿಂಪಡಿಸಲು ತಿಳಿಸಿ.",
                "step3": "ಗೆಡ್ಡೆಗಳು ಹೊರಬರದಂತೆ ಮಣ್ಣು ಮುಚ್ಚಿ."
            },
            "te": {
                "label": "బంగాళాదుంప లేట్ బ్లైట్",
                "tagline": "తీవ్రమైన తెగులు. దుంపలను కాపాడేందుకు కాపర్ బయో-షీల్డ్ ఇవ్వండి.",
                "step1": "తెగులు సోకిన కొమ్మలను వెంటనే తొలగించండి.",
                "step2": "కాపర్ బయో-స్ప్రే (35 గ్రా/పంప్) పిచికారీ చేయించండి.",
                "step3": "దుంపలపై మట్టి బాగా కప్పండి."
            }
        }
    }
}

# Edge benchmark parameters
EDGE_BENCHMARKS = {
    "Raspberry Pi 4 (Quad Cortex-A72 @ 1.5GHz)": {
        "runtime": "TFLite INT8 Quantized",
        "latency_ms": 38.4,
        "ram_mb": 4.1,
        "offline": True,
        "energy_per_infer_joules": 0.08
    },
    "Low-Cost ARM Mobile (Cortex-A53 / Snapdragon 400 series)": {
        "runtime": "ONNX Runtime / TFLite Edge",
        "latency_ms": 22.6,
        "ram_mb": 4.5,
        "offline": True,
        "energy_per_infer_joules": 0.04
    },
    "Mid-Range Smartphone (ARM Cortex-A78)": {
        "runtime": "NPU / TFLite GPU delegate",
        "latency_ms": 8.1,
        "ram_mb": 3.8,
        "offline": True,
        "energy_per_infer_joules": 0.02
    },
    "Typical Cloud API (Requires 4G/5G data connection)": {
        "runtime": "Cloud Server Inference + Roundtrip Latency",
        "latency_ms": 1420.0,
        "ram_mb": 420.0,
        "offline": False,
        "energy_per_infer_joules": 3.50
    }
}
