#!/bin/bash

# UFC Fighter Analysis API - Setup Script
# This script sets up the entire API architecture

set -e  # Exit on any error

echo "🥊 UFC Fighter Analysis API - Setup Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Java
if ! command -v java &> /dev/null; then
    echo -e "${RED}❌ Java is not installed. Please install Java 11 or higher.${NC}"
    exit 1
fi
JAVA_VERSION=$(java -version 2>&1 | head -n 1)
echo -e "${GREEN}✅ Java found: $JAVA_VERSION${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.9 or higher.${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✅ Python found: $PYTHON_VERSION${NC}"

echo ""
echo "🐍 Setting up Python environment..."
echo "-----------------------------------"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install Python dependencies
echo "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
else
    echo -e "${RED}❌ requirements.txt not found!${NC}"
    exit 1
fi

echo ""
echo "☕ Setting up Java project..."
echo "----------------------------"

# Navigate to ufcAPI directory
cd ufcAPI

# Make gradlew executable
chmod +x gradlew

# Build Java project
echo "Building Java project (this may take a few minutes on first run)..."
./gradlew build --quiet
echo -e "${GREEN}✅ Java project built successfully${NC}"

# Check for model files
echo ""
echo "🤖 Verifying model files..."
if [ -f "fighterClassifier.joblib" ] && [ -f "outcomePredictor.joblib" ]; then
    echo -e "${GREEN}✅ Model files found${NC}"
else
    echo -e "${YELLOW}⚠️  Warning: Model files not found in ufcAPI directory${NC}"
    echo "   Make sure fighterClassifier.joblib and outcomePredictor.joblib are present"
fi

cd ..

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "📝 Next steps:"
echo "=============="
echo ""
echo "1. Start the Python API (Inner API) - MUST START FIRST:"
echo "   source venv/bin/activate"
echo "   cd ufcAPI"
echo "   python modelAccessor.py"
echo ""
echo "2. In a new terminal, start the Java API (Outer API):"
echo "   cd ufcAPI"
echo "   ./gradlew run"
echo ""
echo "3. Test the APIs:"
echo "   curl http://localhost:8080/"
echo "   curl \"http://localhost:8080/classify?fighterName=Test&SLpM=3.5&Str_Acc=50.0&SApM=2.5&TD_Acc=60.0&TD_Def=70.0\""
echo ""
echo "For more information, see README.md"

