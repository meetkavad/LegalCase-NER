# 📘 Legal Case Recommendation System (NER-Based)

This project implements a **Named Entity Recognition (NER) powered Legal Case Recommendation System**.  
The system analyzes legal case PDFs, extracts key entities (PERSON, ORG, GPE, DATE, LAW, etc.), stores them in a SQLite database, and recommends similar cases based on entity overlap.

It provides:

- ✔ **Offline PDF indexing pipeline** (one-time preprocessing)  
- ✔ **NER-based entity extraction using spaCy**  
- ✔ **Persistent storage in SQLite database**  
- ✔ **Streamlit UI** for uploading a case and getting recommendations  
- ✔ **Fast, interpretable similarity scores based on entity overlap**  

---

## ⚙️ How It Works (Two-Step Pipeline)

### **1️⃣ Indexing Phase (One-time processing)**
- The system scans all judgment PDFs (year 2020–2025 as of now).  
- Extracts text → applies spaCy NER → stores extracted entities + metadata in **SQLite**.  
- This step only needs to be done once. The included `legal_cases.db` already contains processed data.

### **2️⃣ Recommendation Phase (User Application)**
- User uploads a new case PDF through the **Streamlit interface**.  
- Entities from the uploaded case are extracted and matched against the database.  
- A similarity score is computed based on entity overlap → **Top-K relevant cases are recommended**.

---

## 🌟 Features

### **1. PDF Text Extraction**
- Uses **PyMuPDF** for text extraction  
- Falls back to **pytesseract OCR** for scanned pages  

### **2. Named Entity Recognition (spaCy)**
Extracts the following legal-relevant entities:

`PERSON, ORG, GPE, DATE, LAW, MONEY, LOC, NORP, ORDINAL, CARDINAL`

### **3. SQLite Database (Included)**
The repository includes a pre-processed SQLite file for 2020-2025 cases.
```
legal_cases.db
```

This means users can directly run recommendations **without re-indexing thousands of PDFs**.

### **4. Streamlit App (Frontend UI)**
Upload any legal case PDF to:

- Extract entities  
- Compute similarity  
- Get **Top-K recommended cases**  

---

# 🚀 Getting Started

## **1. Clone the repository**

```bash
git clone https://github.com/meetkavad/LegalCase-NER
cd LegalCase-NER
```

---

## **2. Create a virtual environment**

```bash
python -m venv env
```

Activate it:

**Windows**
```bash
env\Scripts\activate
```

**Linux / Mac**
```bash
source env/bin/activate
```

---

## **3. Install dependencies**

```bash
pip install -r requirements.txt
```

This will automatically install:

- spaCy  
- PyMuPDF  
- Tesseract bindings  
- Streamlit  
- tqdm  
- And the spaCy model `en_core_web_md` (downloaded automatically!)  

---

## **4. Run the Streamlit UI**

```bash
streamlit run app.py
```

The app will start at:

```
http://localhost:8501
```

Upload a PDF → get recommendations instantly.

---

# 🧩 Project Structure

```
📂 NLP PROJECT
│── app.py                 # Streamlit UI
│── extractor.py           # PDF + OCR + NER extraction
│── index_cases.py         # Offline indexing script
│── recommendation.py      # Similarity + recommendation logic
│── db.py                  # SQLite helper functions
│── legal_cases.db         # Pre-indexed cases (small DB)
│── requirements.txt
│── README.md
│── env/                   # (ignored) virtual environment
│── __pycache__/           # (ignored)
```

---

# 🔎 Recommendation Logic

Similarity is based on **entity overlap**:

\[
score = |E_{input} ∩ E_{case}|
\]

Cases are ranked by descending score.  
This makes the system fast, interpretable, and domain-relevant.

# 👍 Acknowledgements
spaCy, PyMuPDF, Streamlit, Tesseract OCR.