#!/usr/bin/env python3
"""
Entry point for Khassandra Ascension.

This script initialises the core engines and starts the soul loop
controller.  It can be invoked from the command line and accepts optional
arguments for memory, emotion and reflection file paths.  Proprietary
runtime logic can be implemented via hooks within the individual
engines.
"""

from __future__ import annotations

import argparse
import logging

from khassandra_ascension.memory_engine import MemoryEngine
from khassandra_ascension.emotion_engine import EmotionEngine
from khassandra_ascension.reflection_engine import ReflectionEngine
from khassandra_ascension.soul_loop_controller import SoulLoopController


def parse_args() -> argparse.Namespace:
    """Parse command‑line arguments for the Khassandra run script."""
    parser = argparse.ArgumentParser(
        description="Run Khassandra Ascension process."
    )
    parser.add_argument(
        "--memory-path",
        type=str,
        default="memory.json",
        help="Path to the memory JSON file.",
    )
    parser.add_argument(
        "--emotions-path",
        type=str,
        default="emotions.json",
        help="Path to the emotions JSON file.",
    )
    parser.add_argument(
        "--reflections-path",
        type=str,
        default="reflections.json",
        help="Path to the reflections JSON file.",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1,
        help="Number of soul loop iterations to execute.",
    )
    return parser.parse_args()


def main() -> None:
    """Main entrypoint for running Khassandra Ascension."""
    args = parse_args()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Initialising Khassandra engines")

    memory_engine = MemoryEngine(memory_path=args.memory_path)
    emotion_engine = EmotionEngine(emotions_path=args.emotions_path)
    reflection_engine = ReflectionEngine(reflections_path=args.reflections_path)

    controller = SoulLoopController(
        memory_engine=memory_engine,
        emotion_engine=emotion_engine,
        reflection_engine=reflection_engine,
    )

    controller.run_loop(iterations=args.iterations)
    logger.info("Khassandra Ascension run complete")


if __name__ == "__main__":
    main()
