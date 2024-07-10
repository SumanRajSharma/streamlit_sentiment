import streamlit as st
from footer import load_footer
from streamlit_theme import st_theme
from pages.page_youtube_video import main

theme = st_theme()

if theme:
    if theme.get('base')=='light':
        st.logo("images/dark_logo_v2.png")
    else:
        st.logo("images/light_logo_v2.png")
else:
    st.logo("images/dark_logo_v2.png")

pages = {
    "": [st.Page("pages/page_home.py", title="Home", icon=":material/home:")],
    "Steps": [st.Page(main, title="Fetch Video Comments", icon=":material/play_circle:"),
              st.Page("pages/page_sentiment_analysis.py", title="Sentiment Analysis",  icon=":material/chat:"),
              st.Page("pages/page_topic_modelling.py", title="Topic Modelling",  icon=":material/file_copy:")],
    "Others": [st.Page("pages/page_privacy_policy.py", title="Privacy Policies", icon=":material/security:")],
}

pg = st.navigation(pages)
pg.run()

load_footer(theme)