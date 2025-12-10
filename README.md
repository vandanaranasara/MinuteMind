# 📝 MinuteMind - AI Meeting Minutes Assistant

MinuteMind is an intelligent meeting minutes generator that uses AI to transform meeting transcripts into actionable insights. Upload your meeting transcripts (PDF or TXT) and get comprehensive summaries, action items, timelines, and sentiment analysis automatically generated.

## ✨ Features

- **📄 Smart Summarization**: Generate both concise short summaries and comprehensive detailed summaries
- **✅ Action Item Extraction**: Automatically identify tasks, assignees, and deadlines from meeting transcripts
- **⏱️ Timeline Generation**: Create chronological timelines of discussion topics with timestamps
- **💬 Discussion Flow**: Track the flow of conversation and key discussion points
- **😊 Speaker Sentiment Analysis**: Analyze the emotional tone of each speaker (positive, neutral, negative)
- **📊 Modern Web Interface**: Beautiful, responsive Streamlit-based UI with gradient designs and intuitive navigation
- **🔧 Flexible Processing Options**: Customize which features to include (speakers, sentiment, timeline)
- **💾 JSON Export**: Download analysis results in JSON format for further processing

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Google Gemini AI**: LLM for intelligent text analysis (via LangChain)
- **PyPDF2**: PDF text extraction
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server

### Frontend
- **Streamlit**: Interactive web application framework
- **Custom CSS**: Modern gradient-based UI design

## 📋 Prerequisites

- Python 3.8 or higher
- Google API Key for Gemini AI (optional - stub mode available for testing)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vandanaranasara/MinuteMind.git
   cd MinuteMind
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
      
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
5. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   
   GOOGLE_API_KEY=your_google_api_key_here
   UPLOAD_DIR=uploads
   
   **Note**: If you don't have a Google API key, the application will run in stub mode with sample data.

## ⚙️ Configuration

The application uses environment variables for configuration. Key settings:

- `GOOGLE_API_KEY`: Your Google Gemini API key (required for AI features)
- `LLM_MODEL`: Model to use (default: `gemini-2.5-flash`)
- `UPLOAD_DIR`: Directory for uploaded files (default: `uploads`)

## 🎯 Usage

### Starting the Backend Server

1. Navigate to the project root directory
2. Start the FastAPI server:sh
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```
      The API will be available at `http://localhost:8000`
   
   You can view the API documentation at:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Starting the Frontend

1. In a new terminal, activate your virtual environment
2. Start the Streamlit app:
   ```bash
   streamlit run frontend/index.py
   ```
      The web interface will open at `http://localhost:8501`

### Using the Application

1. **Navigate to "Upload Transcript"** in the sidebar
2. **Upload a file**: Choose a TXT or PDF file containing your meeting transcript
3. **Configure options**:
   - Set an optional meeting title
   - Choose to preserve speaker labels
   - Include/exclude sentiment analysis
   - Include/exclude timeline generation
4. **Click "Process Transcript"** to analyze the meeting
5. **Review results**: View summaries, action items, timeline, and sentiment analysis
6. **Download results**: Export the analysis as JSON for further use

## 📁 Project Structure

```
MinuteMind/
├── backend/
│   ├── core/
│   │   ├── config.py          # Application configuration
│   │   └── logger.py           # Logging setup
│   ├── routes/
│   │   ├── upload.py           # File upload endpoint
│   │   ├── process.py          # Transcript processing endpoint
│   │   └── sentiment.py        # Sentiment analysis endpoint
│   ├── services/
│   │   ├── extraction.py       # Text extraction from files
│   │   ├── llm_client.py       # LLM client wrapper
│   │   └── prompt_builder.py   # Prompt construction
│   ├── utils/
│   │   ├── file_helpers.py     # File utility functions
│   │   └── validators.py       # Data validation
│   ├── models.py               # Database models
│   ├── schemas.py              # Pydantic schemas
│   └── main.py                 # FastAPI application entry point
├── frontend/
│   ├── components/
│   │   ├── ui.py               # UI rendering components
│   └── index.py                # Streamlit main application
├── uploads/                    # Uploaded files directory
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
└── README.md                   # This file
```

## 🔌 API Endpoints

- `POST /upload` - Upload a meeting transcript file (PDF or TXT)
- `POST /process` - Process a transcript and generate meeting minutes
- `POST /sentiment` - Analyze sentiment for speakers in a transcript

## 🧪 Testing

The application includes a stub mode that works without an API key for testing:

- When `GOOGLE_API_KEY` is not set, the LLM client returns sample JSON responses
- This allows you to test the UI and workflow without API costs
- Sample data includes realistic meeting minutes structure

## 🔒 Privacy & Security

- Uploaded files are stored locally in the `uploads/` directory
- Files can be automatically deleted after text extraction (currently commented out)
- No data is sent to external services except Google Gemini API (when configured)
- Environment variables should never be committed to version control

## 🐛 Troubleshooting

### Issue: "LLMClient running in stub mode"
**Solution**: Set your `GOOGLE_API_KEY` in the `.env` file

### Issue: File upload fails
**Solution**: 
- Ensure the file is in TXT or PDF format
- Check that the `uploads/` directory exists and is writable
- Verify file size is reasonable

### Issue: Processing returns errors
**Solution**:
- Check that the transcript is not too short (minimum 10 characters)
- Verify your Google API key is valid and has quota remaining
- Check backend logs for detailed error messages

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI powered by [Streamlit](https://streamlit.io/)
- AI capabilities via [Google Gemini](https://ai.google.dev/)
- Text extraction using [PyPDF2](https://pypdf2.readthedocs.io/)

## 👥 Contributor

- [Vandana Ranasara](https://github.com/vandanaranasara)



