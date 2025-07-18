# luna-server
A backend for luna device with LLM, TTS, STT, Status, RAG &amp; Display

## llm
```
sudo cp -r llm/llm.service /etc/systemd/system/llm.service

sudo systemctl daemon-reload          # Reload systemd configurations
sudo systemctl enable myapp.service   # Auto-start on boot
sudo systemctl start myapp.service    # Start service now

sudo systemctl stop myapp.service     # Stop the service
sudo systemctl restart myapp.service  # Restart the service
sudo systemctl disable myapp.service  # Remove from boot startup

systemctl status myapp.service        # Current status and recent logs
journalctl -u myapp.service          # View all logs for this service
journalctl -u myapp.service -f       # Follow logs in real-time
journalctl -u myapp.service --since today  # View today's logs only
journalctl -u myapp.service --since "2024-01-01" --until "2024-01-02"  # Date range
