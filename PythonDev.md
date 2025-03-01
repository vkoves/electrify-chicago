# Python Environment Setup: Using the tool UV

### Python Version:

We use Python 3.13 to run checks, so make sure you have it installed. It can be installed with UV (see below)

```bash
export PYTHON_VERSION="3.13"
```

### What is UV?

[uv](https://github.com/astral-sh/uv) is a fast Python package manager that replaces pip and venv while offering better performance, deterministic resolution, and a simplified workflow. Unlike pip, uv does not require the use of venv for isolating dependencies, but it works seamlessly with existing virtual environments.

### Setup UV

Install uv using the following command:

```bash
pip install uv
```

or use the recommended way:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install Python 3.13

Install Python 3.13 with:

```bash
uv python install $PYTHON_VERSION
```

### Virtual Environment Setup

To set up the Python environment with uv:

```bash
uv venv --python=$PYTHON_VERSION .venv
```

This creates a virtual environment in .venv inside Electrify-Chicago

```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate  # Windows
```

### Baseline Dependencies (Core Requirements)

These are the minimal dependencies required for running data processing scripts.

- Defined in pyproject.toml under [project.dependencies]
- Equivalent to the old requirements.txt

```bash
uv pip install -r pyproject.toml
```

### Data Analysis Notebook-Specific Dependencies

Additional dependencies for running Jupyter notebooks are defined as an extra group in pyproject.toml.

- Defined under [tool.uv.extras.notebook]
- Equivalent to the old requirements-notebook.txt

To install both baseline + notebook dependencies into a seperate venv:

```bash
deactivate # deactivate baseline venv if activated
uv venv --python=$PYTHON_VERSION .venv-notebook
source .venv-notebook/bin/activate
uv pip install -r pyproject.toml --extra notebook
```

### Adding new packages:

#### Add a Package to the Core Dependencies

Using `uv add` ensures dependencies are recorded in pyproject.toml instead of manually modifying requirements.txt.

Example:

```bash
uv add numpy
```

This installs numpy and updates pyproject.toml under [project.dependencies].

#### Add a Package to the Notebook-Only Dependencies

- open `pyproject.toml`
- add the package inside [project.optional-dependencies.notebook]:

```text
[project.optional-dependencies]
notebook = [
    "kaleido",
    "jupyterlab",
    "matplotlib",
    "ipywidgets",
    ""<- NEW PACKAGE HERE
]
```

Then install this new package:

```bash
uv pip install -r pyproject.toml --extra notebook
```

### Freezing Dependencies for Backward Compatibility

If you need to generate requirements.txt for environments that don’t use uv, you can do:

```bash
source .venv/bin/activate # activate baseline venv
uv pip freeze > requirements.txt
```

To freeze requirements files for additional dependencies, make sure you activate that .venv first

```bash
source .venv-notebook/bin/activate # activate venv with additional depencies
uv pip freeze > requirements-notebook.txt
```

This allows traditional pip install -r requirements.txt workflows to continue working.

#### Use uv pip install when:

- You are testing a package without persisting it to requirements.txt.
- You want to install a package temporarily for an ad-hoc script or experiment.

_Example: Install a package for temporary use_

```bash
uv pip install seaborn
```

This installs seaborn without modifying pyproject.toml

### Running a Script with a Temporary Set of Requirements

If you want to run a script with a temporary environment (without permanently installing packages), use:

```bash
uv pip install -r requirements-notebook.txt --run python script.py
```

This:

- Installs dependencies only for this session.
- Does not persist them in requirements.txt.
