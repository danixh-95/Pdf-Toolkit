import streamlit as st
from utils.merge import merge_pdfs
from utils.split import split_pdf
from utils.extract import extract_text
from utils.watermark import add_watermark
import tempfile, os

from pypdf import PdfReader
import tempfile, os

st.set_page_config(
    page_title="PDF Toolkit Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── INITIALIZE USER STATISTICS ────────────────────────────────────────────────
if "stats" not in st.session_state:
    st.session_state.stats = {
        "files_uploaded": 0,
        "pages_processed": 0,
        "words_extracted": 0,
        "operations_completed": 0
    }

# ── INJECT PREMIUM FUUTURISTIC CSS STYLING ────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }

/* Global Styling Overrides */
html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background: #050816 !important;
    color: #FFFFFF !important;
}

/* Background Aurora Glowing Effects */
.stApp {
    position: relative;
    overflow-x: hidden;
}
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background: 
        radial-gradient(circle 800px at 100px -100px, rgba(124, 58, 237, 0.12), transparent 80%),
        radial-gradient(circle 800px at calc(100% - 100px) calc(100% - 100px), rgba(6, 182, 212, 0.08), transparent 80%);
    pointer-events: none;
    z-index: -1;
}

@keyframes aurora {
    0% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(3%, 3%) scale(1.05); }
    100% { transform: translate(0, 0) scale(1); }
}
.aurora-glow-1 {
    position: fixed;
    top: -200px;
    left: -200px;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(124, 58, 237, 0.15) 0%, transparent 70%);
    filter: blur(120px);
    pointer-events: none;
    z-index: -2;
    animation: aurora 25s infinite alternate ease-in-out;
}
.aurora-glow-2 {
    position: fixed;
    bottom: -200px;
    right: -200px;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(6, 182, 212, 0.12) 0%, transparent 70%);
    filter: blur(120px);
    pointer-events: none;
    z-index: -2;
    animation: aurora 30s infinite alternate-reverse ease-in-out;
}

/* Glassmorphic Sidebar Design */
section[data-testid="stSidebar"] {
    background: rgba(10, 12, 26, 0.8) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
}
section[data-testid="stSidebar"] * {
    color: rgba(255, 255, 255, 0.85) !important;
}

/* Hide Radio Buttons Circles */
div[role="radiogroup"] label [data-testid="stMarker"] {
    display: none !important;
}

/* Custom Navigation Radio Labels */
div[role="radiogroup"] label {
    display: flex !important;
    align-items: center !important;
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.04) !important;
    border-radius: 14px !important;
    padding: 12px 18px !important;
    margin-bottom: 12px !important;
    cursor: pointer !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
