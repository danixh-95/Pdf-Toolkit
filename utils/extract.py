from pypdf import PdfReader


def extract_text(pdf_path: str) -> str:
    """
    Extract all text from every page of a PDF.
    Returns a single string with page separators.
    """
    reader = PdfReader(pdf_path)
    pages_text = []

    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages_text.append(f"--- Page {i} ---\n{text}")

    return "\n\n".join(pages_text)
