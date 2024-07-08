import streamlit as st

st.set_page_config(
    page_title="Sentiment and Topic Modelling App",
    page_icon="👋",
)

st.write("# Welcome to the Sentiment and Topic Modelling App! 👋")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    This Streamlit app allows you to analyze comments from YouTube videos. 
    **👈 Select a page from the sidebar** to get started:
    
    ### Features:
    - **YouTube Video:** Input a YouTube video URL to fetch metadata and comments.
    - **Sentiment Analysis:** Analyze the sentiment of the fetched comments.
    - **Topic Modelling:** Perform topic modelling on the fetched comments.
    
    ### Instructions:
    1. Navigate to the **YouTube Video** page.
    2. Enter the URL of a YouTube video.
    3. Fetch and display the video metadata and comments.
    4. Go to the **Sentiment Analysis** page to see the sentiment analysis results.
    5. Go to the **Topic Modelling** page to see the topic modelling results.
    
    ### Want to learn more?
    - Check out [Streamlit](https://streamlit.io)
    - Explore our [documentation](https://docs.streamlit.io)
    - Join the [community forums](https://discuss.streamlit.io)
    """
)
