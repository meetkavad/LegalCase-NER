# index_cases.py
import os
import argparse
from extractor import load_nlp, extract_text_from_pdf, extract_entities
from db import init_db, store_case, case_exists

def iter_pdf_files(root_dir):
    for dirpath, _, files in os.walk(root_dir):
        for f in files:
            if f.lower().endswith(".pdf"):
                yield os.path.join(dirpath, f)

def infer_year_from_path(path):
    # try to extract a 4-digit year from path (1950-2025) 
    import re
    m = re.search(r"(19\d{2}|20[0-2]\d|2025)", path)
    if m:
        return int(m.group(0))
    else:
        return None

def main(dataset_root, model_name="en_core_web_md", ocr_if_empty=True, min_year=1950, max_year=2025):
    init_db()
    print(f"Loading spaCy model: {model_name} (this may take a while)...")
    nlp = load_nlp(model_name=model_name)
    print("Model loaded.")

    all_files = list(iter_pdf_files(dataset_root))

    # Filter by year BEFORE processing
    filtered_files = []
    for fp in all_files:
        year = infer_year_from_path(fp)
        if year is not None and (min_year <= year <= max_year):
            filtered_files.append(fp)

    print(f"Found {len(filtered_files)} PDF files between years {min_year}-{max_year}.")

    from tqdm import tqdm
    for file_path in tqdm(filtered_files):
        case_name = os.path.basename(file_path)
        if case_exists(case_name):
            # skip if already inserted (safe resume)
            continue

        year = infer_year_from_path(file_path) or None

        try:
            text = extract_text_from_pdf(file_path, ocr_if_empty=ocr_if_empty)
            if not text or len(text.strip()) < 30:
                # skip tiny / empty
                print(f"Warning: extracted too little text for {case_name}, skipping.")
                continue

            entities = extract_entities(text, nlp)
            store_case(case_name=case_name, year=year or 0, file_path=file_path, entities=entities)
        except Exception as e:
            print(f"Error processing {case_name}: {e}")

    print("Indexing completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Index legal PDF corpus into SQLite DB.")
    parser.add_argument("--dataset-root", required=True, help="Path to folder containing PDFs (can have year subfolders).")
    parser.add_argument("--model", default="en_core_web_md", help="spaCy model to use (en_core_web_md or en_core_web_lg)")
    parser.add_argument("--no-ocr", action="store_true", help="Disable OCR fallback for blank pages.")
    parser.add_argument("--min-year", type=int, default=1950, help="Minimum year to process")
    parser.add_argument("--max-year", type=int, default=2025, help="Maximum year to process")

    args = parser.parse_args()

    main(args.dataset_root,
     model_name=args.model,
     ocr_if_empty=(not args.no_ocr),
     min_year=args.min_year,
     max_year=args.max_year)
