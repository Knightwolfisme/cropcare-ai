"""
CropCare AI - Agronomic Knowledge Base & Multilingual Guidelines
Aligned with PlantVillage dataset standards and UN Sustainable Development Goals (SDG 2 Zero Hunger & SDG 15 Life on Land).
"""

from typing import Dict, Any, List

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
        "action_plan": {
            "immediate_actions": [
                "Carefully prune and remove infected lower leaves with sanitized shears to halt vertical spore spread.",
                "Bag and destroy pruned leaves outside the crop perimeter — do not compost infected foliage.",
                "Sterilize pruning equipment in a 10% sodium hypochlorite or rubbing alcohol solution."
            ],
            "organic_bio_treatments": [
                "Apply cold-pressed Neem Oil bio-spray (5 ml neem oil + 2 ml organic surfactant/dish soap per 1 liter lukewarm water). Spray thoroughly at dawn or dusk.",
                "Foliar spray with Trichoderma viride or Bacillus subtilis bio-fungicide (5g/L water) to colonize leaf surfaces and outcompete fungal hyphae.",
                "Apply Potassium Bicarbonate or Baking Soda bio-spray (3g/L water + horticultural oil) to alter leaf surface pH against spores."
            ],
            "cultural_prevention": [
                "Switch to drip or furrow irrigation; avoid overhead sprinkler watering to keep foliage strictly dry.",
                "Maintain minimum 60 cm inter-plant spacing to enhance air circulation and reduce micro-humidity.",
                "Apply 2 inches of clean straw mulch around plant bases to prevent soil-splashing during rains.",
                "Implement a 3-year crop rotation with non-solanaceous crops (avoid peppers, potatoes, eggplants)."
            ],
            "chemical_advisory": "Synthetic fungicide (e.g. Mancozeb 75% WP or Chlorothalonil) is ONLY advised as a last resort if disease incidence exceeds 30% during warm rainy spells. Prioritize bio-controls to protect soil microbiome and beneficial insects."
        },
        "environmental_risk": {
            "temp_optimum": "24°C - 29°C",
            "humidity_threshold": "> 80% RH",
            "critical_leaf_wetness": "2 to 4 consecutive hours"
        },
        "translations": {
            "en": {
                "label": "Tomato Early Blight",
                "tagline": "Fungal infection detected. Immediate organic containment recommended.",
                "step1": "Remove infected lower leaves immediately.",
                "step2": "Apply neem bio-spray (5ml/L) in early morning or evening.",
                "step3": "Water at the soil base only; keep foliage dry."
            },
            "hi": {
                "label": "टमाटर अगेती झुलसा (अर्ली ब्लाइट)",
                "tagline": "फफूंद संक्रमण का पता चला। जैविक रोकथाम तुरंत शुरू करें।",
                "step1": "संक्रमित निचले पत्तों को तुरंत काटकर खेत से दूर नष्ट करें।",
                "step2": "नीम का काढ़ा या नीम तेल (5 मिली/लीटर) सुबह या शाम छिड़कें।",
                "step3": "पौधों की जड़ों में ही पानी दें; पत्तियों को गीला न होने दें।"
            },
            "kn": {
                "label": "ಟೊಮೆಟೊ ಮುಂಗಾರು ರೋಗ (ಅರ್ಲಿ ಬ್ಲೈಟ್)",
                "tagline": "ಶಿಲೀಂಧ್ರ ಸೋಂಕು ಪತ್ತೆಯಾಗಿದೆ. ಸಾವಯವ ನಿಯಂತ್ರಣ ತಕ್ಷಣ ಪ್ರಾರಂಭಿಸಿ.",
                "step1": "ಸೋಂಕಿತ ಕೆಳಗಿನ ಎಲೆಗಳನ್ನು ತಕ್ಷಣ ಕತ್ತರಿಸಿ ನಾಶಮಾಡಿ.",
                "step2": "ಬೇವಿನ ಎಣ್ಣೆ ಕಷಾಯವನ್ನು (5 ಮಿಲಿ/ಲೀಟರ್) ಬೆಳಿಗ್ಗೆ ಅಥವಾ ಸಂಜೆ ಸಿಂಪಡಿಸಿ.",
                "step3": "ಗಿಡದ ಬುಡಕ್ಕೆ ಮಾತ್ರ ನೀರು ಹಾಕಿ, ಎಲೆಗಳನ್ನು ಒಣಗಿಸಿಡಿ."
            },
            "te": {
                "label": "టమోటా ముందస్తు తెగులు (ఎర్లీ బ్లైట్)",
                "tagline": "శిలీంధ్ర సంక్రమణ గుర్తించబడింది. వెంటనే సేంద్రీయ నివారణ చర్యలు చేపట్టండి.",
                "step1": "సోకిన క్రింది ఆకులను వెంటనే తొలగించి నాశనం చేయండి.",
                "step2": "వేప నూనె మిశ్రమాన్ని (5 మి.లీ/లీటరు) ఉదయం లేదా సాయంత్రం పిచికారీ చేయండి.",
                "step3": "మొక్కల మొదట్లోనే నీరు పోయండి; ఆకులపై నీరు పడనివ్వకండి."
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
        "action_plan": {
            "immediate_actions": [
                "HIGH URGENCY: Immediately isolate affected plants. Phytophthora reproduces within 48 hours under cool wet conditions.",
                "Remove entire badly stricken plants and seal in disposal bags; do not walk through wet field to avoid spreading spores."
            ],
            "organic_bio_treatments": [
                "Spray copper-based bio-approved Bordeaux mixture (1%) or Copper Octanoate on remaining healthy foliage.",
                "Apply Bacillus amyloliquefaciens microbial spray to suppress sporulation.",
                "Compost tea extract foliar wash to reinforce benign microbial barrier."
            ],
            "cultural_prevention": [
                "Maximize ventilation in polyhouse/field; stake and prune foliage to promote quick morning drying.",
                "Eliminate volunteer potato and nightshade weed hosts near field margins."
            ],
            "chemical_advisory": "If outbreak is epidemic and weather forecast shows continuous rain, targeted systemic fungicides (e.g. Metalaxyl + Mancozeb) may be used under agronomic supervision."
        },
        "environmental_risk": {
            "temp_optimum": "15°C - 22°C (Cool and humid)",
            "humidity_threshold": "> 90% RH",
            "critical_leaf_wetness": "6+ hours"
        },
        "translations": {
            "en": {
                "label": "Tomato Late Blight",
                "tagline": "Severe Oomycete infection. High urgency action required.",
                "step1": "Remove severely blighted foliage immediately.",
                "step2": "Apply organic copper bio-spray or Bordeaux mixture.",
                "step3": "Ensure maximum ventilation and eliminate standing water."
            },
            "hi": {
                "label": "टमाटर पछेती झुलसा (लेट ब्लाइट)",
                "tagline": "अत्यधिक संक्रामक रोग। तुरंत बचाव कदम उठाएं।",
                "step1": "संक्रमित पौधों और पत्तियों को तुरंत हटाकर जला दें।",
                "step2": "बोर्डो मिश्रण या कॉपर कवकनाशी का छिड़काव करें।",
                "step3": "खेत में हवा का संचार बढ़ाएं और पानी जमा न होने दें।"
            },
            "kn": {
                "label": "ಟೊಮೆಟೊ ತಡವಾದ ರೋಗ (ಲೇಟ್ ಬ್ಲೈಟ್)",
                "tagline": "ತೀವ್ರ ಸಾಂಕ್ರಾಮಿಕ ರೋಗ. ತುರ್ತು ಕ್ರಮ ಅಗತ್ಯ.",
                "step1": "ತೀವ್ರವಾಗಿ ಬಾಧಿತ ಎಲೆಗಳನ್ನು ಕೂಡಲೇ ಕಿತ್ತು ಸುಟ್ಟುಹಾಕಿ.",
                "step2": "ಬೋರ್ಡೋ ದ್ರಾವಣ ಅಥವಾ ತಾಮ್ರದ ಜೈವಿಕ ಕೀಟನಾಶಕ ಸಿಂಪಡಿಸಿ.",
                "step3": "ಗಾಳಿಯಾಡುವಿಕೆಯನ್ನು ಹೆಚ್ಚಿಸಿ ಮತ್ತು ನಿಂತ ನೀರನ್ನು ತೆರವುಗೊಳಿಸಿ."
            },
            "te": {
                "label": "టమోటా లేట్ బ్లైట్ తెగులు",
                "tagline": "తీవ్రమైన ఫంగస్ తెగులు. తక్షణమే నివారణ చర్యలు తీసుకోండి.",
                "step1": "బాధిత ఆకులను తొలగించి వెంటనే దూరంగా కాల్చివేయండి.",
                "step2": "బోర్డో మిశ్రమం లేదా కాపర్ బయో-స్ప్రే పిచికారీ చేయండి.",
                "step3": "మొక్కల మధ్య గాలి ప్రసరణ ఉండేలా చూడండి."
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
        "action_plan": {
            "immediate_actions": [
                "Refrain from working or cultivating plants when foliage is wet from morning dew or rain.",
                "Remove heavily blighted leaves with alcohol-sanitized tools."
            ],
            "organic_bio_treatments": [
                "Apply fixed copper bio-fungicide combined with certified organic Bacillus subtilis.",
                "Garlic-chili aqueous extract spray as a natural antimicrobial barrier.",
                "Foliar bio-silicon formulation to thicken epidermal cell walls against bacterial entry."
            ],
            "cultural_prevention": [
                "Use certified disease-free, hot-water treated seeds for nursery raising.",
                "Avoid using recirculated pond water for irrigation.",
                "Strict 2-year rotation with non-host crops."
            ],
            "chemical_advisory": "Bactericides with copper hydroxide + mancozeb synergy. Avoid overuse to prevent copper-resistant Xanthomonas strains."
        },
        "environmental_risk": {
            "temp_optimum": "25°C - 30°C",
            "humidity_threshold": "> 85% RH",
            "critical_leaf_wetness": "Frequent rain splashes"
        },
        "translations": {
            "en": {
                "label": "Tomato Bacterial Spot",
                "tagline": "Bacterial pathogen detected. Disinfect and apply copper bio-protectants.",
                "step1": "Do not touch plants while leaves are wet.",
                "step2": "Apply organic copper protectant and Bacillus bio-agent.",
                "step3": "Sanitize tools between handling plants."
            },
            "hi": {
                "label": "टमाटर जीवाणु धब्बा (बैक्टीरियल स्पॉट)",
                "tagline": "जीवाणु जनित रोग। पत्तियां गीली होने पर काम न करें।",
                "step1": "ओस या बारिश में पौधों को न छुएं।",
                "step2": "कॉपर युक्त जैविक दवा और नीम घोल का छिड़काव करें।",
                "step3": "औजारों को सैनिटाइज रखें और संक्रमित पत्तियां हटाएं।"
            },
            "kn": {
                "label": "ಟೊಮೆಟೊ ಬ್ಯಾಕ್ಟೀರಿಯಾ ಚುಕ್ಕೆ ರೋಗ",
                "tagline": "ಬ್ಯಾಕ್ಟೀರಿಯಾ ಸೋಂಕು. ಎಲೆಗಳು ತೇವವಿರುವಾಗ ಕೆಲಸ ಮಾಡಬೇಡಿ.",
                "step1": "ಇಬ್ಬನಿ ಅಥವಾ ಮಳೆ ಇರುವಾಗ ಗಿಡಗಳನ್ನು ಮುಟ್ಟಬೇಡಿ.",
                "step2": "ತಾಮ್ರದ ಜೈವಿಕ ಕೀಟನಾಶಕ ಮತ್ತು ಬೇವು ದ್ರಾವಣ ಸಿಂಪಡಿಸಿ.",
                "step3": "ಉಪಕರಣಗಳನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ ಮತ್ತು ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತೆಗೆಯಿರಿ."
            },
            "te": {
                "label": "టమోటా బ్యాక్టీరియల్ స్పాట్",
                "tagline": "బాక్టీరియా వల్ల వచ్చే తెగులు. ఆకులు తడిగా ఉన్నప్పుడు పని చేయవద్దు.",
                "step1": "మంచు లేదా వర్షం పడినప్పుడు మొక్కలను తాకవద్దు.",
                "step2": "కాపర్ ఆధారిత బయో-స్ప్రే మరియు వేప నూనె చల్లండి.",
                "step3": "ఉపకరణాలను శుభ్రంగా ఉంచుకోండి."
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
        "action_plan": {
            "immediate_actions": [
                "No remedial intervention required. The crop shows optimum physiological vitality.",
                "Continue standard agronomic monitoring routine twice weekly."
            ],
            "organic_bio_treatments": [
                "Apply prophylactic bio-stimulant (Seaweed extract 2ml/L) to strengthen leaf cuticle.",
                "Maintain healthy rhizosphere with Vermicompost and mycorrhizal inoculation."
            ],
            "cultural_prevention": [
                "Maintain uniform soil moisture using tensiometer or soil finger check.",
                "Keep base mulched with paddy straw or organic residue to conserve soil biota."
            ],
            "chemical_advisory": "Zero chemical sprays required. Conserve beneficial ladybird beetles and predatory mites."
        },
        "environmental_risk": {
            "temp_optimum": "18°C - 28°C",
            "humidity_threshold": "40% - 70% RH",
            "critical_leaf_wetness": "Dry canopy"
        },
        "translations": {
            "en": {
                "label": "Healthy Tomato Leaf",
                "tagline": "Leaf is vibrant and pathogen-free. Maintain preventive care.",
                "step1": "No intervention required. Crop is in good health.",
                "step2": "Apply organic seaweed bio-stimulant for stress resilience.",
                "step3": "Continue standard weekly monitoring."
            },
            "hi": {
                "label": "स्वस्थ टमाटर की पत्ती",
                "tagline": "पत्ती पूरी तरह स्वस्थ और रोगमुक्त है। सामान्य देखभाल जारी रखें।",
                "step1": "किसी रासायनिक छिड़काव की आवश्यकता नहीं है।",
                "step2": "जैविक खाद और पोषण बनाए रखें।",
                "step3": "नियमित निगरानी जारी रखें।"
            },
            "kn": {
                "label": "ಆರೋಗ್ಯಕರ ಟೊಮೆಟೊ ಎಲೆ",
                "tagline": "ಎಲೆ ಸಂಪೂರ್ಣ ಆರೋಗ್ಯಕರವಾಗಿದೆ. ಸಾಮಾನ್ಯ ಆರೈಕೆ ಮುಂದುವರಿಸಿ.",
                "step1": "ಯಾವುದೇ ರಾಸಾಯನಿಕ ಸಿಂಪಡಣೆ ಅಗತ್ಯವಿಲ್ಲ.",
                "step2": "ಸಾವಯವ ಪೋಷಣೆ ಮತ್ತು ತೇವಾಂಶ ಕಾಪಾಡಿಕೊಳ್ಳಿ.",
                "step3": "ವಾರಕ್ಕೊಮ್ಮೆ ಪರಿಶೀಲನೆ ಮುಂದುವರಿಸಿ."
            },
            "te": {
                "label": "ఆరోగ్యకరమైన టమోటా ఆకు",
                "tagline": "ఆకు సంపూర్ణ ఆరోగ్యంగా ఉంది. సాధారణ రక్షణ కొనసాగించండి.",
                "step1": "ఎలాంటి పురుగుమందులు పిచికారీ చేయవద్దు.",
                "step2": "సేంద్రీయ ఎరువులతో పోషణ అందించండి.",
                "step3": "వారం వారం పర్యవేక్షణ కొనసాగించండి."
            }
        }
    },
    "Potato___Early_Blight": {
        "crop": "Potato",
        "disease_name": "Early Blight",
        "pathogen": "Alternaria solani",
        "symptoms": "Dark brown, dry, leathery target-pattern spots with prominent concentric rings. Lower leaves turn chlorotic, shrivel, and droop along stems.",
        "severity_thresholds": {
            "mild": "Under 5% foliar lesions on bottom canopy.",
            "moderate": "10-25% foliar loss, lesions expanding to middle canopy.",
            "severe": "Severe early defoliation reducing tuber bulking."
        },
        "action_plan": {
            "immediate_actions": [
                "Prune infected lower potato foliage early morning.",
                "Avoid overhead irrigation during tuber bulking phase."
            ],
            "organic_bio_treatments": [
                "Apply cold-pressed Neem bio-extract (5ml/L) + Trichoderma viride.",
                "Foliar bio-zinc and bio-potash to support cell wall lignification."
            ],
            "cultural_prevention": [
                "Maintain balanced soil nutrition; avoid nitrogen deficiency which predisposes older foliage to Alternaria.",
                "Hilling up ridge soil around tubers to prevent spore wash-down onto developing tubers."
            ],
            "chemical_advisory": "Contact bio-fungicides preferred. Synthetic options (Chlorothalonil) only if regional agro-meteorological advisories flag high risk."
        },
        "environmental_risk": {
            "temp_optimum": "24°C - 30°C",
            "humidity_threshold": "> 75% RH",
            "critical_leaf_wetness": "Alternating wet and dry periods"
        },
        "translations": {
            "en": {
                "label": "Potato Early Blight",
                "tagline": "Concentric fungal spots detected. Begin organic foliar protection.",
                "step1": "Prune infected lower foliage immediately.",
                "step2": "Spray neem bio-extract and Trichoderma viride.",
                "step3": "Ridge soil properly to protect developing tubers."
            },
            "hi": {
                "label": "आलू अगेती झुलसा",
                "tagline": "फफूंद के छल्लेदार धब्बे पाए गए। जैविक उपचार शुरू करें।",
                "step1": "रोगग्रस्त निचली पत्तियों को तुरंत हटा दें।",
                "step2": "नीम तेल और ट्राइकोडर्मा का छिड़काव करें।",
                "step3": "कंदों पर अच्छी तरह मिट्टी चढ़ाएं ताकि सुरक्षा बनी रहे।"
            },
            "kn": {
                "label": "ಆಲೂಗಡ್ಡೆ ಅರ್ಲಿ ಬ್ಲೈಟ್",
                "tagline": "ಶಿಲೀಂಧ್ರ ಚುಕ್ಕೆಗಳು ಪತ್ತೆಯಾಗಿವೆ. ಜೈವಿಕ ನಿಯಂತ್ರಣ ಕ್ರಮ ಕೈಗೊಳ್ಳಿ.",
                "step1": "ಸೋಂಕಿತ ಕೆಳಗಿನ ಎಲೆಗಳನ್ನು ತಕ್ಷಣ ಕತ್ತರಿಸಿ.",
                "step2": "ಬೇವಿನ ಎಣ್ಣೆ ಮತ್ತು ಟ್ರೈಕೋಡರ್ಮಾ ಸಿಂಪಡಿಸಿ.",
                "step3": "ಗೆಡ್ಡೆಗಳಿಗೆ ಮಣ್ಣನ್ನು ಸರಿಯಾಗಿ ಮುಚ್ಚಿ."
            },
            "te": {
                "label": "బంగాళాదుంప ఎర్లీ బ్లైట్",
                "tagline": "శిలీంధ్ర తెగులు గుర్తించబడింది. సేంద్రీయ పిచికారీ ప్రారంభించండి.",
                "step1": "తెగులు సోకిన క్రింది ఆకులను కత్తిరించండి.",
                "step2": "వేప నూనె మరియు ట్రైకోడెర్మా పిచికారీ చేయండి.",
                "step3": "దుంపలపై మట్టిని బాగా ఎగదోయండి."
            }
        }
    },
    "Potato___Late_Blight": {
        "crop": "Potato",
        "disease_name": "Late Blight",
        "pathogen": "Phytophthora infestans",
        "symptoms": "Water-soaked dark lesions spreading rapidly across foliage and stems; white mold layer under leaves during humid weather.",
        "severity_thresholds": {
            "mild": "Isolated dark water spots on terminal leaves.",
            "moderate": "Fast spreading stem rot and dark foliar blotches.",
            "severe": "Canopy collapse within 48-72 hours, tuber rot risk."
        },
        "action_plan": {
            "immediate_actions": [
                "Dehaulm (cut foliage off at ground level) 10-14 days before harvest if late blight threatens tubers.",
                "Destroy infected haulms immediately away from the potato plot."
            ],
            "organic_bio_treatments": [
                "Spray bio-certified Bordeaux mixture (1%) or Copper Oxychloride.",
                "Bio-formulation of Bacillus subtilis QST 713."
            ],
            "cultural_prevention": [
                "Plant certified disease-free seed tubers.",
                "Select resistant potato cultivars suited for local agro-climatic zones."
            ],
            "chemical_advisory": "Cymoxanil + Mancozeb or Dimethomorph if rapid field epidemic threatens entire community yield."
        },
        "environmental_risk": {
            "temp_optimum": "12°C - 20°C",
            "humidity_threshold": "> 90% RH",
            "critical_leaf_wetness": "Persistent mist or fog"
        },
        "translations": {
            "en": {
                "label": "Potato Late Blight",
                "tagline": "Severe blight detected. Protect tuber crop immediately.",
                "step1": "Dehaulm or remove blighted foliage without delay.",
                "step2": "Apply Bordeaux mixture or copper bio-spray.",
                "step3": "Ensure soil mounds cover tubers completely."
            },
            "hi": {
                "label": "आलू पछेती झुलसा",
                "tagline": "गंभीर झुलसा रोग। कंदों को सुरक्षित रखने के लिए तुरंत कदम उठाएं।",
                "step1": "संक्रमित पत्तों को तुरंत काटें और खेत से बाहर करें।",
                "step2": "बोर्डो मिश्रण का सुरक्षात्मक छिड़काव करें।",
                "step3": "आलू के कंदों पर अच्छी मिट्टी ढकी रखें।"
            },
            "kn": {
                "label": "ಆಲೂಗಡ್ಡೆ ಲೇಟ್ ಬ್ಲೈಟ್",
                "tagline": "ತೀವ್ರ ರೋಗ ಪತ್ತೆಯಾಗಿದೆ. ಆಲೂಗೆಡ್ಡೆ ಬೆಳೆ ರಕ್ಷಣೆಗೆ ತಕ್ಷಣ ಕ್ರಮ.",
                "step1": "ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತಕ್ಷಣ ತೆಗೆದುಹಾಕಿ.",
                "step2": "ಬೋರ್ಡೋ ಮಿಶ್ರಣ ಸಿಂಪಡಿಸಿ.",
                "step3": "ಗೆಡ್ಡೆಗಳು ಹೊರಬರದಂತೆ ಮಣ್ಣು ಮುಚ್ಚಿ."
            },
            "te": {
                "label": "బంగాళాదుంప లేట్ బ్లైట్",
                "tagline": "తీవ్రమైన తెగులు. దుంపలను కాపాడేందుకు చర్యలు చేపట్టండి.",
                "step1": "తెగులు సోకిన కొమ్మలను తొలగించండి.",
                "step2": "బోర్డో మిశ్రమాన్ని పిచికారీ చేయండి.",
                "step3": "దుంపలపై మట్టి సమృద్ధిగా ఉండేలా చూసుకోండి."
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
        "action_plan": {
            "immediate_actions": [
                "Monitor spore density weekly on upper leaf canopy.",
                "Avoid unnecessary leaf injury during hoeing or fertilizer banding."
            ],
            "organic_bio_treatments": [
                "Spray wettable sulfur bio-formulation (2.5g/L water).",
                "Neem seed kernel extract (NSKE 5%) foliar spray.",
                "Ampelomyces quisqualis bio-parasitic fungus spray against rust spores."
            ],
            "cultural_prevention": [
                "Plant rust-tolerant hybrid seeds recommended by regional agricultural university.",
                "Early planting in season to avoid peak air-borne spore clouds."
            ],
            "chemical_advisory": "Fungicide (Azoxystrobin or Tebuconazole) only justified if rust appears prior to tasseling and weather favors disease."
        },
        "environmental_risk": {
            "temp_optimum": "16°C - 25°C",
            "humidity_threshold": "> 95% RH or high dew",
            "critical_leaf_wetness": "Overnight dew periods"
        },
        "translations": {
            "en": {
                "label": "Corn Common Rust",
                "tagline": "Powdery rust pustules detected on corn blades.",
                "step1": "Apply wettable sulfur or neem kernel extract spray.",
                "step2": "Monitor upper canopy leaves near ear level.",
                "step3": "Select rust-resistant hybrids for next cycle."
            },
            "hi": {
                "label": "मक्का का सामान्य रतुआ (कॉमन रस्ट)",
                "tagline": "मक्के की पत्तियों पर भूरे-नारंगी फफोले दिखे हैं।",
                "step1": "घुलनशील सल्फर या नीम अर्क (5%) का छिड़काव करें।",
                "step2": "भुट्टे के पास वाले ऊपरी पत्तों पर विशेष नजर रखें।",
                "step3": "अगली बुवाई में रोगरोधी किस्मों का चयन करें।"
            },
            "kn": {
                "label": "ಮೆಕ್ಕೆಜೋಳದ ಸಾಮಾನ್ಯ ತುಕ್ಕು ರೋಗ",
                "tagline": "ಮೆಕ್ಕೆಜೋಳದ ಎಲೆಗಳ ಮೇಲೆ ತುಕ್ಕು ಬಣ್ಣದ ಕಲೆಗಳು ಪತ್ತೆಯಾಗಿವೆ.",
                "step1": "ಕರಗುವ ಗಂಧಕ (ಸಲ್ಫರ್) ಅಥವಾ ಬೇವಿನ ಕಷಾಯ ಸಿಂಪಡಿಸಿ.",
                "step2": "ತೆನೆಯ ಸಮೀಪವಿರುವ ಎಲೆಗಳನ್ನು ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಿ.",
                "step3": "ಮುಂದಿನ ಋತುವಿನಲ್ಲಿ ರೋಗನಿರೋಧಕ ತಳಿಗಳನ್ನು ಆಯ್ಕೆಮಾಡಿ."
            },
            "te": {
                "label": "మొక్కజొన్న సాధారణ తుప్పు తెగులు",
                "tagline": "మొక్కజొన్న ఆకులపై తుప్పు మచ్చలు కనిపించాయి.",
                "step1": "నీటిలో కరిగే గంధకం లేదా వేప కషాయం పిచికారీ చేయండి.",
                "step2": "కంకి వద్ద ఉన్న ఆకులను జాగ్రత్తగా గమనించండి.",
                "step3": "తదుపరి పంటకు తెగులు నిరోధక రకాలను ఎంచుకోండి."
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
        "action_plan": {
            "immediate_actions": [
                "Avoid split overdoses of synthetic nitrogenous fertilizers (excess urea boosts blast susceptibility).",
                "Maintain continuous thin standing water layer in paddy basins."
            ],
            "organic_bio_treatments": [
                "Pseudomonas fluorescens bio-agent (10g/kg seed treatment & 5g/L foliar spray).",
                "Panchagavya (3%) or fermented butter-milk aqueous bio-spray.",
                "Bio-silica supplement (Diatomaceous earth extract) to harden leaf epidermis."
            ],
            "cultural_prevention": [
                "Treat paddy seeds before nursery sowing.",
                "Maintain clean bunds free of weed grass hosts (Echinochloa spp.)."
            ],
            "chemical_advisory": "Tricyclazole 75% WP or Isoprothiolane at neck emergence stage only if threshold crosses 5-10%."
        },
        "environmental_risk": {
            "temp_optimum": "20°C - 26°C",
            "humidity_threshold": "> 90% RH",
            "critical_leaf_wetness": "Extended nocturnal leaf wetness"
        },
        "translations": {
            "en": {
                "label": "Paddy Rice Blast",
                "tagline": "Spindle lesion fungal blast detected. Halt excess nitrogen fertilizer.",
                "step1": "Stop excess urea application immediately.",
                "step2": "Foliar spray Pseudomonas fluorescens bio-agent (5g/L).",
                "step3": "Maintain water table in the basin."
            },
            "hi": {
                "label": "धान का झोंका रोग (राइस ब्लास्ट)",
                "tagline": "पत्तियों पर आंख जैसे धब्बे दिखे हैं। यूरिया का अधिक प्रयोग तुरंत रोकें।",
                "step1": "यूरिया खाद का अत्यधिक उपयोग तुरंत बंद करें।",
                "step2": "स्यूडोमोनास फ्लोरेसेंस (5 ग्राम/लीटर) का छिड़काव करें।",
                "step3": "खेत में उचित नमी और जल स्तर बनाए रखें।"
            },
            "kn": {
                "label": "ಭತ್ತದ ಬೆಂಕಿ ರೋಗ (ರೈಸ್ ಬ್ಲಾಸ್ಟ್)",
                "tagline": "ಎಲೆಗಳ ಮೇಲೆ ಕಣ್ಣಿನಾಕಾರದ ಕಲೆಗಳು ಪತ್ತೆಯಾಗಿವೆ. ಯೂರಿಯಾ ಬಳಕೆಯನ್ನು ನಿಲ್ಲಿಸಿ.",
                "step1": "ಹೆಚ್ಚುವರಿ ಯೂರಿಯಾ ರಸಗೊಬ್ಬರ ಕೊಡುವುದನ್ನು ಕೂಡಲೇ ನಿಲ್ಲಿಸಿ.",
                "step2": "ಸ್ಯೂಡೋಮೊನಾಸ್ ಫ್ಲೋರೆಸೆನ್ಸ್ ಜೈವಿಕ ದ್ರಾವಣ ಸಿಂಪಡಿಸಿ.",
                "step3": "ಗದ್ದೆಯಲ್ಲಿ ಸೂಕ್ತ ನೀರಿನ ಮಟ್ಟವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."
            },
            "te": {
                "label": "వరి అగ్గి తెగులు (రైస్ బ్లాస్ట్)",
                "tagline": "ఆకులపై కంటి ఆకారపు మచ్చలు కనిపించాయి. యూరియా వాడకాన్ని తగ్గించండి.",
                "step1": "అదనపు యూరియా ఎరువుల వాడకాన్ని వెంటనే ఆపండి.",
                "step2": "సూడోమోనాస్ ఫ్లోరోసెన్స్ బయో-స్ప్రే (5 గ్రా/లీ) పిచికారీ చేయండి.",
                "step3": "పొలంలో తగినంత నీటి మట్టాన్ని నిర్వహించండి."
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
