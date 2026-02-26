#!/bin/bash
# Server Setup Script for Embedding Service
# Run these commands on your Ubuntu server

echo "=========================================="
echo "Setting up Embedding Service on Server"
echo "=========================================="

# 1. Upload configuration files to server
echo ""
echo "Step 1: Upload configuration files from your Mac:"
echo "-----------------------------------------------"
echo "scp embedding-service.service YOUR_USER@YOUR_SERVER:/tmp/"
echo "scp nginx-embedding-service.conf YOUR_USER@YOUR_SERVER:/tmp/"
echo ""

# 2. SSH into server and run the following:
echo "Step 2: SSH into your server and run these commands:"
echo "-----------------------------------------------"
echo "ssh YOUR_USER@YOUR_SERVER"
echo ""

# 3. Install dependencies
echo "# Install Python venv if not already installed"
echo "sudo apt update"
echo "sudo apt install -y python3-venv python3-pip nginx"
echo ""

# 4. Create virtual environment and install packages
echo "# Create virtual environment"
echo "cd /var/www/gift-intelligence"
echo "python3 -m venv venv"
echo "source venv/bin/activate"
echo "pip install -r requirements.txt"
echo "deactivate"
echo ""

# 5. Setup systemd service
echo "# Setup systemd service"
echo "sudo mv /tmp/embedding-service.service /etc/systemd/system/"
echo "sudo systemctl daemon-reload"
echo "sudo systemctl enable embedding-service"
echo "sudo systemctl start embedding-service"
echo ""

# 6. Check service status
echo "# Check service status"
echo "sudo systemctl status embedding-service"
echo ""

# 7. Setup Nginx
echo "# Setup Nginx"
echo "sudo mv /tmp/nginx-embedding-service.conf /etc/nginx/sites-available/embedding-service"
echo ""
echo "# EDIT the nginx config file and replace 'your-domain.com' with your actual domain/IP:"
echo "sudo nano /etc/nginx/sites-available/embedding-service"
echo ""
echo "# Enable the site"
echo "sudo ln -s /etc/nginx/sites-available/embedding-service /etc/nginx/sites-enabled/"
echo ""
echo "# Test Nginx configuration"
echo "sudo nginx -t"
echo ""
echo "# Remove default Nginx site (optional)"
echo "sudo rm /etc/nginx/sites-enabled/default"
echo ""
echo "# Restart Nginx"
echo "sudo systemctl restart nginx"
echo ""

# 8. Setup firewall
echo "# Setup firewall (if using UFW)"
echo "sudo ufw allow 'Nginx Full'"
echo "sudo ufw allow OpenSSH"
echo "sudo ufw enable"
echo ""

# 9. Create log files
echo "# Create log files with correct permissions"
echo "sudo touch /var/log/embedding-service.log"
echo "sudo touch /var/log/embedding-service-error.log"
echo "sudo chown www-data:www-data /var/log/embedding-service*.log"
echo ""

# 10. Set correct permissions
echo "# Set correct permissions"
echo "sudo chown -R www-data:www-data /var/www/gift-intelligence"
echo "sudo chmod -R 755 /var/www/gift-intelligence"
echo ""

echo "=========================================="
echo "Useful Commands:"
echo "=========================================="
echo ""
echo "# View service logs (live)"
echo "sudo journalctl -u embedding-service -f"
echo ""
echo "# View service logs (last 100 lines)"
echo "sudo journalctl -u embedding-service -n 100"
echo ""
echo "# View application logs"
echo "sudo tail -f /var/log/embedding-service.log"
echo ""
echo "# Restart service"
echo "sudo systemctl restart embedding-service"
echo ""
echo "# Stop service"
echo "sudo systemctl stop embedding-service"
echo ""
echo "# Check Nginx status"
echo "sudo systemctl status nginx"
echo ""
echo "# Test API"
echo "curl http://localhost:8001/health"
echo "curl http://YOUR_DOMAIN/health"
echo ""
