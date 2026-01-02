#!/bin/bash

# UFC Fighter Analysis API - Startup Script
# This script starts both the Python FastAPI and Java Spark API

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "🥊 UFC Fighter Analysis API - Startup Script"
echo "============================================="
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo "Please run ./setup.sh first to set up the project."
    exit 1
fi

# Check if model files exist
if [ ! -f "ufcAPI/fighterClassifier.joblib" ] || [ ! -f "ufcAPI/outcomePredictor.joblib" ]; then
    echo -e "${YELLOW}⚠️  Warning: Model files not found in ufcAPI directory${NC}"
    echo "The APIs may not work correctly without the model files."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Check if ports are already in use
if check_port 8000; then
    echo -e "${YELLOW}⚠️  Port 8000 is already in use (Python API may already be running)${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

if check_port 8080; then
    echo -e "${YELLOW}⚠️  Port 8080 is already in use (Java API may already be running)${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${BLUE}🐍 Activating Python virtual environment...${NC}"
source venv/bin/activate

# Start Python FastAPI in background
echo -e "${BLUE}🚀 Starting Python FastAPI (Inner API) on port 8000...${NC}"
cd ufcAPI
python modelAccessor.py > ../python_api.log 2>&1 &
PYTHON_PID=$!
cd ..

# Wait for Python API to start
echo -e "${YELLOW}⏳ Waiting for Python API to initialize (5 seconds)...${NC}"
sleep 5

# Check if Python API is running
if ! kill -0 $PYTHON_PID 2>/dev/null; then
    echo -e "${RED}❌ Python API failed to start. Check python_api.log for errors.${NC}"
    exit 1
fi

# Test if Python API is responding
if curl -s http://127.0.0.1:8000/ > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Python API is running (PID: $PYTHON_PID)${NC}"
else
    echo -e "${YELLOW}⚠️  Python API started but not responding yet. Continuing anyway...${NC}"
fi

# Start Java Spark API
echo -e "${BLUE}☕ Starting Java Spark API (Outer API) on port 8080...${NC}"
cd ufcAPI
./gradlew run > ../java_api.log 2>&1 &
JAVA_PID=$!
cd ..

# Wait a moment for Java API to start
sleep 3

# Check if Java API is running
if ! kill -0 $JAVA_PID 2>/dev/null; then
    echo -e "${RED}❌ Java API failed to start. Check java_api.log for errors.${NC}"
    # Kill Python API if Java failed
    kill $PYTHON_PID 2>/dev/null || true
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Both APIs are starting!${NC}"
echo ""
echo "📊 Service Status:"
echo "=================="
echo -e "Python FastAPI (Inner): ${GREEN}Running${NC} (PID: $PYTHON_PID, Port: 8000)"
echo -e "Java Spark API (Outer): ${GREEN}Running${NC} (PID: $JAVA_PID, Port: 8080)"
echo ""
echo "📝 Log Files:"
echo "  - Python API: python_api.log"
echo "  - Java API: java_api.log"
echo ""
echo "🌐 Test the APIs:"
echo "  - Python API: curl http://127.0.0.1:8000/"
echo "  - Java API: curl http://localhost:8080/"
echo ""
echo "🛑 To stop the APIs, run:"
echo "  ./stop.sh"
echo "  OR"
echo "  kill $PYTHON_PID $JAVA_PID"
echo ""
echo -e "${YELLOW}⚠️  Note: APIs are running in the background.${NC}"
echo "   This terminal can be closed, but the APIs will continue running."
echo "   Use ./stop.sh to stop them, or find and kill the processes manually."
echo ""

# Save PIDs to a file for easy stopping
echo "$PYTHON_PID" > .python_api.pid
echo "$JAVA_PID" > .java_api.pid

# Keep script running to show logs (optional - user can Ctrl+C to exit)
echo "Press Ctrl+C to stop viewing logs (APIs will continue running)"
echo "To stop the APIs, run ./stop.sh in another terminal"
echo ""
echo "--- Logs (last 20 lines) ---"
tail -f python_api.log java_api.log 2>/dev/null || true

