# 🚀 Startup Funding Matrix (Dockerized Advanced Analytics Dashboard)

An advanced **Streamlit-based data analytics dashboard** designed to explore, analyze, and predict startup funding trends.

This project integrates:

* 📊 Data Visualization
* 🤖 Machine Learning
* 🗺️ Geospatial Intelligence
* 🔐 Secure Authentication
* 🐳 Dockerized Deployment (App + MySQL)
* ☸️ Kubernetes Orchestration

---

## 📌 Project Overview

*Startup Funding Matrix** provides deep insights into startup ecosystems by analyzing funding data across sectors, cities, investors, and funding patterns.

The project is fully containerized using Docker and orchestrated using Kubernetes, making it scalable and production-ready.

👉 No need to manually install Python, MySQL, or dependencies  
👉 Runs using Docker containers  
👉 Easily scalable using Kubernetes

---

## ✨ Features

### 📊 Data Analysis

* Funding trends over time
* Sector-wise investment breakdown
* Investor portfolio analysis
* Startup-level deep insights

---

### 🤖 Machine Learning

* **Linear Regression** → Funding prediction
* **K-Nearest Neighbors (KNN)** → Similar startup recommendation

---

### 🗺️ Geospatial Intelligence

* 3D interactive maps using PyDeck
* City-wise funding density visualization

---

### 💡 Business Recommendation Engine

Suggests business sectors based on:

* Budget
* Market demand
* Growth trends
* Competition level

---

### 🔐 Authentication System

* Secure Login & Signup
* Password hashing using **bcrypt**
* MySQL database integration
* Session-based authentication
* Auto database table creation

---

## 🐳 Dockerized Architecture

This project uses **Docker Compose** to run:

* 🟢 **Streamlit App Container**
* 🟢 **MySQL Database Container**

👉 No need for local MySQL installation
👉 Fully isolated environment

---

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

## 📂 Project Structure

```
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
```

---

## ⚙️ Run Using Docker (Recommended)

### ✅ Prerequisites

* Install Docker Desktop

---

### 🚀 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/startup-funding-matrix.git
cd startup-funding-matrix
```

---

### 2️⃣ Create Virtual Environment
Windows
```
python -m venv .venv
.venv\Scripts\activate
```

Linux/Mac
```
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---


## 🔐 Environment Variables

Create a `.env` file:

```env
DB_HOST=db
DB_USER=root
DB_PASSWORD=your_db_pass
DB_NAME=auth_db
```

⚠️ Do NOT share your real `.env` file publicly

---

## 🗄️ Database Setup

No manual setup required ✅ OR

---

```bash
CREATE DATABASE auth_db;

USE auth_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARBINARY(255)
);
```
---

## Configure Database Connection

```bash
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="auth_db"
)
```

---

### 🐳 Docker Setup
Build Docker Image

---
```bash
docker build -t startup-funding-app .
```
---

## 🔐 Authentication Flow

1. User opens app
2. Login / Signup page appears
3. User registers → data stored in MySQL (Docker)
4. Password securely hashed using bcrypt
5. Login validates credentials
6. Dashboard access granted
7. Logout ends session

---

## 📊 Key Visualizations

* 📈 Funding Trends
* 🏭 Sector Distribution
* 🫧 Startup Comparison (Bubble Chart)
* 🗺️ 3D Funding Map
* 📊 Investor Portfolio

---

## 🤖 Machine Learning Details

### Linear Regression

* Predicts funding trends

### KNN (K-Nearest Neighbors)

* Recommends similar startups based on:

  * Funding
  * Year
  * Sector
  * City

---

## 🎯 Use Cases

* Startup ecosystem analysis
* Investment insights
* Business idea recommendation
* Market trend prediction

---

## ⚠️ Limitations

* Uses static dataset
* Authentication is basic (no OAuth yet)
* No real-time data integration

---

## 🚀 Future Improvements

* 🌐 Cloud deployment (AWS / Render / Azure)
* 🔑 Google / GitHub OAuth login
* 📧 Email OTP verification
* 📊 Real-time data pipelines
* 🤖 Advanced ML models

---

## 👨‍💻 Author

**Satish Dadas**
📍 India

---

## 📜 License

MIT License

Copyright (c) 2026 Satish Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

---

## 💡 Important Note

This project uses Docker for database and backend services.
👉 Users do NOT need to install MySQL manually
👉 Just run Docker and everything works

---

## ⭐ If You Like This Project

Give it a ⭐ on GitHub and share it 🚀
