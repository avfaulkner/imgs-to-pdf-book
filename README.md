# imgs-to-pdf

This project converts all PNG images in a directory into a print-ready, single-sided PDF file.  
Each image appears on an odd-numbered page, with a blank page inserted after it — ideal for coloring books, art prints, or journaling pages.

*Notes*:

- This application assumes that all images are stored in the same directory.
- **Currently, only .png image files are supported.**



## Features

- Combines all `.png` files from a folder into one PDF.  
- Each image appears on an odd-numbered page, followed by a blank page.  
- Adds an optional intro page.  
- Automatically scales images to fit inside 0.375-inch (9.5 mm) margins.  
- Works both:
  - **Locally** via Python CLI  
  - **Online** through a connected [Netlify web app](https://github.com/avfaulkner/book-page-estimator)

---

## Steps to Run Locally

### Prerequisites/Tooling

- Python 3.12

### Build virtual environment for Python script

Create a virtual environment to run Python code.

Navigate to the project directory and run the following:

```
python3 -m venv venv
```

This will create a /venv directory within the project directory.

Activate the new virtual environment:

```
source venv/bin/activate
```

You’ll know it worked if your terminal prompt changes to:

```
(venv) <your workspace name>@hostname:~/<project directory>$
```

*Note: After running the code, if you wish to deactivate the virtual environment, run:

```
deactivate
```

### Install dependencies

```
pip install -r requirements.txt
```

### Run the script

Run the script with the following command.

```
python3 imgs-to-pdf-book.py <path to introPage.pdf> <image directory path> <path for final output PDF>
```

The arguments are as follows:

1. **path to introPage.pdf**: The path to the introPage.pdf file.
2. **image directory path**: The path to the directory containing your images.
3. **path for final output PDF**: The path where the final created pdf, containing the introPage and all images, will be placed after it is created.

Example:

```
python3 imgs-to-pdf-book.py introPage.pdf ./images ./output/finalBook.pdf
```

---

## Web Usage (Netlify + Render)

This project can now also run fully online by uploading images in a browser via the Netlify frontend and downloading the generated pdf file.
Netlify will send the request to Render, which is used for the backend processing, via an [API endpoint](https://imgs-to-pdf-book.onrender.com/api/create-pdf-book).

### Architecture Overview


          ┌────────────────────┐
          │    User Browser    │
          │  (Netlify Frontend)│
          └─────────┬──────────┘
                    │
        Upload intro.pdf + PNGs via form
                    │
                    ▼
          ┌────────────────────┐
          │  Render Backend    │
          │ (FastAPI + Python) │
          └─────────┬──────────┘
                    │
           Builds single-sided
             PDF using Pillow,
           ReportLab, and PyPDF2
                    │
                    ▼
          ┌────────────────────┐
          │    User Browser    │
          │  (Auto Download)   │
          └────────────────────┘

### Workflow Summary

1. Open Netlify site (frontend).
2. Upload:
    - introPage.pdf
    - .png image pages
3. Click Create Book
4. Render backend processes images → builds the PDF → sends it back
5. Browser automatically downloads book.pdf.

### Testing the Render API

Send a POST request via curl to the API endpoint with some test files. A file called book.pdf should be downloaded with the combined uploaded files. 
This can be done in the 'test' directory in this repo.

To test the connection, run:

```
curl -X OPTIONS https://imgs-to-pdf-book.onrender.com/api/create-pdf-book -i
```

A successful response for this test should include `HTTP/2 200`.