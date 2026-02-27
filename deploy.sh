#!/bin/bash
# Lightweight deployment script - NO MODEL FILES
# Model is installed once on server using install_model_on_server.py

set -e

echo "=========================================="
echo "Deploying Embedding Service (No Models)"
echo "=========================================="

# Configuration
SERVER_USER="YOUR_USER"
SERVER_HOST="YOUR_SERVER"
SERVER_PATH="/var/www/gift-intelligence"

# Files to deploy (EXCLUDE models)
DEPLOY_FILES=(
    "app_embedding_service.py"
    "requirements.txt"
    "README.md"
    "embedding-service.service"
    "nginx-embedding-service.conf"
    "install_model_on_server.py"
)

echo ""
echo "Files to deploy:"
for file in "${DEPLOY_FILES[@]}"; do
    echo "  - $file"
done

echo ""
read -p "Deploy to ${SERVER_USER}@${SERVER_HOST}? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 1
fi

echo ""
echo "Step 1: Creating deployment package..."
tar -czf deploy_package.tar.gz "${DEPLOY_FILES[@]}"
ls -lh deploy_package.tar.gz

echo ""
echo "Step 2: Uploading to server..."
scp deploy_package.tar.gz "${SERVER_USER}@${SERVER_HOST}:/tmp/"

echo ""
echo "Step 3: Extracting on server..."
ssh "${SERVER_USER}@${SERVER_HOST}" << 'ENDSSH'
    cd /var/www/gift-intelligence
    tar -xzf /tmp/deploy_package.tar.gz
    rm /tmp/deploy_package.tar.gz
    
    # Install Python dependencies
    source venv/bin/activate
    pip install -r requirements.txt --upgrade
    deactivate
    
    echo "✅ Files deployed successfully"
ENDSSH

echo ""
echo "Step 4: Restarting service..."
ssh "${SERVER_USER}@${SERVER_HOST}" "sudo systemctl restart embedding-service"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Check status with:"
echo "  ssh ${SERVER_USER}@${SERVER_HOST} 'sudo systemctl status embedding-service'"
echo ""
