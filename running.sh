#!/bin/bash

# ============================================
# React-Flask-MongoDB Docker Setup
# ============================================

echo "Starting React-Flask-MongoDB application with Docker..."

# Prerequisites:
# - Docker installed
# - Docker Compose installed

# ============================================
# STEP 1: Build and Start All Services
# ============================================

echo "Building Docker images and starting services..."
docker-compose up --build -d

echo "Waiting for services to start..."
sleep 10

# ============================================
# STEP 2: Initialize MongoDB Database
# ============================================

echo "Initializing MongoDB database..."

# Create database and insert sample tasks
docker exec -i mongodb mongosh <<EOF
use mongotask

// Insert sample tasks
db.tasks.insertMany([
  {"title": "course"},
  {"title": "training"},
  {"title": "pause"}
])

// Display all tasks
db.tasks.find().pretty()

// Optional: Create users (uncomment if needed)
// db.createUser({user: 'zh', pwd: 'test', roles: [{role: 'readWrite', db: 'mongotask'}]})
// db.createUser({user: 'ziyati', pwd: 'test', roles: [{role: 'readWrite', db: 'mongotask'}]})

exit
EOF

echo "MongoDB initialized successfully!"

# ============================================
# STEP 3: Check Service Status
# ============================================

echo ""
echo "Checking service status..."
docker-compose ps

echo ""
echo "============================================"
echo "Application is ready!"
echo "============================================"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:5000/api/tasks"
echo "MongoDB: localhost:27017"
echo ""
echo "Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Restart services: docker-compose restart"
echo "  - View MongoDB data: docker exec -it mongodb mongosh"
echo "============================================"
