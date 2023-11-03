from PIL import Image
import pytesseract
import os
os.environ['TESSDATA_PREFIX'] = 'C:\\Program Files\\Tesseract-OCR\\tessdata'

def ocr(photo):
    image = Image.open(photo)
    return pytesseract.image_to_string(image)