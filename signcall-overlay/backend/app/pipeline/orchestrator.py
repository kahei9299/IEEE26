from app.cv.types import LandmarkWindow
from app.cv.mediapipe_extractor import extract_landmarks
from app.recognition.classifier import predict
from app.recognition.smoothing import smooth
from app.nlp.translator import translate
from app.nlp.profile import get_profile

# simple per-session buffer
_buffers = {}

def _get_buf_key(session: str, user: str) -> str:
    return f"{session}:{user}"

async def process_frame(session: str, user: str, frame_bgr, ts: int):
    key = _get_buf_key(session, user)
    buf = _buffers.setdefault(key, [])
    buf.append(extract_landmarks(frame_bgr, ts))

    # naive: keep last 10 frames then emit
    if len(buf) < 10:
        return None

    frames = buf[-10:]
    window = LandmarkWindow(frames=frames, ts_start=frames[0].ts, ts_end=frames[-1].ts)

    pred = smooth(predict(window))
    profile = get_profile(session, user)
    out = translate(pred, profile)

    return {
        "type": "caption",
        "session": session,
        "user": user,
        "ts": ts,
        "caption": out["caption"],
        "confidence": out["confidence"],
        "mode": out["mode"]
    }
