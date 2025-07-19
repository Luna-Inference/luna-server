# Central server for status, routing & detection
from flask import Flask, jsonify
from flask_cors import CORS
from config import *
import subprocess
import re
import os

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "supports_credentials": True,
        "max_age": 3600
    }
})

def get_cpu_usage():
    """Get current CPU usage percentage"""
    try:
        result = subprocess.run(
            "top -b -n 1 | grep \"%Cpu(s)\" | awk '{print 100 - $8}'",
            shell=True, check=True, capture_output=True, text=True
        )
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError) as e:
        app.logger.error(f"Error getting CPU usage: {str(e)}")
        return None

def get_npu_usage():
    """Get current NPU usage percentage for all cores and calculate average"""
    npu_file = "/sys/kernel/debug/rknpu/load"
    
    # Check if the file exists
    if not os.path.exists(npu_file):
        app.logger.error(f"NPU file not found at {npu_file}")
        return None
    
    # Check file permissions
    try:
        file_stat = os.stat(npu_file)
        app.logger.info(f"File stats: {file_stat}")
    except Exception as e:
        app.logger.error(f"Could not get file stats: {str(e)}")
    
    # Try to read the file directly first (without sudo)
    try:
        with open(npu_file, 'r') as f:
            content = f.read().strip()
            app.logger.info(f"Successfully read NPU file directly: {content}")
            # If we got here, we can parse the content
            usages = re.findall(r'Core\d+:\s*(\d+)%', content)
            if usages:
                usages = [int(usage) for usage in usages]
                avg_usage = sum(usages) / len(usages) if usages else 0
                return {
                    'cores': usages,
                    'average': round(avg_usage, 2)
                }
            app.logger.warning(f"No NPU usage data found in direct read")
    except Exception as e:
        app.logger.warning(f"Direct read failed (will try sudo): {str(e)}")
    
    # If direct read failed, try with sudo
    try:
        result = subprocess.run(
            ["sudo", "cat", npu_file],
            check=True, 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        
        content = result.stdout.strip()
        app.logger.info(f"Successfully read NPU file with sudo: {content}")
        
        # Extract NPU core usages
        usages = re.findall(r'Core\d+:\s*(\d+)%', content)
        if not usages:
            app.logger.error(f"No NPU usage data found in: {content}")
            return None
            
        usages = [int(usage) for usage in usages]
        avg_usage = sum(usages) / len(usages) if usages else 0
        
        return {
            'cores': usages,
            'average': round(avg_usage, 2)
        }
        
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Sudo command failed with return code {e.returncode}")
        app.logger.error(f"stderr: {e.stderr.strip()}")
        app.logger.error(f"stdout: {e.stdout.strip()}")
    except subprocess.TimeoutExpired:
        app.logger.error("Timeout while trying to read NPU usage")
    except Exception as e:
        app.logger.error(f"Unexpected error in get_npu_usage: {str(e)}", exc_info=True)
    
    return None

def get_ram_usage():
    """Get current RAM usage percentage"""
    try:
        result = subprocess.run(
            "free -m | awk 'NR==2{printf \"%.2f\", $3*100/$2}'",
            shell=True, check=True, capture_output=True, text=True
        )
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError) as e:
        app.logger.error(f"Error getting RAM usage: {str(e)}")
        return None

@app.route('/luna', methods=['GET'])
def luna_recognition():
    """Device recognition endpoint"""
    return jsonify({"device": "luna"})

@app.route('/version', methods=['GET'])
def get_version():
    try:
        with open('../VERSION', 'r') as f:
            version = f.read().strip()
        return jsonify({"version": version}), 200
    except Exception as e:
        app.logger.error(f"Error getting version: {str(e)}")
        return jsonify({"version": "unknown"}), 200

@app.route('/cpu', methods=['GET'])
def cpu_usage():
    """Get current CPU usage"""
    usage = get_cpu_usage()
    if usage is not None:
        return jsonify({"cpu_usage_percent": usage})
    return jsonify({"error": "Could not retrieve CPU usage"}), 500

@app.route('/npu', methods=['GET'])
def npu_usage():
    """Get current NPU usage"""
    try:
        npu_data = get_npu_usage()
        if npu_data is not None:
            return jsonify({
                "npu_cores_usage_percent": npu_data['cores'],
                "npu_average_usage_percent": npu_data['average']
            })
        return jsonify({
            "error": "Could not retrieve NPU usage",
            "details": "Check if the NPU is properly installed and accessible. The server logs contain more details.",
            "troubleshooting": [
                "Run 'ls -l /sys/kernel/debug/rknpu/load' to check file permissions",
                "Try running 'sudo cat /sys/kernel/debug/rknpu/load' manually"
            ]
        }), 500
    except Exception as e:
        app.logger.error(f"Error in npu_usage endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal server error while processing NPU request",
            "details": str(e)
        }), 500

@app.route('/ram', methods=['GET'])
def ram_usage():
    """Get current RAM usage"""
    usage = get_ram_usage()
    if usage is not None:
        return jsonify({"ram_usage_percent": usage})
    return jsonify({"error": "Could not retrieve RAM usage"}), 500

if __name__ == "__main__":
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=False)