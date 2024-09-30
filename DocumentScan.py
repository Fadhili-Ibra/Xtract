# DocumentUpload.py

import streamlit as st
from PIL import Image
import pytesseract
import fitz  # PyMuPDF for handling PDF files
import io

def show_documents_page():
    st.subheader("Extract Text from Scanned Documents (Image or PDF)")

    # Upload image or PDF
    uploaded_doc = st.file_uploader("Upload Scanned Document (Image or PDF)", type=['png', 'jpeg', 'jpg', 'pdf'])

    if uploaded_doc is not None:
        if uploaded_doc.type == "application/pdf":
            # Process PDF document
            pdf_content = uploaded_doc.read()
            pdf_doc = fitz.open(stream=io.BytesIO(pdf_content), filetype="pdf")

            extracted_text = ""
            for page_num in range(pdf_doc.page_count):
                page = pdf_doc.load_page(page_num)
                extracted_text += page.get_text()

            st.subheader("Extracted Text from PDF")
            st.text_area("Extracted Data", extracted_text, height=300)

        else:
            # Process image document
            document = Image.open(uploaded_doc)
            st.image(document, caption="Uploaded Scanned Document", use_column_width=True)

            # Extract text using Tesseract
            extracted_text = pytesseract.image_to_string(document)

            # Display extracted text
            st.subheader("Extracted Text from Image")
            st.text_area("Extracted Data", extracted_text, height=300)

        # Provide editing capability
        validated_text = st.text_area("Corrected Data", extracted_text, height=300)

        if st.button("Submit"):
            # Save the validated text to your database
            st.success("Data submitted successfully!")

def main():
    show_documents_page()

if __name__ == "__main__":
    main()
