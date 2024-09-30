# ImageUpload.py

import streamlit as st
from PIL import Image
import pytesseract
import re
import fitz  # PyMuPDF for PDF handling
import io

def main():
    show_images_page()

def extract_id_data(text):
    # Define regex patterns for the desired fields
    id_data = {
        "Serial Number": None,
        "ID Number": None,
        "Full Names": None,
        "Date of Birth": None,
        "District of Birth": None
    }

    patterns = {
        "Serial Number": r"Serial Number[:\s]*([A-Za-z0-9\-]+)",
        "ID Number": r"ID Number[:\s]*([A-Za-z0-9\-]+)",
        "Full Names": r"Full Names[:\s]*([A-Za-z\s]+)",
        "Date of Birth": r"Date of Birth[:\s]*([\d]{2}/[\d]{2}/[\d]{4}|\d{2}-\d{2}-\d{4})",
        "District of Birth": r"District of Birth[:\s]*([A-Za-z\s]+)"
    }

    # Extract values using regex
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            id_data[key] = match.group(1)

    return id_data

def show_images_page():
    st.subheader("Extract Data from ID Documents (Image or PDF)")

    # Allow the user to upload either an image or a PDF
    uploaded_file = st.file_uploader("Upload Image or PDF", type=['png', 'jpeg', 'jpg', 'pdf'])

    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            # Handle PDF file
            pdf_content = uploaded_file.read()
            pdf_doc = fitz.open(stream=io.BytesIO(pdf_content), filetype="pdf")
            
            extracted_text = ""
            for page_num in range(pdf_doc.page_count):
                page = pdf_doc.load_page(page_num)
                extracted_text += page.get_text()
            
            st.subheader("Extracted Text from PDF")
            st.text_area("Extracted Data", extracted_text, height=300)

        else:
            # Handle image file
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Extract text using Tesseract
            extracted_text = pytesseract.image_to_string(image)

            # Display the extracted text
            st.subheader("Extracted Text from Image")
            st.text_area("Extracted Data", extracted_text, height=300)

        # Extract ID data using regex patterns from the extracted text
        id_data = extract_id_data(extracted_text)

        # Create a form-like structure for editing the ID data
        if any(id_data.values()):  # Check if any data is extracted
            st.write("### Extracted ID Data")

            # Set up a form for editing the extracted data
            with st.form(key="id_form", clear_on_submit=True):
                st.write("Edit the extracted data:")

                # Create a text input for each field
                corrected_data = {}
                for key, value in id_data.items():
                    corrected_data[key] = st.text_input(key, value if value else "")

                # Add a submit button inside the form
                submit_button = st.form_submit_button("Submit Corrected Data")

                if submit_button:
                    # Display the validated data
                    st.success("Data submitted successfully!")
                    st.write(corrected_data)

if __name__ == "__main__":
    main()
