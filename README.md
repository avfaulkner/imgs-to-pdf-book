# imgs-to-pdf

- This repo will add all PNG files in a directory to a single PDF file.
- The PNG images will be visible on all odd number pages, while every even numbered page will be left blank.
This way, when the full PDF is printed, the pages with images will be single sided.
- The margins on each image page will be set to 9.5 mm/0.375 inches, with the image scaled within these margins.

*Notes*:

- This application assumes that all images are stored in the same directory.
- **Currently, only .png image files are supported.**

## Prerequisites/Tooling

- Python 3.12

## Steps

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

## Run the script

Run the script with the following command.

```
python3 imgs-to-pdf-book.py <path to introPage.pdf> <image directory path> <path for final output PDF>
```

The arguments are as follows:

1. **path to introPage.pdf**: The path to the introPage.pdf file.
2. **image directory path**: The path to the directory containing your images.
3. **path for final output PDF**: The path where the final created pdf, containing the introPage and all images, will be placed after it is created.