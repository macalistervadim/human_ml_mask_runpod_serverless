
from PIL import Image
import numpy as np
import cv2
from pathlib import Path

# ================== ATR LABELS ==================
BACKGROUND = 0
HAT = 1
HAIR = 2
SUNGLASSES = 3
UPPER_CLOTHES = 4
SKIRT = 5
PANTS = 6
DRESS = 7
BELT = 8
LEFT_SHOE = 9
RIGHT_SHOE = 10
FACE = 11
LEFT_LEG = 12
RIGHT_LEG = 13
LEFT_ARM = 14
RIGHT_ARM = 15
BAG = 16
SCARF = 17

CLOTHING_LABELS = {UPPER_CLOTHES, SKIRT, PANTS, DRESS, BELT, BAG, SCARF}
BODY_LABELS = {LEFT_ARM, RIGHT_ARM, LEFT_LEG, RIGHT_LEG}
HEAD_LABELS = {FACE, HAIR, HAT, SUNGLASSES}

def build_clothing_mask(parsing_path: Path, output_mask_path: Path):
    # ================== LOAD PARSING MAP ==================
    img = Image.open(parsing_path)
    if img.mode != "P":
        img = img.convert("P")
    parsing = np.array(img)

    # ================== STEP 1: BASE CLOTHING MASK ==================
    mask_clothes = np.isin(parsing, list(CLOTHING_LABELS)).astype(np.uint8)

    # ================== STEP 2: AGGRESSIVE EXPANSION ==================
    expand_kernel = np.ones((40, 40), np.uint8)
    expanded_clothes = cv2.dilate(mask_clothes, expand_kernel, iterations=1)

    # ================== STEP 3: INCLUDE NEARBY BODY ==================
    mask_body = np.isin(parsing, list(BODY_LABELS)).astype(np.uint8)
    mask_body_near_clothes = expanded_clothes & mask_body
    mask_body_near_clothes = cv2.erode(mask_body_near_clothes, np.ones((8, 8), np.uint8), iterations=1)

    # ================== STEP 4: HUMAN SILHOUETTE BUFFER ==================
    HUMAN_LABELS = CLOTHING_LABELS | BODY_LABELS | HEAD_LABELS
    mask_human = np.isin(parsing, list(HUMAN_LABELS)).astype(np.uint8)
    mask_human_buffer = cv2.dilate(mask_human, np.ones((25, 25), np.uint8), iterations=1)

    # ================== STEP 5: COMBINE & CLIP ==================
    mask_combined = (expanded_clothes | mask_body_near_clothes).astype(np.uint8)
    mask = mask_combined * mask_human_buffer

    # ================== STEP 6: PROTECT HEAD ==================
    head_mask = np.isin(parsing, list(HEAD_LABELS))
    mask[head_mask] = 0

    # ================== STEP 6.5: REMOVE HAIR OVER CHEST ==================
    mask_hair = np.isin(parsing, [HAIR]).astype(np.uint8)
    mask_torso = np.isin(parsing, list(BODY_LABELS)).astype(np.uint8)
    torso_expand = cv2.dilate(mask_torso, np.ones((35, 35), np.uint8), iterations=1)
    hair_on_body = mask_hair & torso_expand
    face_mask = np.isin(parsing, [FACE]).astype(np.uint8)
    face_buffer = cv2.dilate(face_mask, np.ones((45, 45), np.uint8), iterations=1)
    hair_on_body[face_buffer == 1] = 0
    mask = mask | hair_on_body

    # ================== STEP 7: SOFT EDGES ==================
    mask = (mask * 255).astype(np.uint8)
    mask = cv2.GaussianBlur(mask, (21, 21), 0)
    mask = cv2.dilate(mask, np.ones((7, 7), np.uint8), iterations=1)
    mask = cv2.GaussianBlur(mask, (25, 25), 0)
    mask = np.clip(mask * 1.3, 0, 255).astype(np.uint8)

    # ================== SAVE ==================
    Image.fromarray(mask, mode="L").save(output_mask_path)
