#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# Update & install Nginx if not installed
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y nginx

# Create required directories
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Create a test HTML file
sudo tee /data/web_static/releases/test/index.html >/dev/null <<EOF
<html>
  <head></head>
  <body>
    Holberton School
  </body>
</html>
EOF

# Create or update the symbolic link
sudo ln -sfn /data/web_static/releases/test/ /data/web_static/current

# Set ownership to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Add Nginx location for /hbnb_static/ if it doesn’t already exist
NGINX_CONF="/etc/nginx/sites-available/default"
if ! grep -q "location /hbnb_static/" "$NGINX_CONF"; then
    sudo sed -i '/server_name _;/a \    location /hbnb_static/ {\n        alias /data/web_static/current/;\n    }' "$NGINX_CONF"
fi

# Test Nginx configuration and restart
sudo nginx -t
sudo systemctl restart nginx

exit 0