from app.cv.types import LandmarkFrame

def extract_landmarks(frame_bgr, ts: int) -> LandmarkFrame:
    # TODO: replace with MediaPipe Hands/Pose extraction
    return LandmarkFrame(ts=ts, hands=None, pose=None, face=None)
