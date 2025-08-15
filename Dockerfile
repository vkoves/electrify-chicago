# Specify our Python version
FROM python:3.12

# Add the NodeSource PPA
RUN echo 'Package: nodejs\nPin: origin deb.nodesource.com\nPin-Priority: 600' > /etc/apt/preferences.d/nodesource \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get update \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install yarn
RUN npm install -g yarn

# Set working directory
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set up uv environment for caching
# See:
# - https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy frontend package and lock files to the working directory
COPY package.json yarn.lock .

# Install dependencies
RUN yarn install

# Copy the rest of the application code
COPY . .

# Finish installing the python project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Expose the port that the app runs on
EXPOSE 8080

# Start the app in development mode
CMD ["yarn", "develop"]
