FROM python:3.9

# Add the NodeSource PPA
RUN echo 'Package: nodejs\nPin: origin deb.nodesource.com\nPin-Priority: 600' > /etc/apt/preferences.d/nodesource \
    && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs

# Install updates
RUN apt-get update

# Install yarn
RUN npm install -g yarn

# Set working directory
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Copy package.json and yarn.lock to the working directory
COPY package.json .
COPY yarn.lock .

# Copy the rest of the application code
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install dependencies
RUN yarn install

# Expose the port that the app runs on
EXPOSE 8080

# Start the app in development mode
CMD ["yarn", "develop"]