div[role="radiogroup"] label:hover {
    background: rgba(124, 58, 237, 0.08) !important;
    border-color: rgba(124, 58, 237, 0.3) !important;
    transform: translateX(4px) !important;
}
div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg, rgba(124, 58, 237, 0.18), rgba(6, 182, 212, 0.12)) !important;
    border-color: rgba(124, 58, 237, 0.5) !important;
    box-shadow: 0 0 25px rgba(124, 58, 237, 0.2) !important;
}
div[role="radiogroup"] label:has(input:checked) span {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* Sidebar Branding */
.sidebar-logo-container {
    padding: 1.5rem 0 1rem;
    text-align: center;
}
.sidebar-logo-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.45rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #06B6D4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}
.sidebar-logo-subtitle {
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    color: rgba(255, 255, 255, 0.35);
    margin-top: 5px;
    text-transform: uppercase;
}

/* Hero Section */
.hero {
    padding: 4rem 0 3rem;
    text-align: center;
    position: relative;
}
.hero-eyebrow-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(124, 58, 237, 0.1);
    border: 1px solid rgba(124, 58, 237, 0.25);
    border-radius: 9999px;
    padding: 6px 14px;
    font-size: 0.72rem;
    font-weight: 600;
    color: #06B6D4;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.25rem;
    animation: badgePulse 2s infinite ease-in-out;
}
@keyframes badgePulse {
    0%, 100% { box-shadow: 0 0 10px rgba(124, 58, 237, 0.05); border-color: rgba(124, 58, 237, 0.2); }
    50% { box-shadow: 0 0 18px rgba(124, 58, 237, 0.2); border-color: rgba(124, 58, 237, 0.45); }
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 4.4rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -2px;
    background: linear-gradient(135deg, #FFFFFF 30%, #7C3AED 70%, #06B6D4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 auto 0.8rem;
    max-width: 900px;
}
.hero-sub {
    font-family: 'Inter', sans-serif;
    font-size: 1.05rem;
    color: rgba(255, 255, 255, 0.65);
    max-width: 600px;
    margin: 0 auto 2.5rem;
    line-height: 1.5;
}

/* Statistics Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 3rem;
}
@media (max-width: 768px) {
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 480px) {
    .stats-grid { grid-template-columns: 1fr; }
}
.stat-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 16px;
    text-align: center;
    backdrop-filter: blur(12px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(6, 182, 212, 0.3), transparent);
}
.stat-card:hover {
    transform: translateY(-4px);
    border-color: rgba(6, 182, 212, 0.25);
    box-shadow: 0 8px 20px rgba(6, 182, 212, 0.06);
}
.stat-icon {
    font-size: 1.2rem;
    margin-bottom: 6px;
}
.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.55rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.2;
}
.stat-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    color: rgba(255, 255, 255, 0.45);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 4px;
}

/* Premium Glass Cards */
.glass-card {
    background: rgba(15, 23, 42, 0.4) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 24px;
    padding: 2.5rem;
    backdrop-filter: blur(16px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.glass-card:hover {
    border-color: rgba(124, 58, 237, 0.2) !important;
    box-shadow: 0 15px 40px rgba(124, 58, 237, 0.05);
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(124, 58, 237, 0.4), rgba(6, 182, 212, 0.3), transparent);
}

/* Section Header styling */
.section-header {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.section-icon {
    width: 56px;
    height: 56px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.6rem;
    background: linear-gradient(135deg, rgba(124, 58, 237, 0.2), rgba(6, 182, 212, 0.15));
    border: 1px solid rgba(124, 58, 237, 0.3);
    box-shadow: 0 0 20px rgba(124, 58, 237, 0.1);
    flex-shrink: 0;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #FFFFFF, rgba(255, 255, 255, 0.75));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.section-desc {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.5);
    margin-top: 4px;
}

/* Custom File Uploader */
[data-testid="stFileUploader"] {
    background: rgba(15, 23, 42, 0.5) !important;
    border: 2px dashed rgba(124, 58, 237, 0.25) !important;
    border-radius: 16px !important;
    padding: 2.2rem !important;
    transition: all 0.3s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #06B6D4 !important;
    background: rgba(124, 58, 237, 0.04) !important;
}
[data-testid="stFileUploader"] * {
    color: rgba(255, 255, 255, 0.65) !important;
}
[data-testid="stFileUploader"] section {
    background: transparent !important;
}

/* Uploader Status Indicator */
.uploader-status-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(6, 182, 212, 0.05);
    border: 1px solid rgba(6, 182, 212, 0.15);
    border-radius: 12px;
    padding: 10px 18px;
    margin: 1.25rem 0;
    font-size: 0.85rem;
    color: #06B6D4;
}

/* Primary Button Styling */
.stButton > button {
    background: linear-gradient(135deg, #7C3AED, #06B6D4) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 2.2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    width: 100% !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(124, 58, 237, 0.4) !important;
    color: #FFFFFF !important;
}
.stButton > button:active {
    transform: translateY(0px) scale(0.97) !important;
}

/* Download / Secondary Button Styling */
[data-testid="stDownloadButton"] > button {
    background: rgba(6, 182, 212, 0.08) !important;
    color: #06B6D4 !important;
    border: 1px solid rgba(6, 182, 212, 0.25) !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    width: 100% !important;
    padding: 0.8rem 2.2rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 15px rgba(6, 182, 212, 0.08) !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(6, 182, 212, 0.18) !important;
    border-color: #06B6D4 !important;
    color: #06B6D4 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(6, 182, 212, 0.2) !important;
}
[data-testid="stDownloadButton"] > button:active {
    transform: translateY(0) scale(0.97) !important;
}

/* Sliders, Inputs and Selectors Styling */
.stNumberInput input, .stTextInput input, .stTextArea textarea {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
    padding: 10px 14px !important;
}
.stNumberInput input:focus, .stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #06B6D4 !important;
    box-shadow: 0 0 10px rgba(6, 182, 212, 0.2) !important;
}
.stSlider [data-testid="stSlider"] div[role="slider"] {
    background: #7C3AED !important;
    border: 2px solid #06B6D4 !important;
}
.stSlider div[data-testid="stWidgetLabel"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    color: rgba(255, 255, 255, 0.75) !important;
}

/* Alert Boxes & Banners */
.fx-success {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(16, 185, 129, 0.1) !important;
    border: 1px solid rgba(16, 185, 129, 0.25) !important;
    border-radius: 12px;
    padding: 14px 20px;
    color: #10B981;
    font-size: 0.9rem;
    font-weight: 500;
    margin-top: 1.5rem;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.05);
}
.fx-error {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(244, 63, 94, 0.1) !important;
    border: 1px solid rgba(244, 63, 94, 0.25) !important;
    border-radius: 12px;
    padding: 14px 20px;
    color: #F43F5E;
    font-size: 0.9rem;
    font-weight: 500;
    margin-top: 1.5rem;
    box-shadow: 0 4px 15px rgba(244, 63, 94, 0.05);
}

/* File Reordering Cards (Merge PDFs) */
.file-chip {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 10px 18px;
    margin-bottom: 8px;
}
.file-index {
    background: #7C3AED;
    color: #FFFFFF;
    font-weight: 700;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.8rem;
}
.file-name {
    font-weight: 500;
    color: #FFFFFF;
    flex-grow: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.file-size {
    color: rgba(255, 255, 255, 0.4);
    font-size: 0.8rem;
}
.sequence-container .stButton > button {
    background: rgba(255, 255, 255, 0.04) !important;
    color: rgba(255, 255, 255, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 8px !important;
    padding: 4px 10px !important;
    font-size: 0.85rem !important;
    width: 100% !important;
    box-shadow: none !important;
    transform: none !important;
}
.sequence-container .stButton > button:hover {
    background: rgba(124, 58, 237, 0.2) !important;
    border-color: rgba(124, 58, 237, 0.4) !important;
    color: #FFFFFF !important;
}

/* Range Preview Card */
.range-preview-card {
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(6, 182, 212, 0.05);
    border: 1px solid rgba(6, 182, 212, 0.15);
    border-radius: 16px;
    padding: 16px 20px;
    margin: 1.5rem 0;
}
.range-preview-icon {
    font-size: 1.8rem;
    color: #06B6D4;
}

/* Live Watermark Preview Mockup Container */
.watermark-preview-card {
    background: rgba(5, 8, 22, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    height: 220px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    box-shadow: inset 0 0 25px rgba(0, 0, 0, 0.7);
    margin-top: 1rem;
}
.watermark-preview-text {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    text-transform: uppercase;
    transform: rotate(-20deg);
    white-space: nowrap;
    pointer-events: none;
    transition: all 0.25s ease;
}

/* Divider Styling */
hr {
    border: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.06), transparent) !important;
    margin: 2rem 0 !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: rgba(124, 58, 237, 0.3);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(6, 182, 212, 0.4);
}
</style>

<div class="aurora-glow-1"></div>
<div class="aurora-glow-2"></div>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow-badge">✦ AI Powered PDF Suite</div>
  <h1 class="hero-title">Transform Documents Effortlessly</h1>
  <p class="hero-sub">Fusion, precision split, text extraction, and watermarking. Beautifully engineered.</p>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR BRANDING & ABOUT ──────────────────────────────────────────────────
st.sidebar.markdown("""
<div class="sidebar-logo-container">
  <div class="sidebar-logo-title">PDF Toolkit Pro</div>
  <div class="sidebar-logo-subtitle">v3.0 · PORTFOLIO EDITION</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

tool = st.sidebar.radio(
    "TOOLS",
    ["🔀  Merge PDFs", "✂️  Split PDF", "📝  Extract Text", "💧  Add Watermark"],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="padding:1.25rem; background:rgba(6, 182, 212, 0.03); border:1px solid rgba(6, 182, 212, 0.15);
            border-radius:16px; font-size:0.8rem; color:rgba(255,255,255,0.6); line-height:1.75; backdrop-filter:blur(10px);">
  <b style="color:#06B6D4; font-family:'Syne',sans-serif; letter-spacing:0.05em;">ℹ️ SECURITY PROTOCOL</b><br>
  All processing is executed strictly in-memory. Files are never stored on the server.
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
_, col, _ = st.columns([0.5, 11, 0.5])

with col:

    # ── GLOBAL METRICS DASHBOARD ──────────────────────────────────────────────
    stats = st.session_state.stats
    st.markdown(f"""
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📂</div>
        <div class="stat-value">{stats['files_uploaded']}</div>
        <div class="stat-label">Files Uploaded</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📄</div>
        <div class="stat-value">{stats['pages_processed']}</div>
        <div class="stat-label">Pages Processed</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-value">{stats['words_extracted']:,}</div>
        <div class="stat-label">Words Extracted</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">⚡</div>
        <div class="stat-value">{stats['operations_completed']}</div>
        <div class="stat-label">Tasks Completed</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 1. MERGE ─────────────────────────────────────────────────────────────
    if "Merge" in tool:
        section_header("🔀", "Merge PDFs", "Combine multiple PDF files into one unified document")

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        if "merge_files" not in st.session_state:
            st.session_state.merge_files = []
            st.session_state.last_uploaded_files = []

        uploaded_files = st.file_uploader(
            "Drop your PDF files here",
            type="pdf",
            accept_multiple_files=True,
            key="merge_uploader",
            help="Files will be merged in the order they are listed below",
        )

        # Sync files list with the file_uploader widget
        uploaded_file_ids = [f.name + str(f.size) for f in (uploaded_files or [])]
        last_file_ids = [f.name + str(f.size) for f in st.session_state.last_uploaded_files]

        if set(uploaded_file_ids) != set(last_file_ids):
            st.session_state.merge_files = list(uploaded_files) if uploaded_files else []
            st.session_state.last_uploaded_files = list(uploaded_files) if uploaded_files else []

        if st.session_state.merge_files:
            total_size = sum(f.size for f in st.session_state.merge_files)
            st.markdown(f"""
            <div class="uploader-status-bar">
                <span>📂 <b>{len(st.session_state.merge_files)}</b> files loaded</span>
                <span>⚖️ Total size: <b>{total_size / (1024*1024):.2f} MB</b></span>
            </div>
            <div style="margin-bottom: 0.8rem; font-family:'Syne',sans-serif; font-size:0.85rem; font-weight:600; color:rgba(255,255,255,0.6);">
                SEQUENCE CONTROLS
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="sequence-container">', unsafe_allow_html=True)
            for i, f in enumerate(st.session_state.merge_files):
                c1, c2 = st.columns([8, 2])
                with c1:
                    st.markdown(f"""
                    <div class="file-chip">
                        <span class="file-index">{i+1}</span>
                        <span class="file-name">📄 {f.name}</span>
                        <span class="file-size">({f.size / 1024:.1f} KB)</span>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    sub1, sub2 = st.columns(2)
                    with sub1:
                        if st.button("▲", key=f"up_{i}_{f.name}"):
                            if i > 0:
                                st.session_state.merge_files[i], st.session_state.merge_files[i-1] = st.session_state.merge_files[i-1], st.session_state.merge_files[i]
                                st.rerun()
                    with sub2:
                        if st.button("▼", key=f"down_{i}_{f.name}"):
                            if i < len(st.session_state.merge_files) - 1:
                                st.session_state.merge_files[i], st.session_state.merge_files[i+1] = st.session_state.merge_files[i+1], st.session_state.merge_files[i]
                                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

        if st.button("🔀  Merge Now"):
            if not st.session_state.merge_files or len(st.session_state.merge_files) < 2:
                error("Please upload at least 2 PDF files to merge.")
            else:
                with st.spinner("Fusing documents…"):
                    tmp_paths = []
                    for f in st.session_state.merge_files:
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                        tmp.write(f.read()); tmp.close()
                        tmp_paths.append(tmp.name)
                    out_path = merge_pdfs(tmp_paths)
                    
                    try:
                        reader = PdfReader(out_path)
                        pages_count = len(reader.pages)
                    except Exception:
                        pages_count = 0

                    st.session_state.stats["files_uploaded"] += len(st.session_state.merge_files)
                    st.session_state.stats["pages_processed"] += pages_count
                    st.session_state.stats["operations_completed"] += 1

                    with open(out_path, "rb") as out:
                        st.download_button("⬇  Download Merged PDF", out,
                                           file_name="merged.pdf", mime="application/pdf")
                    success(f"{len(st.session_state.merge_files)} PDFs merged successfully.")
                    for p in tmp_paths: os.unlink(p)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── 2. SPLIT ─────────────────────────────────────────────────────────────
    elif "Split" in tool:
        section_header("✂️", "Split PDF", "Extract a specific page range into a new standalone file")

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        file = st.file_uploader("Drop your PDF here", type="pdf")

        if file:
            total_pages = 1
            try:
                pdf_reader = PdfReader(file)
                total_pages = len(pdf_reader.pages)
            except Exception:
                pass

            st.markdown(f"""
            <div class="uploader-status-bar">
                <span>📄 <b>{file.name}</b></span>
                <span>⚖️ Size: <b>{file.size / 1024:.1f} KB</b> | Total Pages: <b>{total_pages}</b></span>
            </div>
            """, unsafe_allow_html=True)

            pages_range = st.slider("Select Page Range to Extract", 1, total_pages, (1, min(5, total_pages)))
            start, end = pages_range

            st.markdown(f"""
            <div class="range-preview-card">
                <div class="range-preview-icon">✂️</div>
                <div>
                    <div style="font-family:'Syne',sans-serif; font-size:1.15rem; font-weight:700; color:#FFFFFF;">
                        Extracting Pages {start} – {end}
                    </div>
                    <div style="font-size:0.82rem; color:rgba(255,255,255,0.5); margin-top:2px;">
                        Output file will contain {end - start + 1} pages
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("✂️  Split Now"):
                with st.spinner("Slicing document…"):
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                    tmp.write(file.read()); tmp.close()
                    out_path, msg = split_pdf(tmp.name, int(start), int(end))
                    os.unlink(tmp.name)
                    if out_path:
                        st.session_state.stats["files_uploaded"] += 1
                        st.session_state.stats["pages_processed"] += (int(end) - int(start) + 1)
                        st.session_state.stats["operations_completed"] += 1

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
        section_header("📝", "Extract Text", "Pull all readable text from any PDF document")

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        file = st.file_uploader("Drop your PDF here", type="pdf")

        if file:
            st.markdown(f"""
            <div class="uploader-status-bar">
                <span>📄 <b>{file.name}</b></span>
                <span>⚖️ Size: <b>{file.size / 1024:.1f} KB</b></span>
            </div>
            """, unsafe_allow_html=True)

            if st.button("📝  Extract Text"):
                with st.spinner("Reading document…"):
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                    tmp.write(file.read()); tmp.close()
                    text = extract_text(tmp.name)
                    os.unlink(tmp.name)

                    if text.strip():
                        word_count = len(text.split())
                        char_count = len(text)

                        st.session_state.stats["files_uploaded"] += 1
                        st.session_state.stats["words_extracted"] += word_count
                        st.session_state.stats["operations_completed"] += 1

                        # Word and Character Count Dashboard
                        st.markdown(f"""
                        <div class="stats-grid" style="margin-top: 1.5rem; margin-bottom: 1.5rem;">
                            <div class="stat-card" style="padding: 12px;">
                                <div class="stat-value">{word_count:,}</div>
                                <div class="stat-label">Words Extracted</div>
                            </div>
                            <div class="stat-card" style="padding: 12px;">
                                <div class="stat-value">{char_count:,}</div>
                                <div class="stat-label">Characters</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Code Editor Style Text Box & Copy Clip
                        st.markdown("""
                        <div class="code-editor-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-family: 'DM Mono', monospace; font-size: 0.8rem; color: rgba(255,255,255,0.45);">extracted_text.txt</span>
                            <button class="copy-btn" onclick="
                                const container = document.getElementById('extracted-text-container');
                                const textarea = container.querySelector('textarea');
                                if (textarea) {
                                    navigator.clipboard.writeText(textarea.value);
                                    this.innerHTML = '✓ Copied';
                                    setTimeout(() => this.innerHTML = '📋 Copy', 2000);
                                }
                            " style="background: rgba(124, 58, 237, 0.1); border: 1px solid rgba(124, 58, 237, 0.3); color: #06B6D4; padding: 6px 12px; border-radius: 8px; font-size: 0.75rem; cursor: pointer; font-weight:600;">📋 Copy</button>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown('<div id="extracted-text-container">', unsafe_allow_html=True)
                        st.text_area("Extracted Content", text, height=380, label_visibility="collapsed")
                        st.markdown('</div>', unsafe_allow_html=True)

                        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
                        
                        st.download_button("⬇  Download as .txt", text,
                                           file_name="extracted.txt", mime="text/plain")
                        success("Text extracted successfully.")
                    else:
                        error("No readable text found. This PDF may be image-based or scanned.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ── 4. WATERMARK ─────────────────────────────────────────────────────────
    elif "Watermark" in tool:
        section_header("💧", "Add Watermark", "Stamp a diagonal text watermark across every page")

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        file = st.file_uploader("Drop your PDF here", type="pdf")

        if file:
            st.markdown(f"""
            <div class="uploader-status-bar">
                <span>📄 <b>{file.name}</b></span>
                <span>⚖️ Size: <b>{file.size / 1024:.1f} KB</b></span>
            </div>
            """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("<div style='margin-bottom: 0.8rem; font-family:\"Syne\",sans-serif; font-size:0.85rem; font-weight:600; color:rgba(255,255,255,0.6);'>WATERMARK CONFIGURATION</div>", unsafe_allow_html=True)
            wm_text = st.text_input("Watermark Text", placeholder="e.g.  CONFIDENTIAL  ·  DRAFT  ·  TOP SECRET")
            opacity = st.slider("Opacity", 0.05, 1.0, 0.25, 0.05)
            fontsize = st.slider("Font Size", 20, 80, 40, 5)

        with col2:
            st.markdown("<div style='margin-bottom: 0.8rem; font-family:\"Syne\",sans-serif; font-size:0.85rem; font-weight:600; color:rgba(255,255,255,0.6);'>LIVE PREVIEW MOCKUP</div>", unsafe_allow_html=True)
            preview_display = wm_text if wm_text else "PREVIEW TEXT"
            st.markdown(f"""
            <div class="watermark-preview-card">
                <div class="watermark-preview-text" style="font-size: {min(fontsize, 44)}px; color: rgba(124, 58, 237, {opacity});">
                    {preview_display}
                </div>
                <div style="position: absolute; bottom: 12px; font-size: 0.7rem; color: rgba(255,255,255,0.3); text-transform: uppercase; letter-spacing: 0.1em;">
                    Mockup Page View
                </div>
            </div>
            """, unsafe_allow_html=True)

        if file and wm_text:
            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
            if st.button("💧  Apply Watermark"):
                with st.spinner("Stamping pages…"):
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                    tmp.write(file.read()); tmp.close()
                    out_path = add_watermark(tmp.name, wm_text, opacity=opacity, fontsize=fontsize)
                    os.unlink(tmp.name)

                    try:
                        reader = PdfReader(out_path)
                        pages_count = len(reader.pages)
                    except Exception:
                        pages_count = 1

                    st.session_state.stats["files_uploaded"] += 1
                    st.session_state.stats["pages_processed"] += pages_count
                    st.session_state.stats["operations_completed"] += 1

                    with open(out_path, "rb") as out:
                        st.download_button("⬇  Download Watermarked PDF", out,
                                           file_name="watermarked.pdf", mime="application/pdf")
                    success(f'"{wm_text}" watermark applied to all pages.')

        st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:5rem; padding:2rem 0 1rem; text-align:center;
            border-top:1px solid rgba(255,255,255,0.06);">
  <div style="font-family:'Syne',sans-serif; font-size:0.75rem; font-weight:600;
              letter-spacing:0.2em; text-transform:uppercase;
              color:rgba(255,255,255,0.25);">
    PDF Toolkit Pro · Built with Python & Streamlit · Portfolio Edition
  </div>
</div>
""", unsafe_allow_html=True)