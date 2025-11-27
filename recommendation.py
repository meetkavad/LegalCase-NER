# recommendation.py
import json
from extractor import extract_text_from_pdf, extract_entities, load_nlp
from db import fetch_all_cases
from typing import List, Dict

# Load spaCy NER model once
nlp = load_nlp("en_core_web_md")

def get_input_entities(pdf_path: str) -> List[str]:
    """Extract text+entities from the uploaded PDF."""
    text = extract_text_from_pdf(pdf_path, ocr_if_empty=True)
    entities = extract_entities(text, nlp)
    return entities

def compute_similarity(input_entities: List[str], case_entities: List[str]) -> int:
    """Calculate simple entity overlap score."""
    set_input = set(input_entities)
    set_case = set(case_entities)
    return len(set_input.intersection(set_case))

def recommend_cases(input_pdf: str, top_k: int = 10) -> List[Dict]:
    """
    Extract entities from uploaded case, compare with all DB cases,
    and return top K matches sorted by overlap score.
    """
    input_entities = get_input_entities(input_pdf)

    all_cases = fetch_all_cases()
    recommendations = []

    for case in all_cases:
        score = compute_similarity(input_entities, case["entities"])
        if score > 0:
            recommendations.append({
                "case_name": case["case_name"],
                "year": case["year"],
                "score": score,
                "entities_matched": list(
                    set(input_entities).intersection(set(case["entities"]))
                ),
                "file_path": case["file_path"]
            })

    recommendations.sort(key=lambda x: x["score"], reverse=True)

    return recommendations[:top_k]
