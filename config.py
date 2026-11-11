
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from .env")

if not FLASK_SECRET_KEY:
    raise ValueError("FLASK_SECRET_KEY is missing from .env")
