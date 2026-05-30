import tempfile
from pypdf import PdfWriter


def merge_pdfs(pdf_paths: list[str]) -> str:
    """
    Merge a list of PDF file paths into a single PDF.
    Returns the path to the merged output file.
    """
    writer = PdfWriter()

    for path in pdf_paths:
        writer.append(path)

    out = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    with open(out.name, "wb") as f:
        writer.write(f)

    return out.name
