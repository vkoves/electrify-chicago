# Ensures Node.js 16.x is installed, which is required for running Gridsome app
FROM node:16-alpine

# Install libvips 
#! Not sure if I really need all of these
RUN apk update && apk add --no-cache \
  build-base \
	autoconf \
	automake \
	libtool \
	bc \
	zlib-dev \
	expat-dev \
	jpeg-dev \
	tiff-dev \
	glib-dev \
	libjpeg-turbo-dev \
	libexif-dev \
	lcms2-dev \
	fftw-dev \
	giflib-dev \
	libpng-dev \
	libwebp-dev \
	orc-dev \
	libgsf-dev \
  vips-dev \
  librsvg-dev \
  binutils \
  gcc \
  libgcc \
  libstdc++ \
  linux-headers \
  python3

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install Python pip
RUN apk add --no-cache py3-pip

# Install Python dependencies
#! Pandas install exits with error
RUN pip3 install --no-cache-dir -r requirements.txt

# Set working directory
WORKDIR /app

# Copy package.json and yarn.lock to the working directory
COPY package.json yarn.lock ./

# Copy the rest of the application code
COPY . .

# Install npm dependencies
#! Something went wrong installing the "sharp" module
#! Error loading shared library /app/node_modules/sharp/build/Release/sharp.node: Exec format error
RUN yarn install --frozen-lockfile
# --frozen-lockfile: ensures Yarn uses the exact versions of dependencies in yarn.lock file to ensure consistent builds across different environments

# Expose the port that the app runs on
EXPOSE 8080

# Start the app in development mode
CMD ["yarn", "develop"]