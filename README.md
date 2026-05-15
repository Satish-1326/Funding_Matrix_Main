# 🚀 Startup Funding Matrix (Dockerized + Kubernetes Enabled Advanced Analytics Dashboard)

An advanced **Streamlit-based data analytics dashboard** designed to explore, analyze, and predict startup funding trends.

This project integrates:

* 📊 Data Visualization
* 🤖 Machine Learning
* 🗺️ Geospatial Intelligence
* 🔐 Secure Authentication
* 🐳 Dockerized Deploymentz
* ☸️ Kubernetes Orchestration

---

## 📌 Project Overview

The **Startup Funding Matrix** provides deep insights into startup ecosystems by analyzing funding data across sectors, cities, investors, and funding patterns.

The project is fully containerized using Docker and orchestrated using Kubernetes, making it scalable and production-ready.

👉 No need to manually install Python, MySQL, or dependencies  
👉 Runs using Docker containers  
👉 Easily scalable using Kubernetes

---

# ✨ Features

---

## 📊 Data Analysis

* Funding trends over time
* Sector-wise investment breakdown
* Investor portfolio analysis
* Startup-level deep insights
* Interactive filtering and exploration

---

## 🤖 Machine Learning

### 📈 Linear Regression

Used for:
* Funding prediction
* Growth forecasting

### 🧠 K-Nearest Neighbors (KNN)

Used for:
* Similar startup recommendation
* Competitive startup mapping

Recommendations are based on:

* Funding amount
* Sector
* City
* Year

---

## 🗺️ Geospatial Intelligence

* 3D interactive funding maps using PyDeck
* City-wise funding density visualization
* Investment hotspot analysis

---

## 💡 Business Recommendation Engine

Suggests business sectors based on:

* Budget
* Competition level
* Market demand
* Growth trends

---

## 🔐 Authentication System

Implemented using:

* Login & Signup pages
* MySQL Database
* bcrypt password hashing
* Session-based authentication
* Secure credential validation

---

# 🐳 Dockerized Architecture

This project uses Docker Compose to run:

* 🟢 Streamlit App Container
* 🟢 MySQL Database Container

Benefits:

* No manual dependency installation
* Easy deployment
* Environment consistency
* Fully isolated setup

---

# ☸️ Kubernetes Integration

Kubernetes is used for:

* Container orchestration
* Replica management
* Auto scaling
* Load balancing
* Self-healing deployments

Kubernetes Components Used:

* Deployment
* Service
* Pods
* ReplicaSets

---

# 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| Database | MySQL |
| Machine Learning | scikit-learn |
| Visualization | Plotly, PyDeck |
| Security | bcrypt |
| Containerization | Docker |
| Orchestration | Kubernetes |

---

# 📂 Project Structure

```text
📁 Startup-Funding-Matrix
│
├── project1.py              # Main Streamlit Application
├── project.csv              # Dataset
├── Dockerfile               # Docker Configuration
├── docker-compose.yml       # Multi-container Docker Setup
├── deployment.yaml          # Kubernetes Deployment
├── service.yaml             # Kubernetes Service
├── requirements.txt         # Dependencies
├── .env.example             # Environment Variables
└── README.md                # Documentation

⚙️ Local Installation
1️⃣ Clone Repository
git clone https://github.com/your-username/startup-funding-matrix.git
cd startup-funding-matrix
2️⃣ Create Virtual Environment
Windows
python -m venv .venv
.venv\Scripts\activate
Linux / Mac
python3 -m venv .venv
source .venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
🗄️ MySQL Database Setup

Run the following SQL commands:

CREATE DATABASE auth_db;

USE auth_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARBINARY(255)
);
Configure Database Connection

Update database credentials in your Python file:

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="auth_db"
)
🚀 Run Project Locally
streamlit run project1.py

Open in browser:

http://localhost:8501
🐳 Docker Setup
Build Docker Image
docker build -t startup-funding-app .
Run Docker Container
docker run -p 8501:8501 startup-funding-app
View Running Containers
docker ps
Stop Docker Container
docker stop <container_id>

Example:

docker stop a1b2c3d4
Start Container Again
docker start <container_id>
Remove Docker Container
docker rm <container_id>
View Docker Images
docker images
🐳 Docker Compose Setup
Start Application
docker compose up --build
Stop Application
docker compose down
☸️ Kubernetes Setup
Enable Kubernetes

Open Docker Desktop:

Settings
Kubernetes
Enable Kubernetes
Apply & Restart
Verify Kubernetes
kubectl get nodes
Deploy Application
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
Check Running Pods
kubectl get pods
Check Services
kubectl get services
Access Application
kubectl port-forward service/startup-funding-service 8501:80

Open in browser:

http://localhost:8501
🔄 Kubernetes Scaling
Scale to 5 Replicas
kubectl scale deployment startup-funding-deployment --replicas=5
Stop Application Pods
kubectl scale deployment startup-funding-deployment --replicas=0
Restart Application Pods
kubectl scale deployment startup-funding-deployment --replicas=2
🛑 Stop Kubernetes Deployment
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
📊 Useful Kubernetes Commands
View Pods
kubectl get pods
View Services
kubectl get services
View Deployments
kubectl get deployments
View Logs
kubectl logs <pod-name>
Restart Deployment
kubectl rollout restart deployment startup-funding-deployment
