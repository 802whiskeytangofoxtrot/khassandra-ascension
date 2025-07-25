"""
Emotion management for Khassandra Ascension.

The :class:`EmotionEngine` tracks and updates emotional states associated
with Khassandra's experiences.  It allows updating emotion intensities,
decaying them over time, and querying the dominant emotion.  A
proprietary hook ``_calculate_affective_state`` can be overridden for
more complex affective state modelling.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, Tuple, Optional


class EmotionEngine:
    """Handles emotional state for Khassandra."""

    def __init__(self, emotions_path: str = "emotions.json") -> None:
        """Initialise the emotion engine.

        Parameters
        ----------
        emotions_path:
            Path to the JSON file used to persist emotion intensities.
        """
        self.emotions_path = Path(emotions_path)
        self.logger = logging.getLogger(__name__)
        self.emotions: Dict[str, float] = {}
        if self.emotions_path.exists():
            self.load()

    def update_emotion(self, name: str, intensity: float) -> None:
        """Set the intensity of an emotion.

        Parameters
        ----------
        name:
            Name of the emotion to update.
        intensity:
            New intensity value for the emotion.
        """
        self.emotions[name] = intensity
        self.logger.debug("Updated emotion '%s' to intensity %.3f", name, intensity)

    def decay_emotions(self, rate: float = 0.1) -> None:
        """Apply exponential decay to all emotions.

        Parameters
        ----------
        rate:
            Fraction by which to decrease each emotion intensity.
        """
        for name in list(self.emotions.keys()):
            self.emotions[name] *= max(0.0, 1.0 - rate)
            if self.emotions[name] < 1e-6:
                del self.emotions[name]
        self.logger.debug("Decayed emotions by rate %.3f", rate)

    def get_dominant_emotion(self) -> Optional[Tuple[str, float]]:
        """Return the dominant emotion and its intensity.

        Returns
        -------
        Optional[Tuple[str, float]]
            A pair of the dominant emotion name and its intensity,
            or ``None`` if no emotions are present.
        """
        if not self.emotions:
            return None
        dominant = max(self.emotions.items(), key=lambda item: item[1])
        self.logger.debug("Dominant emotion: %s with intensity %.3f", *dominant)
        return dominant

    def save(self) -> None:
        """Persist emotions to disk."""
        self.logger.info("Saving emotions to %s", self.emotions_path)
        with self.emotions_path.open("w", encoding="utf-8") as f:
            json.dump(self.emotions, f, ensure_ascii=False, indent=2)
        self.logger.debug("Emotions saved successfully")

    def load(self) -> None:
        """Load emotions from disk if the file exists."""
        self.logger.info("Loading emotions from %s", self.emotions_path)
        try:
            with self.emotions_path.open("r", encoding="utf-8") as f:
                self.emotions = json.load(f)
            self.logger.debug("Loaded %d emotion entries", len(self.emotions))
        except FileNotFoundError:
            self.logger.warning("Emotion file not found, starting with empty state")
            self.emotions = {}
        except json.JSONDecodeError as e:
            self.logger.error("Failed to decode emotion file", exc_info=e)
            self.emotions = {}

    def _calculate_affective_state(self) -> None:
        """Proprietary affective state calculation."""
        # 🔒 BUILD LOCALLY: Proprietary, not exported
        self.logger.debug("Affective state hook placeholder called")
