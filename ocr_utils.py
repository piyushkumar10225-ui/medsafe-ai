import pytesseract
from PIL import Image
import os
from utils import setup_logger

logger = setup_logger(__name__)

def extract_text_from_image(image: Image.Image) -> str:
    """
    Extracts raw text from an uploaded PIL Image object using Tesseract OCR.
    """
    try:
        # Perform OCR on the image
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        logger.error(f"OCR extraction failed: {e}")
        return ""
