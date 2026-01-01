# 🥊 UFC Fighter Analysis API

> **Machine Learning-Powered API for UFC Fighter Classification and Fight Outcome Prediction**

A full-stack REST API system that leverages machine learning models to classify UFC fighters' fighting styles and predict fight outcomes. Built with Java (Spark) and Python (FastAPI), featuring a microservices architecture with an outer Java API that orchestrates requests to an inner Python ML service.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Machine Learning Models](#machine-learning-models)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This project provides a production-ready API system for analyzing UFC fighters and predicting fight outcomes using machine learning. The system consists of two interconnected services:

- **Outer API (Java/Spark)**: Public-facing REST API that handles client requests
- **Inner API (Python/FastAPI)**: ML service that processes predictions using trained models

The system uses two trained ML models:
- **Fighter Classifier**: Random Forest model that classifies fighters as "striker" or "grappler"
- **Outcome Predictor**: CatBoost model that predicts fight winners based on statistical differences

---

## ✨ Features

- 🎯 **Fighter Style Classification**: Classify fighters as strikers or grapplers based on performance metrics
- 📊 **Fight Outcome Prediction**: Predict fight winners using advanced statistical analysis
- 🔄 **Microservices Architecture**: Scalable design with separate Java and Python services
- 🚀 **RESTful API**: Clean, well-documented REST endpoints
- 📈 **High Accuracy Models**: Trained on real UFC fight data
- 🔧 **Production Ready**: Includes error handling, proper HTTP status codes, and JSON responses

---

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       │ HTTP Requests
       ▼
┌─────────────────────────────────┐
│   Java API (Spark)              │
│   Port: 8080                    │
│   - /classify                   │
│   - /predict                    │
└──────┬──────────────────────────┘
       │
       │ Internal HTTP Calls
       ▼
┌─────────────────────────────────┐
│   Python API (FastAPI)          │
│   Port: 8000                    │
│   - /classifyFighter            │
│   - /predictOutcome             │
│   - /fighterStylePercentage     │
└──────┬──────────────────────────┘
       │
       │ Model Inference
       ▼
┌─────────────────────────────────┐
│   ML Models                     │
│   - fighterClassifier.joblib    │
│   - outcomePredictor.joblib     │
└─────────────────────────────────┘
```

---

## 💻 Technologies Used

### Backend
- **Java 11**: Core language for outer API
- **Spark Java Framework**: Lightweight web framework for REST API
- **Gradle**: Build automation and dependency management
- **Gson**: JSON serialization/deserialization

### Machine Learning & Data Science
- **Python 3.9+**: ML service runtime
- **FastAPI**: Modern Python web framework for ML API
- **Pandas**: Data manipulation and preprocessing
- **Scikit-learn**: Random Forest classifier
- **CatBoost**: Gradient boosting for outcome prediction
- **Joblib**: Model serialization and loading

### Development Tools
- **Uvicorn**: ASGI server for FastAPI
- **Virtual Environment**: Python dependency isolation

---

## 📁 Project Structure

```
UFC-Fighter-Analysis-API/
│
├── ufcAPI/                          # Main API directory
│   ├── src/main/java/ufcAPI/        # Java source code
│   │   ├── Api.java                 # Main Java API (outer layer)
│   │   └── DetailPackage.java       # Data transfer object
│   ├── modelAccessor.py             # Python FastAPI (inner layer)
│   ├── fighterClassifier.joblib     # Trained fighter classification model
│   ├── outcomePredictor.joblib      # Trained outcome prediction model
│   ├── build.gradle                 # Gradle configuration
│   └── gradlew                      # Gradle wrapper
│
├── AdvancedStats/                   # Model training code (development)
│   ├── OutcomeClassifier.py         # Outcome model training script
│   └── dataCleaner.py               # Data preprocessing
│
├── fighterClassifier/               # Model training code (development)
│   └── fighterClassification.py     # Fighter classifier training script
│
├── venv/                            # Python virtual environment
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## 🔧 Prerequisites

Before setting up the project, ensure you have the following installed:

