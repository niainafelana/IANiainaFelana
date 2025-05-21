from langdetect import detect
import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text.strip()

def detect_language(text):
    try:
        return detect(text)  # 'en', 'fr', etc.
    except:
        return 'unknown'
