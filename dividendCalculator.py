import os
import pdfplumber
import re
import pandas as pd


def extract_dividend_and_company(file_path):
    with pdfplumber.open(file_path) as pdf:
        page = pdf.pages[0]     # dividend amount is always on first page in this case

        # Define the bounding box for the region with the dividend amount in the pdf
        bbox_dividend = (420, 540, 550, 590)  # (x0, top, x1, bottom)
        bbox_company = (180, 360, 350, 395)

        # Extract text within the bounding box
        dividend_text = page.within_bbox(bbox_dividend).extract_text()
        company_text = page.within_bbox(bbox_company).extract_text()
        if not company_text:
            company_text = "Unknown"
        if dividend_text and company_text:
            try:
                dividend = float(dividend_text.replace(',', '.'))
            except ValueError:
                print("Float conversion failed")
                return None

            return company_text, dividend
        return None


def process_pdfs_to_dataframe(directory):
    total_dividend = 0.0
    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf") and "Wertpapierereignis" in filename:
            file_path = os.path.join(directory, filename)
            response = extract_dividend_and_company(file_path)

            company = response[0]
            dividend = response[1]
            total_dividend += dividend

            results.append({"Company": company, "Dividend (EUR)": dividend})

    df = pd.DataFrame(results)

    return df, total_dividend


pdf_directory = "../pdfs"
temp = process_pdfs_to_dataframe(pdf_directory)

print(temp[0])
print("\n", "Total amount", temp[1])
