# luna-server
A backend for luna device with LLM, TTS, STT, Status, RAG &amp; Display

## llm
```
sudo cp -r llm/llm.service /etc/systemd/system/llm.service

sudo systemctl daemon-reload          # Reload systemd configurations
sudo systemctl enable llm.service   # Auto-start on boot
sudo systemctl start llm.service    # Start service now

sudo systemctl stop llm.service     # Stop the service
sudo systemctl restart llm.service  # Restart the service
sudo systemctl disable llm.service  # Remove from boot startup

systemctl status llm.service        # Current status and recent logs
journalctl -u llm.service          # View all logs for this service
journalctl -u llm.service -f       # Follow logs in real-time
journalctl -u llm.service --since today  # View today's logs only
journalctl -u llm.service --since "2024-01-01" --until "2024-01-02"  # Date range
```

## status
```
sudo cp -r status/status.service /etc/systemd/system/status.service

sudo systemctl daemon-reload          # Reload systemd configurations
sudo systemctl enable status.service   # Auto-start on boot
sudo systemctl start status.service    # Start service now

sudo systemctl stop status.service     # Stop the service
sudo systemctl restart status.service  # Restart the service
sudo systemctl disable status.service  # Remove from boot startup

systemctl status status.service        # Current status and recent logs
journalctl -u status.service          # View all logs for this service
journalctl -u status.service -f       # Follow logs in real-time
journalctl -u status.service --since today  # View today's logs only
journalctl -u status.service --since "2024-01-01" --until "2024-01-02"  # Date range
```
