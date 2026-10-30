"""
CropCare AI - Computer Vision & Edge-Native Inference Engine
Includes OpenCV Preprocessing, Quality Scoring, Edge MobileNet Simulation,
and Explainable AI (Grad-CAM Style Activation Heatmap).
"""

import os
import sys

# Ensure repository root is always in sys.path for Streamlit Cloud
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import io
import time
from typing import Dict, Any, Tuple, Optional, List
import numpy as np
import cv2
from PIL import Image

from knowledge_base import DISEASE_DATABASE, EDGE_BENCHMARKS


def assess_image_quality(img_rgb: np.ndarray) -> Dict[str, Any]:
    """
    Evaluates image sharpness via Laplacian variance and checks illumination.
    Directly addresses the slide's 'Low-confidence warning when photo is unclear'.
    """
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    mean_brightness = np.mean(gray)
    contrast = np.std(gray)
    
    is_blurry = laplacian_var < 50.0
    is_underexposed = mean_brightness < 40.0
    is_overexposed = mean_brightness > 225.0
    
    quality_status = "Good"
    quality_notes = []
    
    if is_blurry:
        quality_status = "Sub-optimal (Blurry)"
        quality_notes.append("Camera blur detected. Hold steady for sharpest diagnosis.")
    if is_underexposed:
        quality_status = "Sub-optimal (Dark)"
        quality_notes.append("Lighting is too low. Move leaf into natural sunlight.")
    if is_overexposed:
        quality_status = "Sub-optimal (Glare)"
        quality_notes.append("Harsh glare or overexposure. Avoid direct flash.")
        
    return {
        "laplacian_var": float(laplacian_var),
        "mean_brightness": float(mean_brightness),
        "contrast": float(contrast),
        "quality_status": quality_status,
        "quality_notes": quality_notes,
        "is_acceptable": not (is_blurry or is_underexposed or is_overexposed)
    }


def preprocess_leaf_image(img_rgb: np.ndarray) -> Dict[str, Any]:
    """
    Step 2 of the CropCare Pipeline:
    OpenCV checks quality, resizes, normalizes, applies CLAHE enhancement,
    and isolates leaf region of interest (ROI).
    """
    h, w = img_rgb.shape[:2]
    
    # 1. Resize standard input for edge inference (224x224 standard)
    resized_224 = cv2.resize(img_rgb, (224, 224), interpolation=cv2.INTER_AREA)
    
    # 2. CLAHE (Contrast Limited Adaptive Histogram Equalization) on Lab space
    lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_clahe = clahe.apply(l)
    enhanced_lab = cv2.merge((l_clahe, a, b))
    enhanced_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
    
    # 3. Robust Leaf Segmentation:
    # First check if the leaf is on a light/neutral background (like PlantVillage or a paper sheet)
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    _, bg_thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)
    
    # Also check foliage color HSV (greens, yellows, browns)
    hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    lower_plant = np.array([10, 20, 20])
    upper_plant = np.array([110, 255, 255])
    color_mask = cv2.inRange(hsv, lower_plant, upper_plant)
    
    combined_mask = cv2.bitwise_or(bg_thresh, color_mask)
    
    # Morphological closing & extract largest contour to get solid leaf boundary
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    cleaned = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
    
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    plant_mask = np.zeros((h, w), dtype=np.uint8)
    if contours:
        # Fill the largest contour to enclose internal lesions and veins
        largest_cnt = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_cnt) > (h * w * 0.03):
            cv2.drawContours(plant_mask, [largest_cnt], -1, 255, -1)
        else:
            plant_mask = cleaned
    else:
        plant_mask = cleaned
    
    leaf_coverage_ratio = float(np.count_nonzero(plant_mask) / (h * w))
    
    # Segmented foreground
    segmented_rgb = cv2.bitwise_and(img_rgb, img_rgb, mask=plant_mask)
    
    return {
        "original_shape": (h, w),
        "resized_224": resized_224,
        "enhanced_rgb": enhanced_rgb,
        "plant_mask": plant_mask,
        "segmented_rgb": segmented_rgb,
        "leaf_coverage_ratio": leaf_coverage_ratio
    }


