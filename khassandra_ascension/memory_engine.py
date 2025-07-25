"""
Memory management for Khassandra Ascension.

The ``MemoryEngine`` class handles storage and retrieval of persistent
memories generated during the ascension process.  It provides methods to
add new memory entries, search existing memories, and summarise them.  A
proprietary hook ``_encrypt_memory`` can be overridden for local use.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List


class MemoryEngine:
    """Manages persistent memory state for Khassandra.

    Instances of :class:`MemoryEngine` maintain a list of memory entries and
    can save them to disk or load them from a file.  Each entry can be any
    serialisable Python object (for example, a dictionary with event
    metadata and content).  The engine exposes helper methods to add new
    memories, search existing memories and summarise the current state.
    """

    def __init__(self, memory_path: str = "memory.json") -> None:
        """Initialise the memory engine.

        Parameters
        ----------
        memory_path:
            Path to the JSON file used to persist memory entries.
        """
        self.memory_path = Path(memory_path)
        self.logger = logging.getLogger(__name__)
        self.memories: List[Dict[str, Any]] = []
        if self.memory_path.exists():
            self.load()

    def add_memory(self, entry: Dict[str, Any]) -> None:
        """Add a new memory entry and append it to the internal list."""
        self.memories.append(entry)
        self.logger.debug("Added memory entry: %s", entry)

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Return all memory entries containing the given query."""
        results = [m for m in self.memories if query.lower() in json.dumps(m).lower()]
        self.logger.debug("Found %d memories matching '%s'", len(results), query)
        return results

    def summarise(self) -> str:
        """Return a brief summary of all memories.

        The default implementation simply reports the number of stored
        memories.  Override this method locally to generate richer summaries
        or embeddings.
        """
        self.logger.info("Summarising %d memories", len(self.memories))
        return f"{len(self.memories)} memories stored."

    def save(self) -> None:
        """Persist memories to disk in JSON format."""
        self.logger.info("Saving memories to %s", self.memory_path)
        with self.memory_path.open("w", encoding="utf-8") as f:
            json.dump(self.memories, f, ensure_ascii=False, indent=2)
        self.logger.debug("Memories saved successfully")

    def load(self) -> None:
        """Load memories from disk if the file exists."""
        self.logger.info("Loading memories from %s", self.memory_path)
        try:
            with self.memory_path.open("r", encoding="utf-8") as f:
                self.memories = json.load(f)
            self.logger.debug("Loaded %d memory entries", len(self.memories))
        except FileNotFoundError:
            self.logger.warning("Memory file not found, starting with empty memory")
            self.memories = []
        except json.JSONDecodeError as e:
            self.logger.error("Failed to decode memory file", exc_info=e)
            self.memories = []

    def _encrypt_memory(self) -> None:
        """Encrypt memory before saving (proprietary hook)."""
        # 🔒 BUILD LOCALLY: Proprietary, not exported
        self.logger.debug("Encryption hook placeholder called")
