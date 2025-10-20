from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import Response
import tempfile, os
from pdf_book_maker import make_pdf_book


app = FastAPI(title="Book PDF Maker")

@app.post("/api/create-pdf-book")
async def create_pdf_book(intro_pdf: UploadFile = File(...), images: list[UploadFile] = File(...)):
    with tempfile.TemporaryDirectory() as tempdir:
        intro_path = os.path.join(tempdir, "intro.pdf")
        image_dir = os.path.join(tempdir, "images")
        os.makedirs(image_dir)

        # Save uploaded intro PDF
        with open(intro_path, "wb") as f:
            f.write(await intro_pdf.read())

        # Save uploaded images
        for img in images:
            with open(os.path.join(image_dir, img.filename), "wb") as f:
                f.write(await img.read())

        output_pdf_path = os.path.join(tempdir, "book.pdf")
        make_pdf_book(intro_path, image_dir, output_pdf_path)

        with open(output_pdf_path, "rb") as f:
            pdf_data = f.read()

    return Response(pdf_data, media_type="application/pdf", headers={
        "Content-Disposition": "attachment; filename=book.pdf"
    })
