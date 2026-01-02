#!/bin/bash

# UFC Fighter Analysis API - Stop Script
# This script stops both the Python FastAPI and Java Spark API

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🛑 Stopping UFC Fighter Analysis API Services"
echo "============================================="
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Function to kill process by PID file
kill_by_pid_file() {
    local pid_file=$1
    local service_name=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 $pid 2>/dev/null; then
            echo -e "Stopping ${service_name} (PID: $pid)..."
            kill $pid 2>/dev/null || true
            sleep 1
            # Force kill if still running
            if kill -0 $pid 2>/dev/null; then
                kill -9 $pid 2>/dev/null || true
            fi
            echo -e "${GREEN}✅ ${service_name} stopped${NC}"
            rm -f "$pid_file"
        else
            echo -e "${YELLOW}⚠️  ${service_name} was not running${NC}"
            rm -f "$pid_file"
        fi
    else
        echo -e "${YELLOW}⚠️  PID file not found for ${service_name}${NC}"
    fi
}

# Kill by PID files
kill_by_pid_file ".python_api.pid" "Python FastAPI"
kill_by_pid_file ".java_api.pid" "Java Spark API"

# Also try to kill by port (in case PID files are missing)
echo ""
echo "Checking for processes on ports 8000 and 8080..."

# Kill processes on port 8000
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "Stopping process on port 8000..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    echo -e "${GREEN}✅ Port 8000 cleared${NC}"
else
    echo -e "${YELLOW}⚠️  No process found on port 8000${NC}"
fi

# Kill processes on port 8080
if lsof -ti:8080 > /dev/null 2>&1; then
    echo "Stopping process on port 8080..."
    lsof -ti:8080 | xargs kill -9 2>/dev/null || true
    echo -e "${GREEN}✅ Port 8080 cleared${NC}"
else
    echo -e "${YELLOW}⚠️  No process found on port 8080${NC}"
fi

echo ""
echo -e "${GREEN}✅ All services stopped${NC}"

