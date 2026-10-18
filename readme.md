# Smart Vehicle Parking Management System

An AI-powered parking management system featuring dynamic pricing and real-time spatial pathfinding. Built with FastAPI, Dockerized MySQL, and a lightweight HTML5 Canvas frontend.

## Features
* **Live Spatial Routing:** HTML5 Canvas maps physical parking slots and draws shortest-path routing lines to assigned spots.
* **AI Dynamic Pricing:** A Scikit-Learn Linear Regression model calculates exit fees based on parking duration, time of day, and lot occupancy.
* **Modern Backend API:** Fully decoupled FastAPI backend for high-performance HTTP request handling.
* **Containerized Database:** MySQL database deployed via Docker Compose for instant environment replication.

## Tech Stack
* **Backend:** Python, FastAPI, Uvicorn, Pydantic
* **Database:** MySQL 8.0 (Docker)
* **Machine Learning:** Scikit-Learn, NumPy, Pickle
* **Frontend:** Vanilla JS, HTML5 Canvas, Tailwind CSS

## Run Locally

1. **Start the Database**
   ```bash
   docker compose up -d