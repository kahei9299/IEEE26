import time
from app.recognition.phrase_set import PHRASES

TOKENS = list(PHRASES.keys())

def predict(window) -> dict:
    i = int(time.time()) % len(TOKENS)
    token = TOKENS[i]
    return {
        "token": token,
        "confidence": 0.85,
        "top2": [token, TOKENS[(i+1) % len(TOKENS)]],
        "ts": window.ts_end
    }
