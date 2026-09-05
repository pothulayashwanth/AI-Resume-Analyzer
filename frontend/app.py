import streamlit as st
import tempfile
import os
import sys
from pathlib import Path
from html import escape


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_PATH = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_PATH))

try:
    from analyzer import analyze_resume
except Exception as e:
    st.error(f"Could not load backend/analyzer.py: {e}")
    st.stop()

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown("""
<script>
window.addEventListener('load', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
</script>
""", unsafe_allow_html=True)

st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@300;400;600;700&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# Hide Streamlit Deploy button and three-dot menu
st.markdown("""
<style>
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
        html {
            color-scheme: dark;
        }

        *, *::before, *::after {
            font-family: 'Comfortaa', cursive, sans-serif !important;
            box-sizing: border-box;
            font-weight: 700 !important;
        }

        /* Hide Streamlit's native file list preview inside the dropzone */
        div[data-testid="stFileUploaderFileData"] {
            display: none !important;
        }

        body {
            min-height: 100vh;
        }

        .container-box {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2.5rem 1.5rem;
        }

        /* =========================================================
           FIX: CARDS SAME HEIGHT + SMALLER SIZE
           ========================================================= */
        .st-key-upload_card,
        .st-key-jobdesc_card {
            height: 100% !important;
            min-height: 280px !important;
            display: flex !important;
            flex-direction: column !important;
        }
                /* =========================================================
           FIX: Job Description - Wide + Clean Border (Matches Reference)
           ========================================================= */
        .st-key-jobdesc_card textarea {
            width: 100%;
            background-color: #130a21;
            color: #f3e8ff;
            border: 2px solid rgba(168, 85, 247, 0.3);
            border-radius: 20px;
            padding: 20px;
            font-size: 0.95rem;
            line-height: 1.6;
            outline: none;
            transition: all 0.3s ease;
            resize: vertical;
            min-height: 140px;
            box-sizing: border-box;
            word-wrap: break-word;
            overflow-wrap: break-word;
            white-space: pre-wrap;
        }

        .st-key-jobdesc_card textarea:focus {
            border-color: #c084fc !important;
            box-shadow: 0 0 0 4px rgba(168, 85, 247, 0.3) !important;
            background-color: #180d29 !important;
        }

        .st-key-jobdesc_card textarea::placeholder {
            color: #6b5b8a !important;
            font-weight: 600 !important;
        }

        .st-key-upload_card > div,
        .st-key-jobdesc_card > div {
            background-color: #1a0f2e !important;
            border: 2px solid rgba(168, 85, 247, 0.35) !important;
            border-radius: 24px !important;
            padding: 18px 16px 14px !important;
            box-shadow: 0 12px 32px rgba(13, 7, 20, 0.55);
            transition: all 0.3s ease;
            height: 100% !important;
            min-height: 280px !important;
            display: flex !important;
            flex-direction: column !important;
        }

        .st-key-upload_card > div:hover,
        .st-key-jobdesc_card > div:hover {
            border-color: rgba(192, 132, 252, 0.6) !important;
            box-shadow: 0 18px 40px rgba(168, 85, 247, 0.2) !important;
        }

        /* Make inner containers fill the card */
        .st-key-upload_card [data-testid="stVerticalBlock"],
        .st-key-jobdesc_card [data-testid="stVerticalBlock"] {
            flex: 1 !important;
            display: flex !important;
            flex-direction: column !important;
        }

        /* =========================================================
           FIX: BOTH DROPZONE AND TEXTAREA SAME SIZE
           ========================================================= */
        .st-key-upload_card [data-testid="stFileUploader"],
        .st-key-jobdesc_card [data-testid="stTextArea"] {
            flex: 0 0 auto !important;
            display: flex !important;
            flex-direction: column !important;
        }

        /* Dropzone */
        [data-testid="stFileUploaderDropzone"] {
            min-height: 140px !important;
            max-height: 160px !important;
            padding: 12px 16px !important;
        }

        /* Textarea - MATCH DROPZONE SIZE */
        .st-key-jobdesc_card [data-testid="stTextArea"] textarea {
    min-height: 140px !important;
    height: 160px !important;
    padding: 16px 20px !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    max-width: 100% !important;
    resize: vertical !important;
    box-sizing: border-box !important;
}
/* Make textarea container fill the card */
.st-key-jobdesc_card [data-testid="stTextArea"] {
    width: 100% !important;
    display: flex !important;
    flex-direction: column !important;
}

.st-key-jobdesc_card [data-testid="stTextArea"] > div {
    width: 100% !important;
    flex: 1 !important;
}

                /* =========================================================
           FIX: DROPZONE - Centered vertically
           ========================================================= */
        [data-testid="stFileUploaderDropzone"] {
            position: relative !important;
            background: #130a21 !important;
            border: 2px dashed rgba(168, 85, 247, 0.4) !important;
            border-radius: 22px !important;
            padding: 12px 16px !important;
            transition: all 0.3s ease !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            flex-direction: column !important;
        }

        [data-testid="stFileUploaderDropzone"]:hover {
            border-color: #c084fc !important;
            background: #21133b !important;
        }

        [data-testid="stFileUploaderDropzone"] > * {
            opacity: 0 !important;
        }

        /* Icon - Centered */
        [data-testid="stFileUploaderDropzone"]::before {
            content: "📄";
            position: absolute;
            top: 50% !important;
            left: 0;
            right: 0;
            text-align: center;
            transform: translateY(-50%) !important;
            font-size: 20px !important;
            margin-top: -14px !important;
        }

        /* Text - Centered below icon */
        [data-testid="stFileUploaderDropzone"]::after {
            content: "Click or drag PDF resume here\nRecommended size: under 20MB";
            white-space: pre-line;
            position: absolute;
            top: 50% !important;
            left: 0;
            right: 0;
            text-align: center;
            transform: translateY(-50%) !important;
            font-size: 0.7rem !important;
            color: #f3e8ff;
            font-weight: 400 !important;
            line-height: 1.4 !important;
            margin-top: 18px !important;
        }

        /* =========================================================
           STACK IMMEDIATELY ON ZOOM
           ========================================================= */
        div[data-testid="stHorizontalBlock"] {
            gap: 1.5rem !important;
        }

        div[data-testid="column"] {
            flex: 1 1 0 !important;
            flex-basis: 0 !important;
        }

        /* STACK at 101% zoom or any zoom */
        @media (max-width: 1100px) {
            div[data-testid="stHorizontalBlock"] {
                flex-wrap: wrap !important;
                gap: 1.5rem !important;
            }
            
            div[data-testid="column"] {
                min-width: 100% !important;
                flex: 0 0 100% !important;
                max-width: 100% !important;
            }
        }
        

        /* Keep chip + remove button aligned */

                .st-key-upload_card [data-testid="column"]:last-child {
            flex: 0 0 32px !important;
            min-width: 32px !important;
            max-width: 32px !important;
            width: 32px !important;
            padding-right: 0 !important;
            margin-right: 8px !important;
        }

        /* Add padding to the card to prevent button hitting border */
        .st-key-upload_card > div {
            padding-right: 32px !important;
        }

        .st-key-upload_card [data-testid="stHorizontalBlock"] {
            padding-right: 24px !important;
            margin-right: 0 !important;
            gap:2px;
        }

        /* Remove button styling - SMALLER */
        .st-key-remove_resume_btn button {
            width: 26px !important;
            height: 26px !important;
            min-width: 26px !important;
            max-width: 26px !important;
            min-height: 26px !important;
            max-height: 26px !important;
            aspect-ratio: 1 / 1 !important;
            padding: 0 !important;
            margin: 0 4px 0 0 !important;
            border-radius: 50% !important;
            background: rgba(244, 63, 94, 0.2) !important;
            color: #fb7185 !important;
            border: 1.5px solid rgba(244, 63, 94, 0.5) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-weight: bold !important;
            line-height: 1 !important;
            flex-shrink: 0 !important;
            font-size: 0.6rem !important;
        }

        .st-key-upload_card [data-testid="stHorizontalBlock"] {
                    align-items: center !important;
                    flex-wrap: nowrap !important;
        }

        .st-key-upload_card [data-testid="stHorizontalBlock"] [data-testid="column"]:last-child {
            margin-left: 0px !important;
        }

        .st-key-upload_card [data-testid="stHorizontalBlock"] [data-testid="column"] {
            display: flex !important;
            align-items: center !important;
        }

        .st-key-remove_resume_btn button:hover {
            background: rgba(244, 63, 94, 0.4) !important;
            color: #ffffff !important;
            border-color: #f43f5e !important;
        }

        /* Strip Streamlit's own auto-styling from nested elements */
        .st-key-upload_card [data-testid="stVerticalBlock"],
        .st-key-upload_card [data-testid="stElementContainer"],
        .st-key-upload_card [data-testid="element-container"],
        .st-key-upload_card [data-testid="stHorizontalBlock"],
        .st-key-jobdesc_card [data-testid="stVerticalBlock"],
        .st-key-jobdesc_card [data-testid="stElementContainer"],
        .st-key-jobdesc_card [data-testid="element-container"],
        .st-key-jobdesc_card [data-testid="stHorizontalBlock"] {
            background: transparent !important;
            border: none !important;
            border-radius: 0 !important;
            box-shadow: none !important;
        }

        .st-key-upload_card [data-testid="stHorizontalBlock"] [data-testid="element-container"],
        .st-key-upload_card [data-testid="stHorizontalBlock"] [data-testid="stElementContainer"] {
            margin: 0 !important;
            padding: 0 !important;
        }

        .st-key-upload_card [data-testid="stHorizontalBlock"] [data-testid="stButton"] {
            margin: 0 !important;
        }

        .st-key-upload_inner > div,
        .st-key-jobdesc_inner > div {
            border: 2px solid rgba(168, 85, 247, 0.6) !important;
            border-radius: 20px !important;
            padding: 14px 16px !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        /* Remove grey outer border from textarea container */
div[data-testid="stTextArea"] div[data-baseweb="textarea"] {
    border: none !important;
    border-color: transparent !important;
    outline: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

/* Remove any extra container borders */
.st-key-jobdesc_card [data-testid="stTextArea"] {
    border: none !important;
    background: transparent !important;
}

.st-key-jobdesc_card [data-testid="stTextArea"] > div {
    border: none !important;
    background: transparent !important;
}

        /* =========================================================
           FIX: Input titles smaller
           ========================================================= */
        .input-title {
            color: #ffffff;
            font-size: 0.9rem !important;
            font-weight: 700;
            margin-bottom: 2px !important;
        }

        .input-description {
            color: #c084fc;
            font-size: 0.65rem !important;
            line-height: 1.3 !important;
            margin-bottom: 6px !important;
        }

        /* Hero Container Header */
        .hero-banner {
            background: linear-gradient(135deg, rgba(35, 16, 56, 0.95) 0%, rgba(55, 23, 89, 0.9) 100%);
            border: 2px solid rgba(168, 85, 247, 0.4);
            border-radius: 28px;
            padding: 42px 32px;
            text-align: center;
            box-shadow: 0 20px 50px rgba(13, 7, 20, 0.8), inset 0 1px 1px rgba(255, 255, 255, 0.15);
            margin-bottom: 32px;
            transition: all 0.3s ease;
        }

        .hero-banner:hover {
            border-color: rgba(192, 132, 252, 0.7);
            box-shadow: 0 22px 55px rgba(168, 85, 247, 0.25);
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(168, 85, 247, 0.2);
            border: 1.5px solid rgba(192, 132, 252, 0.5);
            color: #e9d5ff;
            padding: 8px 20px;
            border-radius: 9999px;
            font-size: 0.85rem;
            margin-bottom: 16px;
        }

        .hero-banner h1 {
            font-size: 2.75rem;
            color: #ffffff;
            margin-bottom: 12px;
        }

        .hero-banner p {
            color: #c084fc;
            font-size: 1.05rem;
            max-width: 650px;
            margin: 0 auto;
        }

        .section-header {
            font-size: 1.35rem;
            color: #ffffff;
            margin-top: 40px;
            margin-bottom: 24px;
            padding-bottom: 12px;
            border-bottom: 2px solid rgba(168, 85, 247, 0.25);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .dark-card {
            background-color: #1a0f2e;
            border: 2px solid rgba(168, 85, 247, 0.25);
            border-radius: 24px;
            padding: 28px;
            box-shadow: 0 12px 32px rgba(13, 7, 20, 0.6);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            height: 100%;
            display: flex;
            flex-direction: column;
        }

        .dark-card:hover {
            border-color: rgba(192, 132, 252, 0.6);
            box-shadow: 0 18px 40px rgba(168, 85, 247, 0.2);
        }

        textarea {
            width: 100%;
            background-color: #130a21;
            color: #f3e8ff;
            border: 2px solid rgba(168, 85, 247, 0.3);
            border-radius: 20px;
            padding: 20px;
            font-size: 0.95rem;
            line-height: 1.6;
            outline: none;
            transition: all 0.3s ease;
            resize: vertical;
            min-height: 160px;
            box-sizing: border-box;
            word-wrap: nowrap;
            overflow-wrap: break-word;
            white-space: pre-wrap;
        }

        textarea:focus {
            border-color: #c084fc;
            box-shadow: 0 0 0 4px rgba(168, 85, 247, 0.3);
            background-color: #180d29;
        }

        .btn-analyze {
            width: 100%;
            background: linear-gradient(135deg, #9333ea 0%, #7e22ce 50%, #581c87 100%);
            color: #ffffff;
            font-size: 1.15rem;
            padding: 18px;
            border-radius: 9999px;
            border: 2px solid rgba(192, 132, 252, 0.5);
            box-shadow: 0 10px 30px rgba(147, 51, 234, 0.4);
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .btn-analyze:hover {
            transform: translateY(-3px) scale(1.005);
            box-shadow: 0 15px 35px rgba(168, 85, 247, 0.6);
            background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
        }

        .score-visual-container {
            background: radial-gradient(circle, rgba(147, 51, 234, 0.25) 0%, rgba(26, 15, 46, 0.95) 70%);
            border: 2px solid rgba(168, 85, 247, 0.4);
            border-radius: 32px;
            padding: 40px;
            text-align: center;
            margin-bottom: 28px;
            box-shadow: 0 16px 40px rgba(13, 7, 20, 0.7);
            transition: all 0.3s ease;
        }

        .score-visual-container:hover {
            border-color: rgba(192, 132, 252, 0.7);
            box-shadow: 0 20px 45px rgba(168, 85, 247, 0.3);
        }

        .score-circle-main {
            width: 160px;
            height: 160px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            box-shadow: 0 0 35px rgba(168, 85, 247, 0.4);
            transition: transform 0.3s ease;
        }

        .score-circle-main:hover {
            transform: scale(1.05);
        }

        .score-circle-inner {
            width: 132px;
            height: 132px;
            border-radius: 50%;
            background: #130a21;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 12px;
            text-align: center;
        }
        .main-score-value {
            font-size: 2rem !important;
            line-height: 1 !important;
            color: #ffffff !important;
            display: block;
            white-space: nowrap;
            margin-bottom: 6px;
        }

        .sub-score-circle {
            width: 90px;
            height: 90px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 12px;
            box-shadow: 0 0 18px rgba(168, 85, 247, 0.25);
            transition: transform 0.3s ease;
        }

        .sub-score-inner {
            width: 74px;
            height: 74px;
            border-radius: 50%;
            background: #130a21;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .score-card {
            background: #1a0f2e;
            border: 2px solid rgba(168, 85, 247, 0.25);
            border-radius: 24px;
            padding: 22px 16px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .score-card:hover {
            border-color: rgba(192, 132, 252, 0.6);
            box-shadow: 0 10px 25px rgba(168, 85, 247, 0.25);
        }

        .skill-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 10px 20px;
            border-radius: 9999px;
            font-size: 0.88rem;
            margin: 5px;
            transition: all 0.25s ease;
        }

        .badge-match {
            background-color: rgba(34, 197, 94, 0.15);
            color: #4ade80;
            border: 1.5px solid rgba(34, 197, 94, 0.4);
        }

        .badge-match:hover {
            background-color: rgba(34, 197, 94, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2);
        }

        .badge-missing {
            background-color: rgba(244, 63, 94, 0.15);
            color: #fb7185;
            border: 1.5px solid rgba(244, 63, 94, 0.35);
        }

        .badge-missing:hover {
            background-color: rgba(244, 63, 94, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(244, 63, 94, 0.2);
        }

        .rec-card {
            border-radius: 24px;
            padding: 24px 28px;
            margin-bottom: 20px;
            border: 2px solid;
            background-color: #1a0f2e;
            box-shadow: 0 8px 24px rgba(13, 7, 20, 0.5);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .rec-card:hover {
            box-shadow: 0 16px 36px rgba(168, 85, 247, 0.25);
        }

        .rec-high {
            border-color: rgba(244, 63, 94, 0.6);
            background: linear-gradient(90deg, rgba(244, 63, 94, 0.12) 0%, #1a0f2e 100%);
        }

        .rec-medium {
            border-color: rgba(245, 158, 11, 0.6);
            background: linear-gradient(90deg, rgba(245, 158, 11, 0.12) 0%, #1a0f2e 100%);
        }

        .rec-low {
            border-color: rgba(168, 85, 247, 0.6);
            background: linear-gradient(90deg, rgba(168, 85, 247, 0.12) 0%, #1a0f2e 100%);
        }
        .rec-important {
            border-color: rgba(59, 130, 246, 0.6);
            background: linear-gradient(90deg, rgba(59, 130, 246, 0.12) 0%, #1a0f2e 100%);
        }

        @media (max-width: 640px) {
            .container-box { padding: 1.25rem 0.85rem; }
            .hero-banner { padding: 28px 18px; border-radius: 22px; }
            .hero-banner h1 { font-size: 1.95rem; }
            .dark-card { padding: 20px 16px; border-radius: 20px; }
            textarea { padding: 16px; min-height: 140px; }
            .score-circle-main { width: 130px; height: 130px; }
            .score-circle-inner { width: 106px; height: 106px; }
        }

        /* STREAMLIT UI OVERRIDES */

        .stApp {
            background: #0d0714 !important;
        }

        .main .block-container {
            max-width: 1200px !important;
            padding: 2.5rem 1.5rem !important;
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
        }

                /* ===== FILE UPLOADER — version-proof approach ===== */
        [data-testid="stFileUploaderDropzone"] {
            position: relative !important;
            background: #130a21 !important;
            border: 2px dashed rgba(168, 85, 247, 0.4) !important;
            border-radius: 22px !important;
            min-height: 125px !important;
            padding: 32px 20px !important;
            transition: all 0.3s ease !important;
        }
        [data-testid="stFileUploaderDropzone"]:hover {
            border-color: #c084fc !important;
            background: #21133b !important;
        }
        [data-testid="stFileUploaderDropzone"] > * {
            opacity: 0 !important;
        }
        [data-testid="stFileUploaderDropzone"]::before {
            content: "⬆";
            position: absolute; top: 28px; left: 0; right: 0;
            text-align: center; font-size: 26px; color: #c084fc;
        }
        [data-testid="stFileUploaderDropzone"]::after {
            content: "Click or drag PDF resume here";
            position: absolute; top: 66px; left: 0; right: 0;
            text-align: center; font-size: 0.85rem; color: #f3e8ff; font-weight: 700;
        }

        [data-testid*="FileUploaderFile"] {
            display: none !important;
        }

    .st-key-remove_resume_btn button {
    width: 32px !important;
    height: 32px !important;
    min-width: 32px !important;
    max-width: 32px !important;
    min-height: 32px !important;
    max-height: 32px !important;
    padding: 0 !important;
    margin: 0 !important;
    border-radius: 50% !important;
    background: rgba(244, 63, 94, 0.15) !important;
    color: #fb7185 !important;
    border: 1.5px solid rgba(244, 63, 94, 0.4) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-weight: bold !important;
    font-size: 0.6rem !important;
    cursor: pointer !important;
    flex-shrink: 0 !important;
    transition: all 0.3s ease !important;
    line-height: 1 !important;
}
        .st-key-remove_resume_btn button:hover {
            background: rgba(244, 63, 94, 0.4) !important;
            color: #ffffff !important;
            border-color: #f43f5e !important;
            transform: scale(1.1) !important;
        }

        div[data-testid="stTextArea"] div[data-baseweb="textarea"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        /* Remove Streamlit's "Press Enter/Ctrl+Enter to apply" hint */
div[data-testid="stTextArea"] [data-testid="InputInstructions"] {
    display: none !important;
}

div[data-testid="stTextArea"] div[data-baseweb="textarea"]:focus-within {
    border-color: #c084fc !important;
    box-shadow: 0 0 0 4px rgba(168, 85, 247, 0.3) !important;
    outline: none !important;
}

        .stTextArea textarea {
            background: #130a21 !important;
            color: #f3e8ff !important;
            border: 2px solid rgba(168, 85, 247, 0.3) !important;
            border-radius: 20px !important;
            padding: 20px !important;
            font-family: 'Comfortaa', cursive, sans-serif !important;
            font-weight: 700 !important;
        }

        .stTextArea textarea:focus {
            border-color: #c084fc !important;
            box-shadow: 0 0 0 4px rgba(168, 85, 247, 0.3) !important;
        }

        .stButton > button {
            width: 100% !important;
            background: linear-gradient(135deg, #9333ea 0%, #7e22ce 50%, #581c87 100%) !important;
            color: #ffffff !important;
            font-family: 'Comfortaa', cursive, sans-serif !important;
            font-weight: 700 !important;
            font-size: 1.15rem !important;
            padding: 18px !important;
            min-height: 60px !important;
            border-radius: 9999px !important;
            border: 2px solid rgba(192, 132, 252, 0.5) !important;
            box-shadow: 0 10px 30px rgba(147, 51, 234, 0.4) !important;
        }

        .stButton > button:hover {
            transform: translateY(-3px) scale(1.005) !important;
            box-shadow: 0 15px 35px rgba(168, 85, 247, 0.6) !important;
            background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%) !important;
            color: #ffffff !important;
        }

        .stDownloadButton > button {
            width: 100% !important;
            background: #1a0f2e !important;
            color: #e9d5ff !important;
            border: 2px solid rgba(168, 85, 247, 0.4) !important;
            border-radius: 9999px !important;
            font-family: 'Comfortaa', cursive, sans-serif !important;
            font-weight: 700 !important;
        }

        .stDownloadButton > button:hover {
            border-color: #c084fc !important;
            background: #21133b !important;
            color: #ffffff !important;
        }

        .stCaption {
            color: #c084fc !important;
        }

        [data-testid="stAlert"] {
            background: #1a0f2e !important;
            border-radius: 18px !important;
        }

        div[data-testid="stVerticalBlock"] {
            gap: 0.5rem;
        }

        .footer {
            text-align: center;
            margin-top: 50px;
            padding: 25px;
            color: #c084fc;
            font-size: 0.8rem;
            border-top: 1px solid rgba(168, 85, 247, 0.2);
        }

        div[data-testid="column"] {
            min-width: 0 !important;
        }

        .analyze-container {
            width: 100% !important;
            margin-top: 22px !important;
            margin-bottom: 15px !important;
        }

        /* Scroll Reveal Animations */
        .reveal-left, .reveal-right, .reveal-up {
            opacity: 0;
            animation-duration: 1.2s;
            animation-timing-function: cubic-bezier(0.22, 1, 0.36, 1);
            animation-fill-mode: both;
            animation-timeline: view();
            animation-range: entry 0% cover 35%;
        }
        .reveal-left { animation-name: slideFromLeft; }
        .reveal-right { animation-name: slideFromRight; }
        .reveal-up { animation-name: slideFromBottom; }

        @keyframes slideFromLeft {
            from { opacity: 0; transform: translateX(-120px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes slideFromRight {
            from { opacity: 0; transform: translateX(120px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes slideFromBottom {
            from { opacity: 0; transform: translateY(80px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 768px) {
            div[data-testid="stFileUploader"] section { min-height: 115px !important; }
            div[data-testid="stTextArea"] textarea { min-height: 115px !important; }
        }
</style>
""", unsafe_allow_html=True)

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

