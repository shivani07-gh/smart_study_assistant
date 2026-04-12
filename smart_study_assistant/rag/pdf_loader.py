from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_pdf(file_path):
    text = ""

    # 🔹 try normal extraction first
    reader = PdfReader(file_path)
    for page in reader.pages:
        text += page.extract_text() or ""

    # 🔹 agar empty hai → OCR use kar
    if not text.strip():
        images = convert_from_path(file_path)
        for img in images:
            text += pytesseract.image_to_string(img)

    return text