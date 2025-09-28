# 🚀 Quick Start Guide

## Step-by-Step Setup

### 1. Set up environment
```bash
cd phoenix-ai
cp .env.template .env
echo "OPENAI_API_KEY=your_key_here" > .env
```

### 2. Start services
```bash
docker compose up --build
```

## 🐛 Troubleshooting

### Backend Health Check Issues

If you see "dependency failed to start: container phoenix-ai-backend-1 is unhealthy":

1. **Check backend logs**:
```bash
docker compose logs backend
```

2. **Check if backend is responding**:
```bash
# In another terminal
curl http://localhost:8000/api/chat/healthcheck
```

3. **Run without health check dependencies**:
```bash
# Start Phoenix first
docker compose up phoenix

# Then start backend
docker compose up backend

# Then start frontend
docker compose up frontend
```

4. **Check if all services are running**:
```bash
docker compose ps
```

### Common Issues

- **Missing OpenAI API Key**: Backend will start but may show warnings
- **Port conflicts**: Make sure ports 3000, 6006, 8000 are available
- **Docker issues**: Try `docker compose down` then `docker compose up --build`

### Alternative: Start services individually
```bash
# Start Phoenix only
docker compose up phoenix

# In another terminal, test backend directly
cd backend
pip install -r requirements.txt
python main.py
```
