import streamlit as st
import requests
import json
from components.ui import render_summary, render_action_items, render_timeline, render_sentiment

API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="AI Meeting Minutes", layout="wide")

# --- Initialize session state ---
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "upload_response" not in st.session_state:
    st.session_state.upload_response = None

def home_page():
    st.title("📝 AI Meeting Minutes Assistant")
    st.write("""
    Welcome to the AI Meeting Minutes Assistant!  

    This application allows you to:
    - Upload meeting transcripts (PDF or TXT)  
    - Generate **short and detailed summaries**  
    - Extract **action items, discussion flow, and timelines**  
    - Perform **speaker sentiment analysis**  
    """)
    st.markdown("---")
    st.subheader("Get Started")
    st.write("Go to the **Upload Transcript** page to start processing your meeting transcripts.")
    

def upload_page():
    st.title("Upload Transcript & Generate Summary")

    uploaded = st.file_uploader("Upload transcript (TXT or PDF)", type=["txt", "pdf"])
    meeting_title = st.text_input("Meeting title (optional)")

    include_speakers = st.checkbox("Preserve speaker labels", True)
    include_sentiment = st.checkbox("Include sentiment analysis", True)
    include_timeline = st.checkbox("Include timeline", True)

    # Handle file upload only once
    if uploaded and st.session_state.uploaded_file != uploaded:
        st.session_state.uploaded_file = uploaded
        st.info("Uploading and extracting text...")
        files = {"file": (uploaded.name, uploaded.getvalue())}
        resp = requests.post(f"{API_URL}/upload", files=files)
        if resp.status_code != 200:
            st.error(f"Upload failed: {resp.text}")
            st.session_state.upload_response = None
        else:
            st.session_state.upload_response = resp.json()

    # Display transcript if available
    transcript = ""
    if st.session_state.upload_response:
        transcript = st.session_state.upload_response.get("transcript", "")
        st.text_area("Transcript (extracted)", value=transcript, height=300)

    # Process transcript
    if transcript and st.button("Process Transcript"):
        payload = {
            "transcript": transcript,
            "meeting_title": meeting_title,
            "include_speakers": include_speakers,
            "include_sentiment": include_sentiment,
            "include_timeline": include_timeline,
            "language": "english"
        }
        with st.spinner("Calling LLM..."):
            r = requests.post(f"{API_URL}/process", json=payload)
        if r.status_code != 200:
            st.error(f"Processing failed: {r.text}")
        else:
            result = r.json()
            st.header("Short Summary")
            render_summary(result.get("summary_short", []))
            st.header("Detailed Summary")
            st.write(result.get("summary_detailed", ""))
            st.header("Discussion Flow")
            st.write(result.get("discussion_flow", []))
            st.header("Timeline")
            render_timeline(result.get("timeline", []))
            st.header("Action Items")
            render_action_items(result.get("action_items", []))
            st.header("Speaker Sentiment")
            render_sentiment(result.get("speaker_sentiment", {}))
            st.download_button(
                "Download JSON",
                json.dumps(result, indent=2),
                file_name="meeting_summary.json"
            )

# --- Sidebar Navigation ---
page = st.sidebar.radio("Navigation", ["Home", "Upload Transcript"])
st.session_state.page = page  # update session state

# --- Display the appropriate page ---
if st.session_state.page == "Home":
    home_page()
else:
    upload_page()