from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.upload import router as upload_router
from backend.routes.process import router as process_router
#from backend.routes.sentiment import router as sentiment_router
from backend.core.config import settings
from backend.core.logger import setup_logging
from dotenv import load_dotenv

load_dotenv()
setup_logging()

app = FastAPI(
    title="AI Meeting Minutes Generator + Action Item Tracker",
    description="Upload meeting transcripts (txt/pdf), generate summaries, timeline, action items, speaker sentiment.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(process_router)
#app.include_router(sentiment_router)

@app.get("/")
async def root():
    return {"status": "ok", "version": app.version}
