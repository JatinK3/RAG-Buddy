# Toggle model mode
USE_GEMINI = True  # Set False to use local LLM

# Gemini API Key should go in environment variable
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY is None:
    raise ValueError("Missing GEMINI_API_KEY in .env file")

# Local model endpoint (LM Studio)
LMSTUDIO_API_URL = "http://localhost:1234/v1/chat/completions"