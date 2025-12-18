import streamlit as st
import requests
import json
from components.ui import render_summary, render_action_items, render_timeline, render_sentiment
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

# Custom CSS for modern UI
st.set_page_config(
    page_title="AI Meeting Minutes",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS
st.markdown("""
    <style>

    /* ================================
       GLOBAL PAGE BACKGROUND
    =================================*/
    .main {
        padding-top: 2rem;
        background: linear-gradient(160deg, #f5f3ff 0%, #ede9fe 40%, #e0e7ff 100%);
        min-height: 100vh;
        font-family: "Inter", sans-serif;
    }

    /* ================================
       HEADER
    =================================*/
    .main-header {
        background: linear-gradient(135deg, #b39ddb 0%, #9575cd 40%, #7e57c2 100%);
        padding: 2rem;
        border-radius: 22px;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 14px 35px rgba(123, 97, 255, 0.28);
    }

    .main-header h1 {
        margin: 0;
        font-size: 2.8rem;
        font-weight: 700;
    }

    .main-header p {
        margin-top: 0.5rem;
        opacity: 0.95;
        font-size: 1.15rem;
    }

    /* ================================
    FEATURE CARDS
    ===================================*/
    /* Column wrappers: stretch children */
    [data-testid="column"] > div {
        height: 100% !important;
        display: flex;
    }

    /* Feature cards: fill the column */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.2s;
        height: 100%;          /* fill parent */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .feature-card:hover {    
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);

    }

    /* ================================
       UPLOAD AREA
    =================================*/
    .upload-area {
        border: 2px dashed #b39ddb;
        background: #faf7ff;
        border-radius: 18px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(149,117,205,0.18);
    }

    /* ================================
       SECTION HEADERS
    =================================*/
    .section-header {
        background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
        color: white;
        padding: 1rem 1.6rem;
        border-radius: 14px;
        font-size: 1.5rem;
        font-weight: 600;
        box-shadow: 0 8px 24px rgba(140, 80, 255, 0.25);
        margin: 2rem 0 1.3rem 0;
    }

    /* ================================
       ACTION ITEMS / TIMELINE
    =================================*/
    .action-item-card,
    .timeline-item {
        background: #f8f5ff;
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 4px solid #a78bfa;
        margin-bottom: 1rem;
        box-shadow: 0 4px 14px rgba(167, 139, 250, 0.15);
    }

    /* ================================
       BUTTONS
    =================================*/
    .stButton > button {
        background: linear-gradient(135deg, #9575cd 0%, #7e57c2 100%);
        color: white;
        padding: 0.7rem 2rem;
        font-size: 1rem;
        border-radius: 12px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 18px rgba(126,87,194,0.25);
    }

    .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 28px rgba(126,87,194,0.35);
    }

    /* ================================
       SIDEBAR
    =================================*/
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #c7b8ea 0%, #b39ddb 40%, #9575cd 100%) !important;
        color: white !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-size: 1rem;
        font-weight: 500;
    }

    /* ================================
       INFO BOX
    =================================*/
    .info-box {
        background: #f5f3ff;
        border-left: 4px solid #9575cd;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(149,117,205,0.18);
    }

    </style>
""", unsafe_allow_html=True)


# --- Initialize session state ---
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "upload_response" not in st.session_state:
    st.session_state.upload_response = None
if "processing_result" not in st.session_state:
    st.session_state.processing_result = None

def home_page():
    st.markdown("""
        <div class="main-header">
            <h1>📝 AI Meeting Minutes Assistant</h1>
            <p>Transform your meeting transcripts into actionable insights with AI-powered analysis</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features section
    st.subheader("✨ Key Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <h3>📄 Summarization</h3>
                <p>Generate concise short summaries and comprehensive detailed summaries of your meetings</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h3>✅ Action Items</h3>
                <p>Automatically extract tasks, assignees, and deadlines from your meeting transcripts</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card">
                <h3>📊 Analytics</h3>
                <p>Get timeline visualization, discussion flow, speaker sentiment analysis, and insights</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # How it works
    st.subheader("🚀 How It Works")
    steps = [
        ("1️⃣ Upload", "Upload your meeting transcript in TXT or PDF format"),
        ("2️⃣ Extract", "Our system automatically extracts and processes the text"),
        ("3️⃣ Analyze", "AI analyzes the content to generate insights"),
        ("4️⃣ Review", "Review summaries, action items, timeline, and sentiment")
    ]
    
    for step_num, step_desc in steps:
        st.markdown(f"**{step_num}** {step_desc}")
    
    st.markdown("---")
    
    # Call to action
    st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px;">
            <h2>Ready to get started?</h2>
            <p style="font-size: 1.1rem;">Navigate to <strong>Upload Transcript</strong> to begin processing your meeting minutes</p>
        </div>
    """, unsafe_allow_html=True)

def upload_page():
    st.markdown("""
        <div class="main-header">
            <h1>📤 Upload & Process Transcript</h1>
            <p>Upload your meeting transcript and let AI generate comprehensive insights</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Upload section
    st.markdown("### 📁 File Upload")
    uploaded = st.file_uploader(
        "Upload meeting audio (MP3/WAV/M4A/FLAC/OGG)",
        type=["mp3", "wav", "m4a", "flac", "ogg"],
        help="Upload your meeting audio file"
    )

    # upload_clicked = False
    # if uploaded:
    #     st.success(f"✅ File loaded: **{uploaded.name}** ({uploaded.size:,} bytes)")
    #     upload_clicked = st.button(
    #         "📤 Upload & Extract Text",
    #         type="primary",
    #         use_container_width=False,
    #         help="Send the file to the server and extract the transcript"
    #     )
    
    # Configuration section
    st.markdown("### ⚙️ Processing Options")
    col1, col2 = st.columns(2)
    
    with col1:
        meeting_title = st.text_input(
            "Meeting Title (optional)",
            placeholder="e.g., Q4 Planning Meeting",
            help="Give your meeting a title for better organization"
        )
        # Date of Meeting - used as reference for deadlines
        meeting_date = st.date_input(
            "Date of Meeting",
            value=datetime.today(),
            help="This date will be used as the reference for calculating deadlines (YYYY-MM-DD)"
        )
    
    with col2:
        include_speakers = st.checkbox("Preserve speaker labels", True, help="Keep speaker names/identifiers in the analysis", disabled=True)
        include_sentiment = st.checkbox("Include sentiment analysis", True, help="Analyze emotional tone of each speaker")
        include_timeline = st.checkbox("Include timeline", True, help="Generate chronological timeline of topics")
    
    # Store current checkbox state to detect changes
    current_options = {
        "include_speakers": include_speakers,
        "include_sentiment": include_sentiment,
        "include_timeline": include_timeline,
        "meeting_title": meeting_title,
        "meeting_date": meeting_date.isoformat() if meeting_date else None,
    }
    
    # Clear results if options changed
    if "last_options" in st.session_state:
        if st.session_state.last_options != current_options:
            st.session_state.processing_result = None
            # Remove: st.session_state.result_options = None  
    st.session_state.last_options = current_options

    upload_clicked = False
    if uploaded:
        st.success(f"✅ File loaded: **{uploaded.name}** ({uploaded.size:,} bytes)")
        upload_clicked = st.button(
            "📤 Upload & Extract Text",
            type="primary",
            use_container_width=False,
        )
    
    # Handle file upload only when button is clicked
    if uploaded and upload_clicked:
        with st.spinner("🔄 Uploading and extracting text..."):
            files = {"file": (uploaded.name, uploaded.getvalue())}
            resp = requests.post(f"{API_URL}/upload", files=files)
            if resp.status_code != 200:
                st.error(f"❌ Upload failed: {resp.text}")
                st.session_state.upload_response = None
            else:
                st.session_state.upload_response = resp.json()
                st.success("✅ File uploaded and text extracted successfully!")
    
    # Display transcript if available
    transcript = ""
    if st.session_state.upload_response:
        transcript = st.session_state.upload_response.get("transcript", "")
        st.markdown("### 📝 Extracted Transcript")
        with st.expander("View Transcript", expanded=False):
            st.text_area("Transcript", value=transcript, height=300, label_visibility="collapsed")
    
    # Process transcript button
    if transcript:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            process_btn = st.button(
                "🚀 Process Transcript",
                use_container_width=True,
                type="primary"
            )
        
        if process_btn:
            payload = {
                "transcript": transcript,
                "meeting_title": meeting_title,
                "meeting_date": meeting_date.isoformat() if meeting_date else None,
                "include_speakers": include_speakers,
                "include_sentiment": include_sentiment,
                "include_timeline": include_timeline,
                "language": "english",
            }
            with st.spinner("🤖 AI is analyzing your transcript... This may take a moment."):
                r = requests.post(f"{API_URL}/process", json=payload)
            if r.status_code != 200:
                st.error(f"❌ Processing failed: {r.text}")
            else:
                result = r.json()
                result["meeting_title"] = meeting_title
                result["meeting_date"] = meeting_date.isoformat() if meeting_date else None
                st.session_state.processing_result = result
                # Remove the result_options tracking - no longer needed
                st.success("✅ Processing complete! Scroll down to view results.")
    
    # Display results
    if st.session_state.processing_result:
        result = st.session_state.processing_result
        # Remove result_options - no longer needed
        
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")
        
        # Short Summary
        st.markdown('<div class="section-header">📋 Short Summary</div>', unsafe_allow_html=True)
        render_summary(result.get("summary_short", []))
        
        # Detailed Summary
        st.markdown('<div class="section-header">📄 Detailed Summary</div>', unsafe_allow_html=True)
        st.markdown(result.get("summary_detailed", ""))
        
        # Discussion Flow
        st.markdown('<div class="section-header">💬 Discussion Flow</div>', unsafe_allow_html=True)
        discussion_flow = result.get("discussion_flow", [])
        if discussion_flow:
            for i, point in enumerate(discussion_flow, 1):
                st.markdown(f"**{i}.** {point}")
        else:
            st.info("No discussion flow available.")
        
        # Timeline - always show (will display "No timeline items" if empty)
        st.markdown('<div class="section-header">⏱️ Timeline</div>', unsafe_allow_html=True)
        render_timeline(result.get("timeline", []))
        
        # Action Items
        st.markdown('<div class="section-header">✅ Action Items</div>', unsafe_allow_html=True)
        render_action_items(result.get("action_items", []))
        
        # Speaker Sentiment - always show (will handle empty dict)
        sentiment_data = result.get("speaker_sentiment", {})
        if sentiment_data:
            st.markdown('<div class="section-header">😊 Speaker Sentiment</div>', unsafe_allow_html=True)
            render_sentiment(sentiment_data)
        else:
            st.markdown('<div class="section-header">😊 Speaker Sentiment</div>', unsafe_allow_html=True)
            st.info("No sentiment analysis available.")
        
        # Download button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                "💾 Download JSON Results",
                json.dumps(result, indent=2),
                file_name=f"meeting_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h1 style="color: white; margin: 0;">📝</h1>
            <h2 style="color: white; margin: 0.5rem 0;">MinuteMind</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["Home", "Upload Transcript"],
        label_visibility="visible"
    )
    st.session_state.page = page
    
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; padding: 1rem;">
            <p>AI-Powered Meeting Analysis</p>
        </div>
    """, unsafe_allow_html=True)

# --- Display the appropriate page ---
if st.session_state.page == "Home":
    home_page()
else:
    upload_page()