#!/bin/bash
# scripts/auto-update.sh
# Auto-update script for Luna Server - checks for GitHub updates and applies them safely

# Exit immediately if any command fails (safety measure)
set -e

# ==================== CONFIGURATION ====================
# Where the Luna server code is installed
REPO_DIR="/home/luna/luna-server"

# Which Git branch to track for updates
BRANCH="main"

# Where to write update logs (in user's home directory to avoid permission issues)
LOG_FILE="/home/luna/luna-update.log"

# Where to store backup before updating (for rollback)
BACKUP_DIR="/home/luna/luna-server-backup"

# ==================== UTILITY FUNCTIONS ====================

# Logging function - writes messages with timestamps to both console and log file
log() {
    # $1 is the message to log
    # date creates timestamp, tee writes to both stdout and log file
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Health check function - tests if both services are responding
check_services() {
    # Local variables to track service status (0 = down, 1 = up)
    local llm_status=0
    local status_status=0
    
    # Test LLM service by hitting its health endpoint
    # curl -sf: s=silent (no progress), f=fail on HTTP errors
    # > /dev/null 2>&1: throw away all output
    if curl -sf http://localhost:1306/health > /dev/null 2>&1; then
        llm_status=1  # Mark as healthy
    fi
    
    # Test Status service by hitting its recognition endpoint
    if curl -sf http://localhost:1309/luna > /dev/null 2>&1; then
        status_status=1  # Mark as healthy
    fi
    
    # Return success (0) only if BOTH services are healthy
    if [ $llm_status -eq 1 ] && [ $status_status -eq 1 ]; then
        return 0  # Success: both services healthy
    else
        return 1  # Failure: at least one service is down
    fi
}

# Rollback function - restores previous working version when update fails
rollback() {
    log "ROLLBACK: Rolling back to previous version"
    
    # Stop both services before making changes
    sudo systemctl stop llm.service status.service
    
    # Try to restore from backup directory first
    if [ -d "$BACKUP_DIR" ]; then
        # Remove broken updated version
        rm -rf "$REPO_DIR"
        # Restore backup as the main directory
        mv "$BACKUP_DIR" "$REPO_DIR"
        log "ROLLBACK: Backup restored"
    else
        # No backup available, try Git reset as fallback
        log "ROLLBACK: No backup found, attempting git reset"
        cd "$REPO_DIR"
        # Reset to previous commit (HEAD~1 means "one commit before current")
        git reset --hard HEAD~1
    fi
    
    # Start services with the restored code
    sudo systemctl start llm.service status.service
    
    # Wait for services to start up
    sleep 15
    
    # Test if rollback worked
    if check_services; then
        log "ROLLBACK: Services restored successfully"
        return 0  # Rollback succeeded
    else
        log "ROLLBACK: Services still failing after rollback!"
        return 1  # Rollback failed - serious problem
    fi
}

# ==================== MAIN UPDATE LOGIC ====================

# Main update function - handles the entire update process
perform_update() {
    log "UPDATE: Starting update process"
    
    # Change to the repository directory
    cd "$REPO_DIR"
    
    # Download latest information from GitHub (but don't merge yet)
    git fetch origin "$BRANCH"
    
    # Get the hash of our current commit
    LOCAL_COMMIT=$(git rev-parse HEAD)
    
    # Get the hash of the latest commit on GitHub
    REMOTE_COMMIT=$(git rev-parse origin/$BRANCH)
    
    # Compare commits to see if we need to update
    if [ "$LOCAL_COMMIT" = "$REMOTE_COMMIT" ]; then
        log "UPDATE: Already up to date"
        return 0  # No update needed
    fi
    
    # Show first 8 characters of commit hashes for debugging
    log "UPDATE: Update available. Local: ${LOCAL_COMMIT:0:8}, Remote: ${REMOTE_COMMIT:0:8}"
    
    # Create a backup of current working version before updating
    log "UPDATE: Creating backup"
    rm -rf "$BACKUP_DIR"  # Remove any old backup
    cp -r "$REPO_DIR" "$BACKUP_DIR"  # Copy entire directory
    
    # Check if Python dependencies changed between versions
    REQUIREMENTS_CHANGED=0
    # git diff shows what changed between commits, --name-only shows only filenames
    # grep -q returns success if pattern found (requirements.txt in any changed file)
    if git diff "$LOCAL_COMMIT" "$REMOTE_COMMIT" --name-only | grep -q requirements.txt; then
        REQUIREMENTS_CHANGED=1
        log "UPDATE: Requirements files changed, will update dependencies"
    fi
    
    # Stop services before updating code (prevents issues with running code being changed)
    log "UPDATE: Stopping services"
    sudo systemctl stop llm.service status.service
    
    # Download and apply the latest changes from GitHub
    log "UPDATE: Pulling latest changes"
    git pull origin "$BRANCH"
    
    # Update Python dependencies if requirements.txt files changed
    if [ $REQUIREMENTS_CHANGED -eq 1 ]; then
        log "UPDATE: Updating Python dependencies"
        
        # Update LLM service dependencies
        if [ -f "llm/requirements.txt" ]; then  # Check if file exists
            cd llm  # Enter LLM directory
            
            # Check if virtual environment exists
            if [ -d "myenv" ]; then
                # Use virtual environment
                source myenv/bin/activate  # Activate venv
                pip install -r requirements.txt  # Install/update packages
                deactivate  # Exit venv
            else
                # Use system Python
                python3 -m pip install -r requirements.txt
            fi
            cd ..  # Return to parent directory
        fi
        
        # Update Status service dependencies (same logic as above)
        if [ -f "status/requirements.txt" ]; then
            cd status
            if [ -d "myenv" ]; then
                source myenv/bin/activate
                pip install -r requirements.txt
                deactivate
            else
                python3 -m pip install -r requirements.txt
            fi
            cd ..
        fi
    fi
    
    # Start services with updated code
    log "UPDATE: Starting services"
    sudo systemctl start llm.service status.service
    
    # Give services time to start up properly
    log "UPDATE: Waiting for services to start"
    sleep 15
    
    # Test if update was successful
    if check_services; then
        # Update successful!
        log "UPDATE: Update successful! Services are healthy"
        
        # Clean up backup since we don't need it anymore
        rm -rf "$BACKUP_DIR"
        
        # Read and log the new version number
        NEW_VERSION=$(cat VERSION 2>/dev/null || echo "unknown")
        log "UPDATE: Updated to version $NEW_VERSION"
        
        return 0  # Success
    else
        # Update failed - services aren't responding
        log "UPDATE: Health check failed, initiating rollback"
        rollback  # Try to restore previous working version
        return 1  # Failure
    fi
}

# ==================== MAIN EXECUTION ====================

# Main function - entry point that coordinates everything
main() {
    log "AUTO-UPDATE: Starting auto-update check"
    
    # Verify repository directory exists
    if [ ! -d "$REPO_DIR" ]; then
        log "ERROR: Repository directory $REPO_DIR not found"
        exit 1  # Exit with error code
    fi
    
    # Verify it's actually a Git repository
    if [ ! -d "$REPO_DIR/.git" ]; then
        log "ERROR: $REPO_DIR is not a git repository"
        exit 1  # Exit with error code
    fi
    
    # Run the update process
    if perform_update; then
        # Update succeeded
        log "AUTO-UPDATE: Update process completed successfully"
        exit 0  # Exit with success code
    else
        # Update failed
        log "AUTO-UPDATE: Update process failed"
        exit 1  # Exit with error code
    fi
}

# Start the script by calling main function
# "$@" passes all command line arguments to main (though we don't use any)
main "$@"