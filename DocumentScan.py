# DocumentUpload.py

import streamlit as st
from PIL import Image
import pytesseract

def show_documents_page():
    st.subheader("Extract Text from Docs")

    # Upload image
    uploaded_doc = st.file_uploader("Upload Scanned Document (as image)", type=['png', 'jpeg', 'jpg'])

    if uploaded_doc is not None:
        document = Image.open(uploaded_doc)
        st.image(document, caption="Uploaded Scanned Document", use_column_width=True)

        # Extract text using Tesseract
        extracted_text = pytesseract.image_to_string(document)

        # Display extracted text
        st.subheader("Extracted Text")
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
