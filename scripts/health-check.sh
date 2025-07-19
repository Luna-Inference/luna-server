#!/bin/bash
# scripts/health-check.sh

# Use user-accessible log location to avoid permission issues
LOG_FILE="/home/luna/luna-health.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Check LLM service
if ! curl -sf http://localhost:1306/health > /dev/null 2>&1; then
    log "HEALTH: LLM service is down, restarting"
    sudo systemctl restart llm.service
    sleep 10
    if curl -sf http://localhost:1306/health > /dev/null 2>&1; then
        log "HEALTH: LLM service restarted successfully"
    else
        log "HEALTH: LLM service failed to restart"
    fi
fi

# Check Status service
if ! curl -sf http://localhost:1309/luna > /dev/null 2>&1; then
    log "HEALTH: Status service is down, restarting"
    sudo systemctl restart status.service
    sleep 10
    if curl -sf http://localhost:1309/luna > /dev/null 2>&1; then
        log "HEALTH: Status service restarted successfully"
    else
        log "HEALTH: Status service failed to restart"
    fi
fi