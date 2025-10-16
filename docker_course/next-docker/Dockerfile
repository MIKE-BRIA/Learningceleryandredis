# syntax=docker/dockerfile:1
ARG NODE_VERSION=22.20.0
FROM node:${NODE_VERSION}-alpine

ENV NODE_ENV=production

# Set working directory
WORKDIR /usr/src/app

# Give permissions to the node user for this directory
RUN chown -R node:node /usr/src/app

# Copy dependency files first
COPY package*.json ./

# Install dependencies (as root, then switch later)
RUN npm install --omit=dev

# Copy the rest of the source files
COPY . .

# Switch to non-root user
USER node

EXPOSE 3000

CMD ["npm", "run", "dev"]
