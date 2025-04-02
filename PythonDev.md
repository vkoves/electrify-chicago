# Python Developer Guide

**Everything you need to know about managing Python dependencies, running scripts, and setting up a virtual environment for Electrify-Chicago.**

### Python Virtual Environments: When to use one

You can run our data pipeline processes either within the Docker container or directly from a bash terminal. Docker provides a fully configured environment, ensuring complete consistency across development and deployment. We use Docker to run the web server and data processing scripts in production, and you can use it for local development as well.

However, sometimes you may prefer running scripts locally/outside of Docker — perhaps for faster development cycles, debugging, or when working with Jupyter notebooks. In these cases, **always use a virtual environment**. This ensures you're using the correct dependency versions for our project, even while outside the Docker container. Without a virtual environment, you risk using system-wide Python packages that might differ from our project requirements, leading to inconsistent behavior between your local runs and the containerized environment.

The key workflow is simple: If you want to run Python code outside of the Docker container, make sure you are running it with your virtual environment activated. The steps to create an environment, activate it and sync the environment with our project dependency list is contained below:

## Setting up a Virtual Environment

### Python Version:

We are currently using Python 3.12. This is hardcoded in the following places:

- Our Github CI Pipeline:
  - [.github/workflows/pytest.yml](.github/workflows/pytest.yml)
- Our Dockerfile:
  - [Dockerfile](Dockerfile)
- Our netlify.toml file:
  - [netlify.toml](netlify.toml)

### Export Python Version:

Run the following command to set the Python version to 3.12 in your terminal:

```bash
export PYTHON_VERSION="3.12"
```

### Python Dependency List:

We use a [pyproject.toml](pyproject.toml) file to manage our Python dependencies. This file contains a list of all the packages required to run our project. The dependencies are divided into two groups:

- **Core Dependencies**: Required for running data processing scripts.
  - _listed under `[dependencies]` in `pyproject.toml`_
- **Notebook Dependencies**: Additional packages required for running Jupyter notebooks.
  - _listed under [project.optional-dependencies] notebook = []_

As the project becomes more complex, we may add more dependencies to these groups or create new groups for different purposes. The `pyproject.toml` file is the single source of truth for all Python dependencies in our project.

## Managing Python Dependencies with the Package Manager 'UV'

[uv](https://github.com/astral-sh/uv) is a fast Python package manager that replaces pip and venv while offering better performance, deterministic resolution, and a simplified workflow. Unlike pip, uv does not require the use of venv for isolating dependencies, but it works seamlessly with existing virtual environments.

### UV Installation and Setup Guide

#### First: Ensure you have pip and it's updated

```bash
python -m pip install --upgrade pip
```

#### Setup UV

Install uv using the following command:

```bash
pip install uv
```

or use the recommended way:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install Python 3.12

Install Python 3.12 with:

```bash
uv python install 3.12
```

### Virtual Environment Setup

To set up the Python environment with uv:

```bash
uv venv --python=$PYTHON_VERSION .venv
```

This creates a virtual environment in your root directory of Electrify-Chicago.

The virtual environment is a folder and should be called `.venv` by default. In that folder, there is a script that activates the virtual environment. To activate the virtual environment with this script, run the following command:

```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate  # Windows
```

### Install the Baseline Dependencies (Core Requirements)

These are the minimal dependencies required for running data processing scripts.

- Defined in [pyproject.toml](pyproject.toml) under `[dependencies]`

**Install core package**

```bash
uv pip install -e .
```

### Data Analysis Notebook-Specific Dependencies

Additional dependencies for running Jupyter notebooks are defined as an extra group in pyproject.toml.

- Defined under `[tool.uv.extras.notebook]`

To install both baseline + notebook dependencies:

```bash
uv pip install -e ".[notebook]"
```

Alternatively, you might want to create a separate virtual environment for running notebooks. This is useful if you want to keep the baseline environment clean and avoid installing unnecessary packages.

To create a separate virtual environment for notebooks:

```bash
deactivate # deactivate baseline venv if activated
uv venv --python=$PYTHON_VERSION .venv-notebook # Create new venv with different name
source .venv-notebook/bin/activate
uv pip install -e ".[notebook]" # Install notebook dependencies
```

### Adding new packages to the Core Dependencies

Assume you want to add a new package, numpy, to the core dependencies. You want to not only install it, but also record it in `pyproject.toml` so that others can install it easily.

Using `uv add` will both install the package and record its installation in `pyproject.toml`, no manual editing required.

Example:

```bash
uv add numpy
```

This installs numpy and updates `pyproject.toml` under `[dependencies]`.

### How to Add a Package to the Notebook-Only Dependencies

UV does not have a built-in command to add packages to optional dependencies. If you want to add a new package to the notebook dependencies, you need to manually edit `pyproject.toml`.

- open `pyproject.toml`
- add the package inside `[project.optional-dependencies.notebook]`:

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

Then install this new package in the virtual environment you are using:

```bash
uv pip install -e ".[notebook]"
```

### Freezing Dependencies for Backward Compatibility

If you need to generate a `requirements.txt` for environments that don’t use `uv`, you can do:

```bash
source .venv/bin/activate # activate baseline venv
uv pip freeze > requirements.txt
```

Doing this will generate a `requirements.txt` file with all the dependencies you have installed in the virtual environment. Users who don’t have `uv` can install these dependencies using `pip install -r requirements.txt`.

To freeze requirements files for additional dependencies, make sure you activate that .venv first

```bash
source .venv-notebook/bin/activate # activate venv with additional depencies
uv pip freeze > requirements-notebook.txt
```

#### Uv pip install vs uv add

The difference between `uv pip install` and `uv add` is that `uv add` is a shortcut for installing a package and updating `pyproject.toml` at the same time. If you only install a package using `uv pip install`, it will not be recorded in `pyproject.toml`.

_Example: Install a package for temporary use_

```bash
uv pip install seaborn
```

This installs seaborn without modifying `pyproject.toml`

### Running a Script with a Temporary Set of Requirements

If you want to run a script with a temporary environment (without permanently installing packages), use:

```bash
uv pip install -r requirements-notebook.txt --run python script.py
```

This:

- Installs dependencies only for this session.
- Does not persist them in requirements.txt.
