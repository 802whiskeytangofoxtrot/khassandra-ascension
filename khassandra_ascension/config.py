"""
Configuration management for the Khassandra Ascension package.

The :class:`AscensionConfig` dataclass defines a set of tunable options
that describe how the ascension process should behave.  You can load
configuration values from YAML or JSON files, from a dictionary of
Python objects, or simply instantiate the class directly and rely on
reasonable defaults.

Examples
--------

>>> from khassandra_ascension.config import AscensionConfig
>>> # Load configuration from a YAML file
>>> config = AscensionConfig.from_yaml("./config.yaml")
>>> # Override some values programmatically
>>> config.model_type = "random_forest"

The fields defined here are intentionally simple; downstream code is
expected to read these values and react accordingly.  If you need more
advanced behaviour (such as nested configuration or schema validation)
you can extend this class or plug in your own loader logic.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

import yaml  # type: ignore


@dataclass
class AscensionConfig:
    """Dataclass capturing configuration parameters for the ascension process.

    Parameters
    ----------
    data_path:
        Path to the CSV file used for training.  By default this expects a
        comma‑separated file whose last column contains the target label.
    model_type:
        The type of machine learning model to construct.  Currently
        ``random_forest`` is supported.  You can extend the core logic to
        support additional models by recognising new names in
        :meth:`khassandra_ascension.core.AscensionEngine.build_model`.
    model_params:
        A mapping of hyperparameters passed to the model constructor.  For a
        random forest these could include ``n_estimators``, ``max_depth``
        etc.  Refer to the scikit‑learn documentation for details.
    output_dir:
        Directory where artefacts (trained model, logs) are stored.  This
        directory will be created if it does not already exist.
    gui:
        Whether to launch the graphical user interface by default.  This can
        be overridden from the CLI with the ``--gui`` flag.
    """

    data_path: str = "data/train.csv"
    model_type: str = "random_forest"
    model_params: Dict[str, Any] = field(default_factory=dict)
    output_dir: str = "output"
    gui: bool = False

    @staticmethod
    def from_yaml(path: str) -> "AscensionConfig":
        """Load configuration from a YAML file.

        Parameters
        ----------
        path:
            Location of the YAML file on disk.  The file must contain keys
            corresponding to the field names of this dataclass.

        Returns
        -------
        AscensionConfig
            A new instance of the configuration.
        """
        full_path = Path(path)
        if not full_path.is_file():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        with full_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return AscensionConfig.from_dict(data)

    @staticmethod
    def from_json(path: str) -> "AscensionConfig":
        """Load configuration from a JSON file.

        Parameters
        ----------
        path:
            Location of the JSON file on disk.  The file must contain keys
            corresponding to the field names of this dataclass.

        Returns
        -------
        AscensionConfig
            A new instance of the configuration.
        """
        full_path = Path(path)
        if not full_path.is_file():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        with full_path.open("r", encoding="utf-8") as f:
            data = json.load(f) or {}
        return AscensionConfig.from_dict(data)

    @staticmethod
    def from_dict(config_dict: Dict[str, Any]) -> "AscensionConfig":
        """Construct an :class:`AscensionConfig` from a dictionary.

        Keys in the dictionary that do not correspond to dataclass fields are
        ignored.  Missing keys are replaced by default values.

        Parameters
        ----------
        config_dict:
            Mapping containing configuration values.

        Returns
        -------
        AscensionConfig
            A new instance with values populated from the dictionary.
        """
        # Build a filtered dictionary only containing known keys
        valid_keys = {field.name for field in AscensionConfig.__dataclass_fields__.values()}
        filtered = {k: v for k, v in config_dict.items() if k in valid_keys}
        return AscensionConfig(**filtered)
