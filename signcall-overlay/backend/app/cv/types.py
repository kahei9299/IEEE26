from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class LandmarkFrame:
    """One frame of MediaPipe landmark data.

    Populated by ``cv.mediapipe_extractor.extract_landmarks``.

    Field shapes (when not None):
        hands : List[List[List[float]]]
            Shape  [num_hands][21][3]  –  up to 2 hands, 21 keypoints each,
            each keypoint is [x, y, z] normalised to [0,1] relative to the
            image dimensions.
        handedness : List[str]
            Shape  [num_hands]  –  "Left" or "Right" for each detected hand,
            matching the order of ``hands``.
        pose : List[List[float]]
            Shape  [33][3]  –  33 BlazePose keypoints, same normalisation.
        face : List[List[float]]
            Shape  [468][3]  –  468 FaceMesh keypoints.

    Member 3 can rely on these shapes being stable.
    """

    ts: int
    hands: Optional[List[List[List[float]]]] = None
    handedness: Optional[List[str]] = None
    pose: Optional[List[List[float]]] = None
    face: Optional[List[List[float]]] = None


@dataclass
class LandmarkWindow:
    """A sliding window of consecutive LandmarkFrames.

    Used by Member 3's recognition pipeline.
        frames   – the last N LandmarkFrame objects (default N=10)
        ts_start – timestamp of the earliest frame
        ts_end   – timestamp of the latest frame
    """

    frames: List[LandmarkFrame] = field(default_factory=list)
    ts_start: int = 0
    ts_end: int = 0
