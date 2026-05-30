import streamlit as st
from utils.merge import merge_pdfs
from utils.split import split_pdf
from utils.extract import extract_text
from utils.watermark import add_watermark
import tempfile, os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PDF Toolkit",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@300;400;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.main-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -1px;
    color: #0f0f0f;
}
.subtitle { color: #555; font-size: 1rem; margin-top: -10px; margin-bottom: 30px; }
.tool-card {
    background: #f8f8f8;
    border-left: 4px solid #ff4b4b;
    padding: 16px 20px;
    border-radius: 6px;
    margin-bottom: 10px;
}
.success-box {
    background: #e6f4ea;
    border-left: 4px solid #34a853;
    padding: 14px 18px;
    border-radius: 6px;
    color: #1e4620;
}
.stButton > button {
    background: #0f0f0f;
    color: white;
    border-radius: 6px;
    padding: 10px 28px;
    font-weight: 600;
    border: none;
    width: 100%;
}
.stButton > button:hover { background: #ff4b4b; }
hr { border: none; border-top: 1px solid #eee; margin: 24px 0; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">📄 PDF Toolkit</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Merge · Split · Extract · Watermark — all in one place</div>', unsafe_allow_html=True)
st.markdown("---")

# ── Sidebar navigation ────────────────────────────────────────────────────────
tool = st.sidebar.radio(
    "Choose a Tool",
    ["🔀 Merge PDFs", "✂️ Split PDF", "📝 Extract Text", "💧 Add Watermark"],
    index=0,
)
st.sidebar.markdown("---")
st.sidebar.markdown("**PDF Toolkit** v1.0  \nBuilt with Python & Streamlit")

# ── 1. Merge ──────────────────────────────────────────────────────────────────
if tool == "🔀 Merge PDFs":
    st.subheader("🔀 Merge PDFs")
    st.markdown("Upload two or more PDF files. They will be merged in the order you upload them.")

    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

    if files:
        st.info(f"{len(files)} file(s) uploaded: {', '.join(f.name for f in files)}")

    if st.button("Merge PDFs") and files:
        if len(files) < 2:
            st.warning("Please upload at least 2 PDF files.")
        else:
            with st.spinner("Merging..."):
                tmp_paths = []
                for f in files:
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                    tmp.write(f.read())
                    tmp.close()
                    tmp_paths.append(tmp.name)

                out_path = merge_pdfs(tmp_paths)

                with open(out_path, "rb") as out:
                    st.download_button("⬇️ Download Merged PDF", out, file_name="merged.pdf", mime="application/pdf")

                st.markdown('<div class="success-box">✅ PDFs merged successfully!</div>', unsafe_allow_html=True)
                for p in tmp_paths:
                    os.unlink(p)

# ── 2. Split ──────────────────────────────────────────────────────────────────
elif tool == "✂️ Split PDF":
    st.subheader("✂️ Split PDF")
    st.markdown("Upload a PDF and choose a page range to extract as a new file.")

    file = st.file_uploader("Upload PDF", type="pdf")

    if file:
        col1, col2 = st.columns(2)
        start = col1.number_input("Start Page", min_value=1, value=1, step=1)
        end   = col2.number_input("End Page",   min_value=1, value=1, step=1)

        if st.button("Split PDF"):
            with st.spinner("Splitting..."):
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                tmp.write(file.read())
                tmp.close()

                out_path, msg = split_pdf(tmp.name, int(start), int(end))
                os.unlink(tmp.name)

                if out_path:
                    with open(out_path, "rb") as out:
                        st.download_button("⬇️ Download Split PDF", out, file_name=f"split_p{start}-p{end}.pdf", mime="application/pdf")
                    st.markdown('<div class="success-box">✅ PDF split successfully!</div>', unsafe_allow_html=True)
                else:
                    st.error(msg)

# ── 3. Extract Text ───────────────────────────────────────────────────────────
elif tool == "📝 Extract Text":
    st.subheader("📝 Extract Text")
    st.markdown("Upload a PDF to extract all readable text from it.")

    file = st.file_uploader("Upload PDF", type="pdf")

    if file:
        if st.button("Extract Text"):
            with st.spinner("Extracting..."):
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                tmp.write(file.read())
                tmp.close()

                text = extract_text(tmp.name)
                os.unlink(tmp.name)

                if text.strip():
                    st.text_area("Extracted Text", text, height=350)
                    st.download_button("⬇️ Download as .txt", text, file_name="extracted.txt", mime="text/plain")
                    st.markdown('<div class="success-box">✅ Text extracted successfully!</div>', unsafe_allow_html=True)
                else:
                    st.warning("No readable text found. The PDF may be scanned/image-based.")

# ── 4. Watermark ──────────────────────────────────────────────────────────────
elif tool == "💧 Add Watermark":
    st.subheader("💧 Add Watermark")
    st.markdown("Upload a PDF and type a watermark text. It will be stamped diagonally on every page.")

    file = st.file_uploader("Upload PDF", type="pdf")
    wm_text = st.text_input("Watermark Text", placeholder="e.g. CONFIDENTIAL")

    col1, col2 = st.columns(2)
    opacity  = col1.slider("Opacity",   0.05, 1.0, 0.25, 0.05)
    fontsize = col2.slider("Font Size", 20,   80,  40,   5)

    if file and wm_text:
        if st.button("Add Watermark"):
            with st.spinner("Adding watermark..."):
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                tmp.write(file.read())
                tmp.close()

                out_path = add_watermark(tmp.name, wm_text, opacity=opacity, fontsize=fontsize)
                os.unlink(tmp.name)

                with open(out_path, "rb") as out:
                    st.download_button("⬇️ Download Watermarked PDF", out, file_name="watermarked.pdf", mime="application/pdf")

                st.markdown('<div class="success-box">✅ Watermark added successfully!</div>', unsafe_allow_html=True)
