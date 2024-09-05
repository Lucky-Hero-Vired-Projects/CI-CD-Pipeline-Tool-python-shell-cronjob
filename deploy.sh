#!/bin/bash

# Configuration
REPO_URL="https://github.com/Lucky-Hero-Vired-Projects/CI-CD-Pipeline-Tool-python-shell-cronjob.git"  
LOCAL_REPO_PATH="/opt/nginx_deployment"  
NGINX_SERVICE="nginx"  
TARGET_DIR="/var/www/html/"

# Function to clone or pull the latest code
deploy_code() {
    if [ -d "$LOCAL_REPO_PATH" ]; then
        echo "Repository already exists. Pulling the latest changes..."
        cd "$LOCAL_REPO_PATH" || exit
        git pull origin main  
    else
        echo "Repository not found. Cloning the repository..."
        git clone "$REPO_URL" "$LOCAL_REPO_PATH"
    fi
}

copy_data() {
    sudo cp $LOCAL_REPO_PATH/index.html $TARGET_DIR/index.html     
    sudo chown nginx:nginx $TARGET_DIR/index.html
    sudo chmod 644 $TARGET_DIR/index.html
}

# Function to restart Nginx
restart_nginx() {
    echo "Restarting Nginx..."
    sudo systemctl restart "$NGINX_SERVICE"
}


deploy_code
copy_data
restart_nginx

echo "Deployment complete and Nginx restarted."
