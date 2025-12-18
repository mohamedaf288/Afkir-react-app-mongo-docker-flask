# React-Flask-MongoDB Application

A full-stack task management application with React frontend, Flask backend, and MongoDB database, fully containerized with Docker.

## 📁 Project Structure

```
.
├── backend/
│   ├── app.py              # Flask API application
│   ├── Dockerfile          # Backend container configuration
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/                # React source files
│   ├── public/             # Static assets
│   ├── Dockerfile          # Frontend container configuration
│   └── package.json        # Node dependencies
├── docker-compose.yml      # Multi-container orchestration
└── running.sh              # Quick start script
```

## 🚀 Quick Start

### Prerequisites
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed ([Get Docker Compose](https://docs.docker.com/compose/install/))

### Running the Application

**Option 1: Using the startup script (Linux/Mac)**
```bash
chmod +x running.sh
./running.sh
```

**Option 2: Manual Docker Compose**
```bash
# Build and start all services
docker-compose up --build -d

# Initialize MongoDB with sample data
docker exec -i mongodb mongosh <<EOF
use mongotask
db.tasks.insertMany([
  {"title": "course"},
  {"title": "training"},
  {"title": "pause"}
])
EOF
```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api/tasks
- **MongoDB**: localhost:27017

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks |
| POST | `/api/task` | Create a new task |
| PUT | `/api/task/<id>` | Update a task |
| DELETE | `/api/task/<id>` | Delete a task |

## 🛠️ Development

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongo
```

### Restart Services
```bash
docker-compose restart
```

### Stop Services
```bash
docker-compose down
```

### Stop and Remove Volumes
```bash
docker-compose down -v
```

## 🗄️ MongoDB Management

### Access MongoDB Shell
```bash
docker exec -it mongodb mongosh
```

### View Tasks
```javascript
use mongotask
db.tasks.find().pretty()
```

### Add a Task
```javascript
db.tasks.insert({"title": "New Task"})
```

## 🏗️ Architecture

### Services

1. **MongoDB (mongo)**
   - Image: mongo:4.4
   - Port: 27017
   - Persistent volume for data storage

2. **Flask Backend (backend)**
   - Python 3.9
   - Flask REST API
   - Connects to MongoDB via Docker network

3. **React Frontend (frontend)**
   - Node 16
   - React development server
   - Proxies API requests to backend

### Networking
All services communicate through a custom bridge network (`app-network`), allowing service discovery by container name.

## 🔧 Troubleshooting

### Services won't start
```bash
# Check service status
docker-compose ps

# View error logs
docker-compose logs
```

### Port already in use
Stop any services using ports 3000, 5000, or 27017, or modify the port mappings in `docker-compose.yml`.

### MongoDB connection issues
Ensure the MongoDB container is running:
```bash
docker-compose ps mongo
```

## 📝 Technology Stack

- **Frontend**: React 16.5, Axios
- **Backend**: Flask 2.3, Flask-PyMongo, Flask-CORS
- **Database**: MongoDB 4.4
- **Containerization**: Docker, Docker Compose

## 📄 License

This project is open source and available for educational purposes.# react-mongo-flask
