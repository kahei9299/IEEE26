# Architecture Overview

Pipeline diagram (conceptual):

Camera -> Frame Capture -> Preprocess (JPEG decode) -> Landmark Extraction -> Windowing ->
Classifier -> Smoothing -> Translator (Templates/LLM) -> Caption Overlay via WebSocket

The current implementation is stubbed but preserves interfaces for future swaps.
