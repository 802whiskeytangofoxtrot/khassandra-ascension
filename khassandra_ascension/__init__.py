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

To get started quickly you can run ``python -m khassandra_ascension.cli``.

"""

__all__ = ["AscensionEngine", "AscensionConfig", "cli_main"]

# Package version
__version__ = "0.1.0"

from .config import AscensionConfig  # noqa: E402,F401
from .core import AscensionEngine  # noqa: E402,F401
from .cli import main as cli_main  # noqa: E402,F401
