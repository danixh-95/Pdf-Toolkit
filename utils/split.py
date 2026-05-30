import tempfile
from pypdf import PdfReader, PdfWriter


def split_pdf(pdf_path: str, start_page: int, end_page: int):
    """
    Extract pages [start_page, end_page] (1-indexed, inclusive) from a PDF.
    Returns (output_path, None) on success or (None, error_message) on failure.
    """
    reader = PdfReader(pdf_path)
    total  = len(reader.pages)

    if start_page < 1 or end_page < start_page or end_page > total:
        return None, f"Invalid page range. The PDF has {total} page(s). Choose between 1 and {total}."

    writer = PdfWriter()
    for i in range(start_page - 1, end_page):   # convert to 0-indexed
        writer.add_page(reader.pages[i])

    out = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    with open(out.name, "wb") as f:
        writer.write(f)

    return out.name, None