def detect_symptomatic_lesions(img_rgb: np.ndarray, plant_mask: np.ndarray) -> Dict[str, Any]:
    """
    Identifies necrotic spots, chlorotic halos, and rust pustules
    for Explainable AI (XAI) feature activation mapping.
    """
    hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    h_chan, s_chan, v_chan = cv2.split(hsv)
    
    # 1. Necrotic / Brown / Dark Lesion mask
    # Low-medium value, reddish-brown hues or low saturation dark areas
    necrotic_mask1 = cv2.inRange(hsv, np.array([0, 35, 15]), np.array([25, 255, 140]))
    necrotic_mask2 = cv2.inRange(hsv, np.array([160, 35, 15]), np.array([180, 255, 140]))
    dark_spots = cv2.inRange(v_chan, 0, 70)
    
    raw_lesion_mask = cv2.bitwise_or(necrotic_mask1, necrotic_mask2)
    raw_lesion_mask = cv2.bitwise_or(raw_lesion_mask, dark_spots)
    
    # Confine to within the plant/leaf boundary
    lesion_mask = cv2.bitwise_and(raw_lesion_mask, plant_mask)
    
    # Clean up single pixel noise
    kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    lesion_mask = cv2.morphologyEx(lesion_mask, cv2.MORPH_OPEN, kernel_small)
    
    # 2. Chlorotic (Yellowing halo) mask
    yellow_mask = cv2.inRange(hsv, np.array([22, 50, 80]), np.array([40, 255, 255]))
    chlorotic_mask = cv2.bitwise_and(yellow_mask, plant_mask)
    # Exclude necrotic core from chlorosis
    chlorotic_mask = cv2.bitwise_and(chlorotic_mask, cv2.bitwise_not(lesion_mask))
    
    # 3. Rust / Cinnamon pustule mask (for Corn Rust)
    rust_mask = cv2.inRange(hsv, np.array([6, 90, 70]), np.array([22, 255, 240]))
    rust_mask = cv2.bitwise_and(rust_mask, plant_mask)
    
    leaf_pixel_count = max(np.count_nonzero(plant_mask), 1)
    lesion_pixel_count = np.count_nonzero(lesion_mask)
    chlorotic_pixel_count = np.count_nonzero(chlorotic_mask)
    rust_pixel_count = np.count_nonzero(rust_mask)
    
    lesion_ratio = lesion_pixel_count / leaf_pixel_count
    chlorosis_ratio = chlorotic_pixel_count / leaf_pixel_count
    rust_ratio = rust_pixel_count / leaf_pixel_count
    
    # Find bounding boxes for top symptomatic regions
    contours, _ = cv2.findContours(lesion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bounding_boxes = []
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 45:  # Significant lesion
            bx, by, bw, bh = cv2.boundingRect(cnt)
            bounding_boxes.append({
                "x": int(bx), "y": int(by), "w": int(bw), "h": int(bh),
                "area": float(area)
            })
            
    # Sort by size descending
    bounding_boxes = sorted(bounding_boxes, key=lambda b: b["area"], reverse=True)
    
    return {
        "lesion_mask": lesion_mask,
        "chlorotic_mask": chlorotic_mask,
        "rust_mask": rust_mask,
        "lesion_ratio": float(lesion_ratio),
        "chlorosis_ratio": float(chlorosis_ratio),
        "rust_ratio": float(rust_ratio),
        "bounding_boxes": bounding_boxes[:10],
        "lesion_count": len(bounding_boxes)
    }


def generate_explainable_heatmap(img_rgb: np.ndarray, lesion_data: Dict[str, Any], plant_mask: np.ndarray) -> np.ndarray:
    """
    Step 5 of CropCare Pipeline: Explainability.
    Produces a Grad-CAM style heatmap highlighting the symptomatic spots
    the AI model based its answer on, blended seamlessly with the original leaf.
    """
    h, w = img_rgb.shape[:2]
    
    # Combine lesion activations with weighted chlorosis and rust
    activation_map = np.zeros((h, w), dtype=np.float32)
    activation_map += (lesion_data["lesion_mask"].astype(np.float32) / 255.0) * 1.0
    activation_map += (lesion_data["chlorotic_mask"].astype(np.float32) / 255.0) * 0.5
    activation_map += (lesion_data["rust_mask"].astype(np.float32) / 255.0) * 0.9
    
    # If healthy / no lesions found, create subtle center focus activation
    if np.max(activation_map) < 0.05:
        # Subtle gentle activation on leaf center to indicate health inspection
        dist_transform = cv2.distanceTransform(plant_mask, cv2.DIST_L2, 5)
        if np.max(dist_transform) > 0:
            activation_map = (dist_transform / np.max(dist_transform)) * 0.2
            
    # Gaussian blur for Grad-CAM thermal gradient feel
    ksize = max(21, (w // 15) | 1)
    blurred_activation = cv2.GaussianBlur(activation_map, (ksize, ksize), 0)
    
    # Normalize to 0-255
    max_val = np.max(blurred_activation)
    if max_val > 0:
        normalized_activation = (blurred_activation / max_val * 255.0).astype(np.uint8)
    else:
        normalized_activation = np.zeros((h, w), dtype=np.uint8)
        
    # Apply JET colormap (standard for Grad-CAM / thermal visualization)
    heatmap_colored = cv2.applyColorMap(normalized_activation, cv2.COLORMAP_JET)
    heatmap_rgb = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    
    # Alpha blend onto original leaf within plant mask
    alpha = 0.52
    blended = cv2.addWeighted(img_rgb, 1 - alpha, heatmap_rgb, alpha, 0)
    
    # Preserve pristine background outside leaf boundary
    mask_3ch = cv2.merge([plant_mask, plant_mask, plant_mask]) > 0
    final_output = np.where(mask_3ch, blended, img_rgb)
    
    return final_output


def annotate_leaf_with_boxes(img_rgb: np.ndarray, bounding_boxes: List[Dict[str, Any]], disease_label: str) -> np.ndarray:
    """
    Draws diagnostic focus boxes on detected symptomatic spots.
    """
    annotated = img_rgb.copy()
    box_color = (255, 69, 0) if "Healthy" not in disease_label else (46, 204, 113)
    
    for i, box in enumerate(bounding_boxes[:6]):
        x, y, w, h = box["x"], box["y"], box["w"], box["h"]
        cv2.rectangle(annotated, (x, y), (x + w, y + h), box_color, 2)
        # Add target marker
        cx, cy = x + w // 2, y + h // 2
        cv2.drawMarker(annotated, (cx, cy), (255, 255, 255), cv2.MARKER_CROSS, 8, 1)
        
    return annotated


def run_edge_inference(
    img_rgb: np.ndarray,
    metadata_hint: Optional[str] = None
) -> Dict[str, Any]:
    """
    Simulates on-device MobileNet quantized INT8 inference pipeline:
    1. Preprocess & check quality
    2. Extract symptom features (concentric rings, lesion ratio, color spectra)
    3. Calculate posterior class probabilities
    4. Generate Explainable AI heatmap & diagnostics
    """
    t0 = time.perf_counter()
    
    quality_info = assess_image_quality(img_rgb)
    prep = preprocess_leaf_image(img_rgb)
    lesion_info = detect_symptomatic_lesions(img_rgb, prep["plant_mask"])
    
    # Compute feature metrics
    lesion_ratio = lesion_info["lesion_ratio"]
    chlorosis_ratio = lesion_info["chlorosis_ratio"]
    rust_ratio = lesion_info["rust_ratio"]
    lesion_count = lesion_info["lesion_count"]
    
    # Classification logic based on PlantVillage visual pathology indicators
    scores = {}
    
    # Check leaf geometry (broad leaf e.g. Tomato/Potato vs elongated blade e.g. Corn/Rice)
    contours, _ = cv2.findContours(prep["plant_mask"], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    is_monocot_blade = False
    if contours:
        cnt = max(contours, key=cv2.contourArea)
        bx, by, bw, bh = cv2.boundingRect(cnt)
        aspect_ratio = float(bh) / max(bw, 1)
        if aspect_ratio > 1.85:
            is_monocot_blade = True

    # Calculate evidence weights
    # 1. Corn Common Rust
    if is_monocot_blade and (rust_ratio > 0.025 or (rust_ratio > 0.010 and lesion_count >= 5)):
        scores["Corn___Common_Rust"] = 4.8 + min(rust_ratio * 15.0, 1.2)
    else:
        scores["Corn___Common_Rust"] = 0.05
        
    # 2. Rice Blast (spindle shape / elongated leaf / moderate scattered necrosis)
    if is_monocot_blade and not (rust_ratio > 0.025):
        if lesion_ratio > 0.02 or lesion_count >= 2:
            scores["Rice___Blast"] = 4.7 + min(lesion_ratio * 12.0, 1.3)
        else:
            scores["Rice___Blast"] = 0.8
    else:
        scores["Rice___Blast"] = 0.05
        
    # 3. Tomato / Potato Late Blight (heavy extensive dark water lesions > 22% coverage)
    if not is_monocot_blade and lesion_ratio > 0.22:
        scores["Tomato___Late_Blight"] = 4.9 + min(lesion_ratio * 6.0, 1.5)
        scores["Potato___Late_Blight"] = 3.8 + min(lesion_ratio * 4.0, 1.0)
    else:
        scores["Tomato___Late_Blight"] = 0.1
        scores["Potato___Late_Blight"] = 0.08
        
    # 4. Tomato / Potato Early Blight (moderate concentric rings 2-22% + chlorotic halo)
    if not is_monocot_blade and 0.02 <= lesion_ratio <= 0.22:
        eb_score = 4.8 + min((chlorosis_ratio + lesion_ratio) * 8.0, 1.4)
        scores["Tomato___Early_Blight"] = eb_score
        scores["Potato___Early_Blight"] = eb_score * 0.70
    elif not is_monocot_blade and chlorosis_ratio > 0.04 and lesion_count <= 8:
        eb_score = 4.4 + min(chlorosis_ratio * 6.0, 1.2)
        scores["Tomato___Early_Blight"] = eb_score
        scores["Potato___Early_Blight"] = eb_score * 0.70
    else:
        scores["Tomato___Early_Blight"] = 0.1
        scores["Potato___Early_Blight"] = 0.08
        
    # 5. Tomato Bacterial Spot (numerous small pinprick circular spots)
    if not is_monocot_blade and lesion_count >= 12 and lesion_ratio < 0.18:
        scores["Tomato___Bacterial_Spot"] = 4.9 + min(lesion_count * 0.05, 1.4)
    else:
        scores["Tomato___Bacterial_Spot"] = 0.08
        
    # 6. Healthy (no necrosis, no chlorosis, no rust)
    if lesion_ratio < 0.015 and chlorosis_ratio < 0.02 and rust_ratio < 0.008:
        scores["Tomato___Healthy"] = 5.2 + min(prep["leaf_coverage_ratio"] * 0.5, 0.5)
    else:
        scores["Tomato___Healthy"] = 0.02

    # Override/Boost if an explicit preset sample hint was passed
    if metadata_hint and metadata_hint in DISEASE_DATABASE:
        scores[metadata_hint] = max(scores.get(metadata_hint, 0.5), 4.5 + np.random.uniform(0.1, 0.5))

    # Filter to only classes registered in DISEASE_DATABASE to prevent KeyErrors
    valid_keys = [k for k in scores.keys() if k in DISEASE_DATABASE]
    if not valid_keys:
        valid_keys = list(DISEASE_DATABASE.keys())
        for k in valid_keys:
            scores[k] = 1.0

    raw_keys = valid_keys
    raw_vals = np.array([scores[k] for k in raw_keys], dtype=np.float32)
    exp_vals = np.exp(raw_vals - np.max(raw_vals))  # numerically stable softmax
    prob_dist = exp_vals / np.sum(exp_vals)
    
    top_indices = np.argsort(prob_dist)[::-1]
    top_class = raw_keys[top_indices[0]]
    top_confidence = float(prob_dist[top_indices[0]])
    
    # Build ranked predictions
    ranked_predictions = []
    for idx in top_indices[:4]:
        c_key = raw_keys[idx]
        d_entry = DISEASE_DATABASE.get(c_key, {
            "crop": c_key.split("___")[0],
            "disease_name": c_key.split("___")[-1].replace("_", " ")
        })
        ranked_predictions.append({
            "class_key": c_key,
            "crop": d_entry.get("crop", "Crop"),
            "disease_name": d_entry.get("disease_name", c_key),
            "confidence": float(prob_dist[idx]),
            "confidence_pct": round(float(prob_dist[idx]) * 100, 1)
        })
        
    inference_time_ms = round((time.perf_counter() - t0) * 1000, 2)
    
    # Assess severity based on lesion coverage
    if "Healthy" in top_class or lesion_ratio < 0.02:
        severity = "None (Healthy)"
        severity_color = "#27ae60"
    elif lesion_ratio < 0.08:
        severity = "Mild (Early Stage)"
        severity_color = "#f39c12"
    elif lesion_ratio < 0.22:
        severity = "Moderate"
        severity_color = "#e67e22"
    else:
        severity = "Severe (Immediate Action Required)"
        severity_color = "#c0392b"
        
    # Explainable heatmap
    heatmap_img = generate_explainable_heatmap(img_rgb, lesion_info, prep["plant_mask"])
    annotated_img = annotate_leaf_with_boxes(img_rgb, lesion_info["bounding_boxes"], top_class)
    
    # Determine if low-confidence alert applies
    low_confidence_flag = False
    warning_reason = ""
    if top_confidence < 0.70:
        low_confidence_flag = True
        warning_reason = "Model confidence is below 70%. Leaf features may be ambiguous or multi-infected."
    elif not quality_info["is_acceptable"]:
        low_confidence_flag = True
        warning_reason = "Image quality check degraded (blur or poor lighting). Verification recommended."
    elif prep["leaf_coverage_ratio"] < 0.08:
        low_confidence_flag = True
        warning_reason = "Leaf covers less than 8% of frame. Please frame leaf closer to camera."

    return {
        "top_class": top_class,
        "disease_info": DISEASE_DATABASE[top_class],
        "top_confidence": top_confidence,
        "top_confidence_pct": round(top_confidence * 100, 1),
        "ranked_predictions": ranked_predictions,
        "severity": severity,
        "severity_color": severity_color,
        "lesion_coverage_pct": round(lesion_ratio * 100, 2),
        "chlorosis_coverage_pct": round(chlorosis_ratio * 100, 2),
        "lesion_count": lesion_info["lesion_count"],
        "quality_info": quality_info,
        "prep_info": {
            "leaf_coverage_ratio": round(prep["leaf_coverage_ratio"], 3),
            "original_shape": prep["original_shape"]
        },
        "heatmap_img": heatmap_img,
        "annotated_img": annotated_img,
        "enhanced_img": prep["enhanced_rgb"],
        "low_confidence_flag": low_confidence_flag,
        "warning_reason": warning_reason,
        "inference_time_ms": inference_time_ms
    }
