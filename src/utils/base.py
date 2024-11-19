import cv2
import pytesseract
import numpy as np
from PIL import Image
import io
from fastapi import HTTPException


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """Chuyển đổi byte ảnh thành ảnh dạng mảng NumPy đã xử lý (gray scale và thresholding)."""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image format or error processing image.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def extract_word_images(binary: np.ndarray) -> list:
    """Trích xuất các vùng chứa chữ trong ảnh và trả về các cặp (word_image, bounding_box)."""
    custom_config = r'--oem 3 --psm 6'
    results = pytesseract.image_to_data(binary, output_type=pytesseract.Output.DICT, config=custom_config, lang='eng')
    word_images = []

    for i in range(len(results['text'])):
        if int(results['conf'][i]) > 30:
            x, y, w, h = (results['left'][i], results['top'][i], results['width'][i], results['height'][i])
            word_image = binary[y-5:y+h+5, x-5:x+w+5]
            word_images.append((word_image, (x, y, w, h)))

    return word_images