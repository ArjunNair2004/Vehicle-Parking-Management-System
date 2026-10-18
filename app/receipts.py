import pickle
from database import get_db_connection
import numpy as np

try:
    with open("ml/pricing_model.pkl", "rb") as file:
        pricing_model = pickle.load(file)
except FileNotFoundError:
    pricing_model = None

def generate_receipt(slot_number): 
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT receipts.id, receipts.total_fee, receipts.issued_at,
        TIMESTAMPDIFF(MINUTE, vehicles.entry_time, vehicles.exit_time) AS duration,
        vehicles.vehicle_type, vehicles.vehicle_number, vehicles.entry_time, parking_slots.id
        FROM receipts
        JOIN vehicles ON vehicles.vehicle_number = receipts.vehicle_number
        JOIN parking_slots ON vehicles.slot_id = parking_slots.id
        WHERE parking_slots.slot_number = %s
        ORDER BY receipts.issued_at DESC LIMIT 1
    """, (slot_number,)) 

    receipt = cursor.fetchone()

    if receipt:
        receipt_id, total_fee, issued_at, duration, vehicle_type, vehicle_number, entry_time, slot_id = receipt
        entry_hour = entry_time.hour if entry_time else 0
        occupancy_rate = 0.75 

        if duration == 0 or not duration:
            dynamic_fee = 0
        else:
            if pricing_model:
                features = np.array([[entry_hour, duration, occupancy_rate]])
                dynamic_fee = pricing_model.predict(features)[0]
            else:
                dynamic_fee = total_fee

        print("\n Parking Receipt")
        print(f"Receipt ID   : {receipt_id}")
        print(f"Slot ID      : {slot_id}")
        print(f"Vehicle No   : {vehicle_number}")
        print(f"Vehicle Type : {vehicle_type}")
        print(f"Duration     : {duration} minutes")
        print(f"Total Fee    : ₹{dynamic_fee:.2f}")
        print(f"Issued At    : {issued_at}")
    else:
        print("No receipt found for this slot.")

    cursor.close()
    db.close()