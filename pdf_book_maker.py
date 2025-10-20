import os, io
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfMerger, PdfReader

# This module provides functions to create a PDF book from PNG images in a specified folder.
# Each image is resized to fit the page, and a blank page is added after each image.
# The temporary resized image is deleted after each page is created.
# Note: This code assumes that the images are in PNG format. Adjust the file extension check if needed.
# The code uses the Pillow library to handle image processing and the ReportLab library to create the PDF.
# Since letter size is 8.5 inches × 11 inches (612 × 792 points in ReportLab), 
# and ReportLab works in points (1 inch = 72 points), a standard margin of 0.375 inches equals 27 points (0.375 * 72 = 27 points).
# Define margins
# 0.375 inches margin on each side
# Convert inches to points (1 inch = 72 points)
# Standard letter size in points

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

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    img_reader = ImageReader(image)
    c.drawImage(img_reader, x_offset, y_offset, width=img_width, height=img_height)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


def make_pdf_book(intro_pdf_path, image_folder, output_pdf_path):
    merger = PdfMerger()

    if os.path.exists(intro_pdf_path):
        intro_pdf = PdfReader(intro_pdf_path)
        merger.append(intro_pdf, pages=(0, 1))
        merger.append(PdfReader(blank_page_pdf()))

    for f in sorted([f for f in os.listdir(image_folder) if f.lower().endswith(".png")]):
        pdf_buf = image_to_pdf_page(os.path.join(image_folder, f))
        merger.append(PdfReader(pdf_buf))
        merger.append(PdfReader(blank_page_pdf()))

    merger.write(output_pdf_path)
    merger.close()
    return output_pdf_path
