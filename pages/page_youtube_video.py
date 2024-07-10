import streamlit as st
import requests
import pickle
import os
import pandas as pd

# Function to extract video ID from YouTube URL
def extract_video_id(url):
    import re
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# Function to fetch video metadata using YouTube API
def fetch_video_metadata(API_KEY, videoID):
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
    if response.status_code == 200:
        json_data = response.json()
        if json_data['items']:
            snippet = json_data['items'][0]['snippet']
            video_meta_data.update({
                'title': snippet.get('title', ''),
                'description': snippet.get('description', ''),
                'categoryID': snippet.get('categoryId', ''),
                'thumbnails': snippet.get('thumbnails', {}).get('standard', {}).get('url', ''),
                'tags': snippet.get('tags', []),
                'channelTitle': snippet.get('channelTitle', '')
            })
        return video_meta_data, ""
    else:
        return None, response.status_code

# Function to fetch comments using YouTube API
def fetch_comments(API_KEY, videoID):
    comments = []
    base_url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        'part': 'snippet',
        'key': API_KEY,
        'videoId': videoID,
        'maxResults': 100
    }

    session = requests.Session()
    response = session.get(base_url, params=params)
    if response.status_code == 200:
        json_data = response.json()
        while 'items' in json_data:
            for item in json_data['items']:
                comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
            if 'nextPageToken' in json_data:
                params['pageToken'] = json_data['nextPageToken']
                response = session.get(base_url, params=params)
                if response.status_code != 200:
                    return comments, response.status_code
                json_data = response.json()
            else:
                break
        session.close()
        return comments, ""
    else:
        session.close()
        return None, response.status_code



# Function to display video metadata
def display_video_metadata(video_meta_data):
    if 'boolean' not in st.session_state:
        st.session_state.boolean = False

    if st.session_state.boolean:
        return  # Avoid further execution if clear state is set

    btn_clear = st.empty()
    if video_meta_data:
        btn_clear.button(label="Clear all", type="primary", on_click=clear_data)

        cols = st.columns([1, 1])
        with cols[0]:
            st.image(video_meta_data['thumbnails'], use_column_width=True)
        with cols[1]:
            st.header(video_meta_data['title'])
        with st.expander("More..."):
            st.write(video_meta_data['description'])

# Function to handle the clear button click
def clear_data():
    with open('store.pckl', 'wb') as f:
        pickle.dump({}, f)
    if os.path.exists('sample_comments.csv'):
        os.remove('sample_comments.csv')
    st.session_state.clear = True

# Function to save data to a pickle file
def save_to_pickle(videoID, comments, video_meta_data):
    with open('store.pckl', 'wb') as f:
        pickle.dump({'video_id': videoID, 'comments': comments, 'video_meta_data': video_meta_data, 'topics': '', 'slider_value': 0}, f)

# Function to create and save comments to a CSV file
def save_comments_to_csv(comments):
    df = pd.DataFrame(comments, columns=['Comments'])
    df.to_csv('sample_comments.csv', index=False)
    return df

# Main function to handle the workflow
def main():
    st.title("YouTube Video Comments Fetcher")
    st.write("Enter the URL of a YouTube video to fetch its comments.")
    
    youtube_url = st.text_input("YouTube Video URL")
    
    if st.button("Fetch Comments"):
        if youtube_url:
            videoID = extract_video_id(youtube_url)
            if videoID:
                API_KEY = st.secrets["YOUTUBE_API_KEY"]
                with st.status("Downloading Data...", expanded=True) as status:
                    st.write("Fetching video metadata...")
                    video_meta_data, err = fetch_video_metadata(API_KEY, videoID)
                    if not err:
                        st.write('Fetching video comments...')
                        comments, err = fetch_comments(API_KEY, videoID)
                        if not err:
                            status.update(label="Comments fetched successfully!", state="complete", expanded=False)
                            save_to_pickle(videoID, comments, video_meta_data)
                            df = save_comments_to_csv(comments)
                        else:
                            status.update(label=f"Error fetching comments: {err}", state="error")
                    else:
                        status.update(label=f"Error fetching video metadata: {err}", state="error")
                
                # Display metadata and comments outside the `with` block
                display_video_metadata(video_meta_data)
                
                st.table(df.head())
            else:
                st.error("Invalid YouTube URL")
        else:
            st.error("Please enter a YouTube URL")
    else:
        if os.path.isfile('store.pckl'):
            with open('store.pckl', 'rb') as f:
                data = pickle.load(f)
            if data:
                display_video_metadata(data['video_meta_data'])
        if os.path.exists('sample_comments.csv'):
            df = pd.read_csv('sample_comments.csv')
            st.text("Comments")
            st.table(df.head())