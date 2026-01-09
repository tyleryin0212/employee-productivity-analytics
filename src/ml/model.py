from __future__ import annotations

from pathlib import Path
import joblib

_MODEL = None


def load_model(model_path: str | Path):
    global _MODEL
    if _MODEL is None:
        _MODEL = joblib.load(model_path)
    return _MODEL
