# Monitor Status

## CPU
```
top -b -n 1 | grep "%Cpu(s)" | awk '{print 100 - $8"%"}'
6.1%
```

## NPU
```
sudo cat /sys/kernel/debug/rknpu/load
NPU load:  Core0:  0%, Core1:  0%, Core2:  0%,
```
```
sudo cat /sys/kernel/debug/rknpu/load | awk '{print "Average NPU: " ($4+$6+$8)/3 "%"}'
Average NPU: 0%
```

## Memory
```
 free -m
               total        used        free      shared  buff/cache   available
Mem:           15954        2906       10400         738        2646       12150
Swap:           1023           0        1023
```
```
free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }'
18%
```

## API Endpoints

The status server provides the following endpoints to monitor system resources programmatically:

### CPU Usage
```bash
# Get current CPU usage percentage
curl http://localhost:1309/cpu
# Example response: {"cpu_usage_percent": 6.1}
```

### NPU Usage
```bash
# Get current NPU core usages and average
curl http://localhost:1309/npu
# Example response: 
# {
#   "npu_cores_usage_percent": [0, 0, 0],
#   "npu_average_usage_percent": 0.0
# }
# 
# The response includes:
# - npu_cores_usage_percent: array of usage percentages for Core0, Core1, and Core2
# - npu_average_usage_percent: average usage across all NPU cores
```

### RAM Usage
```bash
# Get current RAM usage percentage
curl http://localhost:1309/ram
# Example response: {"ram_usage_percent": 18.21}
```

### Notes
- Replace `<server-ip>` and `<port>` with your server's IP address and port (default port is usually 5000 if not configured otherwise)
- All endpoints return JSON responses
- In case of errors, the response will include an "error" field with a descriptive message