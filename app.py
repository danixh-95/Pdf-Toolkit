import streamlit as st
from utils.merge import merge_pdfs
from utils.split import split_pdf
from utils.extract import extract_text
from utils.watermark import add_watermark
import tempfile, os

st.set_page_config(
    page_title="PDF Toolkit",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif;
    background: #070710 !important;
    color: #e8e8f0 !important;
}

/* ── Animated mesh background ── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 10% 0%, rgba(99,57,255,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 100%, rgba(0,210,180,0.12) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 80% 20%, rgba(255,60,120,0.08) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(12, 12, 26, 0.85) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}
section[data-testid="stSidebar"] * { color: #c8c8e0 !important; }

/* ── Hero header ── */
.hero {
    padding: 3rem 0 2rem;
    text-align: center;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #6339ff;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.6rem, 6vw, 4.2rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -2px;
    background: linear-gradient(135deg, #ffffff 30%, #a78bfa 70%, #34d8c2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.6rem;
}
.hero-sub {
    font-size: 1rem;
    color: rgba(200,200,220,0.55);
    letter-spacing: 0.02em;
    margin-bottom: 2.5rem;
}

/* ── Tool nav pills ── */
.tool-nav {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 3rem;
}
.tool-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 22px;
    border-radius: 100px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    font-weight: 500;
    cursor: pointer;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.04);
    color: rgba(200,200,220,0.7);
    transition: all 0.2s ease;
    text-decoration: none;
}
.tool-pill:hover {
    background: rgba(99,57,255,0.15);
    border-color: rgba(99,57,255,0.4);
    color: #c4b5fd;
}
.tool-pill.active {
    background: linear-gradient(135deg, rgba(99,57,255,0.3), rgba(52,216,194,0.2));
    border-color: rgba(99,57,255,0.6);
    color: #e0d7ff;
    box-shadow: 0 0 20px rgba(99,57,255,0.25);
}

/* ── Section header ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 2rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
.section-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    background: linear-gradient(135deg, rgba(99,57,255,0.3), rgba(52,216,194,0.15));
    border: 1px solid rgba(99,57,255,0.35);
    flex-shrink: 0;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    color: #f0f0ff;
    margin: 0;
}
.section-desc {
    font-size: 0.88rem;
    color: rgba(180,180,210,0.55);
    margin: 3px 0 0;
}

/* ── Glass cards ── */
.glass-card {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,57,255,0.5), rgba(52,216,194,0.3), transparent);
}

/* ── Upload zone ── */
[data-testid="stFileUploader"] {
    background: rgba(99,57,255,0.06) !important;
    border: 1.5px dashed rgba(99,57,255,0.35) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFileUploader"]:hover {
    background: rgba(99,57,255,0.1) !important;
    border-color: rgba(99,57,255,0.6) !important;
}
[data-testid="stFileUploader"] * { color: #c4b5fd !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6339ff, #34d8c2) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 24px rgba(99,57,255,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(99,57,255,0.45) !important;
}
.stButton > button:active { transform: scale(0.98) !important; }

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: rgba(52,216,194,0.12) !important;
    color: #34d8c2 !important;
    border: 1px solid rgba(52,216,194,0.35) !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    width: 100% !important;
    padding: 0.75rem 2rem !important;
    box-shadow: 0 4px 20px rgba(52,216,194,0.12) !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(52,216,194,0.2) !important;
    box-shadow: 0 6px 28px rgba(52,216,194,0.22) !important;
}

/* ── Inputs & sliders ── */
.stNumberInput input, .stTextInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stNumberInput input:focus, .stTextInput input:focus {
    border-color: rgba(99,57,255,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,57,255,0.15) !important;
}
.stTextInput label, .stNumberInput label,
.stSlider label, .stFileUploader label {
    color: rgba(180,180,210,0.75) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}
.stSlider [data-testid="stSlider"] div[role="slider"] {
    background: #6339ff !important;
}

/* ── Text area ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 14px !important;
    color: #d0d0e8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.83rem !important;
}

/* ── Alert / info boxes ── */
.stAlert {
    background: rgba(99,57,255,0.1) !important;
    border: 1px solid rgba(99,57,255,0.25) !important;
    border-radius: 12px !important;
    color: #c4b5fd !important;
}

/* ── Success / error banners ── */
.fx-success {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(52,216,194,0.08);
    border: 1px solid rgba(52,216,194,0.25);
    border-radius: 14px;
    padding: 14px 20px;
    color: #34d8c2;
    font-size: 0.92rem;
    font-weight: 500;
    margin-top: 1rem;
}
.fx-error {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(255,60,100,0.08);
    border: 1px solid rgba(255,60,100,0.25);
    border-radius: 14px;
    padding: 14px 20px;
    color: #ff6b8a;
    font-size: 0.92rem;
    font-weight: 500;
    margin-top: 1rem;
}

