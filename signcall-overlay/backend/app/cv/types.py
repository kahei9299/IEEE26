from dataclasses import dataclass
from typing import Optional, List

@dataclass
class LandmarkFrame:
    ts: int
    # store minimal placeholder; real implementation can add hands/pose arrays
    hands: Optional[list] = None
    pose: Optional[list] = None
    face: Optional[list] = None

@dataclass
class LandmarkWindow:
    frames: List[LandmarkFrame]
    ts_start: int
    ts_end: int