if "resume_bytes" not in st.session_state:
    st.session_state.resume_bytes = None

if "scroll_to_analytics" not in st.session_state:
    st.session_state.scroll_to_analytics = False

if "resume_name" not in st.session_state:
    st.session_state.resume_name = None

if "job_description" not in st.session_state:
    st.session_state.job_description = ""


def reset_app():
    st.session_state.analysis_results = None
    st.session_state.resume_bytes = None
    st.session_state.resume_name = None
    st.session_state.job_description = ""
    if "resume_uploader" in st.session_state:
        st.session_state.resume_uploader = None
    if "job_description_box" in st.session_state:
        st.session_state.job_description_box = ""
    st.rerun()

def safe_num(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def badge_html(items, css_class, icon):
    if not items:
        return '<span style="color:#c084fc;">None detected.</span>'
    return "".join(
        f'<span class="skill-badge {css_class}">{icon} {escape(str(item))}</span>'
        for item in items
    )


st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">✦ AI-Powered Resume Analysis</div>
    <h1>AI Resume Analyzer</h1>
    <p>Optimize your resume. Align with the job role. Get Shortlisted.</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.analysis_results is None:

    st.markdown(
        '<div class="section-header">📌 Input Documents</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2, gap="large")

    with left:
        with st.container(key="upload_card"):
            with st.container(border=True, key="upload_inner"):
                st.markdown(
                    """
                    <div class="input-title">📄 Upload Your Resume</div>
                    <div class="input-description" style="margin-bottom:0;">
                        Upload your document in PDF format to get analysis (20mb max).
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # ============================================================
                # FIX: Show dropzone OR file chip (mutually exclusive)
                # ============================================================
                if not st.session_state.resume_bytes:
                    uploaded_file = st.file_uploader(
                        "Click or drag PDF resume here",
                        type=["pdf"],
                        key="resume_uploader",
                        label_visibility="collapsed"
                    )
                    if uploaded_file is not None:
                        st.session_state.resume_bytes = uploaded_file.getvalue()
                        st.session_state.resume_name = uploaded_file.name
                        st.rerun()  # ← NEEDED: Refresh UI to show file chip
                else:
                    # ============================================================
                    # FILE CHIP - ✕ button beside the pill
                    # ============================================================
                    size_mb = len(st.session_state.resume_bytes) / (1024 * 1024)

                    def clear_uploaded_file():
                        st.session_state.resume_bytes = None
                        st.session_state.resume_name = None
                        if "resume_uploader" in st.session_state:
                            del st.session_state["resume_uploader"]
                        #st.rerun() #here - callback handles it

                    # Center the chip using flexbox
                    st.markdown(
                        """
                        <div style="display:flex; align-items:center; justify-content:center; 
                                    width:100%; padding:6px 0;">
                        """,
                        unsafe_allow_html=True
                    )

                    # Use columns with proper alignment
                    chip_col1, chip_col2 = st.columns([9, 1], gap="small")

                    with chip_col1:
                        st.markdown(
                            f"""
                            <div style="display:flex; align-items:center; gap:8px; padding:4px 16px; 
                                        background:rgba(88,28,135,0.25); 
                                        border:1.5px solid rgba(168,85,247,0.5); 
                                        border-radius:9999px; 
                                        width:100%; 
                                        height:36px;
                                        margin-top: -15px;">
                                <span style="color:#e9d5ff; font-size:0.8rem; 
                                             display:flex; align-items:center; gap:6px;
                                             white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                                    <span>📄</span>
                                    <strong>{escape(st.session_state.resume_name or "Resume.pdf")}</strong>
                                    <span style="color:#c084fc; font-size:0.7rem; flex-shrink:0;">({size_mb:.2f} MB)</span>
                                </span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with chip_col2:
                        # Button perfectly aligned beside the pill
                        st.button(
                            "✕",
                            key="remove_resume_btn",
                            help="Remove uploaded resume",
                            on_click=clear_uploaded_file,
                            type="secondary"
                        )

                    st.markdown("</div>", unsafe_allow_html=True)

    with right:
        with st.container(key="jobdesc_card"):
            with st.container(border=True, key="jobdesc_inner"):
                st.markdown(
                    """
                    <div class="input-title">📝 Target Job Description</div>
                    <div class="input-description" style="margin-bottom:0;">
                        Paste full target job specs below.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # ============================================================
                # FIX: Job Description - WIDER + PROPER BORDER
                # ============================================================
                job_description = st.text_area(
                    "Job Description",
                    value=st.session_state.job_description,
                    placeholder="Paste full target job requirements here...",
                    height=180,
                    key="job_description_box",
                    label_visibility="collapsed"
                )
                st.session_state.job_description = job_description

    st.markdown('<div class="analyze-container">', unsafe_allow_html=True)

    analyze_clicked = st.button(
        "✦ Analyze My Resume",
        key="analyze_button",
        type="primary",
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

    if analyze_clicked:

        if not st.session_state.resume_bytes:
            st.error("Please upload your resume PDF.")

        elif not st.session_state.job_description.strip():
            st.error("Please enter the job description.")

        else:
            temp_path = None
            try:
                with st.spinner("Analyzing your resume..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
                        temp.write(st.session_state.resume_bytes)
                        temp_path = temp.name

                    results = analyze_resume(temp_path, st.session_state.job_description)

                st.session_state.analysis_results = results
                st.session_state.scroll_to_analytics = True
                st.rerun() #- Streamlit handles this automatically

            except Exception as e:
                st.error(f"Analysis failed: {e}")

            finally:
                if temp_path and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except OSError:
                        pass

else:

    results = st.session_state.analysis_results

    if st.session_state.get("scroll_to_analytics", False):
        st.session_state.scroll_to_analytics = False
        st.markdown("""
        <script>
        setTimeout(function() {
            const doc = window.parent.document;
            const analytics = doc.getElementById("analytics-section");
            if (analytics) {
                analytics.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        }, 300);
        </script>
        """, unsafe_allow_html=True)

    overall = safe_num(results.get("overall_score"))
    ats = safe_num(results.get("ats_score"))
    skill = safe_num(results.get("skill_match_score"))
    content = safe_num(results.get("content_score"))

    matched = results.get("matched_skills", []) or []
    missing = results.get("missing_skills", []) or []
    recommendations = results.get("priority_recommendations", []) or []

    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 24px;">
            <span style="
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 10px 24px;
                border-radius: 9999px;
                font-size: 0.88rem;
                background: rgba(34, 197, 94, 0.15);
                color: #4ade80;
                border: 1.5px solid rgba(34, 197, 94, 0.4);
                box-shadow: 0 8px 20px rgba(34, 197, 94, 0.15);
            ">
                ✦ Analysis completed successfully
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div id="analytics-section"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Analytics & Evaluation Dashboard</div>', unsafe_allow_html=True)

    overall_percentage = max(0, min(overall, 100))

    if overall >= 80:
        match_text, bg_color, text_color, border_color, shadow_color = (
            "✦ Excellent Match", "rgba(16, 185, 129, 0.2)", "#6ee7b7", "rgba(16, 185, 129, 0.4)", "rgba(16, 185, 129, 0.12)"
        )
    elif overall >= 65:
        match_text, bg_color, text_color, border_color, shadow_color = (
            "✦ Good Match", "rgba(59, 130, 246, 0.2)", "#93c5fd", "rgba(59, 130, 246, 0.4)", "rgba(59, 130, 246, 0.12)"
        )
    elif overall >= 50:
        match_text, bg_color, text_color, border_color, shadow_color = (
            "✦ Moderate Match", "rgba(245, 158, 11, 0.2)", "#fcd34d", "rgba(245, 158, 11, 0.4)", "rgba(245, 158, 11, 0.12)"
        )
    else:
        match_text, bg_color, text_color, border_color, shadow_color = (
            "✦ Needs Improvement", "rgba(244, 63, 94, 0.2)", "#fda4af", "rgba(244, 63, 94, 0.4)", "rgba(244, 63, 94, 0.12)"
        )

    main_score_html = f"""<div class="score-visual-container">
<div class="score-circle-main" style="background:conic-gradient(#a855f7 0%, #c084fc {overall_percentage}%, #2e1065 {overall_percentage}%);">
<div class="score-circle-inner">
<span class="main-score-value">{overall:.2f}</span>
<span style="font-size: 0.75rem; color: #c084fc;">/ 100</span>
</div>
</div>
<div>
<span style="display:inline-block; padding:8px 24px; border-radius:9999px; font-size:.875rem; background:{bg_color}; color:{text_color}; border:2px solid {border_color}; box-shadow:0 10px 20px {shadow_color};">{match_text}</span>
</div>
</div>"""
    st.markdown(main_score_html, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="large")
    score_data = [
        (c1, ats, "ATS Compatibility"),
        (c2, skill, "Skill Match Score"),
        (c3, content, "Content Quality")
    ]
    animations = ["reveal-left", "reveal-up", "reveal-right"]

    for (col, value, label), animation in zip(score_data, animations):
        percentage = max(0, min(value, 100))
        card_html = f"""<div class="score-card {animation}">
<div class="sub-score-circle" style="background:conic-gradient(#a855f7 0%, #c084fc {percentage}%, #2e1065 {percentage}%);">
<div class="sub-score-inner">
<span style="font-size: 1.125rem; color: #ffffff;">{value:.2f}%</span>
</div>
</div>
<div style="font-size: 0.75rem; color: #c084fc; text-transform: uppercase;">{label}</div>
</div>"""
        col.markdown(card_html, unsafe_allow_html=True)

    st.markdown('<div class="section-header">🎯 Skill Alignment</div>', unsafe_allow_html=True)

    s1, s2 = st.columns(2, gap="large")

    with s1:
        st.markdown(f"""<div class="dark-card reveal-left">
<h3 style="color: #34d399; font-size: 1.125rem; margin-bottom: 1rem;">✓ Matched Skills</h3>
<div>{badge_html(matched, "badge-match", "✓")}</div>
</div>""", unsafe_allow_html=True)

    with s2:
        st.markdown(f"""<div class="dark-card reveal-right">
<h3 style="color: #fb7185; font-size: 1.125rem; margin-bottom: 1rem;">✕ Missing Key Skills</h3>
<div>{badge_html(missing, "badge-missing", "✕")}</div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">💡 Actionable Improvements</div>', unsafe_allow_html=True)

    if not recommendations:
        recommendations = [{
            "priority": "LOW",
            "category": "Overall",
            "message": "No additional recommendations were generated."
        }]

    for rec in recommendations:
        priority = str(rec.get("priority", "LOW")).upper()
        category = escape(str(rec.get("category", "General")))
        message = escape(str(rec.get("message", "")))

        css = {"HIGH": "rec-high", "MEDIUM": "rec-medium", "IMPORTANT": "rec-important"}.get(priority, "rec-low")
        badge = {"HIGH": "CRITICAL", "MEDIUM": "RECOMMENDED", "IMPORTANT": "IMPORTANT"}.get(priority, "OPTIONAL")

        if priority == "HIGH":
            title_color, badge_color, badge_text, border_color = "#fecdd3", "rgba(244,63,94,.2)", "#fda4af", "rgba(244,63,94,.4)"
        elif priority == "MEDIUM":
            title_color, badge_color, badge_text, border_color = "#fde68a", "rgba(245,158,11,.2)", "#fcd34d", "rgba(245,158,11,.4)"
        elif priority == "IMPORTANT":
            title_color, badge_color, badge_text, border_color = "#bfdbfe", "rgba(59,130,246,.2)", "#93c5fd", "rgba(59,130,246,.4)"
        else:
            title_color, badge_color, badge_text, border_color = "#e9d5ff", "rgba(168,85,247,.2)", "#c084fc", "rgba(168,85,247,.4)"

        rec_html = f"""<div class="rec-card {css} reveal-up">
<div style="display:flex; align-items:center; gap:12px; margin-bottom:8px; flex-wrap:wrap;">
<span style="padding:4px 12px; border-radius:9999px; font-size:.75rem; background:{badge_color}; color:{badge_text}; border:1px solid {border_color};">{badge}</span>
<h3 style="color:{title_color}; font-size:1rem; margin:0;">{category}</h3>
</div>
<p style="color:#f3e8ff; font-size:.875rem; line-height:1.6; margin:0;">{message}</p>
</div>"""
        st.markdown(rec_html, unsafe_allow_html=True)

    st.markdown('<div class="section-header">🚀 Next Steps</div>', unsafe_allow_html=True)

    report = [
        "AI RESUME ANALYZER REPORT", "=" * 30,
        f"Resume: {st.session_state.resume_name or 'Resume'}", "",
        f"Overall Score: {overall:.2f}/100",
        f"ATS Compatibility: {ats:.2f}%",
        f"Skill Match: {skill:.2f}%",
        f"Content Quality: {content:.2f}%", "",
        "MATCHED SKILLS", *[f"- {x}" for x in matched], "",
        "MISSING SKILLS", *[f"- {x}" for x in missing], "",
        "RECOMMENDATIONS"
    ]
    for rec in recommendations:
        report.append(f"- [{rec.get('priority', 'LOW')}] {rec.get('category', 'General')}: {rec.get('message', '')}")

    # ============================================================
    # FIX: Generate proper PDF report
    # ============================================================
    from fpdf import FPDF
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "AI RESUME ANALYZER REPORT", ln=True, align="C")
    pdf.line(10, 20, 200, 20)
    pdf.ln(10)
    
    # Resume name
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Resume: {st.session_state.resume_name or 'Resume'}", ln=True)
    pdf.ln(5)
    
    # Scores
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, f"Overall Score: {overall:.2f}/100", ln=True)
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"ATS Compatibility: {ats:.2f}%", ln=True)
    pdf.cell(0, 8, f"Skill Match: {skill:.2f}%", ln=True)
    pdf.cell(0, 8, f"Content Quality: {content:.2f}%", ln=True)
    pdf.ln(8)
    
    # Matched Skills
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "MATCHED SKILLS", ln=True)
    pdf.set_font("Helvetica", "", 12)
    for skill in matched:
        pdf.cell(0, 8, f"  - {skill}", ln=True)
    pdf.ln(5)
    
    # Missing Skills
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "MISSING SKILLS", ln=True)
    pdf.set_font("Helvetica", "", 12)
    for skill in missing:
        pdf.cell(0, 8, f"  - {skill}", ln=True)
    pdf.ln(5)
    
    # Recommendations
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "RECOMMENDATIONS", ln=True)
    pdf.set_font("Helvetica", "", 12)
    for rec in recommendations:
        pdf.cell(0, 8, f"  - [{rec.get('priority', 'LOW')}] {rec.get('category', 'General')}: {rec.get('message', '')}", ln=True)
    
    # Get PDF bytes
    pdf_bytes = bytes(pdf.output(dest='S'))
    
    a1, a2 = st.columns(2, gap="large")
    
    with a1:
        st.download_button(
            "📥 Download Analysis Report",
            data=pdf_bytes,
            file_name="AI_Resume_Analysis_Report.pdf",
            mime="application/pdf",
            key="download_report",
            use_container_width=True,
            type="primary"
        )
    
    with a2:
        if st.button("🔄 Analyze Another Resume", key="another_resume",use_container_width=True,type="primary"):
            reset_app()
            st.markdown("""
        <script>
        setTimeout(function() {
            window.parent.scrollTo({ top: 0, behavior: 'smooth' });
        }, 300);
        </script>
        """, unsafe_allow_html=True)
            #st.rerun()
