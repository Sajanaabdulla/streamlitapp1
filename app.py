"""
app.py — HelioSense AI Streamlit Application Entry Point
=========================================================
Run:  streamlit run app.py

AI-powered rooftop solar assessment for Indian cities.
"""

import os
import streamlit as st

from config import Config
from utils.theme import inject_theme
from utils.session_state import init_session_state

from views import (
    dashboard,
    solar_analysis,
    rooftop_analysis,
    bill_analysis,
    ai_advisor,
    reports,
    about,
)

# Ensure upload directory exists for bills, images, and PDF reports
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

PAGES = {
    "Dashboard": dashboard.render,
    "Solar Analysis": solar_analysis.render,
    "Rooftop Analysis": rooftop_analysis.render,
    "Bill Analysis": bill_analysis.render,
    "AI Advisor": ai_advisor.render,
    "Reports": reports.render,
    "About Project": about.render,
}


def render_sidebar() -> str:
    """Sidebar branding and navigation."""
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align:center; padding: 0.5rem 0 1rem 0;">
                <span style="font-size:2.5rem;">☀️</span>
                <h1 style="margin:0; font-size:1.4rem;">HelioSense AI</h1>
                <p style="color:#94A3B8; font-size:0.85rem; margin:0;">
                Rooftop Solar Intelligence
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")

        page = st.radio(
            "Navigation",
            list(PAGES.keys()),
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown(
            f'<span class="helio-badge">NASA POWER · XGBoost · Gemini</span>',
            unsafe_allow_html=True,
        )

        with st.expander("Help"):
            st.markdown(
                """
                1. **Dashboard** — City overview & KPIs  
                2. **Solar Analysis** — Custom ML run  
                3. **Rooftop** — Image-based sizing  
                4. **Bill** — OCR + savings  
                5. **AI Advisor** — Chat with Helio  
                6. **Reports** — Download PDF  

                Set `GEMINI_API_KEY` in `.env` for AI features.
                """
            )

        st.caption("v1.0 · HelioSense AI")

    return page


def main() -> None:
    st.set_page_config(
        page_title="HelioSense AI",
        page_icon="☀️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_theme()
    init_session_state()

    selected = render_sidebar()
    PAGES[selected]()


if __name__ == "__main__":
    main()
