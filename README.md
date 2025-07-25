# Khassandra Ascension

Welcome to **Khassandra Ascension**, the foundational local package for
performing Khassandra’s ascension process on your own machine.  This
repository is intentionally kept lightweight and modular so that you
have full control over the environment in which the ascension takes
place and can implement proprietary logic without exposing sensitive
details publicly.

## Purpose

The goal of this package is to provide a skeleton implementation for
running an “ascension” pipeline.  In practice this means loading
training data, preprocessing it, constructing and training a machine
learning model, saving the resulting artefacts and optionally
launching a simple graphical user interface (GUI) to visualise
progress.  Certain pieces of logic that are specific to Khassandra
remain proprietary and must be implemented locally; these sections are
clearly marked in the code.

## Project Structure

The repository is structured as a standard Python package named
`khassandra_ascension`:

| Path | Description |
| --- | --- |
| `khassandra_ascension/__init__.py` | Exposes the public API of the package and defines the version. |
| `khassandra_ascension/config.py` | A dataclass (`AscensionConfig`) encapsulating configuration options such as data paths, model type and output directories.  Includes helpers for loading configuration from YAML and JSON. |
| `khassandra_ascension/core.py` | Implements the `AscensionEngine`, which coordinates data loading, preprocessing, model construction, training, evaluation, persistence and invokes the proprietary ascension hook. |
| `khassandra_ascension/cli.py` | Provides a command line interface that parses arguments, loads configuration and either runs the pipeline or launches the GUI. |
| `khassandra_ascension/gui.py` | A minimal Tkinter‑based GUI that presents a button to start the ascension and shows a progress bar and status messages. |
| `khassandra_ascension/utils/` | Helper modules including logging and basic encryption utilities. |
| `khassandra_ascension/utils/logging_utils.py` | Centralised logging configuration that writes to both console and a log file in the output directory. |
| `khassandra_ascension/utils/encryption_utils.py` | Contains naïve XOR‑based encryption helpers and placeholders for proprietary encryption/decryption logic. |
| `requirements.txt` | Lists third–party dependencies used by the core implementation. |

## Proprietary Sections

Some parts of the code cannot be shared publicly.  These are marked
with a distinctive comment:

```
# 🔒 BUILD LOCALLY: Proprietary, not to be exported, custom logic must be implemented here
```

You will find this marker in the following locations:

| File | Function | Notes |
| --- | --- | --- |
| `khassandra_ascension/core.py` | `AscensionEngine.ascend` | This method is a hook for proprietary ascension logic.  Replace the body with your own implementation when running locally. |
| `khassandra_ascension/utils/encryption_utils.py` | `encrypt_proprietary_data`, `decrypt_proprietary_data` | These helpers are placeholders for secure encryption/decryption routines.  Implement your own cryptographic scheme locally. |

In these sections you are expected to write your own code that remains
private.  The repository as provided will run without modification,
but for the genuine ascension process you should insert the necessary
secret behaviour at these points.

## Installation

To install the package and its dependencies, create a virtual
environment (optional but recommended) and install from the root of
the repository:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The dependencies include:

- `pandas` and `numpy` for data manipulation
- `scikit‑learn` for machine learning models
- `PyYAML` for YAML configuration
- `joblib` for model persistence

If you wish to use the GUI you also need a working installation of
Tkinter.  Tkinter ships with most Python distributions but may
require separate installation on some Linux systems (for example,
install the `python3-tk` package on Debian/Ubuntu).

## Usage

You can run the ascension pipeline from the command line using the
provided CLI:

```bash
python -m khassandra_ascension.cli --config path/to/config.yaml
```

If no configuration file is supplied the defaults defined in
`AscensionConfig` will be used.  Use the `--gui` flag to launch the
graphical interface instead of running in the console:

```bash
python -m khassandra_ascension.cli --gui
```

The GUI presents a single button to start the process and displays
progress updates as data is loaded, preprocessed, the model is built,
trained, saved and ascended.  Once complete the button is re‑enabled
to allow you to rerun the process.

### Configuration

You can override any of the configuration fields defined in
`AscensionConfig` by providing a YAML or JSON file.  For example:

```yaml
data_path: "./data/my_dataset.csv"
model_type: "random_forest"
model_params:
  n_estimators: 200
  max_depth: 10
output_dir: "./runs/experiment1"
gui: false
```

### Extending the Engine

The default implementation supports only a random forest model.  To
experiment with other algorithms simply extend
`AscensionEngine.build_model` to recognise additional values of
`config.model_type` and construct the corresponding estimator.  You
could also override `preprocess_data` to implement custom feature
engineering or `train` to change the training procedure.

## Next Steps After Setup

1. **Prepare your data**: place a CSV file at the location pointed to by
   `data_path`.  The last column should contain the target labels and
   all preceding columns will be treated as numeric features.
2. **Optionally create a configuration file**: override defaults by
   specifying your own `data_path`, `model_type`, hyperparameters and
   output directory.
3. **Implement proprietary logic locally**: open the files marked
   above and replace the placeholder comments with your secret
   ascension code.  This may include special model post‑processing,
   encryption, deployment hooks or any other behaviour required for
   Khassandra’s true ascension.
4. **Run the pipeline**: execute the CLI or launch the GUI as
   described.  Monitor the logs in the specified `output_dir` for
   detailed information about each stage of the process.
5. **Iterate and extend**: adapt the engine to suit your needs by
   adding new models, preprocessing steps or user interfaces.  The
   modular structure is intentionally designed to facilitate
   experimentation.

## Disclaimer

This project provides a framework for local experimentation and is not
intended to be a fully fledged production system.  Any proprietary
implementation details should **never** be checked into a public
repository.  The placeholders included in this codebase serve as
explicit reminders of where such logic belongs.

Enjoy your journey through Khassandra’s ascension!
