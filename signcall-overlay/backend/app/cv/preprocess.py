import base64
import numpy as np
import cv2

def b64jpeg_to_bgr(image_jpeg_b64: str):
    if not image_jpeg_b64:
        return None
    raw = base64.b64decode(image_jpeg_b64)
    arr = np.frombuffer(raw, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img