- **Java 11 or higher** ([Download](https://www.oracle.com/java/technologies/downloads/))
- **Python 3.9 or higher** ([Download](https://www.python.org/downloads/))
- **Git** (for cloning the repository)

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd UFC-Fighter-Analysis-API
```

### Step 2: Python Environment Setup

```bash
# Navigate to project root
cd /path/to/UFC-Fighter-Analysis-API

# Activate the virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Verify model files exist
ls ufcAPI/*.joblib
# Should show: fighterClassifier.joblib and outcomePredictor.joblib
```

### Step 3: Build Java Project

```bash
# Navigate to ufcAPI directory
cd ufcAPI

# Build the project (downloads dependencies and compiles)
./gradlew build

# This will:
# - Download Spark, Gson, and other Java dependencies
# - Compile Java source files
# - Create JAR file in build/libs/
```

### Step 4: Start the Services

**⚠️ Important: Start services in this order!**

#### Start Python FastAPI (Inner API) - **MUST START FIRST**

```bash
# Make sure venv is activated
source venv/bin/activate

# Navigate to ufcAPI directory
cd ufcAPI

# Start the FastAPI server
python modelAccessor.py

# OR using uvicorn directly:
uvicorn modelAccessor:app --host 127.0.0.1 --port 8000 --reload
```

**Verify it's running:** Visit `http://127.0.0.1:8000/` in your browser

#### Start Java Spark API (Outer API) - **START SECOND**

```bash
# In a new terminal, navigate to ufcAPI directory
cd ufcAPI

# Run the Java application
./gradlew run

# OR run the JAR directly:
java -jar build/libs/ufcAPI.jar
```

**Verify it's running:** Visit `http://localhost:8080/` in your browser

---

## 📖 Usage

### Testing the APIs

#### Test Python API (Inner)

```bash
# Test root endpoint
curl http://127.0.0.1:8000/

# Test fighter classification
curl "http://127.0.0.1:8000/classifyFighter?fighterName=John%20Doe&SLpM=3.5&Str_Acc=50.0&SApM=2.5&TD_Acc=60.0&TD_Def=70.0"
```

#### Test Java API (Outer)

```bash
# Test fighter classification endpoint
curl "http://localhost:8080/classify?fighterName=John%20Doe&SLpM=3.5&Str_Acc=50.0&SApM=2.5&TD_Acc=60.0&TD_Def=70.0"

# Test outcome prediction (POST request)
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "fighter1Name": "Fighter A",
    "fighter2Name": "Fighter B",
    "ref": "Mark Smith",
    "features": [1,25,8,30,2,40,0,10,5,3,15,6,4,55,20,10,60,5,8]
  }'
```

---

## 🔌 API Endpoints

### Java API (Outer - Port 8080)

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/classify` | Classify fighter style | `fighterName`, `SLpM`, `Str_Acc`, `SApM`, `TD_Acc`, `TD_Def` |
| `POST` | `/predict` | Predict fight outcome | JSON body with `DetailPackage` |

### Python API (Inner - Port 8000)

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/` | API status | None |
| `GET` | `/classifyFighter` | Classify fighter style | `fighterName`, `SLpM`, `Str_Acc`, `SApM`, `TD_Acc`, `TD_Def` |
| `GET` | `/fighterStylePercentage` | Get style percentage score | `fighterName`, `SLpM`, `Str_Acc`, `SApM`, `TD_Acc`, `TD_Def` |
| `POST` | `/predictOutcome` | Predict fight outcome | JSON body with `OutcomeRequest` |

---

## 🤖 Machine Learning Models

### Fighter Classifier
- **Algorithm**: Random Forest
- **Purpose**: Classifies fighters as "striker" or "grappler"
- **Features**: SLpM, Str_Acc, SApM, TD_Acc, TD_Def
- **Model File**: `ufcAPI/fighterClassifier.joblib`

### Outcome Predictor
- **Algorithm**: CatBoost Classifier
- **Purpose**: Predicts fight winners based on statistical differences
- **Features**: 19 statistical difference features + referee
- **Model File**: `ufcAPI/outcomePredictor.joblib`

---

## 🐛 Troubleshooting

### Common Issues

**"Gson not found" or "Spark not found" error**
```bash
# Rebuild the Gradle project
cd ufcAPI
./gradlew clean build
```

**"Module not found" in Python**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Port already in use**
```bash
# Find and kill processes on ports 8000 or 8080
# macOS/Linux:
lsof -ti:8000 | xargs kill -9
lsof -ti:8080 | xargs kill -9
```

**Model files not found**
- Ensure `fighterClassifier.joblib` and `outcomePredictor.joblib` are in the `ufcAPI/` directory
- These files should be in the same directory as `modelAccessor.py`

**Java API can't connect to Python API**
- Verify Python API is running on port 8000
- Check that Python API responds to: `curl http://127.0.0.1:8000/`
- Ensure firewall isn't blocking localhost connections

---

## 📝 Notes

- The `AdvancedStats/` and `fighterClassifier/` directories contain training code and are not required for API operation
- Model files (`.joblib`) must be present in `ufcAPI/` directory for the API to function
- Always start the Python API before the Java API
- The virtual environment should be activated when running the Python API

---

## 📄 License

This project is for educational and portfolio purposes.

---

## 👤 Author

**Vedant Bangoria**

*Built with ❤️ using Java, Python, and Machine Learning*
