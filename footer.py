import streamlit as st
from PIL import Image
import os

# Load images
image_dir = "images"
medium_icon = Image.open(os.path.join(image_dir, 'medium.png'))
github_icon = Image.open(os.path.join(image_dir, 'github.png'))
portfolio_icon = Image.open(os.path.join(image_dir, 'portfolio.png'))

# Convert images to base64
def pil_to_base64(image):
    import base64
    from io import BytesIO

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

medium_icon_base64 = pil_to_base64(medium_icon)
github_icon_base64 = pil_to_base64(github_icon)
portfolio_icon_base64 = pil_to_base64(portfolio_icon)

# Define a helper function to display image links
def image_link(icon, url, text):
    return f"""
    <div class="link-container">
        <img src="data:image/png;base64,{icon}" width="24"/>
        <a href="{url}" target="_blank">{text}</a>
    </div>
    """

def load_footer():
    st.sidebar.markdown("Hi, I'm Suman Raj Sharma, creator of the Data Algo Medium account. I'm passionate about data science and algorithms.")

    # Add links with Streamlit images
    st.sidebar.markdown(
        """
        <style>
        .link-container {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .link-container img {
            margin-right: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown(image_link(medium_icon_base64, "https://dataalgo.medium.com/", "Data:Algo Medium"), unsafe_allow_html=True)
    st.sidebar.markdown(image_link(github_icon_base64, "https://github.com/SumanRajSharma", "GitHub"), unsafe_allow_html=True)
    st.sidebar.markdown(image_link(portfolio_icon_base64, "https://sumanrajsharma.dev/", "Portfolio"), unsafe_allow_html=True)
