# luna-server
A backend for luna device with LLM, TTS, STT, Status, RAG &amp; Display

## rag
```
sudo cp -r rag/rag.service /etc/systemd/system/rag.service

sudo systemctl daemon-reload          # Reload systemd configurations
sudo systemctl enable rag.service   # Auto-start on boot
sudo systemctl start rag.service    # Start service now

sudo systemctl stop rag.service     # Stop the service
sudo systemctl restart rag.service  # Restart the service
sudo systemctl disable rag.service  # Remove from boot startup

systemctl status rag.service        # Current status and recent logs
journalctl -u rag.service          # View all logs for this service
journalctl -u rag.service -f       # Follow logs in real-time
journalctl -u rag.service --since today  # View today's logs only
journalctl -u rag.service --since "2024-01-01" --until "2024-01-02"  # Date range
```

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

## updates


```
# Auto update
sudo cp -r scripts/luna-update.service /etc/systemd/system/luna-update.service
sudo cp -r scripts/luna-update.timer /etc/systemd/system/luna-update.timer

sudo systemctl daemon-reload          # Reload systemd configurations
sudo systemctl enable luna-update.timer   # Auto-start on boot
sudo systemctl start luna-update.timer    # Start service now

sudo systemctl stop luna-update.timer     # Stop the service
sudo systemctl restart luna-update.timer  # Restart the service
sudo systemctl disable luna-update.timer  # Remove from boot startup

systemctl status luna-update.timer        # Current status and recent logs
journalctl -u luna-update.timer          # View all logs for this service
journalctl -u luna-update.timer -f       # Follow logs in real-time
journalctl -u luna-update.timer --since today  # View today's logs only
journalctl -u luna-update.timer --since "2024-01-01" --until "2024-01-02"  # Date range
```
```
# Manual update
./scripts/auto-update.sh
```

```
# Monitor update logs

# On any device, check update logs
tail -f /var/log/luna-update.log

# Check health logs
tail -f /var/log/luna-health.log

# Check service status
systemctl status llm.service status.service
```
