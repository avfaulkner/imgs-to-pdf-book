import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

# This code converts all PNG images in a specified folder into a one-sided PDF book.
# Each image is resized to fit the page, and a blank page is added after each image.
# The temporary resized image is deleted after each page is created.
# Make sure to install the required libraries:
# pip install Pillow reportlab
# Note: This code assumes that the images are in PNG format. Adjust the file extension check if needed.
# The code uses the Pillow library to handle image processing and the ReportLab library to create the PDF.

def images_to_one_sided_pdf(folder_path, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    page_width, page_height = letter

    #Since letter size is 8.5 inches × 11 inches (612 × 792 points in ReportLab), 
    # and ReportLab works in points (1 inch = 72 points), a standard margin of 0.375 inches equals 27 points (0.375 * 72 = 27 points).
    # Define margins
    # 0.375 inches margin on each side
    # Convert inches to points (1 inch = 72 points)
    # Standard letter size in points
    # Letter size: 8.5 inches × 11 inches
    margin = 0.375 * 72  # 0.375 inches → points → 27 points

    usable_width = page_width - 2 * margin
    usable_height = page_height - 2 * margin

    # Get all PNG files in the folder, sorted alphabetically
    image_files = sorted(
        [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]
    )

    for img_file in image_files:
        img_path = os.path.join(folder_path, img_file)

        # Open and convert image
        image = Image.open(img_path).convert("RGB")

        # Resize image to fit usable area
        image.thumbnail((usable_width, usable_height), Image.Resampling.LANCZOS)

        # Get actual size of resized image
        img_width, img_height = image.size

        # Center image within margins
        x_offset = margin + (usable_width - img_width) / 2
        y_offset = margin + (usable_height - img_height) / 2

        # Convert image to a ReportLab-readable object
        img_reader = ImageReader(image)

        # Draw the image on the page
        c.drawImage(img_reader, x_offset, y_offset, width=img_width, height=img_height)

        c.showPage()

        # Add blank page
        c.showPage()

    c.save()
    print(f"PDF created: {output_pdf}")

# Example usage
images_to_one_sided_pdf("/mnt/c/Users/avfau/Pictures/zillow", "/mnt/c/Users/avfau/Pictures/zillow/output_book.pdf")
