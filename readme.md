🚗 Smart Vehicle Parking Management System

An AI-powered, full-stack parking management system designed to optimize urban parking infrastructure. This project features dynamic pricing calculated via machine learning, real-time spatial pathfinding on a 2D interactive canvas, and a highly scalable containerized backend.

## ✨ Key Features

* **Real-Time Spatial Routing:** An HTML5 Canvas-based frontend that maps physical parking slots and draws simulated shortest-path routing lines from the entrance to the dynamically assigned spot.
* **AI Dynamic Pricing Engine:** A Scikit-Learn Linear Regression model that calculates variable exit fees based on parking duration, time of day (entry hour), and lot occupancy rates.
* **Modern API Architecture:** A fully decoupled, high-performance REST API built with FastAPI and Pydantic for strict data validation.
* **Containerized Database:** MySQL 8.0 database deployed via Docker Compose, ensuring instant environment replication and seamless local development.
* **Live Status Dashboard:** A Tailwind CSS web interface providing real-time visual tracking of occupied vs. available slots.

## 🛠️ Tech Stack

* **Backend:** Python 3.11+, FastAPI, Uvicorn
* **Machine Learning:** Scikit-Learn, NumPy, Pickle
* **Database:** MySQL 8.0, Docker, SQLTools
* **Frontend:** Vanilla JavaScript, HTML5 Canvas, Tailwind CSS

## 📂 Project Structure

```text
📦 VehicleDBMS
├── 📁 app/                     # Core backend logic & API routing
│   ├── api.py                  # FastAPI endpoints and route handlers
│   ├── database.py             # MySQL connection pooling
│   ├── parking.py              # Core parking allocation logic
│   └── receipts.py             # Fee calculation and receipt generation
├── 📁 frontend/                # Web interface assets
│   └── index.html              # Dashboard with HTML5 Canvas map
├── 📁 ml/                      # Machine learning models & scripts
│   ├── pricing_model.py        # Model training script
│   └── pricing_model.pkl       # Serialized Linear Regression model
├── 📁 scripts/                 # Setup and legacy CLI scripts
│   ├── app.py                  # Terminal-based CLI interface
│   └── setup_db.py             # Database schema initialization script
├── 📄 docker-compose.yml       # Docker configuration for MySQL
├── 📄 requirements.txt         # Python dependencies
└── 📄 README.md                # Project documentation

🚀 Installation & SetupPrerequisitesPython 3.11+Docker Desktop (Running)GitStep-by-Step Guide1. Clone the repositoryBashgit clone <YOUR_GITHUB_REPO_URL>

cd VehicleDBMS
2. Start the Dockerized DatabaseSpin up the MySQL container on port 3307.Bashdocker compose up -d
3. Set up the Python Virtual EnvironmentBashpython -m venv venv

# On Windows:

venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

4. Install DependenciesBashpip install -r requirements.txt

5. Initialize the Database SchemaCreate the tables (parking_slots, vehicles, receipts) and seed the initial 10 parking slots.Bashpython scripts/setup_db.py

6. Train the AI Pricing ModelGenerate the serialized .pkl file required by the API to calculate dynamic exit fees.Bashpython ml/pricing_model.py

7. Start the FastAPI ServerLaunch the Uvicorn server with live-reloading enabled.Bashuvicorn app.api:app --reload

8. Access the DashboardOpen your web browser and navigate to: http://127.0.0.1:8000/

📡 A🔮 Future Scope
A (A-Star) Pathfinding:* Upgrade the current L-shape routing simulation to calculate true obstacle-aware shortest paths.
Live Occupancy Telemetry: Replace the static occupancy rate in the ML model with real-time database queries to aggressively scale pricing during peak hours.
Computer Vision Integration: Implement headless OpenCV/EasyOCR to automatically extract license plate strings from camera feeds, removing the need for manual text input
