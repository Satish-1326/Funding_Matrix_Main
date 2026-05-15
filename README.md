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

## ⚙️ Local Installation

### 1️⃣ Clone the Repository
```bash
git clone [https://github.com/your-username/startup-funding-matrix.git](https://github.com/your-username/startup-funding-matrix.git)
cd startup-funding-matrix
View Deployments
kubectl get deployments
View Logs
kubectl logs <pod-name>
Restart Deployment
kubectl rollout restart deployment startup-funding-deployment

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

