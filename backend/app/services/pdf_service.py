import fitz  # PyMuPDF


def extract_text_from_pdf(filepath: str) -> str:
    """
    Extract all text from a PDF.
    """

    doc = fitz.open(filepath)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text