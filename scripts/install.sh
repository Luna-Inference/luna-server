#!/bin/bash
# scripts/install.sh

REPO_URL="https://github.com/yourusername/luna-server.git"
INSTALL_DIR="/home/luna"
SERVICE_USER="luna"

# Create user if doesn't exist
if ! id "$SERVICE_USER" &>/dev/null; then
    sudo useradd -m -s /bin/bash "$SERVICE_USER"
fi

# Clone repository
cd "$INSTALL_DIR"
if [ -d "luna-server" ]; then
    echo "Luna server already exists, updating..."
    cd luna-server
    git pull
else
    echo "Cloning Luna server..."
    git clone "$REPO_URL"
    cd luna-server
fi

# Install dependencies
echo "Installing dependencies..."
cd llm
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

cd status  
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

# Set permissions
sudo chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR/luna-server"

# Install systemd services
sudo cp llm/llm.service /etc/systemd/system/
sudo cp status/status.service /etc/systemd/system/

# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable llm.service status.service
sudo systemctl start llm.service status.service

# Set up auto-updates
chmod +x scripts/auto-update.sh
chmod +x scripts/health-check.sh

# Add cron jobs
(crontab -l 2>/dev/null; echo "*/30 * * * * /home/luna/luna-server/scripts/auto-update.sh") | crontab -
(crontab -l 2>/dev/null; echo "*/5 * * * * /home/luna/luna-server/scripts/health-check.sh") | crontab -

echo "Luna server installation complete!"
echo "LLM Service: http://localhost:1306"
echo "Status Service: http://localhost:1309"