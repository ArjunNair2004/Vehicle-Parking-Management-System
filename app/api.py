from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.database import get_db_connection
import pickle
import numpy as np

app = FastAPI(title="Smart Parking API")

# Allow the frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your ML model
try:
    with open("ml/pricing_model.pkl", "rb") as file:
        pricing_model = pickle.load(file)
except FileNotFoundError:
    pricing_model = None

# Define expected data structures
class ParkRequest(BaseModel):
    vehicle_number: str
    vehicle_type: str

class ExitRequest(BaseModel):
    slot_number: str

# Serve the Frontend Dashboard
@app.get("/")
def serve_dashboard():
    return FileResponse("frontend/index.html")

@app.get("/status")
def get_status():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT ps.slot_number, ps.status, v.vehicle_number 
        FROM parking_slots ps
        LEFT JOIN vehicles v ON ps.id = v.slot_id AND v.exit_time IS NULL
        ORDER BY ps.distance_from_entry ASC
    """)
    slots = cursor.fetchall()
    cursor.close()
    db.close()
    return {"slots": slots}

@app.post("/park")
def park_vehicle(req: ParkRequest):
    db = get_db_connection()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT id, slot_number FROM parking_slots 
        WHERE status='available' ORDER BY distance_from_entry ASC LIMIT 1
    """)
    slot = cursor.fetchone()
    
    if not slot:
        cursor.close()
        db.close()
        raise HTTPException(status_code=400, detail="No available slots.")
        
    slot_id, slot_number = slot
    cursor.execute("""
        INSERT INTO vehicles (vehicle_number, vehicle_type, slot_id, entry_time)
        VALUES (%s, %s, %s, NOW())
    """, (req.vehicle_number, req.vehicle_type, slot_id))
    cursor.execute("UPDATE parking_slots SET status='occupied' WHERE id=%s", (slot_id,))
    db.commit()
    
    cursor.close()
    db.close()
    return {"message": f"Vehicle {req.vehicle_number} parked in slot {slot_number}", "slot": slot_number}

@app.post("/exit")
def exit_vehicle(req: ExitRequest):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT v.id AS vehicle_id, v.vehicle_number, v.vehicle_type, v.entry_time, ps.id AS slot_id,
        TIMESTAMPDIFF(MINUTE, v.entry_time, NOW()) AS duration
        FROM vehicles v
        JOIN parking_slots ps ON v.slot_id = ps.id
        WHERE ps.slot_number = %s AND v.exit_time IS NULL
    """, (req.slot_number,))
    
    vehicle = cursor.fetchone()
    if not vehicle:
        cursor.close()
        db.close()
        raise HTTPException(status_code=404, detail=f"No vehicle found in slot {req.slot_number}")

    duration = vehicle['duration'] if vehicle['duration'] else 0
    entry_hour = vehicle['entry_time'].hour if vehicle['entry_time'] else 0
    occupancy_rate = 0.75 # You can update this to be dynamic later
    
    # Calculate ML Pricing
    if duration == 0:
        total_fee = 0.0
    else:
        if pricing_model:
            features = np.array([[entry_hour, duration, occupancy_rate]])
            total_fee = float(pricing_model.predict(features)[0])
        else:
            total_fee = float(duration * 1.5)

    # Process exit
    cursor.execute("UPDATE vehicles SET exit_time=NOW(), fee_paid=%s WHERE id=%s", (total_fee, vehicle['vehicle_id']))
    cursor.execute("INSERT INTO receipts (vehicle_number, total_fee) VALUES (%s, %s)", (vehicle['vehicle_number'], total_fee))
    cursor.execute("UPDATE parking_slots SET status='available' WHERE id=%s", (vehicle['slot_id'],))
    db.commit()
    
    cursor.close()
    db.close()
    
    return {
        "receipt": {
            "vehicle_number": vehicle['vehicle_number'],
            "slot_number": req.slot_number,
            "duration_minutes": duration,
            "total_fee": round(total_fee, 2)
        }
    }