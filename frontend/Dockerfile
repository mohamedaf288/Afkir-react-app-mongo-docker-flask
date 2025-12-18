FROM node:16
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose React dev server port
EXPOSE 3000

# Start the development server
CMD ["npm", "start"]
