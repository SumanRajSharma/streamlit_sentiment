import streamlit as st
import requests
import pickle
from footer import load_footer

st.set_page_config(page_title="YouTube Video")

st.title("YouTube Video Comments Fetcher")
st.write("Enter the URL of a YouTube video to fetch its comments.")

load_footer()

# Function to extract video ID from YouTube URL
def extract_video_id(url):
    import re
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None


# Fetching a youtube video title using youtube API
def youtube_api_video_metadata(API_KEY, videoID):
    print(API_KEY)
    video_meta_data = {
        'title': '',
        'description': '',
        'categoryID': '',
        'thumbnails': '',
        'tags': '',
        'channelTitle': ''
    }
    
    URL = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={videoID}&key={API_KEY}"
    
    response = requests.get(URL)
    print(response)
    err = ""
    if response.status_code == 200:
        json_data = response.json()
        if json_data['items']:
            for item in json_data['items']:
                if 'title' in item['snippet']:
                    video_meta_data['title'] = item['snippet']['title']
                if 'description' in item['snippet']:
                    video_meta_data['description'] = item['snippet']['description']
                if 'thumbnails' in item['snippet']:
                    video_meta_data['thumbnails'] = item['snippet']['thumbnails']['standard']['url']
                if 'categoryId' in item['snippet']:
                    video_meta_data['categoryID'] = item['snippet']['categoryId']
                if 'channelTitle' in item['snippet']:
                    video_meta_data['channelTitle'] = item['snippet']['channelTitle']
                if 'tags' in item['snippet']:
                    video_meta_data['tags'] = item['snippet']['tags']
    else:
        err = response.status_code
    return video_meta_data, err

def display_video_metadata(video_meta_data):
    btn_clear = st.empty()
    video_header = st.empty()
    video_image = st.empty()
    video_details = st.empty()
    video_info = st.empty()
    if video_meta_data:
        if btn_clear.button(label="Clear all"):
            with open('store.pckl', 'wb') as f:
                pickle.dump({}, f)
        else:
            video_header.header(video_meta_data['title'])
            video_image.image(video_meta_data['thumbnails'])
            if video_details.checkbox('Show video description'):
                video_info.info(video_meta_data['description'])

# Function to fetch comments from YouTube API
def fetch_youtube_comments(video_id, api_key):
    comments = []
    url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=100"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for item in data["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
        return comments
    else:
        st.error("Error fetching comments from YouTube API")
        return []

# Text box for YouTube URL input
youtube_url = st.text_input("YouTube Video URL")

# Button to fetch comments
if st.button("Fetch Comments"):
    if youtube_url:
        videoID = extract_video_id(youtube_url)
        print(videoID)
        if videoID:
            API_KEY = st.secrets["YOUTUBE_API_KEY"]
            video_meta_data, err = youtube_api_video_metadata(API_KEY, videoID)
            print(video_meta_data)
            if not err:
                display_video_metadata(video_meta_data)
        else:
            st.error("Invalid YouTube URL")
    else:
        st.error("Please enter a YouTube URL")
