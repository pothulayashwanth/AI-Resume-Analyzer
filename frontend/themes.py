# themes.py - Light/Dark Mode with Proper Colors

import streamlit as st

# ============================================================
# INITIALIZE THEME
# ============================================================
def init_theme():
    """Initialize theme session state"""
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True


def toggle_theme():
    """Toggle between dark and light mode"""
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()


# ============================================================
# THEME TOGGLE - TOP RIGHT CORNER
# ============================================================
def theme_toggle_top_right():
    """Display working theme toggle at top right corner"""
    
    st.markdown("""
    <style>
    .theme-toggle-container {
        position: fixed;
        top: 20px;
        right: 30px;
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(26, 15, 46, 0.7);
        padding: 6px 14px 6px 16px;
        border-radius: 9999px;
        border: none !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    .theme-toggle-container .icon {
        font-size: 1rem;
        line-height: 1;
        opacity: 0.5;
        user-select: none;
    }
    .theme-toggle-container .icon.active {
        opacity: 1;
    }
    .theme-toggle-container .toggle-switch {
        position: relative;
        width: 36px;
        height: 20px;
        cursor: pointer;
        display: inline-block;
    }
    .theme-toggle-container .toggle-switch input {
        opacity: 0;
        width: 0;
        height: 0;
        position: absolute;
    }
    .theme-toggle-container .slider {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 9999px;
        background: #4a4a6a;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .theme-toggle-container .slider::before {
        content: "";
        position: absolute;
        width: 14px;
        height: 14px;
        left: 3px;
        bottom: 3px;
        border-radius: 50%;
        background: #ffffff;
        transition: all 0.3s ease;
    }
    .theme-toggle-container input:checked + .slider {
        background: #7c3aed;
    }
    .theme-toggle-container input:checked + .slider::before {
        transform: translateX(16px);
    }
    </style>
    """, unsafe_allow_html=True)

    is_dark = st.session_state.dark_mode
    checked = "checked" if is_dark else ""
    sun_active = "active" if not is_dark else ""
    moon_active = "active" if is_dark else ""

    st.markdown(f"""
    <div class="theme-toggle-container">
        <span class="icon {sun_active}">☀️</span>
        <label class="toggle-switch">
            <input type="checkbox" id="themeToggle" {checked}>
            <span class="slider"></span>
        </label>
        <span class="icon {moon_active}">🌙</span>
    </div>

    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        const checkbox = document.getElementById('themeToggle');
        if (checkbox) {{
            checkbox.addEventListener('change', function() {{
                const btns = document.querySelectorAll('button');
                for (let btn of btns) {{
                    if (btn.textContent === 'Toggle Theme') {{
                        btn.click();
                        break;
                    }}
                }}
            }});
        }}
    }});
    </script>
    """, unsafe_allow_html=True)

    if st.button("Toggle Theme", key="theme_toggle_btn", help="Toggle Theme", type="secondary"):
        toggle_theme()


# ============================================================
# THEME CSS - COMPLETE THEME SWITCHING
# ============================================================
def get_theme_css():
    """Return CSS based on current theme"""
    if st.session_state.dark_mode:
        return ""  # Your existing dark theme stays as is
    else:
        return LIGHT_CSS


