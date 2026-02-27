# Gift Intelligence - Embedding Service

FastAPI-based text embedding service using MiniLM-L6-v2 model (384-dimensional vectors).

## Features
- 🚀 Fast text-to-vector conversion
- 🔄 Batch processing support
- 📦 Lightweight deployment (no model files in repo)
- ⚡ Pre-loaded model (no cold starts)
- 🔒 Production-ready with systemd + Nginx

## Quick Start (Local Development)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally (model will auto-download)
uvicorn app_embedding_service:app --reload --port 8000
```

Visit: http://localhost:8000/docs

## Server Deployment

The model is installed **once** on the server. Code deployments are lightweight and fast.

### One-Time Server Setup
See [DEPLOYMENT.md](DEPLOYMENT.md) for complete guide:

1. Install model on server (one time):
   ```bash
   python3 install_model_on_server.py
   ```

2. Setup systemd service and Nginx

### Regular Deployments (Fast)
```bash
# Edit deploy.sh with your server details
./deploy.sh
```

Only code files are deployed (~50KB), not model files (90MB).

## API Endpoints

- `GET /health` - Health check
- `POST /embed` - Generate embeddings
- `GET /docs` - API documentation

## Architecture

- **Model**: sentence-transformers/all-MiniLM-L6-v2
- **Embedding Dimension**: 384D
- **Max Sequence Length**: 256 tokens
- **Server Location**: /opt/models/minilm/

