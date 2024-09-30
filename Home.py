# Home.py
import streamlit as st

def main():
    st.title("Welcome to Xtract")
    
    st.subheader("Overview")
    st.write(
        "Xtract allows you to upload images, scan documents, and handle PDFs for text extraction. "
        "This guide will help you navigate through the app and utilize its features effectively."
    )

    st.subheader("Features")
    st.write(
        "- **Image Upload:** Upload raw or scanned images to extract text using Optical Character Recognition (OCR)."
        "\n- **Document Scan:** Similar functionality as images, suitable for scanned documents."
        "\n- **PDF Upload:** Upload PDF files to extract text from each page, providing the ability to edit and validate the extracted content."
    )

    st.subheader("How to Use Xtract")
    
    st.markdown("""
    1. **Upload Images:**
        - Go to the **Image Upload** section.
        - Click on **Upload Image** and select a file from your device.
        - The uploaded image will be displayed along with the extracted text. You can edit the extracted text as needed.

    2. **Scan Documents:**
        - Navigate to the **Document Upload** section.
        - Upload your scanned document (ensure it's in an image format).
        - Review the extracted text and make any corrections.

    3. **Handle PDFs:**
        - Go to the **PDF Upload** section.
        - Upload your PDF file.
        - Each page will be displayed with its extracted text. You can validate and submit the corrected text.

    4. **Submission:**
        - After validating the extracted text in any section, click the **Submit** button to save your corrections.
    """)

    st.subheader("Tips for Best Results")
    st.write(
        "- Ensure the uploaded images or scanned documents are clear and high-resolution for better text extraction."
        "\n- Review the extracted text thoroughly, as OCR may not be 100% accurate."
        "\n- If you encounter issues, feel free to reach out for support."
    )

    st.subheader("Need Help?")
    st.write(
        "If you have any questions or need assistance, please contact our support team at ibrahimfadhili46@gmail.com."
    )

if __name__ == "__main__":
    main()
