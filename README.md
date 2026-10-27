<div align="center">

# 🚗 Smart Vehicle Parking Management System

**An AI-powered, full-stack parking management system with machine-learning dynamic pricing, real-time spatial routing on an HTML5 Canvas, and a containerized FastAPI + MySQL backend.**

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Uvicorn-009688?logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Linear%20Regression-F7931E?logo=scikitlearn&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-06B6D4?logo=tailwindcss&logoColor=white)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Screenshots](#-screenshots)
- [Key Features](#-key-features)
- [Tech Stack](#️-tech-stack)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [How the AI Pricing Works](#-how-the-ai-pricing-works)
- [Database Schema](#️-database-schema)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [Configuration](#️-configuration)
- [Troubleshooting](#-troubleshooting)
- [Future Scope](#-future-scope)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🔎 Overview

The **Smart Vehicle Parking Management System** is designed to optimize urban parking infrastructure. When a vehicle enters, the system assigns a parking slot and draws a simulated route from the lot entrance to that slot on an interactive 2D canvas. When the vehicle exits, a machine-learning model calculates the parking fee based on how long the vehicle stayed, what time it arrived and how full the lot was.

The project is split into three decoupled parts:

- **Backend** – a high-performance REST API built with FastAPI and validated with Pydantic.
- **Machine learning** – a Scikit-Learn Linear Regression model, trained locally and serialized with Pickle, that powers dynamic exit fees.
- **Frontend** – a Tailwind CSS dashboard with an HTML5 Canvas map showing occupied and available slots in real time.

A MySQL 8.0 database runs in Docker Compose, so the whole environment can be replicated with a single command.

---

## 📸 Screenshots

<!-- TODO: Add screenshots to the repo and replace the placeholders below, for example:
| Dashboard | Slot Routing | Exit Receipt |
|:---:|:---:|:---:|
| ![Dashboard](docs/dashboard.png) | ![Routing](docs/routing.png) | ![Receipt](docs/receipt.png) |
-->

*Screenshots coming soon.*

---

## ✨ Key Features

- **Real-time spatial routing** – an HTML5 Canvas frontend maps the physical parking slots and draws a simulated shortest-path line from the entrance to the dynamically assigned spot.
- **AI dynamic pricing engine** – a Scikit-Learn Linear Regression model calculates variable exit fees from parking duration, time of day (entry hour) and lot occupancy rate.
- **Modern API architecture** – a fully decoupled REST API built with FastAPI and Pydantic for strict data validation.
- **Containerized database** – MySQL 8.0 deployed through Docker Compose for instant environment replication and easy local development.
- **Live status dashboard** – a Tailwind CSS web interface that visually tracks occupied versus available slots.
- **Receipt generation** – fee calculation and receipt creation handled on vehicle exit.
- **Legacy CLI** – a terminal-based interface is included in `scripts/` for working without the web UI.

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.11+, FastAPI, Uvicorn, Pydantic |
| **Machine Learning** | Scikit-Learn, NumPy, Pickle |
| **Database** | MySQL 8.0, Docker, Docker Compose, SQLTools (VS Code extension) |
| **Frontend** | Vanilla JavaScript, HTML5 Canvas, Tailwind CSS |

---

## 🧱 System Architecture

```
┌────────────────────────┐        HTTP / JSON        ┌──────────────────────────┐
│   Frontend Dashboard   │ ────────────────────────► │      FastAPI Backend     │
│  index.html            │                           │  app/api.py              │
│  • HTML5 Canvas map    │ ◄──────────────────────── │  • Route handlers        │
│  • Tailwind CSS UI     │      slot + route + fee   │  • Pydantic validation   │
└────────────────────────┘                           └───────┬───────────┬──────┘
                                                             │           │
                                         slot allocation,    │           │  predict exit fee
                                         receipts, DB access │           │
                                                    ┌────────▼───────┐ ┌─▼──────────────────┐
                                                    │ app/parking.py │ │ ml/pricing_model   │
                                                    │ app/receipts.py│ │ .pkl (Linear Reg.) │
                                                    │ app/database.py│ └────────────────────┘
                                                    └────────┬───────┘
                                                             │ MySQL connection
                                                    ┌────────▼────────────────┐
                                                    │ MySQL 8.0 (Docker)      │
                                                    │ parking_slots, vehicles,│
                                                    │ receipts                │
                                                    └─────────────────────────┘
```

---

## 📂 Project Structure

```
Vehicle-Parking-Management-System/
├── app/                        # Core backend logic & API routing
│   ├── api.py                  # FastAPI endpoints and route handlers
│   ├── database.py             # MySQL connection pooling
│   ├── parking.py              # Core parking allocation logic
│   └── receipts.py             # Fee calculation and receipt generation
├── frontend/                   # Web interface assets
│   └── index.html              # Dashboard with HTML5 Canvas map
├── ml/                         # Machine learning models & scripts
│   ├── pricing_model.py        # Model training script
│   └── pricing_model.pkl       # Serialized Linear Regression model
├── scripts/                    # Setup and legacy CLI scripts
│   ├── app.py                  # Terminal-based CLI interface
│   └── setup_db.py             # Database schema initialization script
├── docker-compose.yml          # Docker configuration for MySQL
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md                   # Project documentation
```

---

## 🤖 How the AI Pricing Works

Instead of charging a flat hourly rate, the system predicts the exit fee with a **Linear Regression** model from Scikit-Learn.

| Input feature | Meaning |
|---|---|
| **Parking duration** | How long the vehicle stayed in the lot |
| **Entry hour** | Time of day the vehicle arrived (captures peak vs. off-peak) |
| **Occupancy rate** | How full the lot was |

1. `ml/pricing_model.py` trains the model and saves it as `ml/pricing_model.pkl`.
2. When a vehicle exits, the API loads the serialized model and predicts the fee.
3. The fee is stored in a receipt for that vehicle.

> ℹ️ The model file is generated locally. You must run the training script (see [Installation & Setup](#-installation--setup)) before the API can calculate dynamic fees.

---

## 🗄️ Database Schema

The database is initialised by `scripts/setup_db.py`, which creates three tables and seeds **10 parking slots**:

| Table | Purpose |
|---|---|
| `parking_slots` | The physical slots in the lot and whether each is occupied |
| `vehicles` | Vehicles currently or previously parked |
| `receipts` | Exit receipts with the calculated fee |

> 📝 See `scripts/setup_db.py` for the exact columns and types.

---

## 📋 Prerequisites

| Requirement | Version / Notes |
|---|---|
| **Python** | 3.11 or higher |
| **Docker Desktop** | Installed and **running** |
| **Git** | To clone the repository |
| **Web browser** | Any modern browser with HTML5 Canvas support |

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/ArjunNair2004/Vehicle-Parking-Management-System.git
cd Vehicle-Parking-Management-System
```

### 2. Start the Dockerized database

Spin up the MySQL container (exposed on port **3307**):

```bash
docker compose up -d
```

### 3. Create and activate a virtual environment

```bash
python -m venv venv
```

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Initialize the database schema

Creates the `parking_slots`, `vehicles` and `receipts` tables and seeds the initial 10 parking slots:

```bash
python scripts/setup_db.py
```

### 6. Train the AI pricing model

Generates the serialized `.pkl` file the API needs to calculate dynamic exit fees:

```bash
python ml/pricing_model.py
```

### 7. Start the FastAPI server

Launch Uvicorn with live reloading:

```bash
uvicorn app.api:app --reload
```

### 8. Open the dashboard

Visit:

```
http://127.0.0.1:8000/
```

---

## 💡 Usage

1. **Open the dashboard** – the canvas shows the parking lot with occupied and available slots.
2. **Park a vehicle** – enter the vehicle details; the system assigns a slot and draws the route from the entrance to it.
3. **Track the lot** – the dashboard updates to reflect which slots are taken.
4. **Exit a vehicle** – the AI model calculates the fee from duration, entry hour and occupancy, and a receipt is generated.
5. **Prefer the terminal?** – run the legacy CLI:

```bash
python scripts/app.py
```

> The FastAPI server also exposes interactive API docs at `http://127.0.0.1:8000/docs` (Swagger UI), which is built into FastAPI.

---

## ⚙️ Configuration

| Setting | Location | Default / Notes |
|---|---|---|
| MySQL host port | `docker-compose.yml` | `3307` |
| Database connection | `app/database.py` | Must match the credentials in `docker-compose.yml` |
| Number of seeded slots | `scripts/setup_db.py` | `10` |
| API address | Uvicorn | `http://127.0.0.1:8000` |
| Trained model path | `ml/pricing_model.pkl` | Created by `ml/pricing_model.py` |

> 🔐 **Security tip:** avoid committing real database passwords. Move credentials into environment variables or a `.env` file that is listed in `.gitignore`.

---

## 🧯 Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `docker compose` fails or can't connect to the Docker daemon | Docker Desktop is not running | Start Docker Desktop and retry `docker compose up -d` |
| `Can't connect to MySQL server` / connection refused | Container not ready or wrong port | Run `docker ps`, wait a few seconds after startup, and confirm the app uses port **3307** |
| `Access denied for user` | Credentials in `app/database.py` differ from `docker-compose.yml` | Make both files use the same user and password |
| `Port is already allocated` on 3307 | Another service is using the port | Stop that service or change the host port in `docker-compose.yml` and `app/database.py` |
| `FileNotFoundError: pricing_model.pkl` | Model was never trained | Run `python ml/pricing_model.py` |
| `ModuleNotFoundError` | Virtual environment not active or dependencies missing | Activate `venv` and run `pip install -r requirements.txt` |
| `Table ... doesn't exist` | Schema not initialised | Run `python scripts/setup_db.py` |
| `uvicorn: command not found` | Uvicorn not installed in the active environment | Reinstall with `pip install -r requirements.txt` inside the venv |
| Dashboard loads but slots don't appear | API not running or database is empty | Check the Uvicorn terminal for errors and re-run the setup script |

---

## 🔮 Future Scope

- **A\* (A-Star) pathfinding** – upgrade the current L-shape routing simulation to calculate true obstacle-aware shortest paths.
- **Live occupancy telemetry** – replace the static occupancy rate in the ML model with real-time database queries so pricing scales during peak hours.
- **Computer vision integration** – use headless OpenCV / EasyOCR to read license plates from camera feeds, removing the need for manual text input.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

No license has been specified for this repository yet. Add a `LICENSE` file (for example MIT) to define how others may use the code.

---

## 👤 Author

**Arjun Nair** – [@ArjunNair2004](https://github.com/ArjunNair2004)

If you found this project useful, consider giving it a ⭐ on GitHub!
