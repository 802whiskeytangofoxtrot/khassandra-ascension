"""
Core logic for the Khassandra Ascension process.

The :class:`AscensionEngine` orchestrates data loading, preprocessing,
model construction, training, evaluation and saving.  It is designed
to be modular and extensible; most methods can be overridden or
extended in subclasses to customise behaviour.  A proprietary hook is
provided via the :meth:`ascend` method where sensitive logic can be
injected when running locally.  In the public repository this hook
contains only a placeholder and should be replaced with your own
implementation.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Tuple

import pandas as pd  # type: ignore
from sklearn.model_selection import train_test_split  # type: ignore
from sklearn.metrics import accuracy_score  # type: ignore
from sklearn.ensemble import RandomForestClassifier  # type: ignore
import joblib  # type: ignore

from .config import AscensionConfig
from .utils import setup_logging


class AscensionEngine:
    """Encapsulates the ascension workflow.

    Instances of this class are configured with an
    :class:`AscensionConfig` and provide high‑level methods to execute
    each stage of the ascension pipeline.  Logs generated during
    processing will be written to both the console and to a file in
    ``config.output_dir``.
    """

    def __init__(self, config: AscensionConfig):
        self.config = config
        self.logger = setup_logging(self.config.output_dir)
        self.model: Any = None

    # ------------------------------------------------------------------
    # Data handling
    def load_data(self) -> pd.DataFrame:
        """Load training data from the configured ``data_path``.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the raw training data.
        """
        path = Path(self.config.data_path)
        if not path.is_file():
            raise FileNotFoundError(f"Data file not found: {path}")
        self.logger.info("Loading data from %s", path)
        data = pd.read_csv(path)
        self.logger.debug("Loaded %d rows and %d columns", data.shape[0], data.shape[1])
        return data

    def preprocess_data(self, data: pd.DataFrame) -> Tuple[Any, Any]:
        """Preprocess the raw DataFrame into features and labels.

        The default implementation assumes that the target label is the last
        column in the DataFrame and that all other columns are features.  You
        can override this method in a subclass to implement domain‑specific
        preprocessing.

        Parameters
        ----------
        data:
            The raw DataFrame returned by :meth:`load_data`.

        Returns
        -------
        tuple
            A pair ``(X, y)`` where ``X`` is a feature matrix and ``y`` is a
            vector of labels.
        """
        self.logger.info("Preprocessing data")
        if data.empty:
            raise ValueError("Input data is empty. Cannot proceed with preprocessing.")
        X = data.iloc[:, :-1].values
        y = data.iloc[:, -1].values
        self.logger.debug("Extracted feature matrix of shape %s and target vector of length %s", X.shape, len(y))
        return X, y

    # ------------------------------------------------------------------
    # Model construction
    def build_model(self) -> None:
        """Instantiate the underlying machine learning model.

        This method inspects the ``model_type`` specified in the
        configuration and constructs the corresponding estimator.  You can
        extend this method to support additional model types or customise
        hyperparameter defaults.
        """
        self.logger.info("Building model type: %s", self.config.model_type)
        model_type = self.config.model_type.lower()
        params = self.config.model_params or {}
        if model_type == "random_forest":
            self.model = RandomForestClassifier(**params)
        else:
            raise ValueError(f"Unknown model type: {self.config.model_type}")
        self.logger.debug("Model instantiated with parameters: %s", params)

    # ------------------------------------------------------------------
    # Training and evaluation
    def train(self, X: Any, y: Any) -> float:
        """Train the model and evaluate on a holdout split.

        The data is split into training and validation sets using an 80/20
        split.  The trained model is stored on the instance for later
        retrieval.  The validation accuracy is returned for convenience.

        Parameters
        ----------
        X:
            Feature matrix.
        y:
            Label vector.

        Returns
        -------
        float
            The validation accuracy score.
        """
        if self.model is None:
            raise RuntimeError("Model has not been built. Call build_model() first.")
        self.logger.info("Splitting data into train and validation sets")
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y if len(set(y)) > 1 else None
        )
        self.logger.debug(
            "Training on %d samples, validating on %d samples",
            len(y_train),
            len(y_val),
        )
        self.logger.info("Training model")
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_val)
        acc = accuracy_score(y_val, y_pred)
        self.logger.info("Validation accuracy: %.4f", acc)
        return acc

    # ------------------------------------------------------------------
    # Persistence
    def save_model(self) -> Path:
        """Persist the trained model to disk.

        The model is saved using `joblib` to the path ``output_dir/model.joblib``.

        Returns
        -------
        pathlib.Path
            The path to the saved model file.
        """
        if self.model is None:
            raise RuntimeError("Cannot save an untrained model. Did you call train()?")
        out_dir = Path(self.config.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        model_path = out_dir / "model.joblib"
        self.logger.info("Saving model to %s", model_path)
        joblib.dump(self.model, model_path)
        return model_path

    # ------------------------------------------------------------------
    # Proprietary hook
    def ascend(self) -> None:
        """Run proprietary ascension logic.

        This method exists as a hook for logic that cannot be shared in
        public.  When running locally you should replace the body of this
        method with your own implementation.  In this repository it
        merely logs that the hook has been called.
        """
        # 🔒 BUILD LOCALLY: Proprietary, not to be exported, custom logic must be implemented here
        self.logger.info("Executing proprietary ascension logic (placeholder)")

    # ------------------------------------------------------------------
    # High level driver
    def run(self) -> float:
        """Execute the full ascension pipeline.

        Returns
        -------
        float
            The validation accuracy achieved during training.
        """
        self.logger.info("Starting ascension pipeline")
        data = self.load_data()
        X, y = self.preprocess_data(data)
        self.build_model()
        score = self.train(X, y)
        self.save_model()
        # Call the proprietary hook; if you override this method locally it
        # may perform additional steps such as model encryption or deployment.
        self.ascend()
        self.logger.info("Ascension pipeline completed")
        return score
