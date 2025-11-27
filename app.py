import streamlit as st
import os
from recommendation import recommend_cases, get_input_entities

st.set_page_config(page_title="Legal Case Recommendation System", layout="wide")

st.title("📘 Legal Case Recommendation System (NER-based)")

st.write(
    "Upload a legal case PDF and get recommendations based on Named Entity matching "
    "with historical cases stored in the database."
)

uploaded_file = st.file_uploader("📤 Upload a Legal Case PDF", type=["pdf"])

if uploaded_file is not None:
    # Save file temporarily
    temp_path = "uploaded_case.pdf"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    st.info("Extracting entities from the uploaded case...")
    input_entities = get_input_entities(temp_path)

    st.subheader("🔍 Extracted Entities")
    st.write(input_entities)

    st.info("Generating recommendations...")

    results = recommend_cases(temp_path, top_k=10)

    if len(results) == 0:
        st.warning("No similar cases found.")
    else:
        st.subheader("📑 Top Recommended Cases")

        for r in results:
            file_path = r["file_path"]

            try:
                with open(file_path, "rb") as f:
                    pdf_data = f.read()
            except Exception as e:
                st.error(f"Error reading PDF file: {file_path}")
                continue

            st.markdown(
                f"""
                <div style="
                    padding: 12px;
                    border-radius: 8px;
                    border: 1px solid #ccc;
                    margin-bottom: 10px;
                ">
                    <h4>{r['case_name']} ({r['year']})</h4>
                    <b>Similarity Score:</b> {r['score']}<br>
                    <b>Matched Entities:</b> {', '.join(r['entities_matched'])}<br><br>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.download_button(
                label="📄 Download PDF",
                data=pdf_data,
                file_name=os.path.basename(file_path),
                mime="application/pdf"
            )

            st.write("---")

    if os.path.exists(temp_path):
        os.remove(temp_path)