/* ── Sidebar radio ── */
.stRadio > label { color: rgba(180,180,210,0.6) !important; font-size: 0.78rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }
.stRadio div[role="radiogroup"] label {
    color: #c8c8e0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.93rem !important;
    padding: 8px 12px !important;
    border-radius: 10px !important;
    transition: background 0.15s ease !important;
}
.stRadio div[role="radiogroup"] label:hover { background: rgba(99,57,255,0.12) !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #6339ff !important; }

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,57,255,0.4); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">✦ Document Intelligence Suite</div>
  <h1 class="hero-title">PDF Toolkit</h1>
  <p class="hero-sub">Merge · Split · Extract · Watermark — beautifully engineered</p>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="padding: 1rem 0 0.5rem; text-align:center;">
  <div style="font-family:'Syne',sans-serif; font-size:1.3rem; font-weight:800;
              background:linear-gradient(135deg,#a78bfa,#34d8c2);
              -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
    PDF Toolkit
  </div>
  <div style="font-size:0.72rem; letter-spacing:0.12em; color:rgba(180,180,210,0.4); margin-top:4px;">
    v2.0 · PORTFOLIO EDITION
  </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

tool = st.sidebar.radio(
    "TOOLS",
    ["⊕  Merge PDFs", "⊘  Split PDF", "⊡  Extract Text", "◈  Add Watermark"],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="padding:1rem; background:rgba(99,57,255,0.08); border:1px solid rgba(99,57,255,0.2);
            border-radius:14px; font-size:0.8rem; color:rgba(180,180,210,0.6); line-height:1.7;">
  <b style="color:#a78bfa;">ℹ️ About</b><br>
  All processing is done in-memory.<br>No files are stored on the server.
</div>
""", unsafe_allow_html=True)

# ── HELPERS ───────────────────────────────────────────────────────────────────
def success(msg):
    st.markdown(f'<div class="fx-success">✦ {msg}</div>', unsafe_allow_html=True)

def error(msg):
    st.markdown(f'<div class="fx-error">✖ {msg}</div>', unsafe_allow_html=True)

def section_header(icon, title, desc):
    st.markdown(f"""
    <div class="section-header">
      <div class="section-icon">{icon}</div>
      <div>
        <div class="section-title">{title}</div>
        <div class="section-desc">{desc}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── CENTERED CONTENT COLUMN ───────────────────────────────────────────────────
_, col, _ = st.columns([0.5, 9, 0.5])

with col:

    # ── 1. MERGE ─────────────────────────────────────────────────────────────
    if "Merge" in tool:
        section_header("⊕", "Merge PDFs", "Combine multiple PDF files into one unified document")

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        files = st.file_uploader(
            "Drop your PDF files here",
            type="pdf",
            accept_multiple_files=True,
            help="Files will be merged in the order they are listed",
        )

        if files:
            st.markdown(f"""
            <div style="display:flex; flex-wrap:wrap; gap:8px; margin:1rem 0;">
              {''.join(f'<span style="background:rgba(99,57,255,0.12);border:1px solid rgba(99,57,255,0.3);border-radius:8px;padding:5px 12px;font-size:0.8rem;color:#c4b5fd;">📄 {f.name}</span>' for f in files)}
            </div>
            """, unsafe_allow_html=True)

        if st.button("⊕  Merge Now"):
            if not files or len(files) < 2:
                error("Please upload at least 2 PDF files to merge.")
            else:
                with st.spinner("Fusing documents…"):
                    tmp_paths = []
                    for f in files:
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                        tmp.write(f.read()); tmp.close()
                        tmp_paths.append(tmp.name)
                    out_path = merge_pdfs(tmp_paths)
                    with open(out_path, "rb") as out:
                        st.download_button("⬇  Download Merged PDF", out,
                                           file_name="merged.pdf", mime="application/pdf")
                    success(f"{len(files)} PDFs merged successfully.")
                    for p in tmp_paths: os.unlink(p)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── 2. SPLIT ─────────────────────────────────────────────────────────────
    elif "Split" in tool:
        section_header("⊘", "Split PDF", "Extract a specific page range into a new standalone file")

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        file = st.file_uploader("Drop your PDF here", type="pdf")

        if file:
            c1, c2 = st.columns(2)
            start = c1.number_input("Start Page", min_value=1, value=1, step=1)
            end   = c2.number_input("End Page",   min_value=1, value=1, step=1)

            st.markdown(f"""
            <div style="margin:1rem 0; padding:12px 18px; background:rgba(52,216,194,0.06);
                        border:1px solid rgba(52,216,194,0.2); border-radius:12px;
                        font-size:0.85rem; color:rgba(180,220,210,0.7);">
              Extracting pages <b style="color:#34d8c2;">{int(start)}</b> to
              <b style="color:#34d8c2;">{int(end)}</b> from
              <b style="color:#34d8c2;">{file.name}</b>
            </div>
            """, unsafe_allow_html=True)

            if st.button("⊘  Split Now"):
                with st.spinner("Slicing document…"):
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                    tmp.write(file.read()); tmp.close()
                    out_path, msg = split_pdf(tmp.name, int(start), int(end))
                    os.unlink(tmp.name)
                    if out_path:
                        with open(out_path, "rb") as out:
                            st.download_button("⬇  Download Split PDF", out,
                                               file_name=f"split_p{start}-p{end}.pdf",
                                               mime="application/pdf")
                        success(f"Pages {int(start)}–{int(end)} extracted successfully.")
                    else:
                        error(msg)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── 3. EXTRACT ───────────────────────────────────────────────────────────
    elif "Extract" in tool:
        section_header("⊡", "Extract Text", "Pull all readable text from any PDF document")

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        file = st.file_uploader("Drop your PDF here", type="pdf")

        if file:
            if st.button("⊡  Extract Text"):
                with st.spinner("Reading document…"):
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                    tmp.write(file.read()); tmp.close()
                    text = extract_text(tmp.name)
                    os.unlink(tmp.name)

                    if text.strip():
                        st.text_area("Extracted Content", text, height=380)
                        c1, c2 = st.columns(2)
                        with c1:
                            st.download_button("⬇  Download as .txt", text,
                                               file_name="extracted.txt", mime="text/plain")
                        with c2:
                            word_count = len(text.split())
                            st.markdown(f"""
                            <div style="padding:14px; background:rgba(99,57,255,0.08);
                                        border:1px solid rgba(99,57,255,0.2); border-radius:12px;
                                        text-align:center; height:100%;">
                              <div style="font-size:1.5rem; font-weight:700; color:#a78bfa;">{word_count:,}</div>
                              <div style="font-size:0.75rem; color:rgba(180,180,210,0.5); letter-spacing:0.1em; text-transform:uppercase;">words extracted</div>
                            </div>
                            """, unsafe_allow_html=True)
                        success("Text extracted successfully.")
                    else:
                        error("No readable text found. This PDF may be image-based or scanned.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ── 4. WATERMARK ─────────────────────────────────────────────────────────
    elif "Watermark" in tool:
        section_header("◈", "Add Watermark", "Stamp a diagonal text watermark across every page")

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        file    = st.file_uploader("Drop your PDF here", type="pdf")
        wm_text = st.text_input("Watermark Text", placeholder="e.g.  CONFIDENTIAL  ·  DRAFT  ·  TOP SECRET")

        c1, c2 = st.columns(2)
        opacity  = c1.slider("Opacity",   0.05, 1.0, 0.25, 0.05)
        fontsize = c2.slider("Font Size", 20,   80,  40,   5)

        if wm_text:
            st.markdown(f"""
            <div style="margin:1rem 0; padding:20px; background:rgba(255,255,255,0.02);
                        border:1px solid rgba(255,255,255,0.07); border-radius:14px;
                        text-align:center; position:relative; overflow:hidden;">
              <span style="font-size:{min(fontsize, 48)}px; font-weight:800;
                           color:rgba(167,139,250,{opacity}); letter-spacing:0.12em;
                           font-family:'Syne',sans-serif; text-transform:uppercase;
                           transform:rotate(-15deg); display:inline-block;">
                {wm_text}
              </span>
              <div style="font-size:0.72rem; color:rgba(180,180,210,0.35);
                          margin-top:8px; letter-spacing:0.1em; text-transform:uppercase;">
                preview
              </div>
            </div>
            """, unsafe_allow_html=True)

        if file and wm_text:
            if st.button("◈  Apply Watermark"):
                with st.spinner("Stamping pages…"):
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                    tmp.write(file.read()); tmp.close()
                    out_path = add_watermark(tmp.name, wm_text, opacity=opacity, fontsize=fontsize)
                    os.unlink(tmp.name)
                    with open(out_path, "rb") as out:
                        st.download_button("⬇  Download Watermarked PDF", out,
                                           file_name="watermarked.pdf", mime="application/pdf")
                    success(f'"{wm_text}" watermark applied to all pages.')

        st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:4rem; padding:2rem 0 1rem; text-align:center;
            border-top:1px solid rgba(255,255,255,0.06);">
  <div style="font-family:'Syne',sans-serif; font-size:0.78rem; font-weight:600;
              letter-spacing:0.18em; text-transform:uppercase;
              color:rgba(180,180,210,0.3);">
    PDF Toolkit · Built with Python & Streamlit · Portfolio Project
  </div>
</div>
""", unsafe_allow_html=True)