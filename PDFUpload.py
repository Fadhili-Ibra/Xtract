import streamlit as st
import fitz  # PyMuPDF
import re
import io
from PIL import Image
import numpy as np
import scipy.stats as stats

def extract_data_from_pdf(uploaded_pdf):
    doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    pages_text = {}

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()
        pages_text[page_num] = text

    return pages_text

def extract_invoice_data(text):
    invoice_data = {
        "Invoice": None,
        "Invoice Date": None,
        "Due Date": None,
        "Service Period": None,
        "Customer ID": None,
        "Subtotal": None,
        "Sales Tax": None,
        "Total": None,
        "Previous Unpaid Balance": None,
        "Amount Due": None
    }

    patterns = {
        "Invoice": r"INVOICE:\s*(\S+)",
        "Invoice Date": r"INVOICE DATE:\s*(\S+)",
        "Due Date": r"DUE DATE:\s*(\S+)",
        "Service Period": r"SERVICE PERIOD:\s*(.+)",
        "Customer ID": r"CUSTOMER ID:\s*(\S+)",
        "Subtotal": r"SUBTOTAL\s*\$?(\d+(\.\d+)?)",
        "Sales Tax": r"SALES TAX\s*\$?(\d+(\.\d+)?)",
        "Total": r"TOTAL\s*\$?(\d+(\.\d+)?)",
        "Previous Unpaid Balance": r"PREVIOUS UNPAID BALANCE\s*\$?(\d+(\.\d+)?)",
        "Amount Due": r"AMOUNT DUE\s*\$?(\d+(\.\d+)?)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            invoice_data[key] = match.group(1)

    # Convert financial values to float
    for key in ["Subtotal", "Sales Tax", "Total", "Previous Unpaid Balance", "Amount Due"]:
        if invoice_data[key] is not None:
            invoice_data[key] = float(invoice_data[key].replace(',', ''))

    return invoice_data

def calculate_confidence_interval(data, confidence=0.95):
    if len(data) < 2:  # At least 2 data points needed
        return None, None

    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)  # Sample standard deviation
    n = len(data)
    z_score = stats.norm.ppf((1 + confidence) / 2)

    margin_of_error = z_score * (std_dev / np.sqrt(n))
    return mean - margin_of_error, mean + margin_of_error

def show_pdf_page():
    st.subheader("Extract Data from PDFs")

    uploaded_pdf = st.file_uploader("Upload PDF", type=['pdf'])

    if uploaded_pdf is not None:
        pdf_content = uploaded_pdf.read()
        pages_text = extract_data_from_pdf(io.BytesIO(pdf_content))

        pdf_image = fitz.open(stream=pdf_content, filetype="pdf")
        page_images = []
        for page in pdf_image:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            page_images.append(img)

        invoices = []

        for page_num, text in pages_text.items():

            invoice_data = extract_invoice_data(text)
            invoices.append(invoice_data)

            if invoice_data["Invoice"] is not None:
                st.write("### Extracted Invoice Data")

                col1, col2 = st.columns(2)

                with col1:
                    st.image(page_images[page_num], caption=f"PDF Page {page_num + 1}", use_column_width=True)

                with col2:
                    with st.form(key=f"invoice_form_{page_num}", clear_on_submit=True):
                        st.write("Edit Invoice Data:")

                        for key, value in invoice_data.items():
                            st.text_input(key, value, key=f"{key}_{page_num}")

                        submit_button = st.form_submit_button("Submit Invoice Data")

                        if submit_button:
                            st.success(f"Invoice data for Page {page_num + 1} submitted successfully!")

                            # Collect financial values for CI calculation
                            financial_data = [invoice_data["Subtotal"], 
                                              invoice_data["Sales Tax"], 
                                              invoice_data["Total"], 
                                              invoice_data["Previous Unpaid Balance"], 
                                              invoice_data["Amount Due"]]

                            # Filter out None values and calculate CI
                            filtered_data = [value for value in financial_data if value is not None]
                            ci_low, ci_high = calculate_confidence_interval(filtered_data)

                            st.write(f"**Confidence Interval (95%):** {ci_low:.2f} to {ci_high:.2f}")

def main():
    show_pdf_page()

if __name__ == "__main__":
    main()
