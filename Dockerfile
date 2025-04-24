# Specify our Python version
FROM python:3.12

# Add the NodeSource PPA
RUN echo 'Package: nodejs\nPin: origin deb.nodesource.com\nPin-Priority: 600' > /etc/apt/preferences.d/nodesource \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get update \
    && apt-get install -y nodejs

# Install yarn
RUN npm install -g yarn

# Set working directory
WORKDIR /app

# Copy pyproject file to the working directory
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir .

# Copy package and lock files to the working directory
COPY package.json yarn.lock .

# Install dependencies
RUN yarn install

# Copy the rest of the application code
COPY . .

# Expose the port that the app runs on
EXPOSE 8080

# Start the app in development mode
CMD ["yarn", "develop"]
