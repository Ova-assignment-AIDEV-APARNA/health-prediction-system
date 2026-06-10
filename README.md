# AI-Powered Health Prediction System

## Project Overview

The AI-Powered Health Prediction System is a web-based healthcare application developed using Flask, SQLite, Bootstrap, and Google Gemini AI.

The application allows healthcare staff to manage patient blood test records and automatically generate AI-powered health risk summaries based on blood test parameters such as Glucose, Haemoglobin, and Cholesterol.

This project was developed as part of an AI/ML Developer technical assessment to demonstrate skills in Python development, CRUD operations, database management, API integration, data validation, and AI-powered healthcare solutions.


## Features

### Patient Management (CRUD)

* Add Patient Records
* View Patient Records
* Update Patient Information
* Delete Patient Records

### Data Validation

* Email Format Validation
* Date of Birth Validation
* Numeric Validation for Blood Test Values

### AI-Powered Health Analysis

* Integration with Google Gemini AI API
* Generates health risk summaries from patient blood test results
* Fallback prediction logic when AI service is unavailable

### Dashboard Features

* Total Patient Count
* Average Glucose Calculation
* Patient Search Functionality

### Reporting

* Export Patient Records to CSV


## Technologies Used

### Backend

* Python
* Flask

### Database

* SQLite

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* Jinja2 Templates

### AI Integration

* Google Gemini AI API

### Version Control

* Git
* GitHub

---

## Project Structure

health_prediction_app/

├── app.py

├── requirements.txt

├── README.md

├── services/

│   └── ai_services.py

├── templates/

│   ├── base.html

│   ├── dashboard.html

│   ├── add_patient.html

│   └── edit_patient.html

└── .gitignore

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Ova-assignment-AIDEV-APARNA/health-prediction-system.git
cd health-prediction-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a file named `.env`

```env
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

### Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## AI Prediction Workflow

1. User enters patient details and blood test values.
2. Input validation is performed.
3. Data is stored in SQLite database.
4. Blood test values are sent to Google Gemini AI.
5. AI generates a health risk summary.
6. Summary is stored in the Remarks field.
7. Results are displayed on the dashboard.

---

## Future Improvements

* User Authentication
* PDF Report Generation
* Health Analytics Dashboard
* Chart-Based Data Visualization
* Machine Learning Prediction Models
* Cloud Deployment

---