# ============================================================
# LIGHT MODE CSS - Complete light theme
# ============================================================
LIGHT_CSS = """
<style>
/* ============================================================
   LIGHT MODE - Complete theme
   ============================================================ */

/* Background */
.stApp { background: #f5f0ff !important; }
body { background: #f5f0ff !important; color: #1a0f2e !important; }

/* All text */
.stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown div, .stMarkdown span, .stMarkdown strong, .stMarkdown b {
    color: #1a0f2e !important;
}

/* ============================================================
   CARDS - White with purple border
   ============================================================ */
.st-key-upload_card > div,
.st-key-jobdesc_card > div {
    background: #ffffff !important;
    border: 2px solid rgba(124, 58, 237, 0.25) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06) !important;
}
.st-key-upload_card > div:hover,
.st-key-jobdesc_card > div:hover {
    border-color: rgba(124, 58, 237, 0.45) !important;
    box-shadow: 0 8px 30px rgba(124, 58, 237, 0.1) !important;
}

/* ============================================================
   HERO BANNER
   ============================================================ */
.hero-banner {
    background: linear-gradient(135deg, #ede6ff 0%, #f5f0ff 100%) !important;
    border: 2px solid rgba(124, 58, 237, 0.2) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
}
.hero-banner h1 { color: #1a0f2e !important; }
.hero-banner p { color: #5b21b6 !important; }
.hero-badge {
    background: rgba(124, 58, 237, 0.1) !important;
    color: #5b21b6 !important;
    border-color: rgba(124, 58, 237, 0.25) !important;
}

/* ============================================================
   TITLES & DESCRIPTIONS
   ============================================================ */
.input-title { color: #1a0f2e !important; }
.input-description { color: #5b21b6 !important; }
.section-header {
    color: #1a0f2e !important;
    border-bottom: 2px solid rgba(124, 58, 237, 0.12) !important;
}

/* ============================================================
   DROPZONE
   ============================================================ */
[data-testid="stFileUploaderDropzone"] {
    background: #f5f0ff !important;
    border: 2px dashed rgba(124, 58, 237, 0.25) !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #7c3aed !important;
    background: #ede6ff !important;
}
[data-testid="stFileUploaderDropzone"]::after {
    color: #1a0f2e !important;
}

/* ============================================================
   TEXTAREA
   ============================================================ */
.st-key-jobdesc_card textarea {
    background: #f5f0ff !important;
    color: #1a0f2e !important;
    border: 2px solid rgba(124, 58, 237, 0.2) !important;
}
.st-key-jobdesc_card textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.1) !important;
    background-color: #ede6ff !important;
}
.st-key-jobdesc_card textarea::placeholder {
    color: #9a8bbd !important;
}

/* ============================================================
   FILE CHIP
   ============================================================ */
.file-chip-text { color: #1a0f2e !important; }
.file-chip-size { color: #5b21b6 !important; }
.st-key-upload_card [data-testid="stHorizontalBlock"] div {
    background: rgba(124, 58, 237, 0.06) !important;
    border: 1.5px solid rgba(124, 58, 237, 0.15) !important;
    color: #1a0f2e !important;
}

/* ============================================================
   SCORE CARDS
   ============================================================ */
.score-visual-container {
    background: radial-gradient(circle, rgba(124, 58, 237, 0.06) 0%, #f5f0ff 70%) !important;
    border: 2px solid rgba(124, 58, 237, 0.15) !important;
}
.score-circle-inner { background: #ffffff !important; }
.main-score-value { color: #1a0f2e !important; }
.score-card {
    background: #ffffff !important;
    border: 2px solid rgba(124, 58, 237, 0.12) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03) !important;
}
.score-card:hover {
    border-color: rgba(124, 58, 237, 0.25) !important;
    box-shadow: 0 8px 30px rgba(124, 58, 237, 0.06) !important;
}
.score-card .sub-score-inner span {
    color: #1a0f2e !important;
}

/* ============================================================
   DARK CARD (for skill alignment section)
   ============================================================ */
.dark-card {
    background: #ffffff !important;
    border: 2px solid rgba(124, 58, 237, 0.12) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03) !important;
}
.dark-card:hover {
    border-color: rgba(124, 58, 237, 0.25) !important;
    box-shadow: 0 8px 30px rgba(124, 58, 237, 0.06) !important;
}
.dark-card h3 {
    color: #1a0f2e !important;
}

/* ============================================================
   RECOMMENDATION CARDS
   ============================================================ */
.rec-card {
    background-color: #ffffff !important;
}
.rec-high {
    background: linear-gradient(90deg, rgba(244, 63, 94, 0.08) 0%, #ffffff 100%) !important;
    border-color: rgba(244, 63, 94, 0.4) !important;
}
.rec-medium {
    background: linear-gradient(90deg, rgba(245, 158, 11, 0.08) 0%, #ffffff 100%) !important;
    border-color: rgba(245, 158, 11, 0.4) !important;
}
.rec-low {
    background: linear-gradient(90deg, rgba(124, 58, 237, 0.08) 0%, #ffffff 100%) !important;
    border-color: rgba(124, 58, 237, 0.4) !important;
}

/* ============================================================
   FOOTER
   ============================================================ */
.footer {
    color: #5b21b6 !important;
    border-top: 1px solid rgba(124, 58, 237, 0.1) !important;
}

/* ============================================================
   BUTTONS
   ============================================================ */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
    color: #ffffff !important;
    border: 2px solid rgba(124, 58, 237, 0.3) !important;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.2) !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
    box-shadow: 0 8px 30px rgba(124, 58, 237, 0.3) !important;
}

/* ============================================================
   REMOVE BUTTON
   ============================================================ */
.st-key-remove_resume_btn button {
    background: rgba(244, 63, 94, 0.1) !important;
    color: #dc2626 !important;
    border: 1.5px solid rgba(244, 63, 94, 0.2) !important;
}
.st-key-remove_resume_btn button:hover {
    background: rgba(244, 63, 94, 0.25) !important;
    color: #ffffff !important;
    border-color: #dc2626 !important;
}

/* ============================================================
   ALERTS
   ============================================================ */
[data-testid="stAlert"] {
    background: #f5f0ff !important;
    border: 2px solid rgba(124, 58, 237, 0.12) !important;
    border-radius: 18px !important;
    color: #1a0f2e !important;
}

/* ============================================================
   BADGES
   ============================================================ */
.badge-match {
    background-color: rgba(34, 197, 94, 0.12) !important;
    color: #15803d !important;
    border: 1.5px solid rgba(34, 197, 94, 0.3) !important;
}
.badge-missing {
    background-color: rgba(244, 63, 94, 0.12) !important;
    color: #dc2626 !important;
    border: 1.5px solid rgba(244, 63, 94, 0.3) !important;
}

/* ============================================================
   SCROLL REVEAL ANIMATIONS - Keep same
   ============================================================ */
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
</style>
"""