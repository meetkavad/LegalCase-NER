# extractor.py
import fitz  # PyMuPDF
from PIL import Image
import io
import pytesseract
import spacy
from typing import List
from tqdm import tqdm

# allowed entity labels for your project
ALLOWED_ENTS = [
    "PERSON", "ORG", "DATE", "GPE", "LAW", "NORP",
    "MONEY", "ORDINAL", "CARDINAL", "LOC"
]

def load_nlp(model_name="en_core_web_md"):
    # load spaCy model once
    nlp = spacy.load(model_name, disable=["parser", "textcat"])
    # keep ner enabled
    return nlp

def extract_text_from_pdf(pdf_path: str, ocr_if_empty=True) -> str:
    """
    Extract text from PDF using PyMuPDF. If a page yields no text and ocr_if_empty True,
    fallback to OCR (pytesseract) on that page's rasterized image.
    """
    doc = fitz.open(pdf_path)
    all_text = []
    for page in doc:
        ptext = page.get_text().strip()
        if ptext:
            all_text.append(ptext)
        else:
            if ocr_if_empty:
                # generate image of page
                pix = page.get_pixmap(dpi=200)  # 200 DPI for OCR balance
                img = Image.open(io.BytesIO(pix.tobytes()))
                try:
                    ocr_text = pytesseract.image_to_string(img)
                except Exception:
                    ocr_text = ""
                all_text.append(ocr_text)
    return "\n".join([t for t in all_text if t])

def extract_entities(text: str, nlp) -> List[str]:
    """
    Run spaCy NER and return deduplicated, normalized entities (lowercased).
    """
    doc = nlp(text)
    ents = []
    for ent in doc.ents:
        if ent.label_ in ALLOWED_ENTS:
            e = ent.text.strip().lower()
            if e:
                ents.append(e)
    # deduplicate preserving order
    seen = set()
    uniq = []
    for e in ents:
        if e not in seen:
            seen.add(e)
            uniq.append(e)
    return uniq
