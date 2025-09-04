# Simple Node.js-based static file server for index.html
# Build stage is not necessary, we can use a single-stage image
FROM node:18-alpine

# Set working directory
WORKDIR /usr/src/app

# Copy static file(s)
COPY index.html ./

# Install a tiny static server
# Using "serve" for simplicity and low footprint
RUN npm install -g serve@14

# Expose port
EXPOSE 3000

# Start the static server serving current directory
CMD ["serve", ".", "-l", "3000", "-s"]
