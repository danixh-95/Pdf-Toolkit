import tempfile, math
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color


def _make_watermark_page(text: str, width: float, height: float,
                          opacity: float, fontsize: int) -> str:
    """Create a single-page PDF containing the diagonal watermark."""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(tmp.name, pagesize=(width, height))

    c.setFont("Helvetica-Bold", fontsize)
    c.setFillColor(Color(0.5, 0.5, 0.5, alpha=opacity))

    # Rotate around the centre of the page
    c.saveState()
    c.translate(width / 2, height / 2)
    angle = math.degrees(math.atan2(height, width))   # ~diagonal angle
    c.rotate(angle)
    c.drawCentredString(0, 0, text)
    c.restoreState()

    c.save()
    return tmp.name


def add_watermark(pdf_path: str, text: str,
                  opacity: float = 0.25, fontsize: int = 40) -> str:
    """
    Stamp a diagonal text watermark on every page of the PDF.
    Returns the path to the watermarked output file.
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)

        wm_path = _make_watermark_page(text, w, h, opacity, fontsize)
        wm_page = PdfReader(wm_path).pages[0]

        page.merge_page(wm_page)
        writer.add_page(page)

    out = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    with open(out.name, "wb") as f:
        writer.write(f)

    return out.name
