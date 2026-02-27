# 🌾 Expert System for Precision Farming
**An AI-Driven Agricultural Decision Support System**

## 📖 Table of Contents
* [Project Overview](#-project-overview)
* [The Intelligence Engine](#-the-intelligence-engine)
* [Key Features](#-key-features)
* [Technical Stack](#-technical-stack)
* [Database Schema](#-database-schema)
* [Data Preview] (#%EF%B8%8F-data-preview)
* [Installation & Setup](#-installation--setup)
* [Usage Guide](#-usage-guide)

---

## 📌 Project Overview
The Precision Farming Expert System is a specialized AI application designed to help farmers maximize yield and minimize resource waste. By analyzing soil data and weather conditions, the system provides "expert-level" advice on crop selection, irrigation scheduling, and pest management.

---

## 🧠 The Intelligence Engine
This project utilizes a hybrid AI architecture:
1. **Machine Learning (Decision Trees):** Uses `scikit-learn` to predict the best crop to plant based on historical soil and weather patterns.
2. **Knowledge-Based Rules:** An inference engine that applies expert agricultural rules to determine:
    * **Irrigation:** Based on soil moisture and precipitation levels.
    * **Fertilization:** Based on nutrient levels and current growth stages.
    * **Pest Management:** Diagnoses specific diseases (like Rust or Rice Blast) based on observed symptoms.

---

## 🚀 Key Features
* **Crop Recommendation:** Predictive modeling to suggest the most suitable crop (Wheat, Rice, Maize, etc.).
* **Smart Irrigation:** Real-time scheduling that accounts for upcoming precipitation to save water.
* **Fertilizer Optimizer:** Provides tailored nutrient advice based on the crop's vegetative or reproductive stage.
* **Automated Pest Diagnosis:** A rule-based lookup for quick identification of crop diseases and chemical recommendations.
* **Web-Based Interface:** A user-friendly **Flask** dashboard for data entry and result visualization.
* **Persistent Storage:** Integrated with **MySQL** to store and retrieve historical farming data.

---

## 🏗️ Technical Stack
* **Backend:** Python 3.x, Flask
* **Machine Learning:** Scikit-learn (Decision Tree Classifier), Pandas, Joblib
* **Database:** MySQL, SQLAlchemy (ORM)
* **Frontend:** HTML/CSS (via Flask Templates)
* **Modeling:** Label Encoding for categorical environmental data.

---

## 🗄️ Database Schema
The system connects to a `precision_farming` database with a structured `crop_data` table containing:
* `soil_type`, `moisture`, `nutrients`
* `temperature`, `humidity`, `precipitation`
* `label` (The target crop)

---

## 🖼️ Data Preview



### 1. Recommendation Dashboard
*The Flask interface where farmers input environmental variables to receive AI insights.*
![Dashboard Preview](INSERT_IMAGE_NAME_1.png)

### 2. Decision Tree Logic
*A visualization of how the Machine Learning model branches to reach a crop conclusion.*
![Model Logic](INSERT_IMAGE_NAME_2.png)

---

## 🛠️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/eshek2020/precision-farming-expert-system.git](https://github.com/eshek2020/precision-farming-expert-system.git)
   cd precision-farming-expert-system
