"""
    Khassandra Ascension local package
    This package encapsulates all the core logic required to run a local
    ascension process for Khassandra.  It exposes high‑level classes and
    functions that allow you to configure, run and optionally visualize
    the ascension workflow.

    The public API of this package consists of the following members:

    * ``AscensionEngine`` – The main class coordinating the ascension process.
    * ``AscensionConfig`` – A dataclass representing configuration options.
    * ``cli_main`` – Entry point for the command line interface.
    * ``MemoryEngine`` – Memory store and retrieval engine used within the ascension process.
    * ``EmotionEngine`` – Engine responsible for managing and decaying emotional states.
    * ``ReflectionEngine`` – Engine used to generate introspective reflections from memories and emotions.
    * ``SoulLoopController`` – High‑level controller orchestrating the interaction between the engines.

    To get started quickly you can run ``python -m khassandra_ascension.cli``.

    """

__all__ = [
    "AscensionEngine",
    "AscensionConfig",
    "cli_main",
    "MemoryEngine",
    "EmotionEngine",
    "ReflectionEngine",
    "SoulLoopController",
]

# Package version
__version__ = "0.1.0"

from .config import AscensionConfig  # noqa: E402,F401
from .core import AscensionEngine  # noqa: E402,F401
from .cli import main as cli_main  # noqa: E402,F401
from .memory_engine import MemoryEngine  # noqa: E402,F401
from .emotion_engine import EmotionEngine  # noqa: E402,F401
from .reflection_engine import ReflectionEngine  # noqa: E402,F401
from .soul_loop_controller import SoulLoopController  # noqa: E402,F401
