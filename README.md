# 🚀 Startup Funding Matrix (Advanced Analytics Dashboard)

An advanced **Streamlit-based data analytics dashboard** designed to explore, analyze, and predict startup funding trends.
This project integrates **data visualization, machine learning, geospatial analysis, and secure authentication** into a single platform.

---

## 📌 Project Overview

The **Startup Funding Matrix** provides insights into startup ecosystems by analyzing funding data across sectors, cities, and investors.

It includes:

* 📊 Interactive dashboards
* 🤖 Machine Learning (Linear Regression + KNN)
* 🗺️ Geospatial Intelligence (3D Map)
* 🔐 Secure Authentication System (MySQL + bcrypt)

---

## ✨ Features

### 📊 Data Analysis

* Funding trends over time
* Sector-wise investment breakdown
* Investor portfolio analysis
* Startup-level deep insights

### 🤖 Machine Learning

* **Linear Regression** → Funding prediction
* **K-Nearest Neighbors (KNN)** → Similar startup recommendation

### 🗺️ Geospatial Intelligence

* 3D interactive map using PyDeck
* City-wise funding density visualization

### 💡 Business Recommendation Engine

* Suggests sectors based on:

  * Budget
  * Market demand
  * Growth trends
  * Competition level

### 🔐 Authentication System

* Login & Signup pages
* MySQL database integration
* Password hashing using bcrypt
* Session-based access control

---

## 🛠️ Tech Stack

| Category      | Technology     |
| ------------- | -------------- |
| Frontend      | Streamlit      |
| Backend       | Python         |
| Database      | MySQL          |
| ML Libraries  | scikit-learn   |
| Visualization | Plotly, PyDeck |
| Security      | bcrypt         |

---

## 📂 Project Structure

```
📁 Startup-Funding-Matrix
│
├── project1.py          # Main Streamlit App
├── project.csv          # Dataset
├── users.db / MySQL     # Authentication Database
├── requirements.txt     # Dependencies
└── README.md            # Project Documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/startup-funding-matrix.git
cd startup-funding-matrix
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit pandas numpy plotly pydeck scikit-learn mysql-connector-python bcrypt
```

---

### 3️⃣ Setup MySQL Database

Run the following SQL commands:

```sql
CREATE DATABASE auth_db;

USE auth_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARBINARY(255)
);
```

---

### 4️⃣ Configure Database Connection

Update your code:

```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="auth_db"
)
```

---

### 5️⃣ Run the Application

```bash
streamlit run project1.py
```

---

## 🔐 Authentication Flow

1. User opens app
2. Login / Signup page appears
3. User registers → data stored in MySQL
4. Login validates credentials (bcrypt hashing)
5. Access granted to dashboard
6. Logout returns to login page

---

## 📊 Key Visualizations

* 📈 Funding Trends (Line Charts)
* 🏭 Sector Distribution (Bar Charts)
* 🫧 Bubble Chart (Startup Comparison)
* 🗺️ 3D City Funding Map
* 📊 Investor Portfolio Pie Charts

---

## 🤖 Machine Learning Details

### Linear Regression

Used for:

* Predicting future funding trends

### KNN (K-Nearest Neighbors)

Used for:

* Finding similar startups based on:

  * Funding
  * Year
  * Sector
  * City

---

## 🎯 Use Cases

* Startup ecosystem analysis
* Investment decision support
* Business idea recommendation
* Market trend prediction

---

## ⚠️ Limitations

* Uses static dataset (no real-time data)
* Basic authentication (not production-ready)
* Requires local MySQL setup

---

## 🚀 Future Improvements

* 🌐 Cloud deployment (AWS / Azure)
* 🔑 OAuth login (Google, GitHub)
* 📧 Email OTP verification
* 📊 Real-time data integration
* 🤖 Advanced ML models (Random Forest, XGBoost)

---

## 👨‍💻 Author

**Satish Dadas**
📍 India

---

## 📜 License

MIT License

Copyright (c) 2026 Satish

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

---

in this i want to write that every user need to their sql db not giving permission to use my
