FROM jupyter/scipy-notebook@sha256:fca4bcc9cbd49d9a15e0e4df6c666adf17776c950da9fa94a4f0a045d5c4ad33

RUN pip install poetry==1.8.2 \
    && poetry config virtualenvs.create false

ARG DOCKER_DIR=src/data/research/docker

COPY ${DOCKER_DIR}/poetry.lock ${DOCKER_DIR}/pyproject.toml ./work/

RUN cd work \
    && poetry install --no-interaction \
    && rm poetry.lock pyproject.toml
