# Python Developer Guide

**Everything you need to know about managing Python dependencies, running scripts, and setting up a virtual environment for Electrify-Chicago.**

### Python Virtual Environments: When to use one

You can run our data pipeline processes either within the Docker container or directly from a bash terminal. Docker provides a fully configured environment, ensuring complete consistency across development and deployment. We use Docker to run the web server and data processing scripts in production, and you can use it for local development as well.

However, sometimes you may prefer running scripts locally/outside of Docker — perhaps for faster development cycles, debugging, or when working with Jupyter notebooks. In these cases, **always use a virtual environment**. This ensures you're using the correct dependency versions for our project, even while outside the Docker container. Without a virtual environment, you risk using system-wide Python packages that might differ from our project requirements, leading to inconsistent behavior between your local runs and the containerized environment.

The key workflow is simple: If you want to run Python code outside of the Docker container, make sure you are running it with your virtual environment activated. The steps to create an environment, activate it and sync the environment with our project dependency list is contained below:

## Setting up a Virtual Environment

### Python Version

We are currently using Python 3.12. This is hardcoded in the following places:

- Our Github CI Pipeline:
  - [.github/workflows/pytest.yml](.github/workflows/pytest.yml)
- Our Dockerfile:
  - [Dockerfile](Dockerfile)
- Our netlify.toml file:
  - [netlify.toml](netlify.toml)

### Export Python Version

Run the following command to set the Python version to 3.12 in your terminal:

```bash
export PYTHON_VERSION="3.12"
```

### Python Dependency List

We use a [pyproject.toml](pyproject.toml) file to manage our Python dependencies. This file contains a list of all the packages required to run our project. The dependencies are divided into two groups:

- **Core Dependencies**: Required for running data processing scripts.
  - _listed under `[dependencies]` in `pyproject.toml`_
- **Notebook Dependencies**: Additional packages required for running Jupyter notebooks.
  - _listed under [project.optional-dependencies] notebook = []_

As the project becomes more complex, we may add more dependencies to these groups or create new groups for different purposes. The `pyproject.toml` file is the single source of truth for all Python dependencies in our project.

## Managing Python Dependencies with the Package Manager 'UV'

[uv](https://github.com/astral-sh/uv) is a fast Python package manager that replaces pip and venv while offering better performance, deterministic resolution, and a simplified workflow. Unlike pip, uv does not require the use of venv for isolating dependencies, but it works seamlessly with existing virtual environments.

### UV Installation and Setup Guide

MacOS and Linux users can install uv using the following command:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

See the [uv installation guide](https://docs.astral.sh/uv/#installation) for more details.

### Set up the project with uv

You should be able to run the following command to set up the project with uv:

```bash
uv sync --locked --all-groups
```

This installs Python and all of the dependencies in a virtual environment `.venv`.

To run scripts or commands under this environment prefix them with `uv run`, like so:

```bash
uv run python script.py
```

Or

```bash
uv run jupyter notebook
```

### Install the Baseline Dependencies (Core Requirements)

These are the minimal dependencies required for running data processing scripts.

- Defined in [pyproject.toml](pyproject.toml) under `[dependencies]`

**Install core package**

```bash
uv sync --locked
```

### Data Analysis Notebook-Specific Dependencies

Additional dependencies for running Jupyter notebooks are defined as an extra group in pyproject.toml.

- Defined under `[dependency-groups]` -> `notebook` in [pyproject.toml](pyproject.toml)

To install both baseline + notebook dependencies:

```bash
uv sync --locked --group notebook
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

You can add a package to the notebook dependencies using `uv add` as well, but you need to specify the group:

```bash
uv add kaleido --group notebook
```

#### Uv pip install vs uv add

The difference between `uv pip install` and `uv add` is that `uv add` is a shortcut for installing a package and updating `pyproject.toml` at the same time. If you only install a package using `uv pip install`, it will not be recorded in `pyproject.toml`.

_Example: Install a package for temporary use_

```bash
uv pip install seaborn
```

This installs seaborn without modifying `pyproject.toml`.
This is useful if you want to experiemnt with a package or use a one off CLI without committing it to the project dependencies.
