import cv2

def preprocess_image(image):
    """
    Apply preprocessing steps like noise reduction and normalization.
    """
    image = cv2.GaussianBlur(image, (5, 5), 0)
    image = cv2.equalizeHist(image)
    return image