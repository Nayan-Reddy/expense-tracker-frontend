<div align="center">
  <h1>Data-Driven Expense Analytics Platform 📊</h1>
</div>
<div align="center">

*An end-to-end data analytics platform demonstrating the complete data lifecycle, from data ingestion and backend processing to interactive visualization.*

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue?style=for-the-badge&logo=mysql)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-130654?style=for-the-badge&logo=pandas)

</div>

---

## 📈 Live Demo

<div align="center">
  <strong>Experience the live application in action: <a href="https://expense-tracker-frontend-nayan-reddy.streamlit.app/">➡️ Interact with the Live Demo Here</a></strong>
</div>

<p align="center">
  <img src="[PATH-TO-YOUR-DEMO-GIF]" alt="Expense Tracker Demo GIF" width="800"/>
</p>

---

## 📖 Table of Contents

- [Introduction](#-introduction)
- [The Data Analytics Perspective](#-the-data-analytics-perspective)
- [Core Features](#-core-features)
- [Architecture & Tech Stack](#️-architecture--tech-stack)
- [Setup and Local Installation](#️-setup-and-local-installation)
- [Environment Configuration](#-environment-configuration)
- [Future Improvements](#-future-improvements)
- [Get In Touch](#-get-in-touch)

---

## 🌟 Introduction

The **Expense Analytics Platform** is a full-stack data application designed to showcase the complete data lifecycle. It functions as a personal expense tracker where users can input, manage, and visualize their financial data through an interactive web interface powered by **Streamlit**.

This project demonstrates proficiency in key data analysis competencies, including data modeling, backend processing with **FastAPI**, SQL-based aggregation, and the creation of insightful, interactive dashboards for end-users.

---

## 📊 The Data Analytics Perspective

This project was built to showcase key skills required for a data analyst role. Here’s how it maps to the data lifecycle:

* **1. Data Ingestion & Storage:**
    * **Data Collection:** Users input their daily expenses through a clean, form-based Streamlit interface.
    * **Data Persistence:** The data is sent to the backend API and stored in a cloud-hosted **MySQL** database.
    * **Data Modeling:** The database uses a simple but effective schema to store transactional data with a unique `session_id` for each user, enabling user-level analysis.

* **2. Data Processing & Transformation (ETL):**
    * **Backend API as a Data Service:** A **FastAPI** backend acts as the data processing layer. It exposes endpoints that query the database, perform aggregations using SQL (`GROUP BY`, `SUM()`), and transform the raw data into analysis-ready JSON payloads.

* **3. Data Analysis & Visualization:**
    * The **Streamlit** frontend is dedicated to presenting insights through two powerful analytical views:
        * **Category-wise Contribution Analysis:** This tab performs segmentation analysis, displaying a bar chart and summary table of spending by category. It helps users answer questions like, *"What are my top spending categories?"*
        * **Month-over-Month Trend Analysis:** This tab performs time-series analysis. It uses a `pandas` pivot table and chart to track spending patterns over time, enabling users to spot trends or seasonality in their financial habits.

---

## ✨ Core Features

* **🧠 Decoupled Full-Stack Architecture:** A modern design separating the frontend presentation layer (Streamlit) from the backend data processing layer (FastAPI), allowing for independent development and scaling.
* **👤 User-Level Granularity:** Each user is assigned a unique session ID upon their first data entry. This ensures all their expense data is kept private and isolated from other users and the initial demo data.
* **🚀 Interactive "Demo Mode":** The application launches with a preloaded dataset, allowing any visitor to immediately explore the analytics dashboards without needing to enter their own data first.
* **⚙️ Smart Analytics Fallback:** If a user without data tries to view the analytics tabs, the application automatically falls back to displaying the demo analytics, ensuring the UI is always populated and functional.
* **📱 Responsive UI:** Includes a "Mobile Friendly View" toggle to adapt the data entry form for smaller screens, demonstrating a focus on user experience.
* **📊 Multi-Tab Interface:**
    * **Add/Update:** A form-based interface to add, view, or update daily expenses. Includes a mobile-friendly layout toggle.
    * **Category Analytics:** A bar chart and table showing the breakdown of expenses by category over a selected date range.
    * **Monthly Analytics:** A pivot table and chart displaying month-over-month spending across different categories.
* **📈 Data Persistence:** All data is stored in a cloud-hosted MySQL database, with a clean schema for managing expenses.
---

## 🛠️ Architecture & Tech Stack

The project is organized into three distinct layers, mirroring a typical data application architecture.

| Layer | Technology / Library | Purpose |
| --- | --- | --- |
| **Data Layer** | **MySQL** | Relational database for persistent storage of expense data. |
| | **`expense_db_creation.sql`** | SQL script to define the schema and load initial demo data. |
| | **`db_helper.py`** | A custom module to abstract all SQL queries and database logic. |
| **Backend (API) Layer** | **FastAPI** & **Uvicorn** | High-performance framework for building and serving the REST API. |
| | **Pydantic** | For robust data validation and clear API request models. |
| | **`mysql-connector-python`**| The Python driver for connecting the backend to the MySQL database. |
| **Frontend (Presentation) Layer** | **Streamlit** | For building the interactive, multi-tab user interface and dashboards. |
| | **`pandas`** | For data manipulation, pivoting, and structuring on the frontend. |
| | **`requests`** | To communicate with the backend FastAPI endpoints. |

---

## ⚙️ Setup and Local Installation

To run this project locally, you need to set up the database, backend, and frontend.

### Prerequisites
* Python 3.9+
* A running MySQL server (local or cloud-based).

### Step 1: Database Setup
1.  Connect to your MySQL server.
2.  Create a new database (e.g., `expense_tracker_db`).
3.  Execute the entire `expense_db_creation.sql` script provided in the database folder. This will create the `expenses` table and populate it with the initial demo data.

### Step 2: Backend Setup
1.  Clone the backend repository:
    ```bash
    git clone https://github.com/Nayan-Reddy/expense-tracker-backend
    cd expense-tracker-backend
    ```
2.  Create a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
3.  **Configure Environment Variables/Secrets:**
    - Follow the instructions in the [Environment Configuration](#-environment-configuration) section below as the backend server requires a set of environment variables to connect to the MySQL database.
  
4.  Run the backend server:
    ```bash
    uvicorn server:app --reload
    ```
    The API will be running at `http://127.0.0.1:8000`.

### Step 3: Frontend Setup
1.  In a new terminal, clone the frontend repository:
    ```bash
    git clone https://github.com/Nayan-Reddy/expense-tracker-frontend
    cd expense-tracker-frontend
    ```
2.  Create a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Important:** For local testing, you may need to change the `API_URL` variable in the Python files from the deployed Render URL to `http://127.0.0.1:8000`.
4.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```
    Your application should now be running in your browser!

---

## 🔑 Environment Configuration

The backend server requires a set of environment variables to connect to the MySQL database.

1.  **Create a `.env` file** in the root of the backend project directory.
2.  **Add your database credentials** to this file:
    ```ini
    # .env
    DB_HOST="your_db_host"
    DB_USER="your_db_user"
    DB_PASSWORD="your_db_password"
    DB_NAME="your_db_name"
    DB_PORT="3306"
    ```

---

## 🔮 Future Improvements

* **User Authentication:** Implement a full user login system to allow users to save and access their data across multiple sessions.
* **Budgeting Feature:** Add a feature to set monthly budgets by category and visualize spending against those targets.
* **Advanced Analytics:** Introduce more complex analytics like forecasting future expenses based on historical data.

---

## 📫 Get In Touch

I'm a passionate data enthusiast actively seeking opportunities in data analytics. If you're impressed by this project or have any questions, I'd love to connect!

* **Email:** <nayanreddy007@gmail.com>
