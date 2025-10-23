from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import Response, StreamingResponse
import tempfile, os, io
from pdf_book_maker import make_pdf_book
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Image-to-PDF Book API")

# Enable CORS (important for browser uploads)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://book-page-estimator.netlify.app",
        "http://localhost:5173",  # for local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/create-pdf-book")
async def create_pdf_book(intro_pdf: UploadFile = File(...), images: list[UploadFile] = File(...)):
    with tempfile.TemporaryDirectory() as tempdir:
        intro_path = os.path.join(tempdir, "intro.pdf")
        image_dir = os.path.join(tempdir, "images")
        os.makedirs(image_dir)

        # Save intro PDF
        with open(intro_path, "wb") as f:
            f.write(await intro_pdf.read())

        # Save uploaded PNGs
        for img in images:
            with open(os.path.join(image_dir, img.filename), "wb") as f:
                f.write(await img.read())

        # Create output PDF
        output_pdf_path = os.path.join(tempdir, "book.pdf")
        make_pdf_book(intro_path, image_dir, output_pdf_path)

        # Read and return the finished PDF
        with open(output_pdf_path, "rb") as f:
            data = f.read()

    return Response(data, media_type="application/pdf", headers={
        "Content-Disposition": "attachment; filename=book.pdf"
    })

@app.options("/{full_path:path}")
async def preflight_handler(request: Request):
    """Handle all CORS preflight OPTIONS requests manually."""
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response
