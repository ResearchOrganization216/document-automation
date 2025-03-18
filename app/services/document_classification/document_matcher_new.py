import cv2
import os
from flask import current_app

def load_templates():
    """
    Loads all templates for each class from their respective subfolders.
    """
    TEMPLATES_FOLDER = os.path.join(current_app.root_path, 'templates')
    templates = {}

    for class_name in os.listdir(TEMPLATES_FOLDER):
        class_path = os.path.join(TEMPLATES_FOLDER, class_name)
        if os.path.isdir(class_path):
            templates[class_name] = []
            for template_file in os.listdir(class_path):
                template_path = os.path.join(class_path, template_file)
                template_image = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
                if template_image is not None:
                    templates[class_name].append(template_image)

    return templates

def feature_based_matching(document_path, templates, match_threshold=50, min_good_matches=30, good_matches_ratio_threshold=0.01): # good_matches_ratio_threshold=0.1 is the initial value
    """
    Matches a document against multiple templates for each class using ORB with enhanced validation.
    """
    document_image = cv2.imread(document_path, cv2.IMREAD_GRAYSCALE)
    if document_image is None:
        raise FileNotFoundError(f"Document image not found at {document_path}")

    # Initialize ORB detector
    orb = cv2.ORB_create()

    # Detect and compute features for the document
    kp_doc, des_doc = orb.detectAndCompute(document_image, None)
    if des_doc is None or len(kp_doc) == 0:
        return {"error": "No features detected in the document"}

    best_match_type = None
    max_good_matches = 0
    max_good_match_ratio = 0  # Store the highest good match ratio

    # BFMatcher with Hamming distance
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

    for class_name, class_templates in templates.items():
        class_match_count = 0
        class_good_match_ratios = []

        for template_image in class_templates:
            kp_template, des_template = orb.detectAndCompute(template_image, None)
            if des_template is None or len(kp_template) == 0:
                continue

            # Match descriptors and apply ratio test
            matches = bf.knnMatch(des_template, des_doc, k=2)
            good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]

            # Calculate good matches ratio
            good_matches_ratio = len(good_matches) / min(len(kp_doc), len(kp_template))
            class_good_match_ratios.append(good_matches_ratio)

            if len(good_matches) >= min_good_matches and good_matches_ratio > good_matches_ratio_threshold:
                class_match_count += len(good_matches)

        # Update the best match if this class has the highest aggregated count
        if class_match_count > max_good_matches:
            max_good_matches = class_match_count
            max_good_match_ratio = max(class_good_match_ratios)
            best_match_type = class_name

    # Final check: Ensure the best match exceeds thresholds
    if max_good_matches < min_good_matches or max_good_match_ratio < good_matches_ratio_threshold:
        return {"document_type": "No Matching Document", "match_count": max_good_matches}

    return {"document_type": best_match_type, "match_count": max_good_matches}
