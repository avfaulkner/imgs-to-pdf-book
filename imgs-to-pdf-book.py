import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfMerger, PdfReader
import io
import sys

# This code converts all PNG images in a specified folder into a one-sided PDF book.
# Each image is resized to fit the page, and a blank page is added after each image.
# The temporary resized image is deleted after each page is created.
# Make sure to install the required libraries:
# pip install Pillow reportlab
# Note: This code assumes that the images are in PNG format. Adjust the file extension check if needed.
# The code uses the Pillow library to handle image processing and the ReportLab library to create the PDF.
#Since letter size is 8.5 inches × 11 inches (612 × 792 points in ReportLab), 
# and ReportLab works in points (1 inch = 72 points), a standard margin of 0.375 inches equals 27 points (0.375 * 72 = 27 points).
# Define margins
# 0.375 inches margin on each side
# Convert inches to points (1 inch = 72 points)
# Standard letter size in points
# Letter size: 8.5 inches × 11 inches

def blank_page_pdf():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def image_to_pdf_page(image_path, margin=0.375 * 72):
    page_width, page_height = letter
    usable_width = page_width - 2 * margin
    usable_height = page_height - 2 * margin

    image = Image.open(image_path).convert("RGB")
    image.thumbnail((usable_width, usable_height), Image.Resampling.LANCZOS)
    img_width, img_height = image.size

    x_offset = margin + (usable_width - img_width) / 2
    y_offset = margin + (usable_height - img_height) / 2

    # Create an in-memory PDF with ReportLab
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    img_reader = ImageReader(image)
    c.drawImage(img_reader, x_offset, y_offset, width=img_width, height=img_height)

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer

def create_output_book(intro_pdf_path, image_folder, output_pdf_path):
    merger = PdfMerger()

    # Optional introPage.pdf
    if os.path.exists(intro_pdf_path):
        print(f"Adding intro page from {intro_pdf_path}")
        intro_pdf = PdfReader(intro_pdf_path)
        merger.append(intro_pdf, pages=(0, 1))

        # Force a blank page after intro
        blank_pdf_buffer = blank_page_pdf()
        merger.append(PdfReader(blank_pdf_buffer))
    else:
        print("introPage.pdf not found — skipping intro page.")

    # Add image pages with blank pages after each
    image_files = sorted(
        [f for f in os.listdir(image_folder) if f.lower().endswith('.png')]
    )

    for img_file in image_files:
        img_path = os.path.join(image_folder, img_file)

        print(f"Adding image: {img_file}")

        # Convert image to a single-page PDF in memory
        pdf_buffer = image_to_pdf_page(img_path)
        merger.append(PdfReader(pdf_buffer))

        # Add blank page after image
        blank_pdf_buffer = blank_page_pdf()
        merger.append(PdfReader(blank_pdf_buffer))

    # Write the final single output PDF
    merger.write(output_pdf_path)
    merger.close()

    print(f"Final book PDF saved as {output_pdf_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python imgs-to-pdf-book.py <path to introPage.pdf> <image directory path> <path for final output PDF>")
        sys.exit(1)
    print(len(sys.argv), sys.argv)
    intro_pdf_path =  sys.argv[1] 
    image_folder = sys.argv[2] 
    output_pdf_path = sys.argv[3]

create_output_book(intro_pdf_path, image_folder, output_pdf_path)