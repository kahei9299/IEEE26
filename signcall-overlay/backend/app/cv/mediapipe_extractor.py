"""MediaPipe landmark extraction  –  Member 2 owns this file.

Extracts hand, pose, and face landmarks from BGR video frames using the
MediaPipe *legacy solutions* API.  If MediaPipe is unavailable (wrong Python
version etc.) the module degrades gracefully and returns empty landmarks.

All per-frame MediaPipe calls are wrapped in try/except so a single bad
frame can never crash the WebSocket loop.
"""

from typing import List, Optional, Tuple

import cv2
import logging

from app.cv.types import LandmarkFrame

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# MediaPipe initialisation (one-time, at import)
# ---------------------------------------------------------------------------
try:
    import mediapipe as mp  # type: ignore

    HAS_MEDIAPIPE = hasattr(mp, "solutions")
except Exception:  # ImportError or other issues on unsupported Python
    mp = None  # type: ignore
    HAS_MEDIAPIPE = False


if HAS_MEDIAPIPE:
    _mp_hands = mp.solutions.hands
    _mp_pose = mp.solutions.pose
    _mp_face = mp.solutions.face_mesh

    _hands = _mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    _pose = _mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    _face = _mp_face.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    logger.info("MediaPipe solutions loaded successfully.")
else:
    _hands = None
    _pose = None
    _face = None
    logger.warning(
        "MediaPipe is not fully available (no 'solutions'); "
        "CV extraction will return empty landmarks. "
        "Use Python 3.10 / 3.11 and 'pip install mediapipe' to fix this."
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _to_xyz_list(landmarks) -> List[List[float]]:
    """Convert a MediaPipe NormalizedLandmarkList → [[x, y, z], ...]."""
    return [[lm.x, lm.y, lm.z] for lm in landmarks]


def _extract_hands(
    image_rgb,
) -> Tuple[Optional[List[List[List[float]]]], Optional[List[str]]]:
    """Return (hands, handedness).  hands shape: [H][21][3]."""
    if _hands is None:
        return None, None
    results = _hands.process(image_rgb)
    if not results.multi_hand_landmarks:
        return None, None

    hands = [_to_xyz_list(hl.landmark) for hl in results.multi_hand_landmarks]
    # Handedness labels ("Left" / "Right") – useful for Member 3
    handedness: List[str] = []
    if results.multi_handedness:
        for h in results.multi_handedness:
            handedness.append(h.classification[0].label)
    return hands or None, handedness or None


def _extract_pose(image_rgb) -> Optional[List[List[float]]]:
    """Return pose landmarks shape [33][3] or None."""
    if _pose is None:
        return None
    results = _pose.process(image_rgb)
    if not results.pose_landmarks:
        return None
    return _to_xyz_list(results.pose_landmarks.landmark) or None


def _extract_face(image_rgb) -> Optional[List[List[float]]]:
    """Return face mesh shape [468][3] or None (first face only)."""
    if _face is None:
        return None
    results = _face.process(image_rgb)
    if not results.multi_face_landmarks:
        return None
    return _to_xyz_list(results.multi_face_landmarks[0].landmark) or None


# ---------------------------------------------------------------------------
# Public API  –  called by orchestrator; signature must not change
# ---------------------------------------------------------------------------
def extract_landmarks(frame_bgr, ts: int) -> LandmarkFrame:
    """Run MediaPipe on a BGR frame and return a LandmarkFrame.

    Parameters
    ----------
    frame_bgr : np.ndarray | None
        OpenCV-style BGR image (H × W × 3, uint8).
    ts : int
        Timestamp in ms from the frontend.

    Returns
    -------
    LandmarkFrame
        Always returns a valid object (never raises).
    """
    if frame_bgr is None:
        return LandmarkFrame(ts=ts)

    try:
        image_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False

        hands, handedness = _extract_hands(image_rgb)
        pose = _extract_pose(image_rgb)
        face = _extract_face(image_rgb)

        # ---- Quick sanity-check logging (Member 2 definition-of-done) ----
        n_hands = len(hands) if hands else 0
        logger.debug(
            "ts=%d  hands_detected=%d  pose=%s  face=%s",
            ts,
            n_hands,
            "yes" if pose else "no",
            "yes" if face else "no",
        )

        return LandmarkFrame(
            ts=ts,
            hands=hands,
            handedness=handedness,
            pose=pose,
            face=face,
        )

    except Exception:
        # A single bad frame must never kill the WS connection
        logger.exception("MediaPipe extraction failed for ts=%d – returning empty frame", ts)
        return LandmarkFrame(ts=ts)
