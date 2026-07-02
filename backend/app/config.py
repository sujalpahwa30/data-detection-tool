from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
ANALYSIS_DIR = BASE_DIR / "analysis"
CHROMA_DIR = BASE_DIR / "chroma_db"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")