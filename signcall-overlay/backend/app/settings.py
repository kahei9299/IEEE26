import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4.1-mini")
CAPTURE_FPS = float(os.getenv("CAPTURE_FPS", "8"))
WINDOW_SECONDS = float(os.getenv("WINDOW_SECONDS", "0.9"))
CONF_HIGH = float(os.getenv("CONF_HIGH", "0.80"))
CONF_MED = float(os.getenv("CONF_MED", "0.55"))
