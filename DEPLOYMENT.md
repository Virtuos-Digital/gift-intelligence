# Deployment Guide - Lightweight (No Model Files)

## Overview
The model is **installed once** on the server in `/opt/models/minilm/` and never needs to be redeployed. Your code deployments are fast and lightweight.

## Initial Server Setup (ONE TIME ONLY)

### 1. Install Model on Server (Run Once)
```bash
# SSH into server
ssh YOUR_USER@YOUR_SERVER

# Create model directory
sudo mkdir -p /opt/models/minilm
sudo chown $USER:$USER /opt/models/minilm

# Navigate to app directory
cd /var/www/gift-intelligence

# Upload install_model_on_server.py to server first
# Then run:
source venv/bin/activate
python3 install_model_on_server.py
deactivate
```

This downloads the model (~90MB) and saves it permanently in `/opt/models/minilm/`

### 2. Setup Service & Nginx (One Time)
```bash
# Copy service file
sudo cp embedding-service.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable embedding-service
sudo systemctl start embedding-service

# Setup Nginx
sudo cp nginx-embedding-service.conf /etc/nginx/sites-available/embedding-service
sudo ln -s /etc/nginx/sites-available/embedding-service /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Regular Deployments (Fast - No Models)

### Option 1: Manual Deployment
```bash
# On your Mac - deploy only code files
scp app_embedding_service.py requirements.txt YOUR_USER@YOUR_SERVER:/var/www/gift-intelligence/

# On server
ssh YOUR_USER@YOUR_SERVER
cd /var/www/gift-intelligence
source venv/bin/activate
pip install -r requirements.txt
deactivate
sudo systemctl restart embedding-service
```

### Option 2: Automated Deployment Script
```bash
# Edit deploy.sh and set YOUR_USER and YOUR_SERVER
nano deploy.sh

# Make executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

---

## What Gets Deployed vs What Stays on Server

### Deployed with Each Update (Lightweight):
- `app_embedding_service.py` (your code)
- `requirements.txt` (dependencies)
- Configuration files (if changed)

### Installed Once on Server (Heavy):
- Model files in `/opt/models/minilm/` (~90MB)
- Virtual environment
- System dependencies (nginx, python)

---

## Files You Can Delete Locally

After initial setup, you can delete these from your local repo:
```bash
rm -rf minilm_full_dimension_models/
rm minilm_model.tar.gz
rm upload_instructions.sh
```

Your deployment package will be **< 50KB** instead of 90MB!

---

## Environment Variables (Optional)

To use a different model path, set environment variable on server:
```bash
# In /etc/systemd/system/embedding-service.service
Environment="EMBEDDING_MODEL_PATH=/custom/path/to/model"
```

---

## Troubleshooting

### Check if model is installed:
```bash
ls -lh /opt/models/minilm/model.safetensors
# Should show: ~87M
```

### Check service logs:
```bash
sudo journalctl -u embedding-service -f
```

### Reinstall model if needed:
```bash
cd /var/www/gift-intelligence
source venv/bin/activate
python3 install_model_on_server.py
```
