# 🐍 Portofolio Website

**Nama** : Muhammad Raihananta Adzaky Yuwono \
**NPM** : 2506547853 \
**Kelas** : PBP D 

---

## 📌 Project Overview
A simple dynamic portofolio web app built using Django for my Platform-Based Programming Class. 

---
## ⚙️ Setup  Instructions
**Important Note:** I built this project to be locally run on a university-owned web service so I've chosen to omit some steps that I originally took when first building and opted to use this section for people wanting to build locally. If you have any problems when trying to set up the project please feel free to reach out!

You can follow these steps to run the application locally on your machine. 

### 1. Clone the repository: 
```bash
   git clone https://github.com/Flixidk/myportofolio.git
   cd your-repo-name
```

### 2. Setup & Activate Virtual Environment  
**Windows:** 
```bash
python -m venv env
env\Scripts\activate
```

**Unix (macOS, Linux):**
```bash
python3 -m venv env
source env/bin/Activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and configure local settings:
```
PRODUCTION=False
SECRET_KEY=your-local-secret-key
```

### 5. Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py runserver
```
Open http://localhost:8000 in your browser.

---
## 📦 Tech Stack & Core Dependencies
- Django: Core web framework handling routing, logic, and page generation.
- Gunicorn: WSGI HTTP server for production environment handling.
- WhiteNoise: Static file (CSS/JS) management for production.
- psycopg2-binary: Database driver for PostgreSQL integration.
- python-dotenv: Reads secrets securely from .env.
- requests & urllib3: Facilitates external API communication.

---
## 📚 Weekly Documentation & AI Disclosure
For complete documentation regarding weekly progress and AI Disclosure + Utilization, please refer to this [folder](docs/). (Used for grading)
