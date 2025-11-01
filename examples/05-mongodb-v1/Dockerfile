# Simple Node.js Express + MongoDB To-Do app
FROM node:20-alpine

# Create app directory
WORKDIR /app

# Install app dependencies
COPY package*.json ./
RUN npm install --omit=dev

# Bundle app source
COPY src ./src

EXPOSE 3000

ENV NODE_ENV=production \
    PORT=3000

CMD ["node", "src/app.js"]
