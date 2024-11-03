import os
import pdfplumber
import re
import pandas as pd

def extract_dividend_by_position(file_path):
    with pdfplumber.open(file_path) as pdf:
        page = pdf.pages[0]     # dividend amount is always on first page
        # Define the bounding box for the region with the dividend amount
        # Adjust these coordinates based on your PDF layout
        bbox = (420, 540, 550, 590)  # (x0, top, x1, bottom)

        # Extract text within the bounding box
        dividend_text = page.within_bbox(bbox).extract_text()
        if dividend_text:
            dividend = float(dividend_text.replace(',', '.'))
            return dividend
        return None


def calculate_total_dividends(directory):
    total_dividends = 0
    for filename in os.listdir(directory):
        if filename.endswith(".pdf") and "Wertpapierereignis" in filename:
            file_path = os.path.join(directory, filename)
            dividend = extract_dividend_by_position(file_path)
            if dividend:
                total_dividends += dividend

    return total_dividends


pdf_directory = "./pdfs"
total = calculate_total_dividends(pdf_directory)

print(f"Total Dividends: {total} EUR")