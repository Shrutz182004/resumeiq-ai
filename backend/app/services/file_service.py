import os
import shutil
from uuid import uuid4

UPLOAD_DIR = "uploads"


def save_uploaded_file(file):
    """
    Save uploaded file to uploads folder.
    Returns the saved file path.
    """

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"{uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return filename, filepath