"""
CropCare AI - Fast Vectorized Sample Generator
Creates high-fidelity visual test leaves replicating PlantVillage dataset samples
in under 1 second using vectorized NumPy.
"""

import os
import numpy as np
import cv2


def create_base_leaf(w=500, h=500, leaf_type="broad", base_bgr=(45, 135, 40)):
    """Creates a leaf image with natural green gradients using fast numpy ops."""
    img = np.full((h, w, 3), (242, 240, 235), dtype=np.uint8)  # Field board background
    mask = np.zeros((h, w), dtype=np.uint8)
    
    if leaf_type == "broad":
        pts = np.array([
            [w // 2, int(h * 0.12)],
            [int(w * 0.78), int(h * 0.32)],
            [int(w * 0.85), int(h * 0.58)],
            [int(w * 0.68), int(h * 0.80)],
            [w // 2, int(h * 0.88)],
            [int(w * 0.32), int(h * 0.80)],
            [int(w * 0.15), int(h * 0.58)],
            [int(w * 0.22), int(h * 0.32)],
        ], np.int32)
        cv2.fillPoly(mask, [pts], 255)
        mask = cv2.GaussianBlur(mask, (31, 31), 0)
        _, mask = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)
    else:
        # Elongated monocot blade
        pts = np.array([
            [w // 2, int(h * 0.08)],
            [int(w * 0.62), int(h * 0.35)],
            [int(w * 0.60), int(h * 0.70)],
            [int(w * 0.54), int(h * 0.92)],
            [int(w * 0.46), int(h * 0.92)],
            [int(w * 0.40), int(h * 0.70)],
            [int(w * 0.38), int(h * 0.35)],
        ], np.int32)
        cv2.fillPoly(mask, [pts], 255)
        mask = cv2.GaussianBlur(mask, (21, 21), 0)
        _, mask = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)

    # Fast vectorized gradient fill
    x_coords = np.arange(w)
    dist_from_mid = np.abs(x_coords - w // 2) / (w / 2)  # shape (w,)
    dist_grid = np.tile(dist_from_mid, (h, 1))           # shape (h, w)
    
    noise = np.random.normal(0, 4, (h, w)).astype(np.float32)
    
    b_chan = np.clip(base_bgr[0] - dist_grid * 15 + noise, 20, 230).astype(np.uint8)
    g_chan = np.clip(base_bgr[1] - dist_grid * 25 + noise, 35, 245).astype(np.uint8)
    r_chan = np.clip(base_bgr[2] - dist_grid * 10 + noise, 15, 220).astype(np.uint8)
    
    leaf_rgb = cv2.merge([b_chan, g_chan, r_chan])

    # Midrib and lateral veins
    vein_color = (int(base_bgr[0] + 15), int(base_bgr[1] + 30), int(base_bgr[2] + 20))
    cv2.line(leaf_rgb, (w // 2, int(h * 0.12)), (w // 2, int(h * 0.88)), vein_color, 3)
    
    if leaf_type == "broad":
        for vy in range(int(h * 0.28), int(h * 0.78), 45):
            cv2.line(leaf_rgb, (w // 2, vy), (int(w * 0.74), vy - 20), vein_color, 2)
            cv2.line(leaf_rgb, (w // 2, vy), (int(w * 0.26), vy - 20), vein_color, 2)
    else:
        for offset in [-30, -15, 15, 30]:
            cv2.line(leaf_rgb, (w // 2 + offset, int(h * 0.15)), (w // 2 + int(offset * 0.75), int(h * 0.88)), vein_color, 1)

    # Combine with background
    inv_mask = cv2.bitwise_not(mask)
    final_img = cv2.add(
        cv2.bitwise_and(leaf_rgb, leaf_rgb, mask=mask),
        cv2.bitwise_and(img, img, mask=inv_mask)
    )
    return final_img, mask


def generate_early_blight_sample():
    img, mask = create_base_leaf(500, 500, "broad", base_bgr=(40, 130, 35))
    # Concentric target spots
    spot_centers = [(210, 260), (315, 340), (275, 185)]
    for cx, cy in spot_centers:
        cv2.circle(img, (cx, cy), 45, (30, 205, 225), -1)  # Yellow halo
        cv2.circle(img, (cx, cy), 30, (25, 55, 110), -1)   # Necrotic brown
        cv2.circle(img, (cx, cy), 20, (15, 30, 65), -1)    # Deep core
        cv2.circle(img, (cx, cy), 13, (25, 65, 125), 2)    # Ring
        cv2.circle(img, (cx, cy), 7, (10, 20, 45), -1)
        
    for cx, cy in [(160, 320), (345, 230)]:
        cv2.circle(img, (cx, cy), 22, (35, 195, 215), -1)
        cv2.circle(img, (cx, cy), 14, (20, 45, 90), -1)

    inv_mask = cv2.bitwise_not(mask)
    bg = np.full((500, 500, 3), (242, 240, 235), dtype=np.uint8)
    return cv2.add(cv2.bitwise_and(img, img, mask=mask), cv2.bitwise_and(bg, bg, mask=inv_mask))


def generate_late_blight_sample():
    img, mask = create_base_leaf(500, 500, "broad", base_bgr=(38, 120, 32))
    cv2.ellipse(img, (230, 185), (80, 50), 30, 0, 360, (20, 38, 48), -1)
    cv2.ellipse(img, (325, 285), (90, 60), -20, 0, 360, (22, 42, 52), -1)
    cv2.ellipse(img, (185, 345), (65, 45), 45, 0, 360, (20, 35, 45), -1)
    # Pale margin
    cv2.ellipse(img, (230, 185), (90, 60), 30, 0, 360, (60, 155, 170), 3)
    cv2.ellipse(img, (325, 285), (100, 70), -20, 0, 360, (60, 155, 170), 3)

    inv_mask = cv2.bitwise_not(mask)
    bg = np.full((500, 500, 3), (242, 240, 235), dtype=np.uint8)
    return cv2.add(cv2.bitwise_and(img, img, mask=mask), cv2.bitwise_and(bg, bg, mask=inv_mask))


def generate_healthy_sample():
    img, mask = create_base_leaf(500, 500, "broad", base_bgr=(52, 160, 48))
    inv_mask = cv2.bitwise_not(mask)
    bg = np.full((500, 500, 3), (242, 240, 235), dtype=np.uint8)
    return cv2.add(cv2.bitwise_and(img, img, mask=mask), cv2.bitwise_and(bg, bg, mask=inv_mask))


def generate_bacterial_spot_sample():
    img, mask = create_base_leaf(500, 500, "broad", base_bgr=(44, 136, 40))
    np.random.seed(42)
    for _ in range(35):
        bx = int(np.random.randint(165, 345))
        by = int(np.random.randint(165, 375))
        r = int(np.random.randint(4, 9))
        cv2.circle(img, (bx, by), r + 3, (40, 195, 210), -1)
        cv2.circle(img, (bx, by), r, (15, 25, 40), -1)

    inv_mask = cv2.bitwise_not(mask)
    bg = np.full((500, 500, 3), (242, 240, 235), dtype=np.uint8)
    return cv2.add(cv2.bitwise_and(img, img, mask=mask), cv2.bitwise_and(bg, bg, mask=inv_mask))


def generate_corn_rust_sample():
    img, mask = create_base_leaf(500, 500, "elongated", base_bgr=(46, 140, 50))
    np.random.seed(99)
    for _ in range(50):
        rx = int(np.random.randint(205, 295))
        ry = int(np.random.randint(125, 415))
        rw = int(np.random.randint(5, 10))
        rh = int(np.random.randint(8, 16))
        cv2.ellipse(img, (rx, ry), (rw, rh), int(np.random.randint(-15, 15)), 0, 360, (20, 105, 220), -1)
        cv2.ellipse(img, (rx, ry), (max(rw - 2, 2), max(rh - 4, 3)), 0, 0, 360, (15, 60, 160), -1)

    inv_mask = cv2.bitwise_not(mask)
    bg = np.full((500, 500, 3), (242, 240, 235), dtype=np.uint8)
    return cv2.add(cv2.bitwise_and(img, img, mask=mask), cv2.bitwise_and(bg, bg, mask=inv_mask))


def generate_rice_blast_sample():
    img, mask = create_base_leaf(500, 500, "elongated", base_bgr=(42, 132, 45))
    spindles = [(250, 180), (230, 260), (270, 330), (245, 400)]
    for sx, sy in spindles:
        pts_outer = np.array([[sx, sy - 28], [sx + 15, sy], [sx, sy + 28], [sx - 15, sy]], np.int32)
        cv2.fillPoly(img, [pts_outer], (25, 55, 110))
        pts_inner = np.array([[sx, sy - 16], [sx + 8, sy], [sx, sy + 16], [sx - 8, sy]], np.int32)
        cv2.fillPoly(img, [pts_inner], (180, 190, 195))

    inv_mask = cv2.bitwise_not(mask)
    bg = np.full((500, 500, 3), (242, 240, 235), dtype=np.uint8)
    return cv2.add(cv2.bitwise_and(img, img, mask=mask), cv2.bitwise_and(bg, bg, mask=inv_mask))


def main():
    target_dir = os.path.join(os.path.dirname(__file__), "samples")
    os.makedirs(target_dir, exist_ok=True)
    
    samples = {
        "Tomato_Early_Blight.jpg": (generate_early_blight_sample(), "Tomato___Early_Blight"),
        "Tomato_Late_Blight.jpg": (generate_late_blight_sample(), "Tomato___Late_Blight"),
        "Tomato_Healthy.jpg": (generate_healthy_sample(), "Tomato___Healthy"),
        "Tomato_Bacterial_Spot.jpg": (generate_bacterial_spot_sample(), "Tomato___Bacterial_Spot"),
        "Corn_Common_Rust.jpg": (generate_corn_rust_sample(), "Corn___Common_Rust"),
        "Rice_Blast.jpg": (generate_rice_blast_sample(), "Rice___Blast")
    }
    
    for filename, (img, key) in samples.items():
        filepath = os.path.join(target_dir, filename)
        cv2.imwrite(filepath, img)
        print(f"Generated sample: {filename} -> {key}")

if __name__ == "__main__":
    main()
