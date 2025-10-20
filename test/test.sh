# !/bin/bash
# Test script to create a PDF book from images and an intro PDF

curl -X POST https://imgs-to-pdf-book.onrender.com/api/create-pdf-book \
  -F "intro_pdf=@intro.pdf" \
  -F "images=@page1.png" \
  -F "images=@page2.png" \
  -o book.pdf
echo "PDF book created: book.pdf"