from database import get_db_connection

db = get_db_connection()
cursor = db.cursor()

last_vehicle = {"slot": None, "number": None, "type": None}

def add_vehicle(vehicle_number=None, vehicle_type=None):
    global last_vehicle
    if not vehicle_number or not vehicle_type:
        if last_vehicle["number"] and last_vehicle["type"]:
            vehicle_number, vehicle_type = last_vehicle["number"], last_vehicle["type"]
        else:
            print("No vehicle data found. Please enter manually.")
            return

    cursor.execute("""
        SELECT id, slot_number, distance_from_entry
        FROM parking_slots
        WHERE status='available'
        ORDER BY distance_from_entry ASC
        LIMIT 1
    """)
    slot = cursor.fetchone()

    if slot:
        slot_id, slot_number, _ = slot
        cursor.execute("""
            INSERT INTO vehicles (vehicle_number, vehicle_type, slot_id, entry_time)
            VALUES (%s, %s, %s, NOW())
        """, (vehicle_number, vehicle_type, slot_id))
        cursor.execute("UPDATE parking_slots SET status='occupied' WHERE id=%s", (slot_id,))
        db.commit()

        last_vehicle = {"slot": slot_number, "number": vehicle_number, "type": vehicle_type}
        print(f"Vehicle {vehicle_number} parked in slot {slot_number}.")
    else:
        print("No available slots.")

def vehicle_exit(slot_number=None):
    global last_vehicle
    cursor.execute("""
        SELECT ps.slot_number, v.vehicle_number, v.id, v.slot_id, TIMESTAMPDIFF(MINUTE, v.entry_time, NOW())
        FROM vehicles v
        JOIN parking_slots ps ON v.slot_id = ps.id
        WHERE v.exit_time IS NULL
    """)
    vehicles = cursor.fetchall()

    if not vehicles:
        print("No vehicles currently parked.")
        return

    if not slot_number:
        print("\n Active Parking Slots:")
        for slot in vehicles:
            print(f"Slot {slot[0]} (Vehicle: {slot[1]})")
        slot_number = input("\nEnter the slot number of the vehicle to exit: ").strip()

    selected_vehicle = next((v for v in vehicles if str(v[0]) == str(slot_number)), None)

    if selected_vehicle:
        slot_num, vehicle_number, vehicle_id, slot_id, duration = selected_vehicle
        rate_per_min = 1.5 
        total_fee = float(duration) * rate_per_min if duration else 0.0

        cursor.execute("UPDATE vehicles SET exit_time=NOW() WHERE id=%s", (vehicle_id,))
        cursor.execute("INSERT INTO receipts (vehicle_number, total_fee) VALUES (%s, %s)", (vehicle_number, total_fee))
        cursor.execute("UPDATE parking_slots SET status='available' WHERE id=%s", (slot_id,))
        db.commit()

        print(f"Vehicle {vehicle_number} (Slot {slot_num}) exited. Base Fee: ₹{total_fee:.2f}")

        if last_vehicle["slot"] == slot_num:
            last_vehicle = {"slot": None, "number": None, "type": None}
    else:
        print(f"No vehicle found in slot {slot_number}.")

def show_parking_status():
    cursor.execute("""
        SELECT ps.slot_number, ps.status, v.vehicle_number
        FROM parking_slots ps
        LEFT JOIN vehicles v ON ps.id = v.slot_id AND v.exit_time IS NULL
    """)
    slots = cursor.fetchall()

    print("\n Parking Slot Status:")
    if not slots:
        print("No slots found in the database!")
    else:
        for slot in slots:
            slot_number, status, vehicle_number = slot
            if vehicle_number:
                print(f"Slot {slot_number} - {status} (Vehicle: {vehicle_number})")
            else:
                print(f"Slot {slot_number} - {status}")